from django.shortcuts import render,redirect
from .models import Veiculo
from .forms import VeiculoForm
from django.contrib import messages


def listar_veiculos_disponiveis(request):
    veiculos = Veiculo.objects.filter(status_disponibilidade=True)
    return render(request, 'veiculos/listar.html', {'veiculos': veiculos})




def cadastrar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo cadastrado com sucesso!')  # ✅ Aqui
            return redirect('home')
    else:
        form = VeiculoForm()

    return render(request, 'veiculos/cadastrar.html', {'form': form})

def entrega_quarta(request):
    veiculos = Veiculo.objects.all()
    return render(request, 'veiculos/entrega_quarta.html', {'veiculos': veiculos})