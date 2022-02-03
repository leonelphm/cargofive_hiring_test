import pyexcel as pyexl

from django.contrib import admin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .forms import ContractForms
from .models import *

from rates.models import Rates

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """
    Clase que permite la representación de contratos en la interfaz de administración.
    """
    list_display = ("name", "date", "file")  
    search_fields = ("name", "date")
    form = ContractForms

    def save_model(self, request, obj, form, change):
        contract = form.save()
        path = default_storage.save(f'tmp/{contract.file.name}', ContentFile(contract.file.read()))
        contracts = pyexl.get_sheet(file_name=f'sources/{path}',  name_columns_by_row=0)
        listado_columna = [
            self.save_data_excel(
            fk_contract= contract, 
            origin= record[0],
            destination= record[1],
            currency= record[4],
            twenty= record[5],
            forty=  record[6],
            fortyhc= record[7]
            )  for record in contracts
        ]
        Rates.objects.bulk_create(listado_columna)
        super().save_model(request, obj, form, change)

    def save_data_excel(self, **kwargs):
        """
        Logica de control para registrar los datos del excel, al modelo de datos de Rates
        """
        create_rates = Rates(
            fk_contract=kwargs.get('fk_contract'),
            origin=kwargs.get('origin'),
            destination=kwargs.get('destination'),
            currency=kwargs.get('currency'),
            twenty=kwargs.get('twenty'),
            forty=kwargs.get('forty'),
            fortyhc=kwargs.get('fortyhc')
        )
        return create_rates

