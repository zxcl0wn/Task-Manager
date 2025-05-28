from django.db import models
from projects.models import Project


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("LOW", "low"),
        ("MEDIUM", "medium"),
        ("HIGH", "high")
    ]
    STATUS_CHOICES = [
        ("NEW", "new"),
        ("INPR", "in_progress"),
        ("DONE", "done")
    ]

    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="M")
    comment = models.TextField()
    deadline_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="NEW")


class Subtask(models.Model):
    title = models.CharField(max_length=30, blank=False)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
