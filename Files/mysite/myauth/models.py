from django.contrib.auth.models import User
from django.db import models
import os

def user_avatar_path(instance, filename):
    # Функция для формирования пути загрузки аватара с использованием pk пользователя
    ext = filename.split('.')[-1]  # расширение файла
    filename = f'avatar.{ext}'  # фиксированное имя файла avatar с оригинальным расширением
    return os.path.join('avatars', str(instance.user.pk), filename)  # путь media/avatars/<user_pk>/avatar.ext

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
