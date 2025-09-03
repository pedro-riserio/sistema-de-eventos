from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

# Decorator palestrante_required removido - funcionalidade agora gerenciada por permission_required

def cliente_required(view_func):
    """
    Decorator que permite acesso apenas para usuários do grupo 'participante'
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='participante').exists():
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Acesso negado. Esta funcionalidade é apenas para participantes.')
            return redirect('home')
    return _wrapped_view


def grupo_required(*grupos_permitidos):
    """
    Decorator que permite acesso apenas para usuários de grupos específicos
    Uso: @grupo_required('palestrante', 'participante')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name__in=grupos_permitidos).exists():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f'Acesso negado. Esta funcionalidade é apenas para: {", ".join(grupos_permitidos)}.')
                return redirect('home')
        return _wrapped_view
    return decorator

def profile_required(view_func):
    """
    Decorator que garante que o usuário tenha um perfil completo
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # Como agora Usuario é o modelo de usuário customizado, verificamos se tem nome
        if request.user.nome:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'Complete seu perfil para continuar.')
            return redirect('usuario:criar_perfil')
    return _wrapped_view