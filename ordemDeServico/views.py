from django.shortcuts import render, redirect
from .forms import OrdemServico

# Create your views here.
def ordemservico(request):
    if request.method == 'POST':
        form = OrdemServico(request.POST)

        #if form.is_valid():
        saved_form = form.save()
        print(saved_form)
            
    else:
        form = OrdemServico()
    return render(request, 'login/form.html', {'form': form, 'submitValue': 'Salvar'})
