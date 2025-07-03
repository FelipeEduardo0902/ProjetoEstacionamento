from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Cliente
from .forms import ClienteForm
from django.contrib.auth.decorators import login_required

# Cadastro
@login_required
def cadastrar_cliente(request):
    sucesso = False
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            sucesso = True
            form = ClienteForm()
    else:
        form = ClienteForm()
    return render(request, 'clientes/cadastrar.html', {'form': form, 'sucesso': sucesso})

# Listagem com busca
@login_required
def listar_clientes(request):
    busca = request.GET.get('busca', '')
    if busca:
        clientes = Cliente.objects.filter(
            Q(nome__icontains=busca) | Q(documento__icontains=busca)
        )
    else:
        clientes = Cliente.objects.all()
    return render(request, 'clientes/listar.html', {'clientes': clientes, 'busca': busca})

# Edição
@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar.html', {'form': form, 'cliente': cliente})

# Exclusão
@login_required
def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'clientes/excluir_cliente.html', {'cliente': cliente})
