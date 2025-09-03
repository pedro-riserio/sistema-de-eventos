from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, UserProfileForm
from .models import Usuario
from ingresso.models import Ingresso

User = get_user_model()


def registro(request):
    """Registro de novos usuários"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('usuario:login')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def criar_perfil(request):
    """Cria ou edita o perfil do usuário"""
    try:
        # Como Usuario é o modelo de usuário customizado, usamos request.user diretamente
        form = UserProfileForm(request.POST or None, instance=request.user)
    except:
        form = UserProfileForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.save()
        messages.success(request, 'Perfil salvo com sucesso!')
        return redirect('home')
    
    context = {'form': form}
    return render(request, 'usuario/criar_perfil.html', context)


@login_required
def meus_ingressos(request):
    """Lista os ingressos do usuário"""
    ingressos = Ingresso.objects.filter(participante=request.user).order_by('-data_compra')
    
    context = {'ingressos': ingressos}
    return render(request, 'eventos/meus_ingressos.html', context)
