from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.


# class Author(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.user.username}'


class Post(models.Model):
    CATEGORIES = [
        ('TA', 'Танки'),
        ('HI', 'Хилы'),
        ('DD', 'ДД'),
        ('TO', 'Торговцы'),
        ('GI', 'Гилдмастеры'),
        ('KV', 'Квестгиверы'),
        ('KU', 'Кузнецы'),
        ('KO', 'Кожевники'),
        ('ZE', 'Зельевары'),
        ('MA', 'Мастера заклинаний'),
    ]

    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=2, choices=CATEGORIES)

    def __str__(self):  # настройка отображения на страницах
        return f'{self.title[:20]}'


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    text = models.TextField()
    accept = models.BooleanField(default=False)


