from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserForm


def login_user(request):
    # form = UserForm
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username, password=password)
        except:
            print('Такого пользователя нет в системе')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('app_user:profile')

    context = {
        # 'form': form,
        'page': 'login',
    }

    return render(request, 'user/login_register.html', context=context)


def register_user(request):
    form = UserForm

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            login(request, user)
            return redirect('app_user:profile')


    context = {
        'form': form,
        'page': 'register'
    }
    return render(request, 'user/login_register.html', context=context)


@login_required(login_url='app_user:login')
def profile_user(request):
    user = request.user
    context = {
        'user': user
    }

    return render(request, 'user/profile.html', context=context)
