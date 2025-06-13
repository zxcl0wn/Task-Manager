from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from projects.models import Project
from .models import Task, Subtask
from .forms import TaskForm, TaskCreateForm, SubtaskChangeForm


@login_required(login_url='app_user:login')
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


@login_required(login_url='app_user:login')
def task_view(request, task_slug):
    task = Task.objects.get(slug=task_slug)
    subtasks = Subtask.objects.filter(task=task.id)

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
        'subtasks': subtasks,
        'form': form
    }

    return render(request, 'tasks/task.html', context=context)


@login_required(login_url='app_user:login')
def task_create(request):
    project_slug = request.GET.get('project')
    initial_data = {}

    if project_slug:
        project = get_object_or_404(Project, slug=project_slug)
        initial_data['project'] = project.id

    if request.method == "POST":
        form = TaskCreateForm(request.POST)
        project_slug = Project.objects.get(id=request.POST['project']).slug

        if form.is_valid():
            form.save()
            return redirect('app_projects:project_view', project_slug=project_slug)
        else:
            print(form.errors)
    else:
        form = TaskCreateForm(initial=initial_data)

    context = {
        'form': form
    }

    return render(request, 'tasks/task_form.html', context=context)


@login_required(login_url='app_user:login')
def task_delete(request, task_slug):
    task = Task.objects.get(slug=task_slug)

    if request.method == "POST":
        task.delete()
    return redirect('app_tasks:tasks_list')


@login_required(login_url='app_user:login')
def subtask_delete(request, subtask_id):
    subtask = Subtask.objects.get(id=subtask_id)
    task = subtask.task

    if request.method == "POST":
        print(f'!!!')
        subtask.delete()
        return redirect('app_tasks:task_view', task_slug=task.slug)


@login_required(login_url='app_user:login')
def subtask_create(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        Subtask.objects.create(task=task, title="Новая подзадача")

        return redirect('app_tasks:task_view', task_slug=task.slug)


@login_required(login_url='app_user:login')
def subtask_change(request, subtask_id):
    subtask = Subtask.objects.get(id=subtask_id)

    if request.method == "POST":
        form = SubtaskChangeForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            return redirect('app_tasks:tasks_list')
    else:
        form = SubtaskChangeForm(instance=subtask)

    context = {
        'form': form
    }

    return render(request, 'tasks/subtask_change.html', context=context)
