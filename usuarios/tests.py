from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Funcionario

class UsuarioViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='teste@email.com', password='123')
        self.funcionario = Funcionario.objects.create(
            nome='Funcionario Teste', cpf='123', cargo='Cargo',
            email='teste@email.com', user=self.user
        )
        self.client.login(username='teste@email.com', password='123')

    def test_listagem_funcionarios_view(self):
        response = self.client.get(reverse('listar_funcionarios'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/listar_funcionarios.html')
