from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'app_user'

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile_user, name='profile'),
]
