from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from eventos.models import Evento


class Command(BaseCommand):
    help = 'Cria grupos e permissões necessários para o sistema'

    def handle(self, *args, **options):
        self.stdout.write('Criando grupos e permissões...')
        
        # Criar grupos
        participante_group, created = Group.objects.get_or_create(name='Participante')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "Participante" criado com sucesso'))
        else:
            self.stdout.write('Grupo "Participante" já existe')
        
        # Obter content types
        evento_ct = ContentType.objects.get_for_model(Evento)
        
        # Criar permissões customizadas se não existirem
        criar_evento_perm, created = Permission.objects.get_or_create(
            codename='pode_criar_evento',
            name='Pode criar evento',
            content_type=evento_ct,
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Permissão "pode_criar_evento" criada'))
        
        gerenciar_evento_perm, created = Permission.objects.get_or_create(
            codename='pode_gerenciar_evento',
            name='Pode gerenciar evento',
            content_type=evento_ct,
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Permissão "pode_gerenciar_evento" criada'))
        
        self.stdout.write(self.style.SUCCESS('Configuração de grupos e permissões concluída!'))