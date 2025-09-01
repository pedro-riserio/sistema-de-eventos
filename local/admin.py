from django.contrib import admin
from .models import Local

@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'endereco', 'capacidade']
    search_fields = ['nome', 'endereco']
    list_filter = ['capacidade']
