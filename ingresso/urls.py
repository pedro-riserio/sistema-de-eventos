from django.urls import path
from . import views

urlpatterns = [
    path('ingressos/', views.lista_ingressos, name='lista_ingressos'),
    path('ingressos/novo/', views.criar_ingresso, name='criar_ingresso'),
    path('ingressos/<int:ingresso_id>/editar/', views.editar_ingresso, name='editar_ingresso'),
    path('ingressos/<int:ingresso_id>/excluir/', views.excluir_ingresso, name='excluir_ingresso'),
]