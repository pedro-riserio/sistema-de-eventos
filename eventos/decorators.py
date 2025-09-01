from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usuario.models import UserProfile

def palestrante_required(view_func):
    """
    Decorator que permite acesso apenas para usuários do tipo 'palestrante'
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.tipo_usuario == 'palestrante':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Acesso negado. Esta funcionalidade é apenas para palestrantes.')
                return redirect('home')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Perfil não encontrado. Complete seu cadastro primeiro.')
            return redirect('criar_perfil')
    return _wrapped_view

def cliente_required(view_func):
    """
    Decorator que permite acesso apenas para usuários do tipo 'cliente'
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.tipo_usuario == 'cliente':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Acesso negado. Esta funcionalidade é apenas para clientes.')
                return redirect('home')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Perfil não encontrado. Complete seu cadastro primeiro.')
            return redirect('criar_perfil')
    return _wrapped_view

def tipo_usuario_required(*tipos_permitidos):
    """
    Decorator flexível que permite especificar quais tipos de usuário podem acessar
    Uso: @tipo_usuario_required('palestrante', 'cliente')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                profile = UserProfile.objects.get(user=request.user)
                if profile.tipo_usuario in tipos_permitidos:
                    return view_func(request, *args, **kwargs)
                else:
                    tipos_str = ', '.join(tipos_permitidos)
                    messages.error(request, f'Acesso negado. Esta funcionalidade é apenas para: {tipos_str}.')
                    return redirect('home')
            except UserProfile.DoesNotExist:
                messages.error(request, 'Perfil não encontrado. Complete seu cadastro primeiro.')
                return redirect('criar_perfil')
        return _wrapped_view
    return decorator

def profile_required(view_func):
    """
    Decorator que garante que o usuário tenha um perfil completo
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            return view_func(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            messages.warning(request, 'Complete seu perfil para continuar.')
            return redirect('criar_perfil')
    return _wrapped_view