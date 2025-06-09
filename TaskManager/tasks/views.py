from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm, TaskCreateForm


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
    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['priority'] = task.priority
        post_data['deadline_date'] = task.deadline_date
        post_data['project'] = task.project
        form = TaskForm(post_data, instance=task)
        if form.is_valid():
            form.save()
            return redirect('app_tasks:tasks_list')
        else:
            print(f'NOT VALID: {form.errors}')
    else:
        form = TaskForm(instance=task)

    context = {
        'task': task,
        'form': form
    }

    return render(request, 'tasks/task.html', context=context)


def task_create(reqeust):
    form = TaskCreateForm

    if reqeust.method == "POST":
        form = TaskCreateForm(reqeust.POST)
        if form.is_valid():
            form.save()
            return redirect('app_tasks:tasks_list')
        else:
            print(form.errors)

    context = {
        'form': form
    }

    return render(reqeust, 'tasks/task_form.html', context=context)


def task_delete(request, task_slug):
    task = Task.objects.get(slug=task_slug)

    if request.method == "POST":
        task.delete()
        return redirect('app_tasks:tasks_list')