from django import forms
from .models import Funcionario
from clientes.validators import validar_documento

class FuncionarioForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'validate'}),
        label='Senha',
        required=True
    )

    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'cargo', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'validate'}),
            'cpf': forms.TextInput(attrs={'class': 'validate'}),
            'cargo': forms.TextInput(attrs={'class': 'validate'}),
            'email': forms.EmailInput(attrs={'class': 'validate'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        validar_documento(cpf, 'CPF')  # Validação centralizada
        return cpf
