from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Funcionario, Administrador

admin.site.register(Funcionario)
admin.site.register(Administrador)
