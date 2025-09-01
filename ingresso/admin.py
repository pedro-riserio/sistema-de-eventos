from django.contrib import admin
from .models import Ingresso
from .models_crud import TipoIngresso

@admin.register(Ingresso)
class IngressoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'evento', 'participante', 'tipo', 'valor', 'data_compra']
    search_fields = ['codigo', 'evento__nome', 'participante__username']
    list_filter = ['tipo', 'data_compra', 'evento']
    readonly_fields = ['codigo', 'data_compra']
    date_hierarchy = 'data_compra'

@admin.register(TipoIngresso)
class TipoIngressoAdmin(admin.ModelAdmin):
    list_display = ['evento', 'tipo', 'preco', 'quantidade_disponivel', 'quantidade_vendida', 'ativo']
    list_filter = ['tipo', 'ativo', 'evento__data']
    search_fields = ['evento__nome']
    readonly_fields = ['data_criacao', 'data_atualizacao', 'quantidade_vendida']
    
    def quantidade_vendida(self, obj):
        return obj.quantidade_vendida
    quantidade_vendida.short_description = 'Vendidos'
