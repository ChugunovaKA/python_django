from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, default="", verbose_name="Биография")

    def __str__(self):
        return f"Profile of {self.user.username}"