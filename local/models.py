from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class Local(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    endereco = models.TextField()
    capacidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    def clean(self):
        super().clean()
        if self.nome:
            self.nome = self.nome.strip().title()
            if len(self.nome) < 3:
                raise ValidationError({'nome': 'O nome deve ter pelo menos 3 caracteres.'})
        
        if self.endereco:
            self.endereco = self.endereco.strip()
            if len(self.endereco) < 10:
                raise ValidationError({'endereco': 'O endereço deve ter pelo menos 10 caracteres.'})
        
        if self.capacidade and self.capacidade < 1:
            raise ValidationError({'capacidade': 'A capacidade deve ser maior que zero.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locais'
        ordering = ['nome']
