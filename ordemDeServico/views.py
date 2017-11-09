from django.shortcuts import render, redirect
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
    if request.method == 'POST':
        form = OrdemServico(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.nr_os = 0
            instance.tipo = tipo
            instance.status = 9
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
        form = OrdemServico()

    return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Salvar'})


def caixadeentrada(request):
    if request.method == 'POST':
        print("previs")
        print(request.POST)
        return redirect("/ordemservico/visualizar/")
    else:
        data = Sistema.objects.all().filter(
            classe=7).values()  # foi feito apenas para fins de teste. mudar para OrdemDeServico
        return render(request, 'ordemDeServico/caixa_test.html', {'data': data})


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
