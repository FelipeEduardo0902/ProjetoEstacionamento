from django.test import TestCase, Client
from django.urls import reverse
from clientes.models import Cliente
from veiculos.models import Veiculo
from usuarios.models import Funcionario, User
from .models import Reserva
from datetime import date, timedelta

class ReservaViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='teste@email.com', password='123')
        self.funcionario = Funcionario.objects.create(
            nome='Funcionario Teste', cpf='123', cargo='Atendente',
            email='teste@email.com', user=self.user
        )

        self.client.login(username='teste@email.com', password='123')

        self.cliente = Cliente.objects.create(
            tipo_pessoa='CPF', documento='12345678901', nome='Cliente Teste',
            endereco='Rua Teste', telefone='99999-9999'
        )

        self.veiculo = Veiculo.objects.create(
            modelo='Gol', marca='VW', ano=2020, cor='Prata',
            categoria='hatch', placa='ABC1234', preco_locacao=100.00
        )

    def test_listagem_reservas_view(self):
        response = self.client.get(reverse('listar_reservas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservas/listar.html')

    def test_criacao_reserva_view(self):
        response = self.client.post(reverse('reservar_veiculo', args=[self.veiculo.id]), {
            'cliente': self.cliente.id,
            'data_inicio': date.today(),
            'data_fim': date.today() + timedelta(days=2)
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após sucesso
        self.assertEqual(Reserva.objects.count(), 1)
