from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuario'

urlpatterns = [
    # Funcionalidades de usuário
    path('perfil/', views.criar_perfil, name='criar_perfil'),
    path('meus-ingressos/', views.meus_ingressos, name='meus_ingressos'),
    
    # Dashboards específicos por grupo
    path('dashboard-palestrante/', views.dashboard_palestrante, name='dashboard_palestrante'),
    path('dashboard-participante/', views.dashboard_participante, name='dashboard_participante'),
    
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('registro/', views.registro, name='registro'),
    
    # Reset de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]