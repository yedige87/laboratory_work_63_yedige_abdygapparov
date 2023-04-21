import django
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        verbose_name='Автор',
        to=get_user_model(),
        related_name='posts',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        verbose_name='Фото',
        null=False,
        blank=True,
        upload_to='images',
        default='images/blank.jpg'
    )
    description = models.TextField(
        verbose_name='Описание',
        null=False,
        max_length=2000
    )
    is_new = models.BooleanField(
        verbose_name='Новый пост?',
        default=True
    )
    user_likes = models.ManyToManyField(
        verbose_name='Лайки пользователей',
        to=get_user_model(),
        related_name='liked_posts'
    )
    date_publish = models.DateTimeField(
        default=django.utils.timezone.now,
        verbose_name='Дата публикации')

    date_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    def __str__(self):
        return f"{self.author}"



class Comment(models.Model):

    author = models.ForeignKey(
        verbose_name='Публикация',
        to=get_user_model(),
        related_name='comments',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        verbose_name='Публикация',
        to='posts.Post',
        related_name='comments',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    text = models.CharField(
        verbose_name='Комментарий',
        null=False,
        blank=False,
        max_length=200
    )
    date_publish = models.DateTimeField(
        default=django.utils.timezone.now,
        verbose_name='Дата публикации')

    date_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
