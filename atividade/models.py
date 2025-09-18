from django.db import models
from eventos.models import Evento
from django.contrib.auth import get_user_model

User = get_user_model()

class Atividade(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='atividades')
    nome = models.CharField(max_length=200)
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='atividades_responsavel')
    tipo = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.nome} - {self.evento.nome}'
    
    class Meta:
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['evento__data', 'nome']
