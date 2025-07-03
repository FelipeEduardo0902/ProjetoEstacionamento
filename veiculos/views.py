from django.shortcuts import render, redirect
from .models import Veiculo
from .forms import VeiculoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def listar_veiculos_disponiveis(request):
    veiculos = Veiculo.objects.all()
    return render(request, 'veiculos/listar.html', {'veiculos': veiculos})


@login_required
def cadastrar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('home')
        else:
            print(form.errors)  # Mostra os erros no terminal
    else:
        form = VeiculoForm()

    return render(request, 'veiculos/cadastrar.html', {'form': form})


@login_required
def entrega_quarta(request):
    veiculos = Veiculo.objects.all()
    return render(request, 'veiculos/entrega_quarta.html', {'veiculos': veiculos})
