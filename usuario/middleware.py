from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class GroupRedirectMiddleware:
    """
    Middleware que redireciona usuários para dashboards específicos baseado em seus grupos
    após o login ou quando acessam a página inicial.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # URLs que devem ser redirecionadas baseadas no grupo
        redirect_urls = [
            reverse('home'),
        ]
        
        # URLs que devem ser excluídas do redirecionamento
        excluded_paths = [
            reverse('usuario:logout'),
            '/admin/logout/',
        ]
        
        # Não redirecionar se estiver acessando URLs excluídas
        if request.path in excluded_paths:
            return None
        
        # Verificar se não está vindo de uma URL excluída (logout)
        referer = request.META.get('HTTP_REFERER', '')
        if any(excluded_path in referer for excluded_path in excluded_paths):
            return None
        
        # Verificar se há uma mensagem de logout na sessão (indica logout recente)
        if 'logout_redirect' in request.session:
            del request.session['logout_redirect']
            return None
        
        # Verificar se o usuário está autenticado e na página inicial
        if (request.user.is_authenticated and 
            request.path in redirect_urls and 
            request.method == 'GET'):
            
            # Verificar grupos do usuário e redirecionar
            if request.user.groups.filter(name='palestrante').exists():
                return redirect('usuario:dashboard_palestrante')
            elif request.user.groups.filter(name='participante').exists():
                return redirect('usuario:dashboard_participante')
        
        return None


class GroupAccessMiddleware:
    """
    Middleware que verifica permissões de acesso baseadas em grupos
    para URLs específicas.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Definir URLs protegidas por grupo
        self.protected_urls = {
            'palestrante': [
                '/usuario/dashboard-palestrante/',
                '/eventos/criar/',
                '/eventos/editar/',
                '/eventos/meus-eventos/',
            ],
            'participante': [
                '/usuario/dashboard-participante/',
                '/eventos/meus-ingressos/',
                '/ingresso/comprar/',
            ]
        }
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Verificar se o usuário está autenticado
        if not request.user.is_authenticated:
            return None
        
        # Verificar se a URL atual está protegida
        current_path = request.path
        
        for grupo, urls in self.protected_urls.items():
            if any(current_path.startswith(url) for url in urls):
                # Verificar se o usuário pertence ao grupo necessário
                if not request.user.groups.filter(name=grupo).exists():
                    # Permitir acesso para superusuários
                    if not request.user.is_superuser:
                        messages.error(request, f'Acesso negado. Você não tem permissão de {grupo}.')
                        return redirect('home')
        
        return None