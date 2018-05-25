"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework import routers
from users import views

router = routers.DefaultRouter()
# router.register(r'(?P<username>.+)/$', views.UserViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'friend', views.FriendViewSet)

urlpatterns = [
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('friends/', views.friend_list),
    url('^(?P<username>.+).com/api/', views.friend_list),
    path('', RedirectView.as_view(url='/home', permanent=False), name='index'),
    path('home/', views.Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')), #, namespace='users')),
    path('users/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
