# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('addPost/', views.addPost.as_view(), name='addPost'),
    path('addFriend/', views.addFriend.as_view(), name='addFriend'),
]
