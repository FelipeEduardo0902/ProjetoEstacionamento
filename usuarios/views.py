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

            # Define o username como o e-mail do funcionário
            username = funcionario.email

            # Verifica se já existe usuário com o mesmo e-mail (username)
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Já existe um usuário com esse e-mail.')
                return render(request, 'usuarios/cadastrar_funcionario.html', {'form': form})

            # Cria o usuário corretamente usando create_user
            user = User.objects.create_user(
                username=username,
                password=form.cleaned_data['senha']
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
        username = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            return redirect('home')  # redireciona para o painel principal
        else:
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
