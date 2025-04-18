from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva
from .forms import ReservaForm, RetiradaVeiculoForm, DevolucaoVeiculoForm
from veiculos.models import Veiculo
from usuarios.models import Funcionario
from django.contrib import messages

# View para reservar veículo
def reservar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)

    if request.method == 'POST':
        form = ReservaForm(request.POST, veiculo=veiculo)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.veiculo = veiculo
            reserva.funcionario = Funcionario.objects.first()  # substituir por funcionário logado futuramente
            dias = (reserva.data_fim - reserva.data_inicio).days
            reserva.valor_total = dias * veiculo.preco_locacao
            reserva.save()

            veiculo.status_disponibilidade = False
            veiculo.save()

            return redirect('home')
    else:
        form = ReservaForm(veiculo=veiculo)

    return render(request, 'reservas/reservar.html', {
        'veiculo': veiculo,
        'form': form
    })


# View para listar reservas
def listar_reservas(request):
    reservas = Reserva.objects.select_related('cliente', 'veiculo').all()
    return render(request, 'reservas/listar.html', {'reservas': reservas})


# View para registrar retirada
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
def registrar_devolucao_veiculo(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        form = DevolucaoVeiculoForm(request.POST, instance=reserva)
        if form.is_valid():
            devolucao = form.save(commit=False)

            # Validação: combustível final deve ser igual ou superior ao inicial
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
