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