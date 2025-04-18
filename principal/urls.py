from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.painel_principal, name='home'),  # ← isso aqui é ESSENCIAL
    path('usuarios/', include('usuarios.urls')),

]
