from django.urls import path
from . import views
from .views import login_view 

urlpatterns = [
    path('cadastrar/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('listar/', views.listar_funcionarios, name='listar_funcionarios'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', login_view, name='login'),
]
