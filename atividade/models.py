from django.db import models
from eventos.models import Evento
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Atividade(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='atividades')
    nome = models.CharField(max_length=200)
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    
    def clean(self):
        super().clean()
        if self.nome:
            self.nome = self.nome.strip().title()
            if len(self.nome) < 3:
                raise ValidationError({'nome': 'O nome deve ter pelo menos 3 caracteres.'})
        
        if self.tipo:
            self.tipo = self.tipo.strip().title()
            if len(self.tipo) < 2:
                raise ValidationError({'tipo': 'O tipo deve ter pelo menos 2 caracteres.'})
        
        # Verificar se o responsável é palestrante do evento
        if self.responsavel and self.evento:
            if not self.evento.palestrantes.filter(user=self.responsavel).exists():
                raise ValidationError({
                    'responsavel': 'O responsável deve ser um palestrante do evento selecionado.'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.nome} - {self.evento.nome}'
    
    class Meta:
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        unique_together = ['evento', 'nome']
        ordering = ['evento__data', 'nome']
