from django.shortcuts import render, redirect
from .forms import OrdemServico
from .models import Sistema #mudar OrdemDeServico

# Create your views here.
def criarordemservico(request):
    if request.method == 'POST':
        form = OrdemServico(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.nr_os = 0
            instance.tipo = 0
            instance.status = 9
            instance.nd = 0
            instance.classe = 5
            instance.ch_cp_id = 1
            instance.ch_classe_id = 1
            instance.cmt_pel_id = 1
            saved_form = instance.save()
            form.save_m2m()
            print(saved_form)
            #redirect
        else:
            print(form.errors)
    else:
        form = OrdemServico()
    return render(request, 'ordemDeServico/form.html', {'form': form, 'submitValue': 'Salvar'})


def caixadeentrada(request):
	data = Sistema.objects.all().filter(classe=7).values()  #foi feito apenas para fins de teste. mudar para OrdemDeServico
	return render(request, 'ordemDeServico/caixa_test.html', {'data': data})
