from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User



class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    cargo = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=128)  # Cuidado com senha aqui, ideal é nem salvar, mas segue se o prof pediu
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome


class Administrador(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return self.nome

