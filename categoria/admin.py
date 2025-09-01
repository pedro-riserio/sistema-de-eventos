from django.contrib import admin
from .models import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo']
    search_fields = ['nome', 'tipo']
    list_filter = ['tipo']
