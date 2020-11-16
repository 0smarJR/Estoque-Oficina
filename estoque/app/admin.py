from django.contrib import admin
from .models import Produto, Estoque, EstoqueItens, EstoqueEntrada, EstoqueSaida
# Register your models here.

@admin.register(Produto)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'marca', 'quantidade', 'preco']

class EstoqueItensInline(admin.TabularInline):
    model = EstoqueItens
    extra = 0

@admin.register(EstoqueEntrada)
class EstoqueEntradaAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'nf', 'usuario',)
    search_fields = ('nf',)
    list_filter = ('usuario',)
    date_hierarchy = 'created'


@admin.register(EstoqueSaida)
class EstoqueSaidaAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'nf', 'usuario',)
    search_fields = ('nf',)
