from django.db import models
from user.models import User


class Project(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    users = models.ManyToManyField(User, blank=False)