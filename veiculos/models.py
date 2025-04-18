from django.db import models

# Create your models here.
from django.db import models

class Veiculo(models.Model):
    STATUS = [
        ('DISPONIVEL', 'Disponível'),
        ('ALUGADO', 'Alugado'),
        ('MANUTENCAO', 'Em Manutenção'),
    ]

    modelo = models.CharField(max_length=100)
    status_disponibilidade = models.BooleanField(default=True)
    preco_locacao = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)
    imagem = models.ImageField(upload_to='veiculos/', null=True, blank=True)


    def __str__(self):
        return f"{self.modelo} - {self.placa}"
