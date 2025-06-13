from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.forms import ModelForm

from user.middleware import get_current_user
from .models import Project, ProjectMember


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
        fields = ['title', 'status', 'description', 'comment']
        labels = {
            'title': "Название",
            'status': "Статус",
            'description': "Описание проекта",
            'comment': "Комментарий",
            # 'users': "Участники"
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'projform-input'}),
            'status': forms.Select(attrs={'class': 'prform-select'}),
            'description': forms.Textarea(attrs={'class': 'projform-textarea'}),
            'comment': forms.Textarea(attrs={'class': 'projform-textarea'}),
            # 'users': forms.SelectMultiple(attrs={'class': 'projform-select'}),
        }


class AddMembersForm(ModelForm):
    class Meta:
        model = ProjectMember
        fields = ['user', 'user_role']
        labels = {
            'user': "Пользователь",
            'user_role': "Роль в проекте"
        }

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.project = kwargs.pop('project', None)
        existing_member_ids = ProjectMember.objects.filter(
            project=self.project
        ).values_list('user_id', flat=True)

        self.fields['user'].queryset = User.objects.exclude(
            id__in=existing_member_ids
        )
