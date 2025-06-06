from django.shortcuts import render
from .forms import UserForm
from .models import User


def login_user(request):
    context = {
        # 'form': form
        'page': 'login',
    }

    return render(request, 'user/login_register.html', context=context)


def register_user(request):
    form = UserForm

    context = {
        'form': form,
        'page': 'register'
    }
    print(f'!{context}')
    return render(request, 'user/login_register.html', context=context)


def profile_user(request):
    user = request.user
    context = {
        'user': user
    }

    return render(request, 'user/profile.html', context=context)
