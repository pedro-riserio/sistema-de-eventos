from usuario.models import Usuario

def user_profile(request):
    """
    Context processor que adiciona informações do perfil do usuário
    a todos os templates
    """
    context = {
        'user_profile': None,
        'is_organizador': False,
        'is_cliente': False,
    }
    
    if request.user.is_authenticated:
        try:
            profile = Usuario.objects.get(id=request.user.id)
            context.update({
                'user_profile': profile,
                'is_organizador': request.user.groups.filter(name='organizador').exists(),
                'is_cliente': request.user.groups.filter(name='participante').exists(),
            })
        except Usuario.DoesNotExist:
            profile = request.user
            context.update({
                'user_profile': profile,
                'is_organizador': request.user.groups.filter(name='organizador').exists(),
                'is_cliente': request.user.groups.filter(name='participante').exists(),
            })
    
    return context