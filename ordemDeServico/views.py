from django.shortcuts import render, redirect
from .forms import OrdemServico
from .models import Sistema #mudar OrdemDeServico

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
