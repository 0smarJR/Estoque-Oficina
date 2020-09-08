from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    ativo = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.nome)

    class Meta:
        db_table = 'produto'