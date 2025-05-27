from django.shortcuts import render


def tasks_list(request):
    context = {

    }

    return render(request, 'tasks/tasks_list.html', context=context)


def task_view(request):
    context = {

    }

    return render(request, 'tasks/task.html', context=context)


def task_create(reqeust):
    context = {

    }

    return render(reqeust, 'tasks/task_form.html', context=context)

