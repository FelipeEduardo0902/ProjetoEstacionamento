from django.urls import path
from . import views

urlpatterns = [
    path('consultar/', views.listar_veiculos_disponiveis, name='listar_veiculos'),
    path('cadastrar/', views.cadastrar_veiculo, name='cadastrar_veiculo'),
    path('entrega-quarta/', views.entrega_quarta, name='entrega_quarta_veiculos'),

]
