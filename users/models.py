from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import TextChoices
from .managers import CustomUserManager

class GenderChoice(TextChoices):
    NO_INFO = 'no_info', 'Не_указан'
    MALE = 'male', 'Мужской'
    FEMALE = 'female', 'Женский'

class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Полное имя')
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='user_pic',
        verbose_name='Аватар',
        default='user_pic/blank.jpg'
    )
    subscriptions = models.ManyToManyField(
        verbose_name='Подписки',
        to='users.CustomUser',
        related_name='subscribers'
    )
    user_info = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='О пользователе'
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Телефон пользователя'
    )
    gender = models.CharField(
        verbose_name='Пол пользователя',
        choices=GenderChoice.choices,
        max_length=20,
        default=GenderChoice.NO_INFO
    )


    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.full_name
