from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Atividade
from .forms import AtividadeForm


@login_required
@permission_required('eventos.add_evento', raise_exception=True)
def lista_atividades(request):
    """Lista todas as atividades com filtros e paginação"""
    # Filtrar atividades apenas dos eventos do usuário logado
    atividades = Atividade.objects.filter(
        evento__criador=request.user
    ).select_related('evento', 'responsavel').order_by('-evento__data', 'nome')
    
    # Filtro de busca
    busca = request.GET.get('busca')
    if busca:
        atividades = atividades.filter(
            Q(nome__icontains=busca) | 
            Q(tipo__icontains=busca) |
            Q(evento__nome__icontains=busca) |
            Q(responsavel__first_name__icontains=busca) |
            Q(responsavel__last_name__icontains=busca)
        )
    
    # Filtro por evento
    evento_id = request.GET.get('evento')
    if evento_id:
        atividades = atividades.filter(evento_id=evento_id)
    
    # Paginação
    paginator = Paginator(atividades, 10)
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
    return render(request, 'atividade/crud_atividades.html', context)

@login_required
@permission_required('atividade.add_atividade', raise_exception=True)
def criar_atividade(request):
    """Cria uma nova atividade"""
    if request.method == 'POST':
        form = AtividadeForm(request.POST, user=request.user)
        if form.is_valid():
            atividade = form.save()
            messages.success(request, f'Atividade "{atividade.nome}" criada com sucesso!')
            return redirect('lista_atividades')
        else:
            messages.error(request, 'Erro ao criar atividade. Verifique os dados informados.')
    else:
        form = AtividadeForm(user=request.user)
    
    context = {'form': form, 'titulo': 'Nova Atividade'}
    return render(request, 'atividade/form_atividade.html', context)

@login_required
@permission_required('atividade.change_atividade', raise_exception=True)
def editar_atividade(request, atividade_id):
    """Edita uma atividade existente"""
    atividade = get_object_or_404(
        Atividade, 
        id=atividade_id, 
        evento__criador=request.user
    )
    
    if request.method == 'POST':
        form = AtividadeForm(request.POST, instance=atividade, user=request.user)
        if form.is_valid():
            atividade = form.save()
            messages.success(request, f'Atividade "{atividade.nome}" atualizada com sucesso!')
            return redirect('lista_atividades')
        else:
            messages.error(request, 'Erro ao atualizar atividade. Verifique os dados informados.')
    else:
        form = AtividadeForm(instance=atividade, user=request.user)
    
    context = {
        'form': form, 
        'titulo': f'Editar Atividade: {atividade.nome}',
        'atividade': atividade
    }
    return render(request, 'atividade/form_atividade.html', context)

@login_required
@permission_required('atividade.delete_atividade', raise_exception=True)
def excluir_atividade(request, atividade_id):
    """Exclui uma atividade"""
    atividade = get_object_or_404(
        Atividade, 
        id=atividade_id, 
        evento__criador=request.user
    )
    
    if request.method == 'POST':
        nome_atividade = atividade.nome
        try:
            atividade.delete()
            messages.success(request, f'Atividade "{nome_atividade}" excluída com sucesso!')
        except Exception as e:
            messages.error(request, 'Erro ao excluir atividade.')
        return redirect('lista_atividades')
    
    context = {'atividade': atividade}
    return render(request, 'atividade/confirmar_exclusao.html', context)
