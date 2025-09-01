from django.urls import path
from . import views

urlpatterns = [
    path('atividades/', views.lista_atividades, name='lista_atividades'),
    path('atividades/nova/', views.criar_atividade, name='criar_atividade'),
    path('atividades/<int:atividade_id>/editar/', views.editar_atividade, name='editar_atividade'),
    path('atividades/<int:atividade_id>/excluir/', views.excluir_atividade, name='excluir_atividade'),
]