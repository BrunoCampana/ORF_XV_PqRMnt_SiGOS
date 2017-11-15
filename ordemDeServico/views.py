from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import OrdemServicoConjunto, OrdemServicoDireto, OrdemServicoSuprimento, ConsultaOrdemServico, Tipo
from .models import Sistema, OrdemDeServico
from login.models import Funcao
from datetime import datetime, timedelta
from src.utils import getFuncaoMilitar, getIDCmtPel, getIDChCP, getOSfromId, generateOSNr, meu_login_required, incrementarStatus

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
                form = OrdemServicoConjunto(request.POST)
                if form.is_valid():
                    instance = form.save(commit=False)
                    
                    #TODO preencher
                    instance.abertura_os_date = datetime.now() - timedelta(hours=4)
                    instance.nr_os = generateOSNr(tipo, classe)
                    instance.tipo = tipo
                    instance.status = 1
                    instance.classe = classe
                    
                    instance.ch_classe_id = request.user.id
                    instance.ch_cp_id = getIDChCP()
                    instance.cmt_pel_id = getIDCmtPel(classe)
                    
                    saved_form = instance.save()
                    form.save_m2m()
                    #TODO redirect pra página de adicionado corretamente
                else:
                    #TODO redirect pra página de falha em adicionar
                    #return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Salvar', 'classe':classe})
                    pass

            elif int(tipo) == 1: #Apoio Direto
                form = OrdemServicoDireto(request.POST, classe=classe)
                if form.is_valid():
                    instance = form.save(commit=False)
                    
                    #TODO preencher
                    instance.abertura_os_date = datetime.now() - timedelta(hours=4)
                    instance.nr_os = generateOSNr(tipo, classe)
                    instance.tipo = tipo
                    instance.status = 10
                    instance.classe = classe
                    
                    instance.ch_classe_id = request.user.id
                    instance.ch_cp_id = getIDChCP()
                    instance.cmt_pel_id = getIDCmtPel(classe)
                    
                    saved_form = instance.save()
                    form.save_m2m()
                    #TODO redirect pra página de adicionado corretamente
                else:
                    #TODO redirect pra página de falha em adicionar
                    #return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Salvar', 'classe':classe})
                    pass
            
            elif int(tipo) == 2: #Apoio em Suprimento
                form = OrdemServicoSuprimento(request.POST, classe=classe)
                if form.is_valid():
                    instance = form.save(commit=False)
                    
                    #TODO preencher
                    instance.abertura_os_date = datetime.now() - timedelta(hours=4)
                    instance.nr_os = generateOSNr(tipo, classe)
                    instance.tipo = tipo
                    instance.status = 10
                    instance.classe = classe
                    
                    instance.ch_classe_id = request.user.id
                    instance.ch_cp_id = getIDChCP()
                    instance.cmt_pel_id = getIDCmtPel(classe)

                    saved_form = instance.save()
                    form.save_m2m()
                    #TODO redirect pra página de adicionado corretamente
                else:
                    #TODO redirect pra página de falha em adicionar
                    #return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Salvar', 'classe':classe})
                    pass
            else:
                form = None
        else:
            if int(tipo) == 0:
                form = OrdemServicoConjunto()
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
    if funcao:
        classe = int(funcao[0]["classe"])
        nome_func = int(funcao[0]["nome_funcao"])
        if nome_func == 1:
	    #CHCP tem acesso a todas classes
            data = alldata.filter(Q(status=1) | Q(status=10)).order_by('status','-abertura_os_date').values()
            print(data)
            return render(request, 'ordemDeServico/caixa.html', {'data': data})
        if nome_func == 3:
	    #CMTPel, acesso apenas a sua classe
            data = alldata.filter(classe=classe, status__gte=2, status__lte=8).order_by('status', '-abertura_os_date').values()
            return render(request, 'ordemDeServico/caixa.html', {'data': data})
        if nome_func == 4:
            #CHClasse
            data = alldata.filter(classe=classe, status=10).order_by('status', '-abertura_os_date').values()
            return render(request, 'ordemDeServico/caixa.html', {'data': data})
    return redirect('/login')

@meu_login_required
def caixadeentradatest(request):
    print("TEST")
    alldata = OrdemDeServico.objects.all()
    funcao = getFuncaoMilitar(request.user)

    classe = funcao.values('classe')
    nome_funcao= funcao.values('nome_funcao')

    permissions = [[x['classe'], y['nome_funcao']] for (x, y) in list(zip(list(classe), list(nome_funcao)))]
    
    print(permissions)
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
    
    data.sort(key=lambda x: x['abertura_os_date'], reverse=True)
    data.sort(key=lambda x: x['status'], reverse=False)
    print(data[0])
    return render(request, 'ordemDeServico/caixa.html', {'data': data})
    #return redirect('/ordemservico/todo/cxentradasemfuncao')



@meu_login_required
def visualizarOS(request, os_id):
    os = getOSfromId(os_id)
    if request.method == 'POST':
        #TODO TRATAR RECEBIMENTO DOS FORMS
        status_os = list(os.values('status'))[0]['status']
        if(status_os in [1, 2, 3, 4, 5, 6, 10]):
            incrementarStatus(os, status_os)
        elif(status_os in [7, 8]):
            sucesso = request.POST.get('testesucesso')
            if(sucesso == 'sim'): #SIM 
                if(status_os == 7):
                    incrementarStatus(os, status_os)
                incrementarStatus(os, status_os)
                #else: #NÃO
                    
        return redirect("/ordemservico/todo")
    else:
        funcao = getFuncaoMilitar(request.user)
        classe = funcao.values('classe')
        nome_funcao= funcao.values('nome_funcao')

        permissions = [[x['classe'], y['nome_funcao']] for (x, y) in list(zip(list(classe), list(nome_funcao)))]
        
        print(permissions)

        classe = {x['classe'] for x in list(classe)}
        nome_funcao = {x['nome_funcao'] for x in list(nome_funcao)}
        if os:

            # sem função
            if nome_funcao and (0 not in nome_funcao or len(nome_funcao)!=1):
                #CRIAR FORM VAZIO
                form_consulta = '' #FORM CIENTE
                submit = '' #HTMLSUBMIT

                print_value = list(os.values())[0]
                ret_os_status = list(os.values('status'))[0]['status']

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
                    ret_os_classe = list(os.values('classe'))[0]['classe']

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
                                submit = '<button name="status" value="7" type="submit">Finalizar testes</button>'

                            elif(ret_os_status == 8): #REMANUTENÇÃO
                                form_consulta = '' #FORM CIENTE
                                submit = '<button name="testesuccesso" value="sim" type="submit">Sim</button><button name="testesucesso" value="nao" type="submit">Não</button>'

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
    if request.method == 'POST':
        form = ConsultaOrdemServico(request.POST)
        form.is_valid()
        data = OrdemDeServico.objects.filter(**form.cleaned_data).order_by('status','-abertura_os_date').values()
    
    else:
        form = ConsultaOrdemServico()
        data = {}
    
    return render(request, 'ordemDeServico/consulta.html', {'form_consulta': form, 'data': data})

def todo(request):
    return render(request, 'ordemDeServico/todo.html')
