from django.shortcuts import render, redirect
from .forms import FuncionarioForm
from .models import Funcionario
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            funcionario = form.save(commit=False)
            username = funcionario.email  # E-mail como username

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Já existe um usuário com esse e-mail.')
                return render(request, 'usuarios/cadastrar_funcionario.html', {'form': form})

            # Criação do usuário
            user = User.objects.create_user(
                username=username,
                password=form.cleaned_data['senha'],
                first_name=funcionario.nome  # Salva o nome no User para login alternativo
            )

            funcionario.user = user
            funcionario.save()

            messages.success(request, 'Funcionário e usuário criados com sucesso!')
            return redirect('home')
    else:
        form = FuncionarioForm()

    return render(request, 'usuarios/cadastrar_funcionario.html', {'form': form})


@login_required
def listar_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    return render(request, 'usuarios/listar_funcionarios.html', {'funcionarios': funcionarios})


def login_view(request):
    if request.method == 'POST':
        login_input = request.POST.get('username')
        senha = request.POST.get('password')

        # Primeiro tenta pelo e-mail (username)
        user = User.objects.filter(username=login_input).first()

        # Se não achou pelo e-mail, tenta pelo nome
        if not user:
            user = User.objects.filter(first_name=login_input).first()

        if user:
            auth_user = authenticate(request, username=user.username, password=senha)
            if auth_user:
                login(request, auth_user)
                return redirect('home')
        
        messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'usuarios/login.html')


@login_required
def entrega_quarta(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/entrega_quarta.html', {'usuarios': usuarios})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
