from django.db import models
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=50)
    
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
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']
