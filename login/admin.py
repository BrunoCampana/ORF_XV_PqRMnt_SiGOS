from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from login.models import InformacaoMilitar, Funcao

# Register your models here.

class InfoMilInline(admin.StackedInline):
    model = InformacaoMilitar
    can_delete = False
    verbose_name_plural = 'Informação Militar'

class UserAdmin(BaseUserAdmin):
    inlines = (InfoMilInline, )

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
admin.site.register(Funcao)

