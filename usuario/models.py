from django.db import models
from django.contrib.auth.models import User, Group


class Usuario(User):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15, blank=True)
    cpf = models.CharField(max_length=14, blank=True, unique=True)
    tipo_user = models.CharField(max_length=50, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    
    def __str__(self):
        return f'{self.nome}'
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
