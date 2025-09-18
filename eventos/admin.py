from django.contrib import admin
from .models import Evento


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data', 'local', 'criador']
    search_fields = ['nome', 'descricao']
    list_filter = ['data', 'local', 'criador']
    date_hierarchy = 'data'
    
    def get_queryset(self, request):
        """Filtrar eventos para mostrar apenas os do usuário logado"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Se o usuário é palestrante, mostrar apenas seus eventos
        if request.user.groups.filter(name='Palestrante').exists():
            return qs.filter(criador=request.user)
        return qs.none()  # Outros usuários não veem nenhum evento
    
    def save_model(self, request, obj, form, change):
        """Definir o criador do evento automaticamente"""
        if not change:  # Se é um novo evento
            obj.criador = request.user
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        """Permitir adicionar eventos apenas para palestrantes"""
        return request.user.groups.filter(name='Palestrante').exists() or request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Permitir editar apenas próprios eventos"""
        if request.user.is_superuser:
            return True
        if obj and request.user.groups.filter(name='Palestrante').exists():
            return obj.criador == request.user
        return request.user.groups.filter(name='Palestrante').exists()
    
    def has_delete_permission(self, request, obj=None):
        """Permitir deletar apenas próprios eventos"""
        if request.user.is_superuser:
            return True
        if obj and request.user.groups.filter(name='Palestrante').exists():
            return obj.criador == request.user
        return request.user.groups.filter(name='Palestrante').exists()
