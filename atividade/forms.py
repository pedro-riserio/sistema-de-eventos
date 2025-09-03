from django import forms
from .models import Atividade
from eventos.models import Evento
from django.contrib.auth import get_user_model

User = get_user_model()

class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ['nome', 'evento', 'responsavel', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da atividade'
            }),
            'evento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'responsavel': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tipo da atividade (ex: Palestra, Workshop, Mesa Redonda)'
            })
        }
        labels = {
            'nome': 'Nome da Atividade',
            'evento': 'Evento',
            'responsavel': 'Responsável',
            'tipo': 'Tipo'
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar eventos apenas do usuário logado
        if user:
            self.fields['evento'].queryset = Evento.objects.filter(criador=user)
        
        # Filtrar responsáveis apenas usuários que criaram eventos
        criadores = User.objects.filter(eventos_criados__isnull=False).distinct()
        self.fields['responsavel'].queryset = criadores
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError('O nome deve ter pelo menos 3 caracteres.')
        return nome