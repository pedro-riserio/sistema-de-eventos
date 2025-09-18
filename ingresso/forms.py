from django import forms
from .models import Ingresso
from eventos.models import Evento
from django.contrib.auth import get_user_model

User = get_user_model()

class IngressoForm(forms.ModelForm):
    class Meta:
        model = Ingresso
        fields = ['evento', 'tipo', 'valor', 'participante']
        widgets = {
            'evento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Digite o valor do ingresso'
            }),
            'participante': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'evento': 'Evento',
            'tipo': 'Tipo de Ingresso',
            'valor': 'Valor (R$)',
            'participante': 'Participante'
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filtrar apenas eventos do usuário logado
            self.fields['evento'].queryset = Evento.objects.filter(
                criador=user
            )
        else:
            self.fields['evento'].queryset = Evento.objects.all()
    
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor and valor < 0:
            raise forms.ValidationError('O valor deve ser maior ou igual a zero.')
        return valor