from django.db import models
from user.models import User
from tasks.models import Task


class Notification(models.Model):
    content = models.CharField(max_length=50, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    task_id = models.OneToOneField(Task, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.content
