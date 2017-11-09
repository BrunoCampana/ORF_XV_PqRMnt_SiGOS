from django.shortcuts import render, redirect
from .forms import OrdemServico
from .models import Sistema, OrdemDeServico
from login.models import Funcao

# Create your views here.
def criarordemservico(request):
    if request.method == 'POST':
        form = OrdemServico(request.POST)
        if form.is_valid():
            saved_form = form.save()
            print(saved_form)
            #redirect
        else:
            print('nope')
    else:
        form = OrdemServico()
    return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Salvar'})


def caixadeentrada(request):
	for e in Sistema.objects.all().filter(classe=7).values():  #foi feito apenas para fins de teste. mudar para OrdemDeServico
		print(e["descricao"])
	return redirect('/login')
'''
def visualizarOS(request):
    if request.method == 'POST':
        funcao = getFuncaoMilitar(request.user)
        classe = funcao["classe"]
        nome_func = funcao["nome_func"]
        os_id = request.POST.get('id')
        os = getOSfromId(os_id)
        if os:
            #sem função
            if nome_func != 0:
                #ch cp ou adj cp
                if nome_func == 1 || nome_func == 2:
                    #fazer parte de edição da os (cientes, fechamento, etc)
                    return render(pagina)
                else:
                    if classe == os["classe"]:
                        #fazer parte de edição da os (cientes, fechamento, etc)
                        return render(pagina)
    
    return redirect('/ordemservico/caixa')
'''
def getFuncaoMilitar(user)
        user_id = user.id
        return Funcao.object.filter(militar=user_id).values()

def getOSfromId(os_id)
        return OrdemDeServico.objects.filter(id=os_id)
