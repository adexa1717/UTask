from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from tasks.models import Task
from tasks import serializers
from tasks.tasks import send_mail_about_task_to_user


class TaskViewSet(viewsets.ModelViewSet):
    """
    Вьюха для взаимодействия с моделью задачи
    """
    queryset = Task.objects.all()
    serializer_class = serializers.TaskListSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Переопределение метода list для удобства и кастомизации
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset.exists():
            raise NotFound()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Переобпределение метода get_queryset для задания необходимого условия фильтрации и
    # возможности задавать разные фильтры на разные ситуации
    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset

    # Переопределение дефолтного метода для добавления возможности вывода без пагинации
    def paginate_queryset(self, queryset):
        if 'all' in self.request.query_params:
            return None
        return super().paginate_queryset(queryset)

    # Переопределение для того что бы задавать разные сериализаторы на разные запросы
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.TaskRetrieveSerializer
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return serializers.TaskCreateSerializer
        return self.serializer_class

    # Добавлен метод для отметки о выполнении задачии
    @action(methods=['POST'], detail=True)
    def execute(self, request, pk):
        queryset = self.get_queryset().filter(id=pk)
        if not queryset.exists():
            raise NotFound()
        queryset.update(done=True)
        task = queryset.first()
        send_mail_about_task_to_user.delay(user_id=str(self.request.user.id), task_id=task.id)
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    # Добавлен метод для отметки о не выполнении задачии, дублируется для удобства
    @action(methods=['POST'], detail=True)
    def un_execute(self, request, pk):
        queryset = self.get_queryset().filter(id=pk)
        if not queryset.exists():
            raise NotFound()
        queryset.update(done=False)
        task = queryset.first()
        send_mail_about_task_to_user.delay(user_id=str(self.request.user.id), task_id=task.id)
        serializer = self.get_serializer(task)
        return Response(serializer.data)
