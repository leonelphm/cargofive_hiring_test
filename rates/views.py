from django.views.generic.list import ListView

from .models import Rates


class RatesListViews(ListView):
    """
    Lista paginada de las tarifas
    """
    template_name = "list_rate.html"
    model = Rates
    paginate_by = 15
    queryset = Rates.objects.select_related()


def import_rates(listado_columna):
    Rates.objects.bulk_create(listado_columna)