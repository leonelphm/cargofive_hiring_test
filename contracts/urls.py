from django.urls import path

from .views import *

app_name = 'contracts'
urlpatterns = [
    path('', ContractCreate.as_view(), name='contract_create'),
    path('comparar', CompararContracts.as_view(), name='contract_compare'),
]