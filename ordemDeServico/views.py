from django.shortcuts import render, redirect
from .forms import OrdemServico

# Create your views here.
def ordemservico(request):
	form = OrdemServico()
	return render(request, 'login/form.html', {'form': form, 'submitValue': 'Salvar'})
