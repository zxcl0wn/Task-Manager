from django.shortcuts import render
from .forms import UserForm


def login_user(request):
    context = {

    }

    return render(request, 'user/login_register.html', context=context)


def register_user(request):
    form = UserForm

    context = {
        'form': form,
    }

    return render(request, 'user/login_register.html', context=context)


def profile_user(request):
    context = {

    }

    return render(request, 'user/profile.html', context=context)
