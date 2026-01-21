import json
from datetime import datetime, date
from django.http import HttpRequest
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404

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

    if len(name) >= 20:
        messages.info(request, 'Nome do projeto deve ser menor que 20 caracteres')
        return redirect('create_project')

    if not user_filter.exists():
        messages.info(request, "Usuário não Encontrado")
        return redirect('create_project')
    
    date_start = datetime.strptime(start_date, '%Y-%m-%d').date()
    if date_start <= date.today():
        messages.info(request, "Data de início deve ser maior que a atual")
        return redirect('create_project')
    
    date_end = datetime.strptime(end_date, '%Y-%m-%d').date()
    if date_end <= date_start:
        messages.info(request, "Data de fim deve ser maior que a de início")
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



@require_http_methods(["GET", "POST", "PATCH", "DELETE"])
@login_required(login_url='login')
def project_details(request: HttpRequest, project_id: int):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method not in ['POST']:
        tasks = Items.objects.filter(project=project)
        users = User.objects.values(
            'id', 'complete_name', 'username'
        )

        pending_tasks = tasks.filter(status=Status.PENDING)
        working_tasks = tasks.filter(status=Status.WORKING)
        done_tasks    = tasks.filter(status=Status.DONE)

        all_users = User.objects.filter(
            Q(owned_projects=project) |
            Q(items__project=project)
        ).distinct()

        context = { 
            'project': project,
            'tasks': [
                (1, Status.PENDING, 'Pendentes', pending_tasks), 
                (2, Status.WORKING, 'Em Andamento', working_tasks), 
                (3, Status.DONE, 'Concluído', done_tasks)
            ],

            'users': users,
            'related_users': all_users,
        }

        return render(request, template_name='project_detail.html', context=context)
    

    if request.method == 'POST':
        status      = request.POST['status']
        title       = request.POST['title']
        description = request.POST['description']
        forecast    = request.POST['date']
        user_id     = request.POST['user_id']

        if forecast != "":
            date_end = datetime.strptime(forecast, '%Y-%m-%d').date()
            if date_end <= date.today():
                messages.info(request, "Data de fim deve ser maior que a atual")
                return redirect('project_detail', project_id=project_id)
        else:
            forecast = None
        
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
            forecast=forecast,
            owner=user,
            project=project,
            status=status,
        )

        item.save()

        return redirect('project_detail', project_id=project_id)
    


    if request.method == 'PUT':
        return redirect('project_detail', project_id=project_id)



@require_http_methods(["PATCH"])
@login_required(login_url='login')
def project_change_name(request: HttpRequest, project_id: int):
    project = get_object_or_404(Project, id=project_id)

    data = json.loads(request.body)

    project_name = data['project_name']

    if len(project_name) >= 20:
        messages.info(request, 'Nome deve ter menos de 20 caracteres')
        return redirect('project_detail', project_id=project_id)

    project.name = project_name
    project.save()

    return redirect('project_detail', project_id=project.id)
