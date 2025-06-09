from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Project
from tasks.models import Task


@receiver([post_save, post_delete], sender=Task)
def update_project_status(sender, instance, **kwargs):
    instance.project.update_completion_status()
