# users/urls.py
from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('addPost/', views.addPost.as_view(), name='addPost'),
    path('addFriend/', views.addFriend.as_view(), name='addFriend'),
    path('newLogin/', views.newLogin.as_view(), name='newLogin'),
    path('loginView/', views.loginView, name='loginView'),
    path('signupView/', views.signupView, name='signupView'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
