from django.forms import ModelForm
from .models import Task
from django.contrib.auth.forms import UserCreationForm


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'comment', 'deadline_date', 'status']
        labels = {
            'title': "Название",
            'description': "Описание",
            'priority': "Приоритет",
            'comment': "Комментарий",
            'deadline_date': "Срок сдачи",
            'status': "Статус"
        }