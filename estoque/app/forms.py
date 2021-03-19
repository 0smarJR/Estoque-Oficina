from django import forms
from .models import Produto, Estoque, EstoqueItens
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = '__all__'

class EstoqueForm(forms.ModelForm):

    class Meta:
        model = Estoque
        fields = ('usuario', 'nf')

class EstoqueItensForm(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = '__all__'

class UsuarioForm(UserCreationForm):
    #email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2', 'is_superuser']
