from django.forms import Form, ModelForm, CheckboxSelectMultiple, ChoiceField
from .models import OrdemDeServico, Sistema, Subsistemas, TIPO_CHOICES

class Tipo(Form):
    tipo = ChoiceField(label='Tipo',choices=TIPO_CHOICES)

class OrdemServicoDireto(ModelForm):
    class Meta:
        model = OrdemDeServico

        #Direto
        fields = ['realizacao_date',
        'tempo',
        'pit',
        'motivo',
        'desc_material',
        'quantidade',
        'serv_realizado',
        'suprimento_aplicado',
        'custo_total',
        'om_requerente',
        'quant_homens',
        'sistema',
        'subsistemas_manutenidos']

        widgets = {
            'subsistemas_manutenidos': CheckboxSelectMultiple(),
        }


    def __init__(self,*args,**kwargs):
        classe = kwargs.pop('classe')
        super(OrdemServicoDireto,self).__init__(*args,**kwargs)
        if classe != 0:
            self.fields['sistema'].queryset = Sistema.objects.filter(classe=classe)
            self.fields['subsistemas_manutenidos'].queryset = Subsistemas.objects.filter(classe=classe)

class OrdemServicoSuprimento(ModelForm):
    class Meta:
        model = OrdemDeServico

        #Direto
        fields = ['realizacao_date',
        'pit',
        'motivo',
        'desc_material',
        'quantidade',
        'serv_realizado',
        'suprimento_aplicado',
        'custo_total',
        'om_requerente',
        'quant_homens',
        'sistema',
        'subsistemas_manutenidos']

        widgets = {
            'subsistemas_manutenidos': CheckboxSelectMultiple(),
        }


    def __init__(self,*args,**kwargs):
        classe = kwargs.pop('classe')
        super(OrdemServicoSuprimento,self).__init__(*args,**kwargs)
        if classe != 0:
            self.fields['sistema'].queryset = Sistema.objects.filter(classe=classe)
            self.fields['subsistemas_manutenidos'].queryset = Subsistemas.objects.filter(classe=classe)
    
class OrdemServicoConjunto(ModelForm):
    class Meta:
        model = OrdemDeServico

        #Direto
        fields = ['realizacao_date',
        'tempo',
        'pit',
        'motivo',
        'desc_material',
        'quantidade',
        'serv_realizado',
        'suprimento_aplicado',
        'custo_total',
        'om_requerente',
        'quant_homens',
        'sistema',
        'subsistemas_manutenidos']

        widgets = {
            'subsistemas_manutenidos': CheckboxSelectMultiple(),
        }


    def __init__(self,*args,**kwargs):
        classe = kwargs.pop('classe')
        super(OrdemServicoConjunto,self).__init__(*args,**kwargs)
        if classe != 0:
            self.fields['sistema'].queryset = Sistema.objects.filter(classe=classe)
            self.fields['subsistemas_manutenidos'].queryset = Subsistemas.objects.filter(classe=classe)

    '''def __init__(self, classe=None, **kwargs):
        super(OrdemServico, self).__init__(classe,**kwargs)
        if classe != 0:
            self.fields['sistema'].queryset = Sistema.objects.filter(classe=classe)
            self.fields['subsistemas_manutenidos'].queryset = Subsistemas.objects.filter(classe=classe)'''
    
    '''fields = [   'aguardando_ciente_date',
                    'aguardando_inspecao_date',
                    'realizando_inspecao_date',
                    'aguardando_manutencao_date',
                    'em_manutencao_date',
                    'aguardando_testes_date',
                    'testes_em_execucao_date',
                    'remanutencao_date',
                    'aguardando_remessa_date',
                    'fechada_sem_ciente_date',
                    'fechada_arquivar_date',
                    'tipo',
                    'status',
                    'nd',
                    'motivo',
                    'desc_material',
                    'prioridade',
                    'quantidade',
                    'serv_realizado',
                    'custo_total',
                    'classe',
                    'om_requerente',
                    'ordem_recolhimento',
                    'guia_recolhimento',
                    'num_diex',
                    'medidas_corretivas',
                    'quant_homens',
                    'prestador_servico',
                    'sistema',
                    'subsistemas_manutenidos',
                    'ch_cp',
                    'ch_classe',
                    'cmt_pel']'''

class ConsultaOrdemServico(ModelForm):
    class Meta:
        model = OrdemDeServico

        #Direto
        fields = ['id',
                    'classe']