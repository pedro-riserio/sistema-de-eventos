from django.contrib import admin
from .models import Atividade

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'evento', 'responsavel', 'tipo']
    search_fields = ['nome', 'evento__nome', 'responsavel__username']
    list_filter = ['tipo', 'evento']
