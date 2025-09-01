from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Evento, Palestrante
from local.models import Local
from ingresso.models import Ingresso
from usuario.models import UserProfile
from usuario.forms import UserProfileForm, CustomUserCreationForm
from .forms import InscricaoEventoForm, EventoForm
from .decorators import palestrante_required, cliente_required, profile_required
from datetime import date


def home(request):
    """View principal da página inicial"""
    eventos_destaque = Evento.objects.filter(data__gte=date.today()).order_by('data')[:3]
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
        try:
            participante = Participante.objects.get(user=request.user)
            ja_inscrito = Ingresso.objects.filter(evento=evento, participante=participante).exists()
        except Participante.DoesNotExist:
            pass
    
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
    
    # Verificar se o usuário tem um perfil de participante
    try:
        participante = Participante.objects.get(user=request.user)
    except Participante.DoesNotExist:
        messages.error(request, 'Você precisa completar seu perfil antes de se inscrever em eventos.')
        return redirect('criar_perfil')
    
    # Verificar se já está inscrito
    if Ingresso.objects.filter(evento=evento, participante=participante).exists():
        messages.warning(request, 'Você já está inscrito neste evento.')
        return redirect('detalhe_evento', evento_id=evento.id)
    
    # Criar ingresso
    ingresso = Ingresso.objects.create(
        evento=evento,
        participante=participante,
        tipo='gratuito' if evento.preco == 0 else 'pago',
        valor=evento.preco
    )
    
    messages.success(request, f'Inscrição realizada com sucesso! Seu código de ingresso é: {ingresso.codigo}')
    return redirect('detalhe_evento', evento_id=evento.id)


