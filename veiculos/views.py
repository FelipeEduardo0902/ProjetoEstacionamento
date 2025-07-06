from django.shortcuts import render, redirect
from .models import Veiculo, Manutencao
from django.shortcuts import get_object_or_404
from .forms import VeiculoForm, ManutencaoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def listar_veiculos_disponiveis(request):
    # Mostra apenas veículos disponíveis
    veiculos = Veiculo.objects.filter(status_disponibilidade='disponivel')
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
            print(form.errors)  # Exibe erros no terminal
    else:
        form = VeiculoForm()

    return render(request, 'veiculos/cadastrar.html', {'form': form})


@login_required
def entrega_quarta(request):
    # Lista todos os veículos, independentemente do status
    veiculos = Veiculo.objects.all()
    return render(request, 'veiculos/entrega_quarta.html', {'veiculos': veiculos})

@login_required
def listar_manutencoes(request):
    manutencoes = Manutencao.objects.select_related('veiculo').all()
    return render(request, 'veiculos/listar_manutencoes.html', {'manutencoes': manutencoes})

@login_required
def registrar_manutencao(request):
    if request.method == 'POST':
        form = ManutencaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_manutencoes')
    else:
        form = ManutencaoForm()
    
    return render(request, 'veiculos/registrar_manutencao.html', {'form': form})

@login_required
def concluir_manutencao(request, manutencao_id):
    manut = get_object_or_404(Manutencao, pk=manutencao_id)
    manut.concluida = True
    manut.save()
    return redirect('listar_manutencoes')

@login_required
def listar_tarifas(request):
    veiculos = Veiculo.objects.all()
    categorias = veiculos.values_list('categoria', flat=True).distinct()
    return render(request, 'veiculos/tarifas.html', {
        'veiculos': veiculos,
        'categorias': categorias,
    })

@login_required
def editar_tarifa_categoria(request, categoria):
    veiculos = Veiculo.objects.filter(categoria=categoria)

    if request.method == 'POST':
        novo_preco = request.POST.get('novo_preco')
        if novo_preco:
            for veiculo in veiculos:
                veiculo.preco_locacao = novo_preco
                veiculo.save()
            return redirect('listar_tarifas')  # ou qualquer nome de view que exiba a tabela de veículos
    return render(request, 'veiculos/editar_tarifa_categoria.html', {
        'categoria': categoria,
        'veiculos': veiculos
    })

