from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import OrdemServicoConjunto, OrdemServicoDireto, OrdemServicoSuprimento, ConsultaOrdemServico, Tipo, MedidasCorretivas, OrdemServicoConjuntoFinal30, OrdemServicoConjuntoFinal39
from .models import Sistema, OrdemDeServico, OM
from login.models import Funcao
from datetime import datetime
from src.utils import getFuncaoMilitar, getIDCmtPel, getIDChCP, getOSfromId, generateOSNr, meu_login_required, incrementarStatus, getPermissions
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from  login.models import InformacaoMilitar
from collections import OrderedDict


TIPO_CHOICES = (
    (1, 'Apoio em conjunto'),
    (2, 'Apoio direto'),
    (3, 'Apoio em suprimento'),
)

STATUS_CHOICES = (
    (1, 'Aguardando ciente de abertura'),
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



# Create your views here.

@meu_login_required
def escolhertipoOS(request):
    funcao = getFuncaoMilitar(request.user)
    classes = funcao.values('classe')
    nome_funcao= funcao.values('nome_funcao')
    nome_funcao = {x['nome_funcao'] for x in list(nome_funcao)}
    if 4 not in nome_funcao:
        return render(request, "ordemDeServico/semPermissao.html")

    if request.method == 'POST':
        form = Tipo(request.POST, classe=classes)
        if form.is_valid():
            tipo = form.cleaned_data['tipo']
            classe = form.cleaned_data['classe']
            return redirect("/ordemservico/criar/" + tipo + '/' + classe)
        else:
            print(form.errors)
    else:
        form = Tipo(classe=classes)
    return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Abrir'})

@meu_login_required
def criarordemservico(request, tipo, classe):
    funcao = getFuncaoMilitar(request.user)
    #classe = funcao.values('classe')
    #classe = funcao[0]['classe']
    #print(classe)

    classe = int(classe)
    classe_militar = funcao.values('classe')
    nome_funcao= funcao.values('nome_funcao')

    permissions = [[x['classe'], y['nome_funcao']] for (x, y) in list(zip(list(classe_militar), list(nome_funcao)))]
 

    if([classe, 4] in permissions):
        if request.method == 'POST':
            if int(tipo) == 0: #Apoio em Conjunto
                form = OrdemServicoConjunto(request.POST,classe=classe)
                if form.is_valid():
                    instance = form.save(commit=False)
                    
                    instance.abertura_os_date = datetime.now()
                    nr_os_temp = generateOSNr(tipo, classe)
                    instance.nr_os = nr_os_temp
                    instance.tipo = tipo
                    instance.status = 1
                    instance.classe = classe
                    
                    instance.ch_classe_id = request.user.id
                    instance.ch_cp_id = getIDChCP()
                    instance.cmt_pel_id = getIDCmtPel(classe)
                    
                    saved_form = instance.save()
                    form.save_m2m()
                    str_success = "OS nr: " + str(nr_os_temp) + ", de tipo: " + str(TIPO_CHOICES[int(tipo)][1]) + " e de classe: " + str(classe)
                    return render(request, 'ordemDeServico/ok.html', {'mensagem':str_success})
                else:
                    #TODO redirect pra página de falha em adicionar
                    #return render(request, 'ordemDeServico/falha.html', {'form': form, 'submitValue': 'Salvar', 'classe':classe})
                    pass

            elif int(tipo) == 1: #Apoio Direto
                form = OrdemServicoDireto(request.POST, classe=classe)
                if form.is_valid():
                    instance = form.save(commit=False)
                    
                    instance.abertura_os_date = datetime.now()
                    nr_os_temp = generateOSNr(tipo, classe)
                    instance.nr_os = nr_os_temp
                    instance.tipo = tipo
                    instance.status = 10
                    instance.classe = classe
                    
                    instance.ch_classe_id = request.user.id
                    instance.ch_cp_id = getIDChCP()
                    instance.cmt_pel_id = getIDCmtPel(classe)
                    
                    saved_form = instance.save()
                    form.save_m2m()
                    str_success = "OS nr: " + str(nr_os_temp) + ", de tipo: " + str(TIPO_CHOICES[int(tipo)][1]) + " e de classe: " + str(classe)
                    return render(request, 'ordemDeServico/ok.html', {'mensagem':str_success})
                else:
                    #TODO redirect pra página de falha em adicionar
                    #return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Salvar', 'classe':classe})
                    pass
            
            elif int(tipo) == 2: #Apoio em Suprimento
                form = OrdemServicoSuprimento(request.POST, classe=classe)
                if form.is_valid():
                    instance = form.save(commit=False)
                    
                    instance.abertura_os_date = datetime.now()
                    nr_os_temp = generateOSNr(tipo, classe)
                    instance.nr_os = nr_os_temp
                    instance.tipo = tipo
                    instance.status = 10
                    instance.classe = classe
                    
                    instance.ch_classe_id = request.user.id
                    instance.ch_cp_id = getIDChCP()
                    instance.cmt_pel_id = getIDCmtPel(classe)

                    saved_form = instance.save()
                    form.save_m2m()
                    str_success = "OS nr: " + str(nr_os_temp) + ", de tipo: " + str(TIPO_CHOICES[int(tipo)][1]) + " e de classe: " + str(classe)
                    return render(request, 'ordemDeServico/ok.html', {'mensagem':str_success})
                else:
                    #TODO redirect pra página de falha em adicionar
                    #return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Salvar', 'classe':classe})
                    pass
            else:
                form = None
        else:
            if int(tipo) == 0:
                form = OrdemServicoConjunto(classe=classe)
            elif int(tipo) == 1:
                form = OrdemServicoDireto(classe=classe)
            elif int(tipo) == 2:
                form = OrdemServicoSuprimento(classe=classe)
            else:
                form = None

        return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Salvar', 'classe':classe})
    else:
        return render(request, "ordemDeServico/semPermissao.html")


@meu_login_required
def caixadeentrada(request):
    alldata = OrdemDeServico.objects.all()
    funcao = getFuncaoMilitar(request.user)
    sistema = Sistema.objects.all().values()
    classe = funcao.values('classe')
    nome_funcao= funcao.values('nome_funcao')

    permissions = [[x['classe'], y['nome_funcao']] for (x, y) in list(zip(list(classe), list(nome_funcao)))]

    data = []
    if funcao:

        #CADA MILITAR TEM ACESSO APENAS A OS DA SUA CLASSE,
        #PORÉM APENAS QUANDO O STATUS FOR COMPATIVEL COM SUA FUNCAO
        for p in permissions:
            if p[1] == 1: #CH CP
                data = data + list(alldata.filter(status__in=[1, 10]).values())
            elif p[1] == 3: #CMT PEL
                data = data + list(alldata.filter(classe=p[0], status__in=[2, 3, 4, 5, 6, 7, 8]).values())
            elif p[1] == 4: #CH CL
                data = data + list(alldata.filter(classe=p[0], status=9).values())
       
        for p in data:
          if p['sistema_id']:
              j=int(p['sistema_id'])
              p['sistema_id']=sistema[j-1]['descricao']
          j=int(p['status'])
          p['status']=STATUS_CHOICES[j-1][1]
          j=int(p['tipo'])
          p['tipo']=TIPO_CHOICES[j-1][1]
        data.sort(key=lambda x: x['abertura_os_date'], reverse=True)
        data.sort(key=lambda x: x['status'], reverse=False)
        return render(request, 'ordemDeServico/caixa.html', {'data': data})
    return redirect('/login')



@meu_login_required
def visualizarOS(request, os_id):
    os = getOSfromId(os_id)
    permissions = getPermissions(request.user)
    ret_os_classe = list(os.values('classe'))[0]['classe']
    status_os = list(os.values('status'))[0]['status']
    print_value = model_to_dict(os.get())

    if request.method == 'POST':
        print(permissions)
        print(request.POST)
        chaves = request.POST.keys()
        print(chaves)
        if('medidas_corretivas' in chaves): #TEST NAO
            medidas_corretivas_os = list(os.values('medidas_corretivas'))[0]['medidas_corretivas']
            medidas_corretivas = medidas_corretivas_os + request.POST['medidas_corretivas'] + "; " 
            form = MedidasCorretivas({'medidas_corretivas': medidas_corretivas}, instance = os.get())
            if(form.is_valid()):
                form.save()
                if(status_os == 7):
                    incrementarStatus(os, 7)
                return render(request, 'ordemDeServico/ok.html')
            else:
                #TODO mudar página de redirecionamento qnd der erro
                return redirect("/")
        elif('quant_homens' in chaves): #ND30
            form = OrdemServicoConjuntoFinal30(request.POST, instance = os.get(), classe=ret_os_classe)
            if(form.is_valid()):
                form.save()
                incrementarStatus(os, 8)
                return render(request, 'ordemDeServico/ok.html')
            else:
                #TODO mudar página de redirecionamento qnd der erro
                return redirect("/")
        elif('prestador_servico' in chaves): #ND39
            form = OrdemServicoConjuntoFinal39(request.POST, instance = os.get(), classe=ret_os_classe)
            if(form.is_valid()):
                form.save()
                incrementarStatus(os, 8)
                return render(request, 'ordemDeServico/ok.html')
            else:
                #TODO mudar página de redirecionamento qnd der erro
                return redirect("/")
        else:
            if os:

                if(status_os in [1, 10]):
                    #CHCP
                    p = [x[1] for x in permissions]
                    if 1 in p:
                        print("STATUS " + str(status_os))
                        incrementarStatus(os, status_os)
                        return render(request, 'ordemDeServico/ok.html',{"mensagem":"Seu ciente foi registrado"})
                    else:
                        return render(request, "ordemDeServico/semPermissao.html")
                elif(status_os in [2, 3, 4, 5, 6]):
                    #CMT PEL
                    if [ret_os_classe, 3] in permissions:
                        print("STATUS " + str(status_os))
                        incrementarStatus(os, status_os)
                    else:
                        return render(request, "ordemDeServico/semPermissao.html")
                elif(status_os in [7, 8]):
                    #CMT PEL
                    if [ret_os_classe, 3] in permissions:
                        sucesso = request.POST.get('testesucesso')
                        print(sucesso)
                        if(sucesso == 'sim'): #SIM 
                            nd_os = list(os.values('nd'))[0]['nd']
                            if(nd_os == 30):
                                form_consulta = OrdemServicoConjuntoFinal30(classe=ret_os_classe)
                            else:
                                form_consulta = OrdemServicoConjuntoFinal39(classe=ret_os_classe)
                            submit = '<button name="status" value="' + str(status_os) + '" type="submit">Salvar</button>'
                            return render(request, 'ordemDeServico/visualizar.html', {'ordemDeServico': print_value, 'form_consulta': form_consulta, 'submit': submit})
                            print("SIM")
                        else:
                            print("NAO")
                            medidas_corretivas_os = list(os.values('medidas_corretivas'))[0]['medidas_corretivas']
                            pre_message = "Medidas corretivas já aplicadas:<br>" + medidas_corretivas_os + "<br>"
                            form_consulta = MedidasCorretivas() #FORM CIENTE
                            submit = '<button name="status" value="' + str(status_os) + '" type="submit">Salvar</button>'
                            return render(request, 'ordemDeServico/visualizar.html', {'ordemDeServico': print_value, 'form_consulta': form_consulta, 'submit': submit, 'pre_form_message': pre_message})
                            #if(status_os == 7):
                            #    incrementarStatus(os, 7)
                        print("STATUS " + str(status_os))

                    else:
                        return render(request, "ordemDeServico/semPermissao.html")

                elif(status_os in [9]):
                    #CHCL
                    if [ret_os_classe, 4] in permissions:
                        incrementarStatus(os, 9)
                    else:
                        return render(request, "ordemDeServico/semPermissao.html")
                    print("STATUS " + str(status_os))

                else:
                    return render(request, "ordemDeServico/semPermissao.html")

            return render(request, 'ordemDeServico/ok.html')
    else:
        funcao = getFuncaoMilitar(request.user)
        classe = funcao.values('classe')
        nome_funcao= funcao.values('nome_funcao')

        print(permissions)

        classe = {x['classe'] for x in list(classe)}
        nome_funcao = {x['nome_funcao'] for x in list(nome_funcao)}
        if os:

            # sem função
            if nome_funcao and (0 not in nome_funcao or len(nome_funcao)!=1):
                #CRIAR FORM VAZIO
                form_consulta = '' #FORM CIENTE
                submit = '' #HTMLSUBMIT

                ret_os_status = print_value['status']
                print_value = os_print(print_value)


                # ch cp ou adj cp
                if (1 in nome_funcao or 2 in nome_funcao):
                    # ch cp
                    if (1 in nome_funcao):
                        if(ret_os_status == 1): #AGUARDANDO CIENTE
                            submit = '<button name="status" value="1" type="submit">Ciente</button>'

                        elif(ret_os_status == 10): #AGUARDANDO CIENTE - FECHAR
                            submit = '<button name="status" value="10" type="submit">Ciente</button>'

                    return render(request, 'ordemDeServico/visualizar.html', {'ordemDeServico': print_value, 'form_consulta': form_consulta, 'submit': submit})
                # cmt pel ou ch classe
                else:
                    print("CMT PEL / CH CL")
                    ret_os_classe = print_value['Classe']

                    if (ret_os_classe in classe):
                        # cmt pel
                        if ([ret_os_classe, 3] in permissions):
                            print("CMT PEL")
                            if(ret_os_status == 2): #AGUARDANDO INSPEÇÃO
                                submit = '<button name="status" value="2" type="submit">Iniciar inspeção</button>'

                            elif(ret_os_status == 3): #REALIZANDO INSPEÇÃO
                                submit = '<button name="status" value="3" type="submit">Finalizar inspeção</button>'

                            elif(ret_os_status == 4): #AGUARDANDO MANUTENÇÃO
                                submit = '<button name="status" value="4" type="submit">Iniciar manutenção</button>'

                            elif(ret_os_status == 5): #EM MANUTENÇÃO
                                submit = '<button name="status" value="5" type="submit">Finalizar manutenção</button>'

                            elif(ret_os_status == 6): #AGUARDANDO TESTES
                                submit = '<button name="status" value="6" type="submit">Iniciar testes</button>'

                            elif(ret_os_status == 7): #TESTES EM EXECUÇÃO
                                submit = '<p>Passou no teste?</p><br><button name="testesucesso" value="sim" type="submit">Sim</button><button name="testesucesso" value="nao" type="submit">Não</button>'

                            elif(ret_os_status == 8): #REMANUTENÇÃO
                                form_consulta = '' #FORM CIENTE
                                submit = '<p>Passou no teste?</p><br><button name="testesucesso" value="sim" type="submit">Sim</button><button name="testesucesso" value="nao" type="submit">Não</button>'

                        # ch classe
                        elif ([ret_os_classe, 4] in permissions):
                            print("CH CL")
                            if(ret_os_status == 9): #REMANUTENÇÃO
                                form_consulta = '' #FORM CIENTE
                                submit = '<button name="status" value="9" type="submit">Enviar</button>'

                        return render(request, 'ordemDeServico/visualizar.html', {'ordemDeServico': print_value, 'form_consulta': form_consulta, 'submit': submit})

        return redirect("/ordemservico/todo")

@meu_login_required
def consultarOS(request):
    sistema = Sistema.objects.all().values()
    if request.method == 'POST':
        form = ConsultaOrdemServico(request.POST)
        if form.is_valid():
            result_dict = {}
            data_from_form = form.cleaned_data
            for entry in data_from_form.keys():
                if data_from_form[entry] != '' and data_from_form[entry] != None:
                    result_dict[entry] = data_from_form[entry]
            if result_dict:
                data = OrdemDeServico.objects.filter(**result_dict).order_by('status','-abertura_os_date').values()
            else:
                data = OrdemDeServico.objects.all().order_by('status','-abertura_os_date').values()
        else:
            pass
    
    else:
        form = ConsultaOrdemServico()
        data = {}
    for p in data:
       if p['sistema_id']:
          j=int(p['sistema_id']) - 1
          p['sistema_id']=sistema[j]['descricao']
       j=int(p['status'])
       p['status']=STATUS_CHOICES[j-1][1]
       j=int(p['tipo'])
       p['tipo']=TIPO_CHOICES[j-1][1]
    return render(request, 'ordemDeServico/consulta.html', {'form_consulta': form, 'data': data})

def os_print(db_dict):

    sistema = Sistema.objects.all().values()
    om = OM.objects.all().values()

    os_names = OrderedDict()
    os_names['id'] = 'ID'
    os_names['prioridade'] = 'Prioridade'
    os_names['nr_os'] = 'Nr OS'
    os_names['status'] = 'Status'
    os_names['classe'] = 'Classe'
    os_names['tipo'] = 'Tipo'
    os_names['abertura_os_date'] = 'Data de abertura'
    os_names['pit'] = 'PIT'
    os_names['nd'] = 'ND'
    os_names['guia_recolhimento'] = 'Guia de recolhimento'
    os_names['ordem_recolhimento'] = 'Ordem de Recolhimento'
    os_names['num_diex'] = 'Nr DIEX'
    os_names['desc_material'] = 'Descrição do material'
    os_names['quantidade'] = 'Quantidade'
    os_names['om_requerente'] = 'OM requerente'
    os_names['serv_realizado'] = 'Serviço realizado'
    os_names['subsistemas_manutenidos'] = 'Subsistemas manutenidos'
    os_names['quant_homens'] = 'Quantidade de homens'
    os_names['custo_total'] = 'Custo total (em R$)'
    os_names['medidas_corretivas'] = 'Medidas corretivas'
    os_names['aguardando_inspecao_date'] = 'Data de aguardando inspeção'
    os_names['realizando_inspecao_date'] = 'Data de realizando inspeção'
    os_names['aguardando_manutencao_date'] = 'Data de aguardando manutenção'
    os_names['em_manutencao_date'] = 'Data de ínicio de manutenção'
    os_names['realizacao_date'] = 'Data de realização'
    os_names['remanutencao_date'] = 'Data de remanutenção'
    os_names['aguardando_testes_date'] = 'Data de aguardando testes'
    os_names['testes_em_execucao_date'] = 'Data de testes em execução'
    os_names['aguardando_remessa_date'] = 'Data de aguardando remessa'
    os_names['aguardando_ciente_date'] = 'Data de aguardando ciente'
    os_names['fechada_sem_ciente_date'] = 'Data de fechamento sem ciente'
    os_names['fechada_arquivar_date'] = 'Data de fechamento/arquivamento'
    os_names['prestador_servico'] = 'Prestador de serviço'
    os_names['suprimento_aplicado'] = 'Suprimento aplicado'
    os_names['sistema'] = 'Sistema'
    os_names['tempo'] = 'Tempo (em horas trabalhadas)'
    os_names['motivo'] = 'Motivo'
    os_names['ch_classe'] = 'Chefe de classe'
    os_names['cmt_pel'] = 'Cmt Pel'
    os_names['ch_cp'] = 'Chefe de CP'

    print_dict = OrderedDict()



    for key, v in os_names.items():
        if db_dict[key] and key is not 'id':
            if key == 'pit':
                value = "Sim" if db_dict[key] == True else "Não"
            elif key == 'tipo':
                if db_dict[key] == 0:
                    value = "Apoio em conjunto"
                elif db_dict[key] == 1:
                    value = "Apoio direto"
                else:
                    value = "Apoio em suprimento"
            elif key == 'ch_classe' or key == 'cmt_pel' or  key == 'ch_cp':
               value = InformacaoMilitar.objects.get(user=db_dict[key]).posto + ' ' + InformacaoMilitar.objects.get(user=db_dict[key]).nome_guerra
            elif key == 'sistema':
               j=int(db_dict['sistema'])
               value = sistema[j-1]['descricao']
            elif key =='om_requerente':
               j=int(db_dict['om_requerente'])
               value = om[j-1]['nome']
            elif key == 'status':
               j=int(db_dict['status'])
               value = STATUS_CHOICES[j-1][1]
            else:
                value = db_dict[key]
            print_dict[v] = value

    return print_dict

def todo(request):
    return render(request, 'ordemDeServico/todo.html')

