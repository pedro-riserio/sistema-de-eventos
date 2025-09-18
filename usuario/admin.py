from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Usuario

User = get_user_model()


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'nome', 'telefone', 'cpf', 'area', 'get_email']
    search_fields = ['user__username', 'nome', 'telefone', 'cpf', 'area', 'user__email']
    fields = ['user', 'nome', 'telefone', 'cpf', 'area']
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


# Função para criar grupos e permissões
def create_groups_and_permissions():
    # Criar grupos
    palestrante_group, created = Group.objects.get_or_create(name='Palestrante')
    participante_group, created = Group.objects.get_or_create(name='Participante')
    
    # Obter content types
    from eventos.models import Evento
    from ingresso.models import Ingresso
    evento_ct = ContentType.objects.get_for_model(Evento)
    ingresso_ct = ContentType.objects.get_for_model(Ingresso)
    
    # Criar permissões customizadas se não existirem
    criar_evento_perm, created = Permission.objects.get_or_create(
        codename='pode_criar_evento',
        name='Pode criar evento',
        content_type=evento_ct,
    )
    
    gerenciar_evento_perm, created = Permission.objects.get_or_create(
        codename='pode_gerenciar_evento',
        name='Pode gerenciar evento',
        content_type=evento_ct,
    )
    
    # Atribuir permissões aos grupos
    # Permissões para palestrantes
    palestrante_permissions = [
        'add_evento', 'change_evento', 'delete_evento', 'view_evento',
        'add_ingresso', 'change_ingresso', 'delete_ingresso', 'view_ingresso'
    ]
    
    for perm_code in palestrante_permissions:
        if 'evento' in perm_code:
            perm = Permission.objects.get(codename=perm_code, content_type=evento_ct)
        else:
            perm = Permission.objects.get(codename=perm_code, content_type=ingresso_ct)
        palestrante_group.permissions.add(perm)
    
    # Adicionar permissões customizadas aos palestrantes
    palestrante_group.permissions.add(criar_evento_perm, gerenciar_evento_perm)
    
    # Participantes têm permissões básicas (visualizar eventos, comprar ingressos)
    # Essas permissões já existem por padrão


# Executar a criação de grupos ao importar o módulo
try:
    create_groups_and_permissions()
except Exception as e:
    # Ignorar erros durante migrações
    pass
