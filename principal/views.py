from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def painel_principal(request):  # ← Esse nome tem que bater com o da URL
    return render(request, 'principal/principal.html')
