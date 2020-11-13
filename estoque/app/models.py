from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.IntegerField(default=None)
    marca = models.CharField(max_length=100, default=None)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=100, decimal_places= 2, default=None)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return str(self.nome)

    class Meta:
        db_table = 'produto'

    def get_absolute_url(self):
        return reverse_lazy('produto', kwargs={'id': self.id})

    def to_dict_json(self):
        return {
            'pk': self.pk,
            'produto': self.nome,
            'estoque': self.quantidade,
        }

class TimeStampedModel(models.Model):
    created = models.DateField('criado em', auto_now_add=True, auto_now=False)
    modified = models.DateField('modificado em', auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True

MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida')
)

class Estoque(TimeStampedModel):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nf = models.PositiveIntegerField('nota fiscal', null=True, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} | {} | {}'.format(self.pk, self.nf, self.created.strftime('%d-%m-%Y'))

    def get_absolute_url(self):
        return reverse_lazy('estoque_entrada_detail', kwargs={'id': self.id})

    def nf_formated(self):
        return str(self.nf).zfill(3)

class EstoqueItens(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='estoques')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    saldo = models.PositiveIntegerField()

    class Meta:
        ordering=('pk',)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.estoque.pk,self.produto.pk)