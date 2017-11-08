from django import forms

class Login(forms.Form):
    username = forms.CharField(label='Usuário', error_messages={'required': 'Usuário não informado'})
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, error_messages={'required': 'Senha não informada'})

