from django.contrib import admin
from .models import Produto, Estoque, EstoqueItens
# Register your models here.

@admin.register(Produto)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'marca', 'quantidade', 'preco']

class EstoqueItensInline(admin.TabularInline):
    model = EstoqueItens
    extra = 0

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    list_display = ['__str__', 'usuario', 'nf',]
    search_fields = ('nf',)
    list_filter = ('usuario',)
    date_hierarchy = 'created'

