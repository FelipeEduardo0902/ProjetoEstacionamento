from django import forms
from .models import Veiculo


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
