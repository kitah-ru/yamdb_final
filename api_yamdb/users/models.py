from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
]


class User(AbstractUser):
    """Модель пользователя."""

    confirmations_code = models.CharField(
        'Код подтверждения для поулчения токена',
        max_length=37,
        null=True, blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=9,
        choices=ROLES,
        default='user'
    )

    class Meta:
        ordering = ('id',)
