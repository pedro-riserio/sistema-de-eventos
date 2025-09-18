from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Usuario

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'telefone', 'cpf', 'area']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: (11) 99999-9999'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123.456.789-00'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Tecnologia, Marketing, Educação...'})
        }
        labels = {
            'nome': 'Nome Completo',
            'telefone': 'Telefone',
            'cpf': 'CPF',
            'area': 'Área de Atuação'
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nome = forms.CharField(max_length=200, required=True)
    cpf = forms.CharField(max_length=14, required=True)
    area = forms.CharField(max_length=100, required=False)
    tipo_usuario = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Palestrante', 'Participante']),
        empty_label="Selecione seu tipo de usuário",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'nome', 'cpf', 'area', 'tipo_usuario')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuário'
        self.fields['nome'].widget.attrs['placeholder'] = 'Nome completo'
        self.fields['cpf'].widget.attrs['placeholder'] = 'Ex: 123.456.789-00'
        self.fields['area'].widget.attrs['placeholder'] = 'Ex: Tecnologia, Marketing, Educação...'
        self.fields['email'].widget.attrs['placeholder'] = 'seu@email.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme a senha'
        
        # Personalizar labels
        self.fields['tipo_usuario'].label = 'Tipo de Usuário'

    def save(self, commit=True):
        # Criar o usuário como Usuario (que herda de User)
        usuario = Usuario(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            nome=self.cleaned_data['nome'],
            telefone='',  # Campo telefone vazio por padrão
            cpf=self.cleaned_data['cpf'],
            area=self.cleaned_data.get('area', '')
        )
        usuario.set_password(self.cleaned_data['password1'])
        
        if commit:
            usuario.save()
            # Adicionar usuário ao grupo selecionado
            grupo = self.cleaned_data['tipo_usuario']
            usuario.groups.add(grupo)
        return usuario