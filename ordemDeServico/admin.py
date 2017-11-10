from django.contrib import admin
from .models import Sistema, Subsistemas, OM


# Register your models here.
'''
class SistemaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'classe')


class SubsistemasAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'classe')

#admin.site.register(Sistema, SistemaAdmin)
#admin.site.register(Subsistemas, SubsistemasAdmin)
'''

admin.site.register(Sistema)
admin.site.register(Subsistemas)
admin.site.register(OM)
