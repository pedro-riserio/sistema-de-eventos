from django.db import models
from eventos.models import Evento
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Atividade(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='atividades')
    nome = models.CharField(max_length=200)
    responsavel = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='atividades_responsavel')
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
        
        # Verificar se o responsável é o criador do evento
        if self.responsavel and self.evento:
            if self.evento.criador != self.responsavel:
                raise ValidationError({
                    'responsavel': 'O responsável deve ser o criador do evento selecionado.'
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
