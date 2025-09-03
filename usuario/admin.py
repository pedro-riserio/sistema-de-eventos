from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Usuario

User = get_user_model()


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'nome', 'telefone', 'cpf', 'group']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'nome', 'telefone', 'cpf']


# Função para criar grupos e permissões
def create_groups_and_permissions():
    # Criar grupos
    # Grupo de palestrante removido
    participante_group, created = Group.objects.get_or_create(name='Participante')
    
    # Obter content types
    from eventos.models import Evento
    evento_ct = ContentType.objects.get_for_model(Evento)
    
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
    # Permissões de palestrante removidas
    
    # Participantes têm permissões básicas (visualizar eventos, comprar ingressos)
    # Essas permissões já existem por padrão


# Executar a criação de grupos ao importar o módulo
# Comentado para evitar acesso ao banco durante inicialização
# try:
#     create_groups_and_permissions()
# except Exception as e:
#     # Ignorar erros durante migrações
#     pass
