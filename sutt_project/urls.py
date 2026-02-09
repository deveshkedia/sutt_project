from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
     path('accounts/', include('allauth.socialaccount.urls')),
    path('users/', include('users.urls')),
    path('forum/', include('forum.urls')),
    path('martor/', include('martor.urls')),
    path('', views.home ,name='home'),
]
