from django.db import models
from user.models import User


class Project(models.Model):
    title = models.CharField(max_length=40, null=True)
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, through='ProjectMember', blank=False)

    def __str__(self):
        return self.title


class ProjectMember(models.Model):
    USER_ROLE_CHOICES = [
        ('VIEWER', 'viewer'),
        ('EDITOR', 'editor'),
        ('OWNER', 'owner')
    ]

    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES)
