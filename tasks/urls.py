from rest_framework import routers

from tasks.views import users, tasks_views

router = routers.DefaultRouter()
router.register(r'users', users.UserViewSet, basename='users_list')
router.register(r'todo', tasks_views.TaskViewSet, basename='tasks_list')
