import datetime
from time import strftime
from .utils import get_user_role
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect

from notification.models import Notification
from user.middleware import get_current_user
from .models import Project, ProjectMember
from .forms import ProjectForm, ProjectCreateForm, AddMembersForm
from tasks.models import Task


def main_page(request):

    context = {

    }

    return render(request, 'projects/main.html', context=context)


@login_required(login_url='app_user:login')
def projects_list(request):
    all_projects = Project.objects.filter()
    # projects = []
    projects_with_roles = []

    # for project in all_projects:
    #     project_members = ProjectMember.objects.filter(project=project, user=get_current_user()).exists()
    #     if project_members:
    #         projects.append(project)
    #         # print(f'Project: {project}\nProject members: {project_members}\n')
    #
    # context = {
    #     'projects': projects
    # }

    memberships = ProjectMember.objects.filter(
        user=request.user
    ).select_related('project')

    for membership in memberships:
        projects_with_roles.append({
            'project': membership.project,
            'is_admin': membership.user_role == 'OWNER'
        })

    context = {
        'projects_with_roles': projects_with_roles
    }

    return render(request, 'projects/projects_list.html', context=context)


@login_required(login_url='app_user:login')
def project_view(request, project_slug):
    project = Project.objects.get(slug=project_slug)
    project_tasks = Task.objects.filter(project=project.id)
    members = ProjectMember.objects.filter(project=project).select_related('user')
    user_status = get_user_role(project)

    if get_current_user() not in User.objects.filter(id__in=ProjectMember.objects.filter(project=project).values_list('user', flat=True)):
        raise PermissionDenied("У вас нет доступа к этой задаче")

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['status'] = project.status
        post_data.setlist('users', ProjectMember.objects.filter(
            project=project
        ).values_list('user', flat=True))

        print(f'post data users: {post_data}')
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
        'form': form,
        'user_status': user_status
    }

    return render(request, 'projects/project.html', context=context)


@login_required(login_url='app_user:login')
def create_project(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        current_user = get_current_user()
        form = ProjectCreateForm(post_data)
        # print(f'!{form['users'].value()}')
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            form.save_m2m()

            ProjectMember.objects.get_or_create(
                project=project,
                user=current_user,
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


@login_required(login_url='app_user:login')
def project_delete(request, project_slug):
    project = Project.objects.get(slug=project_slug)
    members = User.objects.filter(id__in=ProjectMember.objects.filter(project=project).values_list('user', flat=True))
    user_role = get_user_role(project)
    if (get_current_user() not in members) or (user_role != "OWNER"):
        raise PermissionDenied("У вас нет доступа к этой задаче")

    if request.method == "POST":
        project.delete()

        return redirect('app_projects:projects_list')


@login_required(login_url='app_user:login')
def add_members(request, project_slug):
    project = Project.objects.get(slug=project_slug)
    members = User.objects.filter(id__in=ProjectMember.objects.filter(project=project).values_list('user', flat=True))
    user_role = get_user_role(project)

    if (get_current_user() not in members) or (project.status == "PRIVATE") or (user_role != "OWNER"):
        raise PermissionDenied("У вас нет доступа к этой задаче")

    if request.method == "POST":
        form = AddMembersForm(request.POST, project=project)
        user = User.objects.get(id=request.POST['user'])
        user_role = request.POST['user_role']

        ProjectMember.objects.create(
            project=project,
            user=user,
            user_role=user_role
        )
        return redirect('app_projects:project_view', project_slug=project.slug)
    else:
        form = AddMembersForm(project=project)
    context = {
        'form': form
    }

    return render(request, 'projects/add_members.html', context=context)