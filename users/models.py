from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    telegram_account = models.CharField(max_length=50, unique=True, verbose_name='телеграм аккаунт')
    email = models.EmailField(max_length=30, unique=True, verbose_name='Почта')
    chat_id = models.IntegerField(null=True, blank=True, verbose_name='ID чата')

    USERNAME_FIELD = 'telegram_account'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
