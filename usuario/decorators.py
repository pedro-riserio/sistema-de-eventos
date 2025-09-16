from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def grupo_required(grupo_name):
    """
    Decorator que verifica se o usuário pertence a um grupo específico.
    Uso: @grupo_required('palestrante')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=grupo_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f'Acesso negado. Você não tem permissão de {grupo_name}.')
                return redirect('home')
        return _wrapped_view
    return decorator


def palestrante_required(view_func):
    """
    Decorator específico para palestrantes.
    Uso: @palestrante_required
    """
    return grupo_required('palestrante')(view_func)


def participante_required(view_func):
    """
    Decorator específico para participantes.
    Uso: @participante_required
    """
    return grupo_required('participante')(view_func)


def multiplos_grupos_required(*grupos):
    """
    Decorator que permite acesso a usuários de múltiplos grupos.
    Uso: @multiplos_grupos_required('palestrante', 'participante')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            user_groups = request.user.groups.values_list('name', flat=True)
            if any(grupo in user_groups for grupo in grupos):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Acesso negado. Você não tem as permissões necessárias.')
                return redirect('home')
        return _wrapped_view
    return decorator


def admin_or_grupo_required(grupo_name):
    """
    Decorator que permite acesso a admins ou usuários de um grupo específico.
    Uso: @admin_or_grupo_required('palestrante')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if (request.user.is_staff or 
                request.user.is_superuser or 
                request.user.groups.filter(name=grupo_name).exists()):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f'Acesso negado. Você não tem permissão de {grupo_name} ou admin.')
                return redirect('home')
        return _wrapped_view
    return decorator