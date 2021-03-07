from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import User
from tasks.serializers import UserSerializer, LoginSerializer, UserShortSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюха для взаимодействия с моделью пользователя
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthViewSet(GenericAPIView):
    """
    Вьюха для логина
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {'token': token.key, 'user': UserShortSerializer(user).data})
        else:
            return Response('error', status=400)


class Logout(APIView):
    """Вьюха для логаута"""
    @staticmethod
    def get(request):
        user = User.objects.get(id=request.user.id)
        token = Token.objects.get(user=user)
        user.save()
        token.delete()
        if request.auth:
            request.auth.delete()
        if request.session:
            request.session.delete()
        return Response("User successfully logged out")
