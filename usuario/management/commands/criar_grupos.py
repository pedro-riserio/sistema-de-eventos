from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Cria os grupos Palestrante e Participante'

    def handle(self, *args, **options):
        # Criar grupo Palestrante
        palestrante_group, created = Group.objects.get_or_create(name='Palestrante')
        if created:
            self.stdout.write(
                self.style.SUCCESS('Grupo "Palestrante" criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Grupo "Palestrante" já existe.')
            )

        # Criar grupo Participante
        participante_group, created = Group.objects.get_or_create(name='Participante')
        if created:
            self.stdout.write(
                self.style.SUCCESS('Grupo "Participante" criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Grupo "Participante" já existe.')
            )

        self.stdout.write(
            self.style.SUCCESS('Comando executado com sucesso!')
        )