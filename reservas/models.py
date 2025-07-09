from django.db import models
from django.core.exceptions import ValidationError
from clientes.models import Cliente
from veiculos.models import Veiculo
from usuarios.models import Funcionario

class Reserva(models.Model):
    STATUS_CHOICES = [
        ('confirmada', 'Confirmada'),
        ('pendente', 'Pendente'),
        ('retirada', 'Retirada'),
        ('finalizada', 'Finalizada'),
    ]

    COMBUSTIVEL_CHOICES = [
        ('cheio', 'Cheio'),
        ('3/4', '3/4'),
        ('meio', 'Meio'),
        ('1/4', '1/4'),
        ('quase_vazio', 'Quase vazio'),
        ('vazio', 'Vazio'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    # Dados da retirada
    quilometragem_inicial = models.IntegerField(null=True, blank=True)
    nivel_combustivel_inicial = models.CharField(
        max_length=20,
        choices=COMBUSTIVEL_CHOICES,
        null=True,
        blank=True
    )
    observacoes_inicial = models.TextField(null=True, blank=True)

    # Dados da devolução
    quilometragem_final = models.IntegerField(null=True, blank=True)
    nivel_combustivel_final = models.CharField(
        max_length=20,
        choices=COMBUSTIVEL_CHOICES,
        null=True,
        blank=True
    )
    observacoes_final = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.cliente.nome} - {self.veiculo.modelo}"

    def clean(self):
        if not self.veiculo_id:
            return  # ainda não foi vinculado, não valida

        if self.data_inicio and self.data_fim:
            if self.data_fim < self.data_inicio:
                raise ValidationError('A data de devolução não pode ser anterior à data de retirada.')

            conflitos = Reserva.objects.filter(
                veiculo=self.veiculo,
                data_inicio__lt=self.data_fim,
                data_fim__gt=self.data_inicio
            ).exclude(id=self.id).exclude(status='finalizada')

            if conflitos.exists():
                raise ValidationError('Este veículo já está reservado para o período informado.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Validação antes de salvar
        if self.data_inicio and self.data_fim and self.veiculo:
            dias = (self.data_fim - self.data_inicio).days
            if dias <= 0:
                dias = 1
            self.valor_total = dias * self.veiculo.preco_locacao
        super().save(*args, **kwargs)
