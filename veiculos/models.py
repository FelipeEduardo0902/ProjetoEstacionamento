from django.db import models

class Veiculo(models.Model):
    CATEGORIAS = [
        ('hatch', 'Hatch'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('pickup', 'Pickup'),
        ('luxo', 'Luxo'),
        ('utilitario', 'Utilitário'),
    ]

    STATUS = [
        ('disponivel', 'Disponível'),
        ('alugado', 'Alugado'),
        ('manutencao', 'Em Manutenção'),
    ]

    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    ano = models.IntegerField()
    cor = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    placa = models.CharField(max_length=10, unique=True)
    preco_locacao = models.DecimalField(max_digits=8, decimal_places=2)
    status_disponibilidade = models.CharField(max_length=20, choices=STATUS, default='disponivel')
    imagem = models.ImageField(upload_to='veiculos/', null=True, blank=True)

    def __str__(self):
        return f"{self.modelo} - {self.placa}"
    
class Manutencao(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.RESTRICT, related_name='manutencoes')
    motivo = models.TextField()
    data_inicio = models.DateField(auto_now_add=True)
    previsao_conclusao = models.DateField()
    concluida = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Atualiza o status do veículo automaticamente
        if not self.concluida:
            self.veiculo.status = 'Em manutenção'
        else:
            # Verifica se existem outras manutenções abertas
            abertas = Manutencao.objects.filter(veiculo=self.veiculo, concluida=False).exclude(id=self.id).exists()
            if not abertas:
                self.veiculo.status = 'Disponível'
        self.veiculo.save()
