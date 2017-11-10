from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import OrdemServico, ConsultaOrdemServico, Tipo
from .models import Sistema, OrdemDeServico
from login.models import Funcao


# Create your views here.
def escolhertipoOS(request):
    funcao = getFuncaoMilitar(request.user)
    nome_funcao= funcao.values('nome_funcao')
    nome_funcao = {x['nome_funcao'] for x in list(nome_funcao)}
    if 4 not in nome_funcao:
        return render(request, "ordemDeServico/semPermissao.html")

    if request.method == 'POST':
        form = Tipo(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['tipo']
            return redirect("/ordemservico/criar/" + tipo)
        else:
            print(form.errors)
    else:
        form = Tipo()
    return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Abrir'})


def criarordemservico(request, tipo):
    funcao = getFuncaoMilitar(request.user)
    #classe = funcao.values('classe')
    classe = funcao[0]['classe']
    print(classe)

    if request.method == 'POST':
        form = OrdemServico(request.POST, classe=classe)
        if form.is_valid():
            instance = form.save(commit=False)
            
            #TODO preencher
            instance.nr_os = generateOSNr()
            instance.tipo = tipo
            instance.status = 1
            instance.nd = 0
            instance.classe = 5
            instance.ch_cp_id = 1
            instance.ch_classe_id = 1
            instance.cmt_pel_id = 1
            
            saved_form = instance.save()
            form.save_m2m()
            print(saved_form)
            # redirect
        else:
            print(form.errors)
    else:
        form = OrdemServico(classe=classe)

    return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Salvar', 'classe':classe})


def caixadeentrada(request):
    alldata = OrdemDeServico.objects.all()
    funcao = getFuncaoMilitar(request.user)
    if funcao:
        classe = int(funcao[0]["classe"])
        print(classe)
        if classe != 0:
	    #cada militar ter acesso apenas a sua classe
            data = alldata.filter(classe=classe, status__gte=2, status__lte=8).values()  # foi feito apenas para fins de teste. mudar para OrdemDeServico
            return render(request, 'ordemDeServico/caixa.html', {'data': data})
        #CHCP tem acesso a todas classes
        data = alldata.filter(Q(status=1) | Q(status=10)).values()  # foi feito apenas para fins de teste. mudar para OrdemDeServico
      
     #   data = alldata.values()
        return render(request, 'ordemDeServico/caixa.html', {'data': data})

    return redirect('/login')


def getFuncaoMilitar(user):
    user_id = user.id
    return Funcao.objects.all().filter(militar=user_id).values()


def getOSfromId(os_id):
    print("GET OS ID")
    return OrdemDeServico.objects.filter(id=os_id)
    #return Sistema.objects.filter(id=os_id)


def visualizarOS(request, os_id):
    funcao = getFuncaoMilitar(request.user)
    print(funcao)
    classe = funcao.values('classe')
    nome_funcao= funcao.values('nome_funcao')

    permissions = [[x['classe'], y['nome_funcao']] for (x, y) in list(zip(list(classe), list(nome_funcao)))]
    
    classe = {x['classe'] for x in list(classe)}
    nome_funcao = {x['nome_funcao'] for x in list(nome_funcao)}

    print(permissions)
    print(classe)
    print(nome_funcao)
    os = getOSfromId(os_id)
    if os:

        # sem função
        if nome_funcao and (0 not in nome_funcao or len(nome_funcao)!=1):
            print_value = list(os.values())[0]
            ret_os_status = list(os.values('status'))[0]['status']

            # ch cp ou adj cp
            if (1 in nome_funcao or 2 in nome_funcao):
                # ch cp
                if (1 in nome_funcao):
                    if(ret_os_status == 1): #AGUARDANDO CIENTE
                        form_consulta = '' # FORMAGCIENTE
                        submit = '' #HTMLSUBMIT

                    elif(ret_os_status == 10): #AGUARDANDO CIENTE - FECHAR
                        form_consulta = '' #FORMAGCIENTE
                        submit = '' #HTMLSUBMIT

                    else:
                        #CRIAR FORM VAZIO
                        form_consulta = '' #FORMAGCIENTE
                        submit = '' #HTMLSUBMIT

                # adj cp

                else:
                    #CRIAR FORM VAZIO
                    form_consulta = '' #FORMAGCIENTE
                    submit = '' #HTMLSUBMIT

                return render(request, 'ordemDeServico/visualizar.html', {'ordemDeServico': print_value, 'form_consulta': form_colsulta, 'submit': submit})
            # cmt pel ou ch classe
            else:
                ret_os_classe = list(os.values('classe'))[0]['classe']
                if (ret_os_classe in classe):
                    # cmt pel
                    if (3 in nome_funcao):
                        if(ret_os_status == 2): #AGUARDANDO INSPEÇÃO
                            form_consulta = '' #FORMAGCIENTE
                            submit = '' #HTMLSUBMIT

                        elif(ret_os_status == 3): #REALIZANDO INSPEÇÃO
                            form_consulta = '' #FORMAGCIENTE
                            submit = '' #HTMLSUBMIT

                        elif(ret_os_status == 4): #AGUARDANDO MANUTENÇÃO
                            form_consulta = '' #FORMAGCIENTE
                            submit = '' #HTMLSUBMIT

                        elif(ret_os_status == 5): #EM MANUTENÇÃO
                            form_consulta = '' #FORMAGCIENTE
                            submit = '' #HTMLSUBMIT

                        elif(ret_os_status == 6): #AGUARDANDO TESTES
                            form_consulta = '' #FORMAGCIENTE
                            submit = '' #HTMLSUBMIT

                        elif(ret_os_status == 7): #TESTES EM EXECUÇÃO
                            form_consulta = '' #FORMAGCIENTE
                            submit = '' #HTMLSUBMIT

                        elif(ret_os_status == 8): #REMANUTENÇÃO
                            form_consulta = '' #FORMAGCIENTE
                            submit = '' #HTMLSUBMIT

                        else:
                            #CRIAR FORM VAZIO
                            form_consulta = '' #FORMAGCIENTE
                            submit = '' #HTMLSUBMIT

                    # ch classe
                    else:
                        if(ret_os_status == 9): #REMANUTENÇÃO
                            form_consulta = '' #FORMAGCIENTE
                            submit = '' #HTMLSUBMIT

                        else:
                            #CRIAR FORM VAZIO
                            form_consulta = '' #FORMAGCIENTE
                            submit = '' #HTMLSUBMIT

                    return render(request, 'ordemDeServico/visualizar.html', {'ordemDeServico': print_value, 'form_consulta': form_consulta, 'submit': submit})


    return redirect("/ordemservico/caixa")


def generateOSNr():
    return 0

def consultarOS(request):
    if request.method == 'POST':
        form = ConsultaOrdemServico(request.POST)
        form.is_valid()
        #result = Sistema.objects.filter(**form.cleaned_data).values()
        result = OrdemDeServico.objects.filter(**form.cleaned_data).values()
    
    else:
        form = ConsultaOrdemServico()
        result = {}
    
    return render(request, 'ordemDeServico/consulta.html', {'form_consulta': form, 'data': result})
