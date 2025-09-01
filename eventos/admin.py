from django.contrib import admin
from .models import Palestrante, Evento


@admin.register(Palestrante)
class PalestranteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tema', 'horario']
    search_fields = ['nome', 'tema']
    list_filter = ['tema']


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data', 'local', 'categoria', 'tipo', 'preco', 'vagas_disponiveis', 'vagas_restantes']
    search_fields = ['nome', 'descricao']
    list_filter = ['tipo', 'data', 'local', 'categoria']
    filter_horizontal = ['palestrantes']
    date_hierarchy = 'data'
    
    def vagas_restantes(self, obj):
        return obj.vagas_restantes
    vagas_restantes.short_description = 'Vagas Restantes'
