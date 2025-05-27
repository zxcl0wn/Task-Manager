from django.shortcuts import render


def tasks_test(request):
    context = {

    }

    return render(request, 'tasks/test.html', context=context)
