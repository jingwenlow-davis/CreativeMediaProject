from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.conf import settings
# users/models.py

class Post(models.Model):
    post = models.CharField(max_length=500)
    img = models.FileField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)

class Friend(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', null=True, on_delete=models.PROTECT)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.remove(new_friend)


class CustomUser(AbstractUser):
    # First/last name is not a global-friendly pattern
    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.username