@login_required
def criar_perfil(request):
    """Cria ou edita o perfil do usuário"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(request.POST or None, instance=profile)
    except UserProfile.DoesNotExist:
        form = UserProfileForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        messages.success(request, 'Perfil salvo com sucesso!')
        return redirect('home')
    
    context = {'form': form}
    return render(request, 'eventos/criar_perfil.html', context)


@login_required
@permission_required('eventos.add_evento', raise_exception=True)
def criar_evento(request):
    """View para criação de eventos - apenas palestrantes"""
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            # Definir o criador do evento
            evento.criador = request.user
            evento.save()
            
            # Criar ou obter palestrante vinculado ao usuário
            palestrante, created = Palestrante.objects.get_or_create(
                user=request.user,
                defaults={
                    'nome': request.user.get_full_name() or request.user.username,
                    'biografia': getattr(request.user.profile, 'biografia', '') or 'Palestrante',
                    'tema': 'Geral',
                    'horario': '09:00'
                }
            )
            
            # Adicionar o palestrante ao evento
            evento.palestrantes.add(palestrante)
            
            messages.success(request, 'Evento criado com sucesso!')
            return redirect('meus_eventos')
    else:
        form = EventoForm()
    
    context = {'form': form}
    return render(request, 'eventos/criar_evento.html', context)


@login_required
@permission_required('eventos.view_evento', raise_exception=True)
def meus_eventos(request):
    """View para listar eventos do palestrante logado"""
    # Buscar eventos criados pelo usuário ou onde ele é palestrante
    eventos_criados = Evento.objects.filter(criador=request.user)
    
    # Buscar eventos onde o usuário é palestrante
    try:
        palestrante = Palestrante.objects.get(user=request.user)
        eventos_palestrante = Evento.objects.filter(palestrantes=palestrante)
        # Combinar os dois querysets
        eventos = (eventos_criados | eventos_palestrante).distinct().order_by('-data')
    except Palestrante.DoesNotExist:
        eventos = eventos_criados.order_by('-data')
    
    context = {'eventos': eventos}
    return render(request, 'eventos/meus_eventos.html', context)


@login_required
@permission_required('eventos.change_evento', raise_exception=True)
def editar_evento(request, evento_id):
    """View para edição de eventos - apenas palestrantes que criaram o evento"""
    evento = get_object_or_404(Evento, id=evento_id)
    
    # Verificar se o usuário é o criador do evento ou palestrante do evento
    is_creator = evento.criador == request.user
    is_palestrante = False
    
    try:
        palestrante = Palestrante.objects.get(user=request.user)
        is_palestrante = palestrante in evento.palestrantes.all()
    except Palestrante.DoesNotExist:
        pass
    
    if not (is_creator or is_palestrante):
        messages.error(request, 'Você não tem permissão para editar este evento.')
        return redirect('meus_eventos')
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('meus_eventos')
    else:
        form = EventoForm(instance=evento)
    
    context = {'form': form, 'evento': evento}
    return render(request, 'eventos/editar_evento.html', context)


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
        return redirect('meus_ingressos')
    
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
        return redirect('meus_ingressos')
    
    context = {
        'evento': evento,
    }
    return render(request, 'eventos/comprar_ingresso.html', context)


@login_required
def meus_ingressos(request):
    """Lista os ingressos do usuário"""
    ingressos = Ingresso.objects.filter(participante=request.user).order_by('-data_compra')
    
    context = {'ingressos': ingressos}
    return render(request, 'eventos/meus_ingressos.html', context)


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
        return redirect('meus_ingressos')
    
    context = {
        'ingresso': ingresso,
    }
    return render(request, 'eventos/cancelar_ingresso.html', context)


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
def cadastrar_palestrante(request):
    """View para usuários se cadastrarem como palestrantes"""
    # Verificar se o usuário já é palestrante
    if hasattr(request.user, 'profile') and request.user.profile.tipo_usuario == 'palestrante':
        messages.info(request, 'Você já está cadastrado como palestrante.')
        return redirect('usuario:painel_palestrante')
    
    if request.method == 'POST':
        # Atualizar o perfil do usuário para palestrante
        profile = request.user.profile
        profile.tipo_usuario = 'palestrante'
        
        # Obter dados do formulário
        biografia = request.POST.get('biografia', '')
        tema = request.POST.get('tema', 'Geral')
        horario = request.POST.get('horario', '09:00')
        
        profile.biografia = biografia
        profile.save()
        
        # Criar registro de palestrante
        palestrante, created = Palestrante.objects.get_or_create(
            user=request.user,
            defaults={
                'nome': request.user.get_full_name() or request.user.username,
                'biografia': biografia,
                'tema': tema,
                'horario': horario
            }
        )
        
        messages.success(request, 'Cadastro como palestrante realizado com sucesso! Agora você pode criar eventos.')
        return redirect('usuario:painel_palestrante')
    
    context = {}
    return render(request, 'eventos/cadastrar_palestrante.html', context)


@login_required
@permission_required('eventos.view_evento', raise_exception=True)
def painel_palestrante(request):
    """Painel do palestrante com estatísticas e funcionalidades específicas"""
    from django.db.models import Count, Sum
    from datetime import date
    
    # Busca eventos do palestrante
    eventos_criados = Evento.objects.filter(criador=request.user)
    
    try:
        palestrante = Palestrante.objects.get(user=request.user)
        eventos_palestrante = Evento.objects.filter(palestrantes=palestrante)
    except Palestrante.DoesNotExist:
        eventos_palestrante = Evento.objects.none()
    
    # Combina os querysets
    eventos = (eventos_criados | eventos_palestrante).distinct().order_by('-data')
    
    # Calcula estatísticas
    total_eventos = eventos.count()
    eventos_proximos = eventos.filter(data__gte=date.today()).count()
    
    # Calcula total de participantes
    total_participantes = 0
    receita_total = 0
    
    for evento in eventos:
        participantes_evento = evento.ingressos.count()
        total_participantes += participantes_evento
        
        if evento.preco:
            receita_total += evento.preco * participantes_evento
    
    # Adiciona informações de participantes para cada evento
    for evento in eventos:
        evento.vagas_ocupadas = evento.ingressos.count()
    
    context = {
        'eventos': eventos,
        'total_eventos': total_eventos,
        'total_participantes': total_participantes,
        'eventos_proximos': eventos_proximos,
        'receita_total': receita_total,
    }
    
    return render(request, 'eventos/painel_palestrante.html', context)
