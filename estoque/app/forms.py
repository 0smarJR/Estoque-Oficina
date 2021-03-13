from django import forms
from .models import Produto, Estoque, EstoqueItens

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