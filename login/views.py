from django.shortcuts import render, redirect
from .forms import Login

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        print("funciona")
        return redirect('/admin')
    else:
        form = Login()

    return render(request, 'login/form.html', {'form': form})
