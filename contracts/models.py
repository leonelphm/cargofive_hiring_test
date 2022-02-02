from django.db import models

class Contract(models.Model):
    """
    Modelo de datos para los contratos
    """
    def get_upload_to(self, filename):
        return f"contract/{self.name}/{filename}"

    name = models.CharField(max_length=128, verbose_name='Nombre')
    date = models.DateField(verbose_name='Fecha')
    file = models.FileField(verbose_name='Archivo', upload_to=get_upload_to)

    def __str__(self):
        """
        Retorna el nombre del objeto
        """
        return self.name