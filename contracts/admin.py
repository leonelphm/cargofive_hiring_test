from django.contrib import admin

from .models import *

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """
    Clase que permite la representación de contratos en la interfaz de administración.
    """
    list_display = ("name", "date", "file")  
    search_fields = ("name", "date")
