from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.models import User
from items.models import Items, Status
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



@login_required(login_url='login')
def project_details(request: HttpRequest, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method != 'POST':
        tasks = Items.objects.filter(project=project)
        users = User.objects.values(
            'id', 'complete_name', 'username'
        )

        pending_tasks = tasks.filter(status=Status.PENDING)
        working_tasks = tasks.filter(status=Status.WORKING)
        done_tasks    = tasks.filter(status=Status.DONE)

        context = { 
            'project': project,
            'tasks': [
                (1, Status.PENDING, 'Pendentes', pending_tasks), 
                (2, Status.WORKING, 'Em Andamento', working_tasks), 
                (3, Status.DONE, 'Concluído', done_tasks)
            ],

            'users': users,
        }

        return render(request, template_name='project_detail.html', context=context)
    

    if request.method == 'POST':
        status      = request.POST['status']
        title       = request.POST['title']
        description = request.POST['description']
        date        = request.POST['date']
        user_id     = request.POST['user_id']

        if date == "":
            date = None
        
        if status not in [Status.PENDING, Status.WORKING, Status.DONE]:
            messages.info(request, 'Status não está na lista')
            return redirect('project_detail', project_id=project_id)
        
        if len(title) > 20:
            messages.info(request, 'Título muito longo')
            return redirect('project_detail', project_id=project_id)
        
        if len(description) > 100:
            messages.info(request, 'Descrição muito longa')
            return redirect('project_detail', project_id=project_id)
        
        if user_id == "":
            messages.info(request, 'Usuário responsável não definido')
            return redirect('project_detail', project_id=project_id)
        

        user = get_object_or_404(User, id=user_id)
        
        item = Items.objects.create(
            title=title,
            description=description,
            forecast=date,
            owner=user,
            project=project,
            status=status,
        )

        item.save()

        return redirect('project_detail', project_id=project_id)
    
    

