from django.urls import path
from . import views

app_name = 'eventos'

urlpatterns = [
    # Funcionalidades de eventos
    path('criar-evento/', views.criar_evento, name='criar_evento'),
    path('meus-eventos/', views.meus_eventos, name='meus_eventos'),
    path('editar-evento/<int:evento_id>/', views.editar_evento, name='editar_evento'),
]