from django import forms
from .models import Evento
from local.models import Local
from categoria.models import Categoria


class InscricaoEventoForm(forms.Form):
    aceito_termos = forms.BooleanField(
        required=True,
        label='Aceito os termos e condições',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class BuscaEventoForm(forms.Form):
    data = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    busca = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar eventos...'})
    )


class ContatoForm(forms.Form):
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'})
    )
    assunto = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assunto da mensagem'})
    )
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Sua mensagem...'})
    )


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'tipo', 'descricao', 'data', 'horario', 'local', 'categoria', 'criador', 'capacidade', 'preco', 'status', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do evento'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição do evento...'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'horario': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'local': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'criador': forms.Select(attrs={'class': 'form-select'}),
            'capacidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome do Evento',
            'tipo': 'Tipo',
            'descricao': 'Descrição',
            'data': 'Data do Evento',
            'horario': 'Horário',
            'local': 'Local',
            'categoria': 'Categoria',
            'criador': 'Criador do Evento',
            'capacidade': 'Capacidade',
            'preco': 'Preço',
            'status': 'Status',
            'imagem': 'Imagem do Evento',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carregar apenas locais e categorias ativas se houver
        self.fields['local'].queryset = Local.objects.all()
        self.fields['categoria'].queryset = Categoria.objects.all()