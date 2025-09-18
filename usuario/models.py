from django.db import models
from django.contrib.auth.models import User


class Usuario(User):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14, unique=True)
    area = models.CharField(max_length=200, blank=True, null=True, help_text='Área de atuação do palestrante')
    
    def __str__(self):
        return f'{self.nome}'
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
