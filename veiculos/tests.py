from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class VeiculoViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='teste@email.com', password='123')
        self.client.login(username='teste@email.com', password='123')

    def test_listagem_veiculos_view(self):
        response = self.client.get(reverse('listar_veiculos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'veiculos/listar.html')
