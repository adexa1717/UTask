from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from tasks.models import User, Task


class TaskShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'done', 'end_timestamp', 'id')


class UserSerializer(serializers.ModelSerializer):
    tasks = TaskShortSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'tasks')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'done')
        read_only_fields = ('id', 'title', 'done')


class TaskRetrieveSerializer(serializers.ModelSerializer):
    owner = UserShortSerializer()

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('done', 'owner')


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('done',)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_('Email'))
    password = serializers.CharField(
        label=_('Password'),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email, password=password)
            except User.DoesNotExist as e:
                user = None
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

    class Meta:
        model = User
        fields = ('email', 'password',)
