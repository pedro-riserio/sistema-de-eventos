from usuario.models import UserProfile

class UserProfileMiddleware:
    """
    Middleware que adiciona o perfil do usuário ao request
    para facilitar o acesso em templates e views
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Adiciona o perfil do usuário ao request se estiver autenticado
        if request.user.is_authenticated:
            try:
                request.user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                request.user_profile = None
        else:
            request.user_profile = None

        response = self.get_response(request)
        return response