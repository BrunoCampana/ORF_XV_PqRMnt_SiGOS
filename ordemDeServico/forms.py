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
        'suprimento_aplicado',
        'custo_total',
        'om_requerente',
        'sistema']

    def __init__(self,*args,**kwargs):
        classe = kwargs.pop('classe')
        super(OrdemServicoSuprimento,self).__init__(*args,**kwargs)
        if classe != 0:
            self.fields['sistema'].queryset = Sistema.objects.filter(classe=classe)
    
class OrdemServicoConjunto(ModelForm):
    class Meta:
        model = OrdemDeServico

        #Direto
        fields = ['om_requerente',
        'ordem_recolhimento',
        'guia_recolhimento',
        'num_diex',
        'pit',
        'nd',
        'motivo',
        'desc_material']

class ConsultaOrdemServico(ModelForm):
    class Meta:
        model = OrdemDeServico

        #Direto
        fields = ['id',
                    'classe']