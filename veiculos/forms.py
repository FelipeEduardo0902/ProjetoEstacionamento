from django import forms
from .models import Veiculo, Manutencao


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['modelo', 'marca', 'ano', 'cor', 'placa', 'categoria',
                  'preco_locacao', 'status_disponibilidade', 'imagem']


    widgets = {
        'modelo': forms.TextInput(attrs={'class': 'validate'}),
        'marca': forms.TextInput(attrs={'class': 'validate'}),
        'ano': forms.NumberInput(attrs={'class': 'validate'}),
        'cor': forms.TextInput(attrs={'class': 'validate'}),
        'placa': forms.TextInput(attrs={'class': 'validate'}),
        'categoria': forms.TextInput(attrs={'class': 'validate'}),
        'preco_locacao': forms.NumberInput(attrs={'class': 'validate'}),
        'status_disponibilidade': forms.CheckboxInput(attrs={'class': 'filled-in'}),
}

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['veiculo', 'motivo', 'previsao_conclusao']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'previsao_conclusao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'veiculo': 'Veículo',
            'motivo': 'Motivo da Manutenção',
            'previsao_conclusao': 'Previsão de Conclusão',
        }
