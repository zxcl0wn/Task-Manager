import datetime
from time import strftime

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from notification.models import Notification
from user.middleware import get_current_user
from .models import Project, ProjectMember
from .forms import ProjectForm, ProjectCreateForm
from tasks.models import Task


def main_page(request):

    context = {

    }

    return render(request, 'projects/main.html', context=context)


def projects_list(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }

    return render(request, 'projects/projects_list.html', context=context)


def project_view(request, project_slug):
    project = Project.objects.get(slug=project_slug)
    project_tasks = Task.objects.filter(project=project.id)
    members = ProjectMember.objects.filter(project=project).select_related('user')

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['status'] = project.status
        post_data['users'] = list(map(str, project.users.all().values_list('id', flat=True)))[0]

        # print(f'post_data 2: {post_data}')
        form = ProjectForm(post_data, instance=project)
        if form.is_valid():
            form.save()
            return redirect('app_projects:projects_list')
        else:
            print(f'\n\n{form.errors}\n\n')
    else:
        form = ProjectForm(instance=project)

    context = {
        'project': project,
        'tasks': project_tasks,
        'members': members,
        'form': form
    }

    return render(request, 'projects/project.html', context=context)


def create_project(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        current_user = get_current_user()
        form = ProjectCreateForm(post_data)
        print(f'!{form['users'].value()}')
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            form.save_m2m()

            ProjectMember.objects.get_or_create(
                project=project,
                user=request.user,
                defaults={'user_role': 'OWNER'}
            )
            return redirect('app_projects:projects_list')
        else:
            print(form.errors)
    else:
        form = ProjectCreateForm()

    context = {
        'form': form
    }

    return render(request, 'projects/project_form.html', context=context)


def project_delete(request, project_slug):
    project = Project.objects.get(slug=project_slug)

    if request.method == "POST":
        project.delete()

        return redirect('app_projects:projects_list')