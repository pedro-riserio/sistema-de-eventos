from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, UserProfileForm
from .models import Usuario
from .decorators import palestrante_required, participante_required
from ingresso.models import Ingresso
from eventos.models import Evento

def registro(request):
    """Registro de novos usuários"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Fazer login automático após registro
            login(request, user)
            
            # Redirecionar baseado no grupo do usuário
            if user.groups.filter(name='Palestrante').exists():
                messages.success(request, 'Conta de palestrante criada com sucesso! Bem-vindo ao seu dashboard.')
                return redirect('usuario:dashboard_palestrante')
            elif user.groups.filter(name='Participante').exists():
                messages.success(request, 'Conta de participante criada com sucesso! Bem-vindo ao seu dashboard.')
                return redirect('usuario:dashboard_participante')
            else:
                messages.success(request, 'Conta criada com sucesso!')
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'registration/registro.html', context)


@login_required
def criar_perfil(request):
    """Cria ou edita o perfil do usuário"""
    try:
        # Buscar ou criar o perfil Usuario
        usuario, created = Usuario.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST or None, instance=usuario)
    except:
        form = UserProfileForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(request, 'Perfil salvo com sucesso!')
        return redirect('home')
    
    context = {'form': form}
    return render(request, 'usuario/criar_perfil.html', context)


@login_required
def meus_ingressos(request):
    """Lista os ingressos do usuário"""
    ingressos = Ingresso.objects.filter(participante=request.user).order_by('-evento__data')
    
    context = {'ingressos': ingressos}
    return render(request, 'eventos/meus_ingressos.html', context)


@palestrante_required
def dashboard_palestrante(request):
    """Dashboard específico para palestrantes"""
    # Buscar eventos do palestrante
    eventos = Evento.objects.filter(criador=request.user).order_by('-data')
    
    # Contar ingressos vendidos dos eventos do palestrante
    total_ingressos = Ingresso.objects.filter(evento__criador=request.user).count()
    
    # Buscar perfil do usuário
    try:
        user_profile = Usuario.objects.get(pk=request.user.pk)
    except Usuario.DoesNotExist:
        user_profile = None
    
    context = {
        'eventos': eventos,
        'total_eventos': eventos.count(),
        'total_ingressos': total_ingressos,
        'user_profile': user_profile,
    }
    return render(request, 'usuario/dashboard_palestrante.html', context)


@participante_required
def dashboard_participante(request):
    """Dashboard específico para participantes"""
    # Buscar ingressos do participante
    ingressos = Ingresso.objects.filter(participante=request.user).order_by('-data_criacao')
    eventos_inscritos = [ingresso.evento for ingresso in ingressos]
    
    # Buscar perfil do usuário
    try:
        user_profile = Usuario.objects.get(pk=request.user.pk)
    except Usuario.DoesNotExist:
        user_profile = None
    
    context = {
        'ingressos': ingressos,
        'eventos_inscritos': eventos_inscritos,
        'total_ingressos': ingressos.count(),
        'user_profile': user_profile,
    }
    return render(request, 'usuario/dashboard_participante.html', context)


def custom_logout(request):
    """View customizada de logout para evitar problemas com middleware"""
    # Definir flag na sessão antes do logout
    request.session['logout_redirect'] = True
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso!')
    return redirect('home')
