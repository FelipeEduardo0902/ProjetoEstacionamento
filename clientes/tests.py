from django.test import TestCase, Client
from django.urls import reverse
from .models import Cliente

class ClienteViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_listagem_clientes_view(self):
        response = self.client.get(reverse('listar_clientes'))
        self.assertEqual(response.status_code, 200)

    def test_cadastro_cliente_view(self):
        response = self.client.post(reverse('cadastrar_cliente'), {
            'tipo_pessoa': 'CPF',
            'documento': '12345678901',
            'nome': 'Cliente Teste',
            'endereco': 'Rua Teste',
            'telefone': '99999-9999'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cliente cadastrado com sucesso!')
