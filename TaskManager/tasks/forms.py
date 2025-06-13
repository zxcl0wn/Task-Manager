from django import forms
from django.forms import ModelForm

from projects.models import Project, ProjectMember
from user.middleware import get_current_user
from .models import Task, Subtask
from django.contrib.auth.forms import UserCreationForm


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'comment', 'project', 'deadline_date', 'status']
        labels = {
            'title': "Название",
            'description': "Описание",
            'priority': "Приоритет",
            'comment': "Комментарий",
            'project': "Проект",
            'deadline_date': "Срок сдачи",
            'status': "Статус"
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'task-title'}),
            'description': forms.Textarea(attrs={'class': 'task-textarea'}),
            'priority': forms.Select(attrs={'class': 'task-select'}),
            'project': forms.Select(attrs={'class': 'task-select'}),
            'comment': forms.Textarea(attrs={'class': 'task-textarea'}),
            'deadline_date': forms.DateInput(attrs={'class': 'task-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'status-btn'}),
        }


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'comment', 'project', 'deadline_date']
        labels = {
            'title': "Название",
            'description': "Описание",
            'priority': "Приоритет",
            'comment': "Комментарий",
            'project': "Проект",
            'deadline_date': "Срок сдачи",
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'taskedit-title'}),
            'description': forms.Textarea(attrs={'class': 'taskedit-textarea'}),
            'priority': forms.Select(attrs={'class': 'taskedit-select'}),
            'project': forms.Select(attrs={'class': 'taskedit-select'}),
            'comment': forms.Textarea(attrs={'class': 'taskedit-textarea'}),
            'deadline_date': forms.DateInput(attrs={'class': 'taskedit-input', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = get_current_user()
        super().__init__()

        if self.user:
            self.fields['project'].queryset = Project.objects.filter(
                projectmember__user=self.user,
                projectmember__user_role='OWNER'
            ).distinct()

            if 'project' in self.initial:
                project_id = self.initial['project']
                if not ProjectMember.objects.filter(
                        project_id=project_id,
                        user=self.user,
                        user_role='OWNER'
                ).exists():
                    self.initial.pop('project')


class SubtaskChangeForm(ModelForm):
    class Meta:
        model = Subtask
        fields = ['title']
        labels = {
            'title': 'Заголовок'
        }

