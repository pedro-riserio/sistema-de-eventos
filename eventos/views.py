from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Evento
from local.models import Local
from ingresso.models import Ingresso
from .forms import InscricaoEventoForm, EventoForm
from .decorators import cliente_required, profile_required
from datetime import date


def home(request):
    """View principal da página inicial"""
    eventos_destaque = Evento.objects.filter(data__gte=date.today()).order_by('data')[:3]

    # recupera os grupos que o usuário faz parte
    grupos = request.user.groups.all()

    print("###############", grupos)

    if grupos.filter(name='GrupoZ').exists():
        return redirect('globo.com')
    # elif grupos.filter(name='GrupoB').exists():
    #     return redirect('record.com')

    context = {
        'eventos_destaque': eventos_destaque,
    }
    return render(request, 'home.html', context)


def lista_eventos(request):
    """Lista todos os eventos com filtros"""
    eventos = Evento.objects.filter(data__gte=date.today()).order_by('data')
    
    # Filtros
    tipo = request.GET.get('tipo')
    data_evento = request.GET.get('data')
    busca = request.GET.get('busca')
    
    if tipo and tipo != 'todos':
        eventos = eventos.filter(tipo=tipo)
    
    if data_evento:
        eventos = eventos.filter(data=data_evento)
    
    if busca:
        eventos = eventos.filter(
            Q(nome__icontains=busca) | 
            Q(descricao__icontains=busca) |
            Q(local__nome__icontains=busca)
        )
    
    # Paginação
    paginator = Paginator(eventos, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tipo_atual': tipo,
        'data_atual': data_evento,
        'busca_atual': busca,
        'tipos_evento': Evento.TIPO_CHOICES,
    }
    return render(request, 'eventos/lista_eventos.html', context)


def detalhe_evento(request, evento_id):
    """Exibe detalhes de um evento específico"""
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar se o usuário já está inscrito
    ja_inscrito = False
    if request.user.is_authenticated:
        ja_inscrito = Ingresso.objects.filter(evento=evento, participante=request.user).exists()
    
    context = {
        'evento': evento,
        'ja_inscrito': ja_inscrito,
    }
    return render(request, 'eventos/detalhe_evento.html', context)


@login_required
def inscrever_evento(request, evento_id):
    """Inscreve o usuário em um evento"""
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar se há vagas disponíveis
    if evento.vagas_restantes <= 0:
        messages.error(request, 'Este evento não possui mais vagas disponíveis.')
        return redirect('detalhe_evento', evento_id=evento.id)
    
    # Verificar se o usuário tem um perfil completo
    if not request.user.nome:
        messages.error(request, 'Você precisa completar seu perfil antes de se inscrever em eventos.')
        return redirect('usuario:criar_perfil')
    
    # Verificar se já está inscrito
    if Ingresso.objects.filter(evento=evento, participante=request.user).exists():
        messages.warning(request, 'Você já está inscrito neste evento.')
        return redirect('detalhe_evento', evento_id=evento.id)
    
    # Criar ingresso
    ingresso = Ingresso.objects.create(
        evento=evento,
        participante=request.user,
        tipo='gratuito' if evento.preco == 0 else 'pago',
        valor=evento.preco
    )
    
    messages.success(request, f'Inscrição realizada com sucesso! Seu código de ingresso é: {ingresso.codigo}')
    return redirect('detalhe_evento', evento_id=evento.id)


# View criar_perfil movida para usuario/views.py


@login_required
@permission_required('eventos.add_evento', raise_exception=True)
def criar_evento(request):
    """View para criação de eventos"""
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            # Definir o criador do evento
            evento.criador = request.user
            evento.save()
            
            messages.success(request, 'Evento criado com sucesso!')
            return redirect('eventos:meus_eventos')
    else:
        form = EventoForm()
    
    context = {'form': form}
    return render(request, 'eventos/criar_evento.html', context)


@login_required
@permission_required('eventos.view_evento', raise_exception=True)
def meus_eventos(request):
    """View para listar eventos do usuário logado"""
    # Buscar eventos criados pelo usuário
    eventos = Evento.objects.filter(criador=request.user).order_by('-data')
    
    context = {'eventos': eventos}
    return render(request, 'eventos/meus_eventos.html', context)


@login_required
@permission_required('eventos.change_evento', raise_exception=True)
def editar_evento(request, evento_id):
    """View para edição de eventos - apenas criadores do evento"""
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar se o usuário é o criador do evento
    if evento.criador != request.user:
        messages.error(request, 'Você não tem permissão para editar este evento.')
        return redirect('eventos:meus_eventos')
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento atualizado com sucesso!')
        return redirect('eventos:meus_eventos')
    else:
        form = EventoForm(instance=evento)
    
    context = {'form': form, 'evento': evento}
    return render(request, 'eventos/editar_evento.html', context)


@login_required
@permission_required('eventos.delete_evento', raise_exception=True)
def deletar_evento(request, evento_id):
    """View para exclusão de eventos - apenas criadores do evento"""
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar se o usuário é o criador do evento
    if evento.criador != request.user:
        messages.error(request, 'Você não tem permissão para excluir este evento.')
        return redirect('eventos:meus_eventos')
    
    if request.method == 'POST':
        nome_evento = evento.nome
        evento.delete()
        messages.success(request, f'Evento "{nome_evento}" excluído com sucesso!')
        return redirect('eventos:meus_eventos')
    
    # Se não for POST, redirecionar para a página de edição
    return redirect('eventos:editar_evento', evento_id=evento_id)


# Views comprar_ingresso e cancelar_ingresso movidas para ingresso/views.py


# View meus_ingressos movida para usuario/views.py





def sobre(request):
    """Página sobre"""
    return render(request, 'eventos/sobre.html')


def contato(request):
    """Página de contato"""
    if request.method == 'POST':
        # Aqui você pode implementar o envio de email
        messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
        return redirect('contato')
    
    return render(request, 'eventos/contato.html')


# Função de registro movida para usuario/views.py


# Função removida - funcionalidade de palestrante agora gerenciada pelo admin


# Função removida - funcionalidade de palestrante agora gerenciada pelo admin
