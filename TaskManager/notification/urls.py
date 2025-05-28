from django.contrib import admin
from django.urls import path
from . import views


app_name = 'app_notification'

urlpatterns = [
    path('', views.notifications_list, name="notifications")
]
