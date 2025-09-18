from django.db import models

class Local(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=500)
    capacidade = models.IntegerField()
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locais'
        ordering = ['nome']
