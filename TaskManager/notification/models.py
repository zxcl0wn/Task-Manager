from django.db import models
from user.models import User
from tasks.models import Task


class Notification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.OneToOneField(Task, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False, blank=False)
