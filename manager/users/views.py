from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import User

def profile(request: HttpRequest):
    context = {
        'user': request.user
    }

    print(context['user'])

    return render(request, template_name='profile.html', context=context)

def signup(request: HttpRequest):

    if request.method != 'POST':
        return render(
            request,
            template_name='registration/register.html'
        )
    

    complete_name = request.POST['name']
    email         = request.POST['email']
    password      = request.POST['password']
    password_conf = request.POST['password_confirm']
    cpf           = request.POST['cpf']
    phone         = request.POST['phone']
    birth         = request.POST['birth']

    accept_terms  = request.POST['use_term']

    if accept_terms != 'on':
        messages.info(request, 'Termos de Uso devem ser aceitos')
        return redirect('signup')

    if password != password_conf:
        messages.info(request, 'Senhas não coincidem')
        return redirect('signup')

    if User.objects.filter(cpf=cpf).exists():
        messages.info(request, 'CPF já Cadastrado')
        return redirect('signup')
    
    if User.objects.filter(phone=phone).exists():
        messages.info(request, 'Telefone já Cadastrado')
        return redirect('signup')
    

    user: User = User.objects.create_user(
        username=complete_name,
        complete_name=complete_name,
        email=email,
        password=password,
        cpf=cpf,
        phone=phone,
        birth_date=birth,
        is_active=True,
    )

    user.save()

    return redirect('login')



def signin(request: HttpRequest):

    if request.method != 'POST':
        print('cai aqui')
        return render(
            request,
            template_name='registration/login.html'
        )
    

    
    
    email = request.POST['email']
    password = request.POST['password']

    only_user = User.objects.filter(email=email)

    if not only_user.exists():
        messages.info(request, 'Usuário não encontrado')
        return redirect('login')
    
    username = only_user.first().username

    user = authenticate(username=username, password=password)

    if user is None:
        messages.info(request, 'Credenciais Inválidas')
        return redirect('login')
    
    login(request, user)
    return redirect('/')



def signout(request: HttpRequest):

    logout(request)
    return redirect('login')


