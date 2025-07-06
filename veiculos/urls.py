from django.urls import path
from . import views

urlpatterns = [
    path('consultar/', views.listar_veiculos_disponiveis, name='listar_veiculos'),
    path('cadastrar/', views.cadastrar_veiculo, name='cadastrar_veiculo'),
    path('entrega-quarta/', views.entrega_quarta, name='entrega_quarta_veiculos'),
    path('veiculos/manutencoes/registrar/', views.registrar_manutencao, name='registrar_manutencao'),
    path('manutencoes/', views.listar_manutencoes, name='listar_manutencoes'),
    path('manutencoes/registrar/', views.registrar_manutencao, name='registrar_manutencao'),
    path('manutencoes/concluir/<int:manutencao_id>/', views.concluir_manutencao, name='concluir_manutencao'),
    path('tarifas/', views.listar_tarifas, name='listar_tarifas'),
    path('tarifas/editar/<str:categoria>/', views.editar_tarifa_categoria, name='editar_tarifa_categoria'),
]
