from django.db.models import Count, Max, Min
from django.shortcuts import render
from django.views import generic
from django_tables2 import RequestConfig

from .models import Train
from .tables import TrainTable


def train_list(request):
    query_set = Train.objects.annotate(num_services=Count("route"),
                                       first_service=Max("route__departure__time"),
                                       last_service=Min("route__departure__time"))
    query_set = query_set.order_by("sn").all()
    table = TrainTable(query_set)
    RequestConfig(request).configure(table)
    return render(request, 'shanghaimetro/trains.html', {'table': table})
