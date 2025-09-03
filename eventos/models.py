from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Evento(models.Model):
    TIPO_CHOICES = [
        ('conferencia', 'Conferência'),
        ('workshop', 'Workshop'),
        ('festa', 'Festa'),
        ('exposicao', 'Exposição'),
    ]
    
    nome = models.CharField(max_length=200)
    data = models.DateField()
    descricao = models.TextField()
    local = models.ForeignKey('local.Local', on_delete=models.CASCADE, related_name='eventos')
    categoria = models.ForeignKey('categoria.Categoria', on_delete=models.CASCADE, related_name='eventos', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nome} - {self.data}"
    
    @property
    def vagas_ocupadas(self):
        return self.ingressos.count()
    
    @property
    def vagas_restantes(self):
        return max(0, self.vagas_disponiveis - self.vagas_ocupadas)
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['data']
