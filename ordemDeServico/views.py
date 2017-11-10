from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import OrdemServico, Tipo
from .models import Sistema, OrdemDeServico
from login.models import Funcao


# Create your views here.
def escolhertipoOS(request):
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

# def visualizarOS(request, os_id):
#     print(os_id)
#     return redirect("/login")
#

def getFuncaoMilitar(user):
    user_id = user.id
    return Funcao.objects.filter(militar=user_id).values()


def getOSfromId(os_id):
    return OrdemDeServico.objects.filter(id=os_id)


def visualizarOS(request, os_id):
    print(os_id)
    funcao = getFuncaoMilitar(request.user)
    print(funcao)
    return redirect("/login")
'''
def visualizarOS(request, os_id):
    if request.method == 'POST':
        funcao = getFuncaoMilitar(request.user)
        classe = funcao["classe"]
        nome_func = funcao["nome_func"]
        os_id = request.POST.get('id')
        os = getOSfromId(os_id)
        if os:
            # sem função
            if nome_func != 0:
                # ch cp ou adj cp
                if (nome_func == 1 or nome_func == 2):
                    # fazer parte de edição da os (cientes, fechamento, etc)
                    return render(pagina)
                else:
                    if (classe == os["classe"]):
                        # fazer parte de edição da os (cientes, fechamento, etc)
                        return render(pagina)
    
    return redirect('/ordemservico/caixa')
'''

def generateOSNr():
    return 0
