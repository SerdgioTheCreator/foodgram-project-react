from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api.constants import EMAIL_MAXLENGTH, NAME_MAX_LENGTH


class User(AbstractUser):
    username = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        help_text=('Обязательно для заполнения. Не более 150 символов.'
                   'Только буквы, цифры и @/./+/-/_'),
        validators=(UnicodeUsernameValidator(), ),
        error_messages={'unique': 'Это имя пользователя занято'},
        verbose_name='Уникальный юзернейм'
    )
    email = models.EmailField(
        max_length=EMAIL_MAXLENGTH,
        unique=True,
        error_messages={
            'unique': 'Этот адрес электронной почты уже зарегистрирован'
        },
        blank=True,
        verbose_name='Адрес электронной почты'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', )

    class Meta:
        ordering = ('username', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_prevent_self_follow',
                check=~models.Q(user=models.F('author')),
            ),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
