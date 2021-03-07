from celery import shared_task
from django.core.mail import send_mail

from UTask.settings import EMAIL_HOST_USERNAME
from .models import Task, User


@shared_task
def send_mail_about_task_to_user(user_id, task_id):
    user = User.objects.get(id=user_id)
    task = Task.objects.get(id=task_id)
    if task.done is True:
        message = f'Задача {task.title} выполнена.'
    else:
        message = f'Задача {task.title} не выполнена.'
    send_mail(
        f'{task.title}',
        message,
        EMAIL_HOST_USERNAME,
        [f'{user.email}'],
        fail_silently=False,
    )
