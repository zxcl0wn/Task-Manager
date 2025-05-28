from django.shortcuts import render


def main_page(request):
    context = {

    }

    return render(request, 'projects/main.html', context=context)


def projects_list(request):
    context = {

    }

    return render(request, 'projects/projects_list.html', context=context)


def project_view(request):
    context = {

    }

    return render(request, 'projects/project.html', context=context)


def create_project(request):
    context = {

    }

    return render(request, 'projects/project_form.html', context=context)
