import json
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from .models import Items, Status
from projects.models import Project

@require_http_methods(["PATCH"])
@login_required(login_url='login')
def update_card(request, item_id):
    data = json.loads(request.body)

    card = get_object_or_404(Items, id=item_id)
    project: Project = card.project

    status = data["status"]

    if status not in [Status.PENDING, Status.WORKING, Status.DONE]:
        messages.info(request, 'Status não está na lista')
        return redirect('project_detail', project_id=project.id)
    
    card.status = status

    card.save()

    return redirect('project_detail', project_id=project.id)
