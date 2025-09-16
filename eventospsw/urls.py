"""
URL configuration for eventospsw project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from eventos import views as eventos_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Páginas principais
    path('', eventos_views.home, name='home'),
    path('eventos/', eventos_views.lista_eventos, name='lista_eventos'),
    path('evento/<int:evento_id>/', eventos_views.detalhe_evento, name='detalhe_evento'),
    path('sobre/', eventos_views.sobre, name='sobre'),
    path('contato/', eventos_views.contato, name='contato'),
    path('inscrever/<int:evento_id>/', eventos_views.inscrever_evento, name='inscrever_evento'),
    
    # Apps URLs com prefixos únicos
    path('gerenciar/eventos/', include('eventos.urls')),
    path('usuario/', include('usuario.urls')),
    path('categoria/', include('categoria.urls')),
    path('atividade/', include('atividade.urls')),
    path('local/', include('local.urls')),
    path('ingresso/', include('ingresso.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
