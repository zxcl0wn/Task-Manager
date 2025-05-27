from django.shortcuts import render


def projects_test(request):
    context = {

    }

    return render(request, 'projects/test.html', context=context)
