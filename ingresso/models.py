from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class Ingresso(models.Model):
    TIPO_CHOICES = [
        ('gratuito', 'Gratuito'),
        ('pago', 'Pago'),
        ('promocional', 'Promocional'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='pago')
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    evento = models.ForeignKey('eventos.Evento', on_delete=models.CASCADE, related_name='ingressos')
    participante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ingressos')
    data_compra = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Ingresso {self.codigo} - {self.evento.nome}'
    
    class Meta:
        verbose_name = 'Ingresso'
        verbose_name_plural = 'Ingressos'
        unique_together = ['evento', 'participante']
