from django.forms import ModelForm
from .models import OrdemDeServico

class OrdemServico(ModelForm):
    class Meta:
        model = OrdemDeServico
        fields = ['realizacao_servico_date','motivo','desc_material','quantidade','serv_realizado','custo_total','classe','om_requerente','quant_homens','sistema','subsistemas_manutenidos']

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