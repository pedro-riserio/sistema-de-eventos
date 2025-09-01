from django import forms
from .models import Local

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['nome', 'endereco', 'capacidade']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do local'
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Digite o endereço completo do local'
            }),
            'capacidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Capacidade máxima de pessoas'
            })
        }
        labels = {
            'nome': 'Nome do Local',
            'endereco': 'Endereço',
            'capacidade': 'Capacidade'
        }
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome and len(nome) < 3:
            raise forms.ValidationError('O nome deve ter pelo menos 3 caracteres.')
        return nome
    
    def clean_capacidade(self):
        capacidade = self.cleaned_data.get('capacidade')
        if capacidade and capacidade < 1:
            raise forms.ValidationError('A capacidade deve ser maior que zero.')
        return capacidade