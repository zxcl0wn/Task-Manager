from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from django.template import defaultfilters
from tasks.models import Task
from user.models import User
from django.db.models import Q


class Project(models.Model):
    STATUS_CHOICES = [
        ("PUBLIC", "публичный"),
        ("PRIVATE", "приватный"),
    ]
    IS_COMPLETED_CHOICES = [
        ("NO", "В работе"),
        ("YES", "Выполнено")
    ]
    
    title = models.CharField(max_length=40, null=True, unique=True)
    status = models.CharField(max_length=20, null=True, choices=STATUS_CHOICES, default="PUBLIC")
    is_completed = models.CharField(max_length=20, null=True, choices=IS_COMPLETED_CHOICES, default="NO")
    slug = models.SlugField(max_length=40, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, through='ProjectMember', blank=False)

    def __str__(self):
        return self.title

    def update_completion_status(self):
        has_uncompleted_tasks = Task.objects.filter(project_id=self.pk).exclude(status='DONE').exists()

        self.is_completed = 'NO' if has_uncompleted_tasks else 'YES'
        self.save(update_fields=['is_completed'])

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = defaultfilters.slugify(unidecode(value))
        super().save(*args, **kwargs)


class ProjectMember(models.Model):
    USER_ROLE_CHOICES = [
        ('VIEWER', 'Читатель'),
        ('EDITOR', 'Редактор'),
        ('OWNER', 'Администратор')
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES)
