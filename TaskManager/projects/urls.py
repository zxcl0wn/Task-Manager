from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'app_projects'

urlpatterns = [
    path('', views.main_page, name='main'),
    path('projects-list/', views.projects_list, name='projects_list'),
    path('project/<slug:project_slug>', views.project_view, name='project'),
    path('create-project/', views.create_project, name='create_project'),
]
