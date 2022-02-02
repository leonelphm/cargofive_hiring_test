import pyexcel as pyexl

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.shortcuts import (
    redirect, render
)
from django.views.generic import (
    FormView, TemplateView
)

from rates.models import Rates

from .forms import ContractForms
from .models import Contract

class ContractCreate(SuccessMessageMixin,  FormView):
    """
    Control de la creacion del contrato
    """
    model = Contract
    form_class = ContractForms
    template_name = "contracts_create.html"
    success_url = reverse_lazy('rates:rates_list')
    success_message = "Se registró el contrato con exito"

    def form_valid(self, form):
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
        return super().form_valid(form)

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


class CompararContracts(TemplateView):
    """
    Control para comprar los 2 ultimos archivos registrados
    """
    model = Contract
    queryset = Contract.objects.select_related()
    template_name = "contracts_compare.html"

    def post(self, request, *args, **kwargs):
        """
        Metodo que controla la peticion via post desde el template

        @params self objeto de referencia de la clase
        @params request parametro de la peticion desde el html
        return render renderiza la respuesta de la peticion, retorna el contexto diff enviando al template
        """
        #: se obtiene los 2 ultimos registos del contrato
        queryset = self.queryset.order_by('-id')[:2]
        if len(queryset) <=1:
            messages.error(
                self.request,
                F'No se pude iniciar el proceso de comparación, no se han agregado mas registros')
            messages.info(
                self.request,
                F'Por favor, agrega nuevos registros para poder comparar')
            return redirect(reverse_lazy('contracts:contract_create'))
        contract_file = []
        for files in queryset:
            #: Se agrega a una hoja de pyexcel los documentos registrados
            contract_file.append(pyexl.get_sheet(file_name=files.file.path,  name_columns_by_row=0))

        #: Realiza la compracion de cada columna de ambos documentos
        compare_pol = self.compare([contract_file[0].column["POL"], contract_file[1].column["POL"]])
        compare_pod = self.compare([contract_file[0].column["POD"], contract_file[1].column["POD"]])
        compare_rout = self.compare([contract_file[0].column["Routing"], contract_file[1].column["Routing"]])
        compare_ett = self.compare([contract_file[0].column["ETT"], contract_file[1].column["ETT"]])
        compare_curr = self.compare([contract_file[0].column["Curr."], contract_file[1].column["Curr."]])
        compare_20gp = self.compare([contract_file[0].column["20'GP"], contract_file[1].column["20'GP"]])
        compare_40gp = self.compare([contract_file[0].column["40'GP"], contract_file[1].column["40'GP"]])
        compare_40hc = self.compare([contract_file[0].column["40'HC"], contract_file[1].column["40'HC"]])
        compare_20fr = self.compare([contract_file[0].column["20'FR"], contract_file[1].column["20'FR"]])
        compare_40fh = self.compare([contract_file[0].column["40'FH"], contract_file[1].column["40'FH"]])
        compare_40fr = self.compare([contract_file[0].column["40'FR"], contract_file[1].column["40'FR"]])
        compare_40oh = self.compare([contract_file[0].column["40'OH"], contract_file[1].column["40'OH"]])
        compare_40ot = self.compare([contract_file[0].column["40'OT"], contract_file[1].column["40'OT"]])
        compare_20tk = self.compare([contract_file[0].column["20'TK"], contract_file[1].column["20'TK"]])
        compare_40rh = self.compare([contract_file[0].column["40'RH"], contract_file[1].column["40'RH"]])
        compare_40rh = self.compare([contract_file[0].column["40'RH-1"], contract_file[1].column["40'RH-1"]])
        
        #: Se concatena la lista que se genero al comparar los archivos
        diff_total = compare_pol + compare_pod + compare_rout + compare_ett + compare_curr + compare_20gp + compare_40gp + compare_40hc + compare_20fr + compare_40fh + compare_40fr + compare_40oh + compare_40ot + compare_20tk + compare_40rh + compare_40rh
        #: Se ordena el set de datos
        order_diff = sorted(set(diff_total))
        
        #: Si el set de datos es mayor a 0 se generaron cambios en alguno de los archivos     
        if len(order_diff) > 0:
            msgs = f"existe {len(order_diff)} cambios en el documento"
        else:
            msgs = "no hay variacion en el documento"
        messages.success(
                self.request,
                F'Se ralizo la comparacion con éxito, {msgs}')
        
        return render(request, self.template_name, {'diff': order_diff})
        

    def compare(self, columns):
        """
        Metodo que se usa para compara las columnas de los 2 ultimos excel registrados en contracts
        
        @params self objeto de referencia de la clase
        @params columns lista que contiene las 2 columnas a compara del archivo1 y archivo2
        @return diff_compare muestra en que linea se encontro la variacion
        """
        if len(columns) > 2:
            messages.error(
                self.request,
                F'La operación no se puede realizar, la comparacion se debe hacer solo de dos archivos')
        else:
            columns_first = columns[0]
            columns_second = columns[1]
            #: Valida cual de los documentos tiene mas filas
            if len(columns_first) >= len(columns_second):
                for_init = columns_first
                list_compare = columns_second
            else:
                for_init = columns_second
                list_compare = columns_first
            i = 0
            diff_compare = []
            #: Hace la iteracion con el documento que posee mas filas
            for row in for_init:
                # Se realiza la comparacion fila por fila de la columna enviada
                try:
                    if row == list_compare[i]:
                        pass
                    else:
                        diff_compare.append(f"Muestra variación en la fila {i+2}")
                except Exception as e:
                    diff_compare.append(f"No existe la fila {i+2} en uno de los documentos")
                i +=1
            return diff_compare

            

