from django.contrib import admin
from .models import Evento


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data', 'local']
    search_fields = ['nome', 'descricao']
    list_filter = ['data', 'local']
    date_hierarchy = 'data'
