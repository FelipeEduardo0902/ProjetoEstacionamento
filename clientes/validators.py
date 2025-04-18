from django.core.exceptions import ValidationError
import re

def validar_documento(documento, tipo_pessoa):
    """
    Validação genérica apenas para trabalhos acadêmicos:
    - CPF deve ter 11 dígitos numéricos
    - CNPJ deve ter 14 dígitos numéricos
    - Não faz verificação de dígitos verificadores
    """
    doc = re.sub(r'[^0-9]', '', documento)  # remove . / -

    if tipo_pessoa == 'CPF':
        if len(doc) != 11:
            raise ValidationError("CPF deve conter 11 dígitos numéricos.")
    elif tipo_pessoa == 'CNPJ':
        if len(doc) != 14:
            raise ValidationError("CNPJ deve conter 14 dígitos numéricos.")
