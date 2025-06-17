from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'veiculo', 'data_inicio', 'data_fim', 'valor_total', 'status')
    readonly_fields = ('valor_total',)

    fieldsets = (
        ('Dados da Reserva', {
            'fields': ('cliente', 'veiculo', 'funcionario', 'data_inicio', 'data_fim', 'valor_total', 'status')
        }),
        ('Retirada', {
            'fields': ('quilometragem_inicial', 'nivel_combustivel_inicial', 'observacoes_inicial')
        }),
        ('Devolução', {
            'fields': ('quilometragem_final', 'nivel_combustivel_final', 'observacoes_final')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Calcular valor_total aqui também, só se tiver datas e veículo
        if obj.data_inicio and obj.data_fim and obj.veiculo:
            dias = (obj.data_fim - obj.data_inicio).days
            if dias <= 0:
                dias = 1
            obj.valor_total = dias * obj.veiculo.preco_locacao
        super().save_model(request, obj, form, change)
