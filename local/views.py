from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Local
from .forms import LocalForm


@login_required
@permission_required('local.view_local', raise_exception=True)
def lista_locais(request):
    """Lista todos os locais com filtros e paginação"""
    locais = Local.objects.all().order_by('nome')
    
    # Filtro de busca
    busca = request.GET.get('busca')
    if busca:
        locais = locais.filter(
            Q(nome__icontains=busca) | 
            Q(endereco__icontains=busca)
        )
    
    # Paginação
    paginator = Paginator(locais, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'busca_atual': busca,
    }
    return render(request, 'local/crud_locais.html', context)

@login_required
@permission_required('local.add_local', raise_exception=True)
def criar_local(request):
    if request.method == 'POST':
        form = LocalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Local criado com sucesso!')
            return redirect('lista_locais')
    else:
        form = LocalForm()
    
    return render(request, 'local/form_local.html', {
        'form': form,
        'titulo': 'Criar Local'
    })

@login_required
@permission_required('local.change_local', raise_exception=True)
def editar_local(request, local_id):
    local = get_object_or_404(Local, id=local_id)
    
    if request.method == 'POST':
        form = LocalForm(request.POST, instance=local)
        if form.is_valid():
            form.save()
            messages.success(request, 'Local atualizado com sucesso!')
            return redirect('lista_locais')
    else:
        form = LocalForm(instance=local)
    
    return render(request, 'local/form_local.html', {
        'form': form,
        'titulo': 'Editar Local',
        'local': local
    })

@login_required
@permission_required('local.delete_local', raise_exception=True)
def excluir_local(request, local_id):
    local = get_object_or_404(Local, id=local_id)
    
    if request.method == 'POST':
        local.delete()
        messages.success(request, 'Local excluído com sucesso!')
        return redirect('lista_locais')
    
    return render(request, 'local/confirmar_exclusao.html', {
        'local': local
    })
