from django.db import models
from contracts.models import Contract

class Rates(models.Model):
    """
    Modelo de datos para las tarifas
    """
    fk_contract = models.ForeignKey(Contract,on_delete=models.CASCADE, verbose_name='Empresas')
    origin = models.CharField(max_length=128, verbose_name='POL')
    destination = models.CharField(max_length=128, verbose_name='POD')
    currency = models.CharField(max_length=128, verbose_name='Curr')
    twenty = models.CharField(max_length=128, verbose_name='20’GP')
    forty = models.CharField(max_length=128, verbose_name='40’GP')
    fortyhc = models.CharField(max_length=128, verbose_name='40’HC')

    def __str__(self):
        """
        Retorna el nombre del objeto
        """
        return f"{self.origin} - {self.destination}"
