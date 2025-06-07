from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm


def tasks_list(request):
    tasks = Task.objects.all()
    filter_type = request.GET.get('filter')

    if filter_type == 'priority':
        tasks = tasks.order_by('priority')
    elif filter_type == 'deadline':
        tasks = tasks.order_by('deadline_date')
    elif filter_type == 'done':
        tasks = tasks.filter(status='DONE')
    elif filter_type == 'in_progress':
        tasks = tasks.filter(status='INPR')

    context = {
        'tasks': tasks,
    }

    return render(request, 'tasks/tasks_list.html', context=context)


def task_view(request, task_slug):
    task = Task.objects.get(slug=task_slug)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('app_tasks:tasks_list')
    else:
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
