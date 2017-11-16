from ordemDeServico.models import Sistema, OrdemDeServico
from login.models import Funcao
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime, timedelta

def getFuncaoMilitar(user):
    user_id = user.id
    return Funcao.objects.filter(militar=user_id).values()

def getIDCmtPel(classe):
    return Funcao.objects.filter(classe=classe, nome_funcao=3).values()[0]['militar_id']

def getIDChCP():
    return Funcao.objects.filter(nome_funcao=1).values()[0]['militar_id']

def getOSfromId(os_id):
    print("GET OS ID")
    #return OrdemDeServico.objects.filter(id=os_id)
    return OrdemDeServico.objects.get(id=os_id)

def generateOSNr(tipo, classe):
    recent_os_list = OrdemDeServico.objects.filter(classe=classe,tipo=tipo).order_by('-abertura_os_date').values()
    if len(recent_os_list) == 0:
        return 1
    recent_os = recent_os_list[0]
    recent_date = recent_os['abertura_os_date']
    now_date = datetime.now() - timedelta(hours=4)
    print(recent_date)
    if now_date.year > recent_date.year:
        return 1
    return (recent_os['nr_os'] + 1)

def meu_login_required(function=None, login_url=None):
	actual_decorator = login_required(function=function, redirect_field_name=None, login_url=login_url)
	return actual_decorator

def meu_anonymous_required(func):
	def func_wrapper(request):
		if not request.user.is_authenticated():
			return func(request)
		else:
			return redirect('/')
	return func_wrapper

def meu_mudar_senha(form, request):
	username = request.user.get_username()
	password = form.cleaned_data['novaSenha']

	user = User.objects.get(username__exact=request.user.get_username())
	user.set_password(form.cleaned_data['novaSenha'])
	user.save()	

	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)

def incrementarStatus(os, status):
    os = os.get()
    os.status = status + 1
    os.save()

def getPermissions(user):
    funcao = getFuncaoMilitar(user)
    classe = funcao.values('classe')
    nome_funcao= funcao.values('nome_funcao')
 
    permissions = [[x['classe'], y['nome_funcao']] for (x, y) in list(zip(list(classe), list(nome_funcao)))]
 
    return permissions


def os_form(os_dict):
    os_names = {'serv_realizado': 'Serviço realizado',
                'quant_homens': 'Quantidade de homens',
                'realizacao_date': 'Data de realização',
                'classe': 'Classe',
                'remanutencao_date': 'Data de remanutenção',
                'custo_total': 'Custo total',
                'medidas_corretivas': 'Medidas corretivas',
                'quantidade': 'Quantidade',
                'subsistemas_manutenidos': 'Subsistemas manutenidos',
                'abertura_os_date': 'Data de abertura',
                'pit': 'PIT',
                'ordem_recolhimento': 'Ordem de Recolhimento',
                'aguardando_inspecao_date': 'Data de aguardando inspeção',
                'aguardando_ciente_date': 'Data de aguardando ciente',
                'aguardando_remessa_date': 'Data de aguardando remessa',
                'desc_material': 'Descrição do material',
                'tipo': 'Tipo',
                'em_manutencao_date': 'Data de ínicio de manutenção',
                'guia_recolhimento': 'Guia de recolhimento',
                'fechada_arquivar_date': 'Data de fechamento/arquivamento',
                'testes_em_execucao_date': 'Data de testes em execução',
                'prestador_servico': 'Prestador de serviço',
                'om_requerente': 'OM requerente',
                'fechada_sem_ciente_date': 'Data de fechamento sem ciente',
                'ch_classe': 'Chefe de classe',
                'status': 'Status',
                'sistema': 'Sistema',
                'cmt_pel': 'Cmt Pel',
                'nr_os': 'Nr OS',
                'aguardando_testes_date': 'Data de aguardando testes',
                'realizando_inspecao_date': 'Data de realizando inspeção',
                'tempo': 'tempo',
                'motivo': 'Motivo',
                'suprimento_aplicado': 'Suprimento aplicado',
                'prioridade': 'Prioridade',
                'num_diex': 'Nr DIEX',
                'nd': 'ND',
                'ch_cp': 'Chefe de CP',
                'aguardando_manutencao_date':'Data de aguardando manutenção',
                'id': 'ID'
             }

    form_dict = {}
    for key in os_dict:
        if os_dict[key] is not None and key is not 'id' and os_dict[key] is not '':
           form_dict[os_names[key]] = os_dict[key]

    return form_dict
