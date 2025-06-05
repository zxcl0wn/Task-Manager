from django.shortcuts import render
from .models import Project


def main_page(request):
    print(request)
    
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

    context = {
        'project': project
    }

    return render(request, 'projects/project.html', context=context)


def create_project(request):
    context = {

    }

    return render(request, 'projects/project_form.html', context=context)
