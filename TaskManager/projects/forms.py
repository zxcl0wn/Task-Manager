from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.forms import ModelForm

from user.middleware import get_current_user
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
            'status': forms.Select(attrs={'class': 'prform-select'}),
            'description': forms.Textarea(attrs={'class': 'projform-textarea'}),
            'comment': forms.Textarea(attrs={'class': 'projform-textarea'}),
            'users': forms.SelectMultiple(attrs={'class': 'projform-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_user = get_current_user()
        users = self.fields['users'].queryset
        print(f'current_user: {current_user}')
        for user in users:
            if str(user.username) == str(current_user):
                self.fields['users'].queryset = self.fields['users'].queryset.exclude(id=current_user.id)

        # if self.request and self.request.user.is_authenticated:
        #     print(f'!!!!')
        #     self.fields['users'].queryset = User.objects.exclude(id=self.request.user.id)
        #
        # if self.initial.get('status') == 'PRIVATE':
        #     self.fields['users'].widget.attrs['style'] = 'display:none'
        #     self.fields['users'].label = ''

    def cleaned_users(self):
        data = self.cleaned_data['users']
        return data
