from django.shortcuts import render


def user_test(request):
    context = {

    }

    return render(request, 'user/test.html', context=context)