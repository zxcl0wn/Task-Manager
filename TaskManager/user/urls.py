from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'app_user'

urlpatterns = [
    path('', views.user_test, name='test'),
]
