from django.contrib import admin
from .models import Ingresso

@admin.register(Ingresso)
class IngressoAdmin(admin.ModelAdmin):
    list_display = ['evento', 'tipo', 'valor', 'participante']
    search_fields = ['evento__nome', 'participante__username']
    list_filter = ['tipo', 'evento']
    
    def get_queryset(self, request):
        """Filtrar ingressos para mostrar apenas os dos eventos do usuário logado"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Se o usuário é palestrante, mostrar apenas ingressos dos seus eventos
        if request.user.groups.filter(name='Palestrante').exists():
            return qs.filter(evento__criador=request.user)
        return qs.none()  # Outros usuários não veem nenhum ingresso
    
    def has_add_permission(self, request):
        """Permitir adicionar ingressos apenas para palestrantes"""
        return request.user.groups.filter(name='Palestrante').exists() or request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """Permitir editar apenas ingressos dos próprios eventos"""
        if request.user.is_superuser:
            return True
        if obj and request.user.groups.filter(name='Palestrante').exists():
            return obj.evento.criador == request.user
        return request.user.groups.filter(name='Palestrante').exists()
    
    def has_delete_permission(self, request, obj=None):
        """Permitir deletar apenas ingressos dos próprios eventos"""
        if request.user.is_superuser:
            return True
        if obj and request.user.groups.filter(name='Palestrante').exists():
            return obj.evento.criador == request.user
        return request.user.groups.filter(name='Palestrante').exists()
