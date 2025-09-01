from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Páginas principais
    path('', views.home, name='home'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('evento/<int:evento_id>/', views.detalhe_evento, name='detalhe_evento'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    
    # Funcionalidades de eventos
    path('inscrever/<int:evento_id>/', views.inscrever_evento, name='inscrever_evento'),
    path('comprar-ingresso/<int:evento_id>/', views.comprar_ingresso, name='comprar_ingresso'),
    path('cancelar-ingresso/<int:ingresso_id>/', views.cancelar_ingresso, name='cancelar_ingresso'),
    path('criar-evento/', views.criar_evento, name='criar_evento'),
    path('meus-eventos/', views.meus_eventos, name='meus_eventos'),
    path('editar-evento/<int:evento_id>/', views.editar_evento, name='editar_evento'),
]