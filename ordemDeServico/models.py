from django.db import models

# Limitação de tipos
CLASSE_CHOICES = (
    (0, 'Sem Classe'),
    (1, 'I'),
    (2, 'II'),
    (3, 'III'),
    (4, 'IV'),
    (5, 'V'),
    (6, 'VI'),
    (7, 'VII'),
    (8, 'VIII'),
    (9, 'IX'),
    (10, 'X'),
    (11, 'XI'),
    (12, 'XII'),
)

TIPO_CHOICES = (
    (0, 'Apoio em conjunto'),
    (1, 'Apoio direto'),
    (2, 'Apoio em suprimento'),
)

STATUS_CHOICES = (
    (1, 'Aguardando ciente'),
    (2, 'Aguardando inspeção'),
    (3, 'Realizando inspeção'),
    (4, 'Aguardando manutenção'),
    (5, 'Em manutenção'),
    (6, 'Aguardando testes'),
    (7, 'Testes em execução'),
    (8, 'Remanutenção'),
    (9, 'Aguardando remessa'),
    (10, 'Fechada - aguardando ciente'),
    (11, 'Fechada - ciente dado'),
)


# Create your models here.
class Sistema(models.Model):
    descricao = models.TextField(max_length=255)
    classe = models.IntegerField(choices=CLASSE_CHOICES)

    def __str__(self):
        return u'%s' % (self.descricao)


class Subsistemas(models.Model):
    descricao = models.TextField(max_length=255)
    classe = models.IntegerField(choices=CLASSE_CHOICES)

    def __str__(self):
        return u'%s' % (self.descricao)

class OM(models.Model):
    nome = models.CharField(max_length=10)

    def __str__(self):
        return u'%s' % (self.nome)

class OrdemDeServico(models.Model):
    nr_os = models.IntegerField()

    # datas salvas
    abertura_os_date = models.DateTimeField('data abertura os', blank=True, null=True)
    aguardando_ciente_date = models.DateTimeField('data aguardando ciente', blank=True, null=True)
    aguardando_inspecao_date = models.DateTimeField('data aguardando inspecao', blank=True, null=True)
    realizando_inspecao_date = models.DateTimeField('data realizando inspecao', blank=True, null=True)
    aguardando_manutencao_date = models.DateTimeField('data aguardando manutencao', blank=True, null=True)
    em_manutencao_date = models.DateTimeField('data em manutencao', blank=True, null=True)
    aguardando_testes_date = models.DateTimeField('data aguardando testes', blank=True, null=True)
    testes_em_execucao_date = models.DateTimeField('data testes em execucao', blank=True, null=True)
    remanutencao_date = models.DateTimeField('data remanutencao', blank=True, null=True)
    aguardando_remessa_date = models.DateTimeField('data aguardando remessa', blank=True, null=True)
    fechada_sem_ciente_date = models.DateTimeField('data fechada sem ciente', blank=True, null=True)
    fechada_arquivar_date = models.DateTimeField('data fechada arquivar', blank=True, null=True)
    realizacao_date = models.DateTimeField('data realizacao', blank=True, null=True)

    # atributos
    tipo = models.IntegerField(choices=TIPO_CHOICES)
    status = models.IntegerField()
    nd = models.IntegerField()

    pit = models.BooleanField()

    # TODO TEMPO (DURAÇÃO EM APOIO DIRETO)
    tempo = models.IntegerField(null=True)

    # TODO SUPRIMENTO APLICADO (TEXT-AREA EM ALL)
    suprimento_aplicado = models.TextField(blank=True)

    motivo = models.CharField(max_length=255)
    desc_material = models.TextField(blank=True)
    prioridade = models.IntegerField(blank=True, null=True)
    quantidade = models.IntegerField()
    serv_realizado = models.TextField(blank=True)
    custo_total = models.IntegerField()
    classe = models.IntegerField(choices=CLASSE_CHOICES)
    om_requerente = models.ForeignKey(OM)
    ordem_recolhimento = models.CharField(max_length=30, blank=True)
    guia_recolhimento = models.CharField(max_length=30, blank=True)
    num_diex = models.CharField(max_length=30, blank=True)

    # medidas corretivas - Remanutenção
    medidas_corretivas = models.TextField(blank=True)

    # ND30
    quant_homens = models.IntegerField(blank=True, default=0)

    # ND39
    prestador_servico = models.CharField(max_length=255, blank=True)

    # Chaves estrangeiras
    sistema = models.ForeignKey(Sistema)
    subsistemas_manutenidos = models.ManyToManyField(Subsistemas)
    ch_cp = models.ForeignKey('login.InformacaoMilitar', related_name='Ch_CP')
    ch_classe = models.ForeignKey('login.InformacaoMilitar', related_name='Ch_Classe')
    cmt_pel = models.ForeignKey('login.InformacaoMilitar', related_name='Cmt_Pel')


