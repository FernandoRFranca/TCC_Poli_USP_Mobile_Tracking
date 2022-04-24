from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

home_itens = [
    {
        'title': 'Mobile Tracking',
        'subtitle': 'Rastreamento Veicular com Interface Mobile e Bloqueio Remoto',
        'button_title': 'ENTRAR NO DASHBOARD',
        'intro_text': 'Sistema de rastreamento para caminhões fazendo uso de Tablet e Smartphones, com acionamento de bloqueio via Dashboard ou condição anormal de uso.'
    }
]

example = [
    {
        'truck_ids': {'truck_1': 1, 'truck_2': 2, 'truck_3': 3},
        'json_received_from_backend': {'test': "test"}
    }
]

def home(request):
    context = {
        'home_itens': home_itens
    }
    return render(request, 'dashboard/home.html', context)

def dashboard_page(request):
    context = {
        'example': example
    }
    return render(request, 'dashboard/dashboard.html', context)


"""def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})"""