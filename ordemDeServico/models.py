from django.db import models
#Limitação de tipos
CLASSES_CHOICE = ()

# Create your models here.
class Sistema(models.Model):
    descricao = models.TextField(max_length=255)
    classe = models.IntegerField()

class Subsistemas(models.Model):
    descricao = models.TextField(max_length=255)
    classe = models.IntegerField()

class OrdemDeServico(models.Model):

	#datas salvas
    aguardando_ciente_date = models.DateTimeField('data aguardando ciente')
    aguardando_inspecao_date = models.DateTimeField('data aguardando inspecao')
    realizando_inspecao_date = models.DateTimeField('data realizando inspecao')
    aguardando_manutencao_date = models.DateTimeField('data aguardando manutencao')
    em_manutencao_date = models.DateTimeField('data em manutencao')
    aguardando_testes_date = models.DateTimeField('data aguardando testes')
    testes_em_execucao_date = models.DateTimeField('data testes em execucao')
    remanutencao_date = models.DateTimeField('data remanutencao')
    aguardando_remessa_date = models.DateTimeField('data aguardando remessa')
    fechada_sem_ciente_date = models.DateTimeField('data fechada sem ciente')
    fechada_arquivar_date = models.DateTimeField('data fechada arquivar')
    realizacao_date = models.DateTimeField('data realizacao')
    
    #atributos
    tipo = models.IntegerField()
    status = models.IntegerField()
    nd = models.IntegerField()
    
    pit = models.BooleanField()
    
    # TODO TEMPO (DURAÇÃO EM APOIO DIRETO)
    tempo = models.IntegerField()
    
    # TODO SUPRIMENTO APLICADO (TEXT-AREA EM ALL)
    suprimento_aplicado = models.TextField()
    
    motivo = models.CharField(max_length=255)
    desc_material = models.TextField()
    prioridade = models.IntegerField()
    quantidade = models.IntegerField()
    serv_realizado = models.TextField()
    custo_total = models.IntegerField()
    classe = models.IntegerField()
    om_requerente = models.CharField(max_length=255)
    ordem_recolhimento = models.CharField(max_length=30)
    guia_recolhimento = models.CharField(max_length=30)
    num_diex = models.CharField(max_length=30)

    #medidas corretivas - Remanutenção
    medidas_corretivas = models.TextField()

    #ND30
    quant_homens = models.IntegerField()

    #ND39
    prestador_servico = models.CharField(max_length=255)

    #Chaves estrangeiras
    sistema = models.ForeignKey(Sistema)
    subsistemas_manutenidos = models.ManyToManyField(Subsistemas)
    ch_cp = models.ForeignKey('login.InformacaoMilitar', related_name='Ch_CP')
    ch_classe = models.ForeignKey('login.InformacaoMilitar', related_name='Ch_Classe')
    cmt_pel = models.ForeignKey('login.InformacaoMilitar', related_name='Cmt_Pel')
