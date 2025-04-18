from django import forms
from .models import Cliente
from .validators import validar_documento
import re

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['tipo_pessoa', 'documento', 'nome', 'telefone', 'endereco']
        widgets = {
            'tipo_pessoa': forms.Select(attrs={'class': 'browser-default'}),
            'documento': forms.TextInput(attrs={
                'class': 'validate',
                'maxlength': '18',
                'title': 'Digite CPF ou CNPJ com ou sem pontuação'
            }),
            'nome': forms.TextInput(attrs={'class': 'validate'}),
            'telefone': forms.TextInput(attrs={'class': 'validate'}),
            'endereco': forms.Textarea(attrs={'class': 'materialize-textarea'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo_pessoa")
        doc = cleaned_data.get("documento")

        if tipo and doc:
            # 🔥 Remove a pontuação ANTES de validar
            documento_sem_pontuacao = re.sub(r'[^0-9]', '', doc)
            try:
                validar_documento(documento_sem_pontuacao, tipo)
            except forms.ValidationError as e:
                self.add_error('documento', e)

            # ✅ Atualiza o campo no cleaned_data com a versão sem pontuação
            cleaned_data['documento'] = documento_sem_pontuacao
