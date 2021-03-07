import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True,
                              help_text=_('Required.'),
                              error_messages={'required': 'Please provide your email address.',
                                              'unique': 'An account with this email exist.'}, )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']


class Task(models.Model):
    """Модель задач"""
    # по идее id по дефолту устанавливается, но я решил добавить
    id = models.AutoField(primary_key=True, null=False, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    end_timestamp = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tasks')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-end_timestamp']
