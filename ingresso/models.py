from django.db import models
from decimal import Decimal
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingresso(models.Model):
    tipo = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    evento = models.ForeignKey('eventos.Evento', on_delete=models.CASCADE, related_name='ingressos')
    participante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ingressos')
    
    def __str__(self):
        return f'{self.tipo} - {self.evento.nome}'
    
    class Meta:
        verbose_name = 'Ingresso'
        verbose_name_plural = 'Ingressos'
        ordering = ['evento__data', 'tipo']
