from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Post(models.Model):
    CATEGORIES = [
        'Танки',
        'Хилы',
        'ДД',
        'Торговцы',
        'Гилдмастеры',
        'Квестгиверы',
        'Кузнецы',
        'Кожевники',
        'Зельевары',
        'Мастера заклинаний',
    ]

    title = models.CharField(max_length=100, unique=True)
    content = HTMLField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORIES)


class Reply(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    text = models.TextField()
    accept = models.BooleanField(default=False)


