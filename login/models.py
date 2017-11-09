from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from ordemDeServico.models import CLASSE_CHOICES

NOME_FUNCAO_CHOICES = (
    (0, 'Sem função'),
    (1, 'Chefe CP'),
    (2, 'Adj CP'),
    (3, 'Cmt Pel'),
    (4, 'Chefe Classe'),
)
# Create your models here.

class InformacaoMilitar(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    posto = models.CharField(max_length=10)
    om = models.CharField(max_length=50)

    REQUIRED_FIELDS = ['posto', 'om']
    
def inserir_infoMil(sender, **kwargs):
    user = kwargs["instance"]

    if kwargs["created"]:
        ### MUDAR ABAIXO PARA VALORES RECEBIDOS. PESQUISAR ###
        infoMil = InformacaoMilitar(user=user, posto='1ten', om='IME')
        infoMil.save()
post_save.connect(inserir_infoMil, sender=settings.AUTH_USER_MODEL)

class Funcao(models.Model):
    militar = models.ForeignKey(User)
    nome_funcao = models.IntegerField(choices=NOME_FUNCAO_CHOICES)
    classe = models.IntegerField(choices=CLASSE_CHOICES)
