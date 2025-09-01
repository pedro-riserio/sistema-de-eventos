from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Categoria
from .forms import CategoriaForm


@login_required
@permission_required('categoria.view_categoria', raise_exception=True)
def lista_categorias(request):
    """Lista todas as categorias com filtros e paginação"""
    categorias = Categoria.objects.all().order_by('nome')
    
    # Filtro de busca
    busca = request.GET.get('busca')
    if busca:
        categorias = categorias.filter(
            Q(nome__icontains=busca) | Q(tipo__icontains=busca)
        )
    
    # Paginação
    paginator = Paginator(categorias, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'busca_atual': busca,
    }
    return render(request, 'categoria/crud_categorias.html', context)

@login_required
@permission_required('categoria.add_categoria', raise_exception=True)
def criar_categoria(request):
    """Cria uma nova categoria"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoria "{categoria.nome}" criada com sucesso!')
            return redirect('lista_categorias')
        else:
            messages.error(request, 'Erro ao criar categoria. Verifique os dados informados.')
    else:
        form = CategoriaForm()
    
    context = {'form': form, 'titulo': 'Nova Categoria'}
    return render(request, 'categoria/form_categoria.html', context)

@login_required
@permission_required('categoria.change_categoria', raise_exception=True)
def editar_categoria(request, categoria_id):
    """Edita uma categoria existente"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoria "{categoria.nome}" atualizada com sucesso!')
            return redirect('lista_categorias')
        else:
            messages.error(request, 'Erro ao atualizar categoria. Verifique os dados informados.')
    else:
        form = CategoriaForm(instance=categoria)
    
    context = {
        'form': form, 
        'titulo': f'Editar Categoria: {categoria.nome}',
        'categoria': categoria
    }
    return render(request, 'categoria/form_categoria.html', context)

@login_required
@permission_required('categoria.delete_categoria', raise_exception=True)
def excluir_categoria(request, categoria_id):
    """Exclui uma categoria"""
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        nome_categoria = categoria.nome
        try:
            categoria.delete()
            messages.success(request, f'Categoria "{nome_categoria}" excluída com sucesso!')
        except Exception as e:
            messages.error(request, 'Erro ao excluir categoria. Verifique se não há eventos associados.')
        return redirect('lista_categorias')
    
    context = {'categoria': categoria}
    return render(request, 'categoria/confirmar_exclusao.html', context)
