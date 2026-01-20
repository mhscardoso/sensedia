from django.urls import path
from . import views


urlpatterns = [
    path('', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('login', views.signin, name='login'),
    path('logout', views.signout, name='logout'),
]
