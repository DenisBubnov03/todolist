from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'
