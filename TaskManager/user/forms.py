from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from user.models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': "Имя пользователя",
            'email': "Электронная почта",
            'password1': "Пароль",
            'password2': "Подтверждение пароля"
        }


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': "Имя пользователя",
            'email': "Электронная почта"
        }
