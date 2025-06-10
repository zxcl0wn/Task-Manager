from django import forms
from django.forms import ModelForm
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'status', 'description', 'comment', 'users']
        labels = {
            'title': "Название",
            'status': "Статус",
            'description': "Описание проекта",
            'comment': "Комментарий",
            'users': "Участники"
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'prform-input'}),
            'status': forms.Select(attrs={'class': 'prform-select'}),
            'description': forms.Textarea(attrs={'class': 'prform-textarea'}),
            'comment': forms.Textarea(attrs={'class': 'prform-textarea'}),
            'users': forms.SelectMultiple(attrs={'class': 'prform-select'}),
        }

class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'status', 'description', 'comment', 'users']
        labels = {
            'title': "Название",
            'status': "Статус",
            'description': "Описание проекта",
            'comment': "Комментарий",
            'users': "Участники"
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'projform-input'}),
            'status': forms.Select(attrs={'class': 'projform-select'}),
            'description': forms.Textarea(attrs={'class': 'projform-textarea'}),
            'comment': forms.Textarea(attrs={'class': 'projform-textarea'}),
            'users': forms.SelectMultiple(attrs={'class': 'projform-select'}),
        }
