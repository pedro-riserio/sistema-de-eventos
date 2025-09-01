from django.urls import path
from . import views

urlpatterns = [
    path('locais/', views.lista_locais, name='lista_locais'),
    path('locais/novo/', views.criar_local, name='criar_local'),
    path('locais/<int:local_id>/editar/', views.editar_local, name='editar_local'),
    path('locais/<int:local_id>/excluir/', views.excluir_local, name='excluir_local'),
]