from django import forms
from .models import Usuarios  # Corrigido aqui

class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuarios
        fields = ['email', 'senha']
