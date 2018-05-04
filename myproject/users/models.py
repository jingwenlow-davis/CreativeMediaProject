from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# users/models.py
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.forms import ModelForm


class Post(models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class AddPost(ModelForm):
    class meta:
        model = Post
        fields = ['post']


class CustomUser(AbstractUser):
    # First/last name is not a global-friendly pattern
    name = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.email
