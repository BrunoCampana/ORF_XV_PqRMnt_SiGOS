from ordemDeServico.models import Sistema, OrdemDeServico
from login.models import Funcao

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

