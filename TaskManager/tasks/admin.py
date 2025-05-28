from django.contrib import admin
from .models import Task, Subtask


admin.site.register(Task)
admin.site.register(Subtask)
