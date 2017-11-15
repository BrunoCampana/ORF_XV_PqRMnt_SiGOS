from ordemDeServico.models import Sistema, OrdemDeServico
from login.models import Funcao
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def getFuncaoMilitar(user):
    user_id = user.id
    return Funcao.objects.filter(militar=user_id).values()

def getIDCmtPel(classe):
    return Funcao.objects.filter(classe=classe, nome_funcao=3).values()[0]['militar_id']

def getIDChCP():
    return Funcao.objects.filter(nome_funcao=1).values()[0]['militar_id']

def getOSfromId(os_id):
    print("GET OS ID")
    #return OrdemDeServico.objects.filter(id=os_id)
    return OrdemDeServico.objects.filter(id=os_id)

def generateOSNr(tipo, classe):
    return 0

def meu_login_required(function=None, login_url=None):
	actual_decorator = login_required(function=function, redirect_field_name=None, login_url=login_url)
	return actual_decorator

def meu_anonymous_required(func):
	def func_wrapper(request):
		if not request.user.is_authenticated():
			return func(request)
		else:
			return redirect('/')
	return func_wrapper

def meu_mudar_senha(form, request):
	username = request.user.get_username()
	password = form.cleaned_data['novaSenha']

	user = User.objects.get(username__exact=request.user.get_username())
	user.set_password(form.cleaned_data['novaSenha'])
	user.save()	

	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)

def incrementarStatus(os, status):
    print("AINDA NÃO TA INCREMENTANDO!!!")
    print("FAZER ISSO LOGO!!!")
    print(type(os))
    setattr(os, 'status', status+1)
    os.save()
