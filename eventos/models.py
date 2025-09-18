from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Evento(models.Model):
    TIPO_CHOICES = [
        ('presencial', 'Presencial'),
        ('online', 'Online'),
        ('hibrido', 'Híbrido'),
    ]
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('cancelado', 'Cancelado'),
        ('finalizado', 'Finalizado'),
    ]
    
    nome = models.CharField(max_length=200)
    data = models.DateField()
    horario = models.TimeField(default='09:00')
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='presencial')
    local = models.ForeignKey('local.Local', on_delete=models.CASCADE, related_name='eventos')
    categoria = models.ForeignKey('categoria.Categoria', on_delete=models.CASCADE, related_name='eventos')
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos_criados')
    capacidade = models.PositiveIntegerField(default=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    imagem = models.ImageField(upload_to='eventos/', blank=True, null=True)
    
    @property
    def vagas_restantes(self):
        from ingresso.models import Ingresso
        ingressos_vendidos = Ingresso.objects.filter(evento=self).count()
        return self.capacidade - ingressos_vendidos
    
    def __str__(self):
        return f"{self.nome} - {self.data}"
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['data']
