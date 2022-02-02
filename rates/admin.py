from django.contrib import admin

from .models import *

admin.site.site_header = 'Test CargoFive'

@admin.register(Rates)
class RatesAdmin(admin.ModelAdmin):
    """
    Clase que permite la representación de las tarifas en la interfaz de administración.
    """
    list_display = ("fk_contract", "origin", "destination", "currency", "twenty", "forty", "fortyhc")  
    search_fields = (
        "fk_contract__name",
        "fk_contract__date",
        "origin",
        "destination",
        "currency",
    )
