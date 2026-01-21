from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_projects, name='user_projects'),
    path('create', views.create_project, name='create_project'),
    path('all', views.all_projects, name='all_projects'),
    path('<int:project_id>/', views.project_details, name='project_detail'),
    path('<int:project_id>/name/', views.project_change_name, name='project_change_name'),
]