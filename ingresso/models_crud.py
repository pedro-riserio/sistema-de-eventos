from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal
from eventos.models import Evento

class TipoIngresso(models.Model):
    """Modelo para tipos de ingressos que podem ser criados pelos palestrantes"""
    TIPO_CHOICES = [
        ('V', 'VIP'),
        ('N', 'Normal'),
        ('E', 'Estudante'),
        ('G', 'Gratuito'),
    ]
    
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='tipos_ingressos')
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default='N')
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Preço do ingresso em reais'
    )
    quantidade_disponivel = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Quantidade de ingressos disponíveis para venda'
    )
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def clean(self):
        super().clean()
        
        # Validar preço baseado no tipo
        if self.tipo == 'G' and self.preco > 0:
            raise ValidationError({
                'preco': 'Ingressos gratuitos devem ter preço zero.'
            })
        
        if self.tipo != 'G' and self.preco <= 0:
            raise ValidationError({
                'preco': 'Ingressos pagos devem ter preço maior que zero.'
            })
        
        # Validar quantidade disponível
        if self.quantidade_disponivel <= 0:
            raise ValidationError({
                'quantidade_disponivel': 'A quantidade deve ser maior que zero.'
            })
        
        # Verificar se já existe um tipo igual para o mesmo evento
        if self.evento:
            existing = TipoIngresso.objects.filter(
                evento=self.evento, 
                tipo=self.tipo
            ).exclude(pk=self.pk)
            
            if existing.exists():
                raise ValidationError({
                    'tipo': f'Já existe um ingresso do tipo {self.get_tipo_display()} para este evento.'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def quantidade_vendida(self):
        """Retorna a quantidade de ingressos vendidos deste tipo"""
        from .models import Ingresso
        return Ingresso.objects.filter(
            evento=self.evento,
            tipo=self.tipo
        ).count()
    
    @property
    def quantidade_restante(self):
        """Retorna a quantidade restante de ingressos"""
        return max(0, self.quantidade_disponivel - self.quantidade_vendida)
    
    @property
    def esta_esgotado(self):
        """Verifica se o ingresso está esgotado"""
        return self.quantidade_restante <= 0
    
    def __str__(self):
        return f'{self.evento.nome} - {self.get_tipo_display()} - R$ {self.preco}'
    
    class Meta:
        verbose_name = 'Tipo de Ingresso'
        verbose_name_plural = 'Tipos de Ingressos'
        unique_together = ['evento', 'tipo']
        ordering = ['evento__data', 'tipo']