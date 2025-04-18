from django.db import models
from .validators import validar_documento


# Create your models here.
from django.db import models

class Cliente(models.Model):
    TIPO_PESSOA = [
        ('CPF', 'Pessoa Física'),
        ('CNPJ', 'Pessoa Jurídica'),
    ]

    tipo_pessoa = models.CharField(max_length=4, choices=TIPO_PESSOA)
    documento = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
    
    def clean(self):
        validar_documento(self.documento, self.tipo_pessoa)
    
