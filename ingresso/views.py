from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Ingresso
from .models_crud import TipoIngresso
from .forms import IngressoForm
from eventos.models import Evento
from eventos.decorators import cliente_required


@login_required
@permission_required('ingresso.view_ingresso', raise_exception=True)
def lista_ingressos(request):
    """Lista todos os tipos de ingressos com filtros e paginação"""
    # Filtrar tipos de ingressos apenas dos eventos do usuário logado
    tipos_ingressos = TipoIngresso.objects.filter(
        evento__criador=request.user
    ).select_related('evento').order_by('-data_criacao')
    
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
    eventos_usuario = request.user.eventos_criados.all().order_by('nome')
    
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
        evento__criador=request.user
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
        evento__criador=request.user
    )
    
    if request.method == 'POST':
        ingresso.delete()
        messages.success(request, 'Ingresso excluído com sucesso!')
        return redirect('lista_ingressos')
    
    return render(request, 'ingresso/confirmar_exclusao.html', {
        'ingresso': ingresso
    })


@cliente_required
def comprar_ingresso(request, evento_id):
    """View para compra de ingressos - apenas clientes"""
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar se ainda há vagas disponíveis
    if evento.vagas_disponiveis <= 0:
        messages.error(request, 'Este evento não possui mais vagas disponíveis.')
        return redirect('detalhe_evento', evento_id=evento_id)
    
    # Verificar se o usuário já possui ingresso para este evento
    if Ingresso.objects.filter(participante=request.user, evento=evento).exists():
        messages.warning(request, 'Você já possui um ingresso para este evento.')
        return redirect('usuario:meus_ingressos')
    
    if request.method == 'POST':
        # Criar o ingresso
        ingresso = Ingresso.objects.create(
            participante=request.user,
            evento=evento,
            preco_pago=evento.preco
        )
        
        # Reduzir vagas disponíveis
        evento.vagas_disponiveis -= 1
        evento.save()
        
        messages.success(request, f'Ingresso para "{evento.nome}" comprado com sucesso!')
        return redirect('usuario:meus_ingressos')
    
    context = {
        'evento': evento,
    }
    return render(request, 'eventos/comprar_ingresso.html', context)


@cliente_required
def cancelar_ingresso(request, ingresso_id):
    """View para cancelamento de ingressos - apenas clientes"""
    ingresso = get_object_or_404(Ingresso, id=ingresso_id, participante=request.user)
    
    if request.method == 'POST':
        evento = ingresso.evento
        # Aumentar vagas disponíveis
        evento.vagas_disponiveis += 1
        evento.save()
        
        # Deletar o ingresso
        ingresso.delete()
        
        messages.success(request, f'Ingresso para "{evento.nome}" cancelado com sucesso!')
        return redirect('usuario:meus_ingressos')
    
    context = {
        'ingresso': ingresso,
    }
    return render(request, 'eventos/cancelar_ingresso.html', context)
