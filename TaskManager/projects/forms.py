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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     current_user = get_current_user()
    #     users = self.fields['users'].queryset
    #     print(f'current_user: {current_user}')
    #     for user in users:
    #         if str(user.username) == str(current_user):
    #             self.fields['users'].queryset = self.fields['users'].queryset.exclude(id=current_user.id)

    # def cleaned_users(self):
    #     data = self.cleaned_data['users']
    #     return data


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

        # Фильтруем queryset пользователей, исключая уже добавленных
        self.fields['user'].queryset = User.objects.exclude(
            id__in=existing_member_ids
        )

# User = get_user_model()


# class AddMembersForm(forms.ModelForm):
#     email = forms.EmailField(label="Email пользователя")
#
#     class Meta:
#         model = ProjectMember
#         fields = ['user_role']
#         widgets = {
#             'user_role': forms.Select(attrs={'class': 'form-select'})
#         }
#
#     def __init__(self, *args, **kwargs):
#         self.project = kwargs.pop('project', None)
#         super().__init__(*args, **kwargs)
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         try:
#             user = get_user_model().objects.get(email=email)
#             if ProjectMember.objects.filter(project=self.project, user=user).exists():
#                 raise forms.ValidationError("Этот пользователь уже в проекте")
#             return user
#         except get_user_model().DoesNotExist:
#             raise forms.ValidationError("Пользователь с таким email не найден")
