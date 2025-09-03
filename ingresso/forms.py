from django import forms
from .models import Ingresso
from .models_crud import TipoIngresso
from eventos.models import Evento

class IngressoForm(forms.ModelForm):
    class Meta:
        model = TipoIngresso
        fields = ['evento', 'tipo', 'preco', 'quantidade_disponivel']
        widgets = {
            'evento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Digite o preço do ingresso'
            }),
            'quantidade_disponivel': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Quantidade disponível'
            })
        }
        labels = {
            'evento': 'Evento',
            'tipo': 'Tipo de Ingresso',
            'preco': 'Preço (R$)',
            'quantidade_disponivel': 'Quantidade Disponível'
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
    
    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco and preco < 0:
            raise forms.ValidationError('O preço deve ser maior ou igual a zero.')
        return preco
    
    def clean_quantidade_disponivel(self):
        quantidade = self.cleaned_data.get('quantidade_disponivel')
        if quantidade and quantidade < 1:
            raise forms.ValidationError('A quantidade deve ser maior que zero.')
        return quantidade