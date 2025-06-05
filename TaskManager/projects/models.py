from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from django.template import defaultfilters
from user.models import User


class Project(models.Model):
    title = models.CharField(max_length=40, null=True, unique=True)
    slug = models.SlugField(max_length=40, unique=True, null=True)
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, through='ProjectMember', blank=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = defaultfilters.slugify(unidecode(value))
        super().save(*args, **kwargs)


class ProjectMember(models.Model):
    USER_ROLE_CHOICES = [
        ('VIEWER', 'viewer'),
        ('EDITOR', 'editor'),
        ('OWNER', 'owner')
    ]

    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES)
