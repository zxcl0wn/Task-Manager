from django.db import models
from django.template import defaultfilters
from unidecode import unidecode


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("LOW", "низкий"),
        ("MEDIUM", "средний"),
        ("HIGH", "высокий")
    ]
    STATUS_CHOICES = [
        ("NEW", "Новая"),
        ("INPR", "В работе"),
        ("DONE", "Сделано")
    ]

    title = models.CharField(max_length=20, blank=False, unique=True)
    slug = models.SlugField(max_length=20, null=True, blank=True, unique=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="MEDIUM")
    comment = models.TextField(blank=True)
    deadline_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="NEW")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = defaultfilters.slugify(unidecode(value))
        super().save(*args, **kwargs)


class Subtask(models.Model):
    title = models.CharField(max_length=30, blank=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
