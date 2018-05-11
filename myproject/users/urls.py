# users/urls.py
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('addPost/', views.addPost.as_view(), name='addPost'),
    path('addFriend/', views.addFriend.as_view(), name='addFriend'),
    #path('connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends')
]
