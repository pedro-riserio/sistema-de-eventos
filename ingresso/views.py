from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Ingresso
from .models_crud import TipoIngresso
from .forms import IngressoForm


@login_required
@permission_required('ingresso.view_ingresso', raise_exception=True)
def lista_ingressos(request):
    """Lista todos os tipos de ingressos com filtros e paginação"""
    # Filtrar tipos de ingressos apenas dos eventos do palestrante logado
    ingressos = TipoIngresso.objects.filter(
        evento__palestrantes=request.user
    ).select_related('evento').order_by('-evento__data', 'tipo')
    
    # Filtro de busca
    busca = request.GET.get('busca')
    if busca:
        ingressos = ingressos.filter(
            Q(evento__nome__icontains=busca) |
            Q(tipo__icontains=busca)
        )
    
    # Filtro por evento
    evento_id = request.GET.get('evento')
    if evento_id:
        ingressos = ingressos.filter(evento_id=evento_id)
    
    # Paginação
    paginator = Paginator(ingressos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Eventos para filtro
    eventos_usuario = request.user.eventos_palestrante.all().order_by('nome')
    
    context = {
        'page_obj': page_obj,
        'busca_atual': busca,
        'evento_atual': evento_id,
        'eventos_usuario': eventos_usuario,
    }
    return render(request, 'ingresso/crud_ingressos.html', context)

@login_required
@permission_required('ingresso.add_ingresso', raise_exception=True)
def criar_ingresso(request):
    if request.method == 'POST':
        form = IngressoForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingresso criado com sucesso!')
            return redirect('lista_ingressos')
    else:
        form = IngressoForm(user=request.user)
    
    return render(request, 'ingresso/form_ingresso.html', {
        'form': form,
        'titulo': 'Criar Ingresso'
    })

@login_required
@permission_required('ingresso.change_ingresso', raise_exception=True)
def editar_ingresso(request, ingresso_id):
    ingresso = get_object_or_404(
        TipoIngresso, 
        id=ingresso_id, 
        evento__palestrantes=request.user
    )
    
    if request.method == 'POST':
        form = IngressoForm(request.POST, instance=ingresso, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ingresso atualizado com sucesso!')
            return redirect('lista_ingressos')
    else:
        form = IngressoForm(instance=ingresso, user=request.user)
    
    return render(request, 'ingresso/form_ingresso.html', {
        'form': form,
        'titulo': 'Editar Ingresso',
        'ingresso': ingresso
    })

@login_required
@permission_required('ingresso.delete_ingresso', raise_exception=True)
def excluir_ingresso(request, ingresso_id):
    ingresso = get_object_or_404(
        TipoIngresso, 
        id=ingresso_id, 
        evento__palestrantes=request.user
    )
    
    if request.method == 'POST':
        ingresso.delete()
        messages.success(request, 'Ingresso excluído com sucesso!')
        return redirect('lista_ingressos')
    
    return render(request, 'ingresso/confirmar_exclusao.html', {
        'ingresso': ingresso
    })
