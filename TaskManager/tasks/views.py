from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm


def tasks_list(request):
    tasks = Task.objects.all()
    context = {
        'tasks': tasks,
    }

    return render(request, 'tasks/tasks_list.html', context=context)


def task_view(request, task_slug):
    task = Task.objects.get(slug=task_slug)
    form = TaskForm(instance=task)

    context = {
        'task': task,
        'form': form
    }

    return render(request, 'tasks/task.html', context=context)


def task_create(reqeust):
    context = {

    }

    return render(reqeust, 'tasks/task_form.html', context=context)


def task_delete(request, task_slug):
    task = Task.objects.get(slug=task_slug).delete()

    return redirect('app_tasks:tasks_list')
