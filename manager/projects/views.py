from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.models import User
from .models import Project


@login_required(login_url='login')
def create_project(request: HttpRequest):

    if request.method != "POST":
        users = User.objects.values(
            'id', 'complete_name', 'username'
        )

        context = { "users": users }

        return render(request, template_name='create_project.html', context=context)


    name        = request.POST['name']
    description = request.POST['description']
    start_date  = request.POST['start_date']
    end_date    = request.POST['end_date']
    user_id     = request.POST['user_id']

    user_filter = User.objects.filter(id=user_id)

    if not user_filter.exists():
        messages.info(request, "Usuário não Encontrado")
        return redirect('create_project')
    
    user: User = user_filter.first()

    project = Project.objects.create(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        owner = user,
    )

    project.save()

    messages.info(request, "Projeto Criado")

    return redirect('create_project')


@login_required(login_url='login')
def all_projects(request: HttpRequest):
    projects = Project.objects.all().values()

    context = {
        'projects': projects
    }

    return render(request, template_name='all_projects.html', context=context)



@login_required(login_url='login')
def user_projects(request: HttpRequest):
    user = request.user

    projects = Project.objects.filter(owner=user)

    context = {
        'projects': projects
    }

    return render(request, template_name='user_projects.html', context=context)

