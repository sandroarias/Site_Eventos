from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth
import re

def cadastro(request):
    if request.method =="GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not (senha == confirmar_senha):
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem.')
            return redirect(reverse('cadastro'))
        
        if len(senha) < 8:
            messages.add_message(request, constants.ERROR, 'Sua senha deve conter 8 ou mais caracteres.')
            return redirect(reverse('cadastro'))
        
        if not re.search('[A-Z]', senha):
            messages.add_message(request, constants.ERROR, 'Sua senha não contem letras maiúsculas')
            return redirect(reverse('cadastro'))
        
        if not re.search('[a-z]', senha):
            messages.add_message(request, constants.ERROR, 'Sua senha não contem letras minúsculas')
            return redirect(reverse('cadastro'))
        
        if not re.search('[0-9]', senha):
            messages.add_message(request, constants.ERROR, 'Sua senha não contém números')
            return redirect(reverse('cadastro'))
        
        

        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existe.')
            return redirect(reverse('cadastro'))
        
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        messages.add_message(request, constants.SUCCESS, 'Usuário salvo com sucesso')
        
        return redirect(reverse('login'))
        

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(username=username, password=senha)
        
        if not user:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos!')
            return redirect(reverse('login'))
            
        
        auth.login(request, user)
        return redirect('/eventos/novo_evento/')