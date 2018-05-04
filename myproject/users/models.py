from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.conf import settings
# users/models.py

class Post(models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)


class CustomUser(AbstractUser):
    # First/last name is not a global-friendly pattern
    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.email
