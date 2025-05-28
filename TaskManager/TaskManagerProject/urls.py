from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls', namespace='app_projects')),
    path('tasks/', include('tasks.urls', namespace='app_tasks')),
    path('user/', include('user.urls', namespace='app_user')),
    path('notifications/', include('notification.urls', namespace='app_notification')),
]
