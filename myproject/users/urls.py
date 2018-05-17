# users/urls.py
from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('addPost/', views.addPost.as_view(), name='addPost'),
    path('addFriend/', views.addFriend.as_view(), name='addFriend'),
    path('newLogin/', views.newLogin.as_view(), name='newLogin'),
    path('loginView/', views.loginView),
    path('signupView/', views.signupView),
    #path('connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),
    # url(r'^log/(?P<operation>.+)/$', views.log, name='log')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
