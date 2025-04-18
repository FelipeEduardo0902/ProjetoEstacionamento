from django import forms
from .models import Reserva
from django.core.exceptions import ValidationError

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'data_inicio', 'data_fim']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'browser-default'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'validate'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'validate'}),
        }

    def __init__(self, *args, **kwargs):
        self.veiculo = kwargs.pop('veiculo', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValidationError("A data de devolução não pode ser anterior à data de retirada.")

        if self.veiculo and not self.veiculo.status_disponibilidade:
            raise ValidationError(f"O veículo '{self.veiculo}' está indisponível.")


class RetiradaVeiculoForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['quilometragem_inicial', 'nivel_combustivel_inicial', 'observacoes_inicial']
        widgets = {
            'nivel_combustivel_inicial': forms.Select(choices=Reserva.COMBUSTIVEL_CHOICES, attrs={'class': 'browser-default'}),
            'observacoes_inicial': forms.Textarea(attrs={'class': 'materialize-textarea'}),
        }


class DevolucaoVeiculoForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['quilometragem_final', 'nivel_combustivel_final', 'observacoes_final']
        widgets = {
            'nivel_combustivel_final': forms.Select(choices=Reserva.COMBUSTIVEL_CHOICES, attrs={'class': 'browser-default'}),
            'observacoes_final': forms.Textarea(attrs={'class': 'materialize-textarea'}),
        }
