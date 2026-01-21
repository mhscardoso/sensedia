from django.urls import path
from . import views


urlpatterns = [
    path('<int:item_id>/', views.update_card, name='update_card'),
    path('<int:item_id>/delete/', views.delete_card, name='delete_card'),
]