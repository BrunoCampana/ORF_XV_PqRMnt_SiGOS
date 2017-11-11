from django.shortcuts import render, redirect
from .forms import Login
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from src.utils import getFuncaoMilitar


# Create your views here.

def login(request):
    if request.method == 'POST':
        form = Login(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])

            if user is not None:
                if user.is_superuser:
                    auth_login(request, user)
                    return redirect('/admin')

                funcao = getFuncaoMilitar(user)
                
                if funcao:
                    auth_login(request, user)
                    print(request)
                    return redirect('/ordemservico/caixa')
                else:
                    #TODO CRIAR NOVA PAGINA PARA SER DIRECIONADO
                    form.add_error(None, 'Usuário sem função. Acesso negado')
                    return render(request, 'login/form.html', {'form': form})

            else:
                form.add_error(None, 'Usuário ou senha incorretos.')
    else:
        form = Login()

    return render(request, 'login/form.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('/login')
