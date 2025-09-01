from django.apps import AppConfig


class UsuarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuario'
    verbose_name = 'Usuários'
    
    def ready(self):
        import usuario.admin  # Importar admin para executar a criação de grupos
