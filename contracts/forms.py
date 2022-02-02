import os
import pyexcel as pyexl

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from config.DateInput import DateInput

from .models import Contract


class ContractForms(forms.ModelForm):
    """
    Creacion del formulario de contracto
    """
    class Meta:
        model = Contract
        fields = '__all__'
        widgets = {
            'date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'accept': '.xlsx, .xls, .csv, .ods'})

    def clean_file(self):
        file = self.cleaned_data.get("file", False)
        ext = os.path.splitext(file.name)[1]
        path = default_storage.save(f'tmp/{file.name}', ContentFile(file.read()))
        
        valid_extensions = ['.xlsx', '.xls', 'csv', 'ods']
        if not ext in valid_extensions:
            raise ValidationError("Extensión de archivo no admitida.")
        contracts = pyexl.get_sheet(file_name=f'sources/{path}',  name_columns_by_row=0)
        path = default_storage.delete(path)
        column_file = list(contracts.colnames)
        valid_column = ['POL', 'POD', 'Routing', 'ETT', 'Curr.']
        if column_file[0:5] != valid_column:
            raise ValidationError("El archivo no tiene las columnas correspondiente deben ser: 'POL', 'POD', 'Routing', 'ETT', 'Curr.' ...")
        
        return file