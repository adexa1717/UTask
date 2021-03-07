# Generated by Django 3.1.7 on 2021-03-07 06:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, error_messages={'required': 'Please provide your email address.', 'unique': 'An account with this email exist.'}, help_text='Required.', max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]