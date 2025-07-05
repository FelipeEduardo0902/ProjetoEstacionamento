from django import forms
from .models import Reserva
from django.core.exceptions import ValidationError

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'data_inicio', 'data_fim']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.veiculo = kwargs.pop('veiculo', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        if data_inicio and data_fim and self.veiculo:
            conflitos = Reserva.objects.filter(
                veiculo=self.veiculo,
                data_inicio__lt=data_fim,
                data_fim__gt=data_inicio,
                status__in=['ativa', 'retirada']  # supondo que reservas finalizadas não interferem
            )
            if conflitos.exists():
                raise ValidationError("Este veículo já possui uma reserva no período selecionado.")

        return cleaned_data


class RetiradaVeiculoForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['quilometragem_inicial', 'nivel_combustivel_inicial', 'observacoes_inicial']
        widgets = {
            'nivel_combustivel_inicial': forms.Select(choices=Reserva.COMBUSTIVEL_CHOICES, attrs={'class': 'form-select'}),
            'observacoes_inicial': forms.Textarea(attrs={'class': 'form-control'}),
        }


class DevolucaoVeiculoForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['quilometragem_final', 'nivel_combustivel_final', 'observacoes_final']
        widgets = {
            'nivel_combustivel_final': forms.Select(choices=Reserva.COMBUSTIVEL_CHOICES, attrs={'class': 'form-select'}),
            'observacoes_final': forms.Textarea(attrs={'class': 'form-control'}),
        }
