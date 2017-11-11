from django import forms


class Login(forms.Form):
    username = forms.CharField(label='Usuário', error_messages={'required': 'Usuário não informado'})
    password = forms.CharField(label='Senha', widget=forms.PasswordInput,
                               error_messages={'required': 'Senha não informada'})

class Mudar_senha(forms.Form):
	senha = forms.CharField(label='Senha', widget=forms.PasswordInput, error_messages={'required': 'Senha não informada'})
	novaSenha = forms.CharField(label='Nova senha', widget=forms.PasswordInput, error_messages={'required': 'Nova senha não informada'})
	cnovaSenha = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput, error_messages={'required': 'Confirmação de nova senha não informada'})
