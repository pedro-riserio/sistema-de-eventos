from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Usuario

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'telefone', 'cpf', 'group']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: (11) 99999-9999'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123.456.789-00'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome Completo',
            'telefone': 'Telefone',
            'cpf': 'CPF',
            'group': 'Grupo/Tipo de Usuário',
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nome = forms.CharField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ('username', 'nome', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuário'
        self.fields['nome'].widget.attrs['placeholder'] = 'Nome completo'
        self.fields['email'].widget.attrs['placeholder'] = 'seu@email.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme a senha'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.nome = self.cleaned_data['nome']
        if commit:
            user.save()
        return user