from django.db import models
from django.contrib.auth.models import User, Group


class Usuario(User):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15, blank=True)
    cpf = models.CharField(max_length=14, blank=True, unique=True)
    # group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    # Group já relaciona com User. Experimente request.user.groups e verá todos os grupos do usuário
    
    # Desabilitar o campo email do User padrão
    email = None
    
    def __str__(self):
        return f'{self.nome}'
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
