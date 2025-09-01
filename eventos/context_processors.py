from usuario.models import UserProfile

def user_profile(request):
    """
    Context processor que adiciona informações do perfil do usuário
    a todos os templates
    """
    context = {
        'user_profile': None,
        'is_palestrante': False,
        'is_cliente': False,
    }
    
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            context.update({
                'user_profile': profile,
                'is_palestrante': profile.tipo_usuario == 'palestrante',
                'is_cliente': profile.tipo_usuario == 'cliente',
            })
        except UserProfile.DoesNotExist:
            pass
    
    return context