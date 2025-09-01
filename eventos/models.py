from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Palestrante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='palestrante', null=True, blank=True)
    nome = models.CharField(max_length=200)
    biografia = models.TextField()
    tema = models.CharField(max_length=200)
    horario = models.TimeField()
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Palestrante'
        verbose_name_plural = 'Palestrantes'


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
    palestrantes = models.ManyToManyField(Palestrante, related_name='eventos', blank=True)
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_criados', null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='conferencia')
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vagas_disponiveis = models.PositiveIntegerField(default=0)
    imagem = models.URLField(blank=True, null=True)
    
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
