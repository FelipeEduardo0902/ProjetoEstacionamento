from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva
from .forms import ReservaForm, RetiradaVeiculoForm, DevolucaoVeiculoForm
from veiculos.models import Veiculo
from usuarios.models import Funcionario
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# View para reservar veículo
@login_required
def reservar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)

    if request.method == 'POST':
        form = ReservaForm(request.POST, veiculo=veiculo)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.veiculo = veiculo
            reserva.funcionario = Funcionario.objects.first()  # substituir por funcionário logado futuramente

            dias = (reserva.data_fim - reserva.data_inicio).days
            if dias <= 0:
                dias = 1
            reserva.valor_total = dias * veiculo.preco_locacao

            reserva.save()

            veiculo.status_disponibilidade = False
            veiculo.save()

            messages.success(request, "Reserva criada com sucesso.")
            return redirect('listar_reservas')
    else:
        form = ReservaForm(veiculo=veiculo)

    return render(request, 'reservas/reservar.html', {
        'veiculo': veiculo,
        'form': form
    })


# View para listar reservas
@login_required
def listar_reservas(request):
    ordenar = request.GET.get('ordenar', 'data_inicio')
    reservas = Reserva.objects.select_related('cliente', 'veiculo').order_by(ordenar)
    return render(request, 'reservas/listar.html', {'reservas': reservas})

# View para registrar retirada
@login_required
def registrar_retirada(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    veiculo = reserva.veiculo

    if request.method == 'POST':
        form = RetiradaVeiculoForm(request.POST, instance=reserva)
        if form.is_valid():
            retirada = form.save(commit=False)
            retirada.status = "retirada"
            retirada.save()

            veiculo.status_disponibilidade = False
            veiculo.save()

            messages.success(request, "Retirada registrada com sucesso.")
            return redirect('listar_reservas')
    else:
        form = RetiradaVeiculoForm(instance=reserva)

    return render(request, 'reservas/registrar_retirada.html', {
        'reserva': reserva,
        'form': form
    })


# View para registrar devolução
@login_required
def registrar_devolucao_veiculo(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        form = DevolucaoVeiculoForm(request.POST, instance=reserva)
        if form.is_valid():
            devolucao = form.save(commit=False)

            nivel_inicial = reserva.nivel_combustivel_inicial
            nivel_final = devolucao.nivel_combustivel_final
            ordem_combustivel = ['muito_baixo', 'baixo', 'meio', 'cheio']

            if ordem_combustivel.index(nivel_final) < ordem_combustivel.index(nivel_inicial):
                form.add_error('nivel_combustivel_final', 'O nível de combustível deve ser igual ou maior do que na retirada.')
            else:
                devolucao.status = 'finalizada'
                devolucao.save()

                reserva.veiculo.status_disponibilidade = True
                reserva.veiculo.save()

                messages.success(request, "Devolução registrada com sucesso.")
                return redirect('listar_reservas')
    else:
        form = DevolucaoVeiculoForm(instance=reserva)

    return render(request, 'reservas/registrar_devolucao_veiculo.html', {
        'reserva': reserva,
        'form': form
    })

# Relatório e busca
@login_required
def entrega_quarta(request):
    if request.method == 'POST':
        cliente_nome = request.POST.get('cliente_nome', '').strip()
        return redirect(f"{reverse('entrega_quarta')}?cliente_nome={cliente_nome}&ordenar=data_inicio")

    ordenar = request.GET.get('ordenar', 'data_inicio')
    cliente_nome = request.GET.get('cliente_nome', '').strip()

    queryset = Reserva.objects.select_related('cliente', 'veiculo', 'funcionario')

    if cliente_nome:
        queryset = queryset.filter(cliente__nome__icontains=cliente_nome)

    campos_validos = ['data_inicio', 'data_fim', 'valor_total', 'cliente__nome', 'cliente__documento',
                      'veiculo__modelo', 'veiculo__placa', 'funcionario__nome', 'status']

    ordenar_base = ordenar.lstrip('-')
    if ordenar_base not in campos_validos:
        ordenar = 'data_inicio'

    reservas = queryset.order_by(ordenar)

    return render(request, 'reservas/entrega_quarta.html', {
        'reservas': reservas,
        'ordenar': ordenar,
        'cliente_nome': cliente_nome,
    })

# Editar reserva
@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva, veiculo=reserva.veiculo)
        if form.is_valid():
            reserva = form.save(commit=False)
            dias = (reserva.data_fim - reserva.data_inicio).days
            reserva.valor_total = dias * reserva.veiculo.preco_locacao
            reserva.save()
            messages.success(request, 'Reserva atualizada com sucesso.')
            return redirect('entrega_quarta')
    else:
        form = ReservaForm(instance=reserva, veiculo=reserva.veiculo)

    return render(request, 'reservas/editar_reserva.html', {'form': form, 'reserva': reserva})

# Excluir reserva
@login_required
def excluir_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, 'Reserva excluída com sucesso.')
        return redirect('entrega_quarta')
    return render(request, 'reservas/excluir_reserva.html', {'reserva': reserva})
