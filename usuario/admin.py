from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'tipo_usuario', 'telefone', 'cpf']
    list_filter = ['tipo_usuario']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    

# Reregistrar o User admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Função para criar grupos e permissões
def create_groups_and_permissions():
    # Criar grupos
    palestrante_group, created = Group.objects.get_or_create(name='Palestrante')
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
    palestrante_group.permissions.add(criar_evento_perm, gerenciar_evento_perm)
    
    # Participantes têm permissões básicas (visualizar eventos, comprar ingressos)
    # Essas permissões já existem por padrão


# Executar a criação de grupos ao importar o módulo
try:
    create_groups_and_permissions()
except Exception as e:
    # Ignorar erros durante migrações
    pass
