from django.shortcuts import render, redirect
from .forms import FuncionarioForm
from .models import Funcionario
from django.contrib.auth import authenticate, login
from django.contrib import messages

def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FuncionarioForm()
    return render(request, 'usuarios/cadastrar_funcionario.html', {'form': form})

def listar_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'usuarios/listar_funcionarios.html', {'funcionarios': funcionarios})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            return redirect('home')  # redireciona para o painel principal
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'usuarios/login.html')