from django.urls import path

from .views import *

app_name = 'rates'
urlpatterns = [
    path('list-rates', RatesListViews.as_view(), name='rates_list'),
]