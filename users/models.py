from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.conf import settings

# store posts made by users
class Post(models.Model):
    post = models.CharField(max_length=500) # text
    img = models.FileField(upload_to='uploads', null=True, blank=True) # image
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT) # user who posted
    date = models.DateTimeField(auto_now=True) # date posted: not used

# store list of friends of each user
class Friend(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL) # list of friends
    # user
    current_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner', null=True, on_delete=models.PROTECT)

    # add friend to list of friends
    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.add(new_friend) # add to users

    # remove friend from list of friends
    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user
        )
        friend.users.remove(new_friend) # delete from users

# store users and passwords
class CustomUser(AbstractUser):
    # First/last name is not a global-friendly pattern
    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.username
