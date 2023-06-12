from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    username = models.CharField('Username', max_length=150, unique=True)
    email = models.EmailField(
        verbose_name='email',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        'Роль',
        choices=CHOICES,
        default='user',
        max_length=15
    )
    confirmation_code = models.CharField(
        max_length=255, blank=True, null=True
    )
    bio = models.TextField(
        'Описание',
        blank=True, )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True,
        null=True
    )
    bio = models.TextField('Биография', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['username'])
        ]

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'

    def __str__(self) -> str:
        return self.username
