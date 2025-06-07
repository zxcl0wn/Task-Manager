from django import forms
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
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'task-title'}),
            'description': forms.Textarea(attrs={'class': 'task-textarea'}),
            'priority': forms.Select(attrs={'class': 'task-select'}),
            'comment': forms.Textarea(attrs={'class': 'task-textarea'}),
            'deadline_date': forms.DateInput(attrs={'class': 'task-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'status-btn'}),
        }
