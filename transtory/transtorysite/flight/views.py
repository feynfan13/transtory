from django.db.models import Count, Max, Min
from django.shortcuts import render
from django.views import generic
from django_tables2 import RequestConfig

from .models import Plane
from .tables import PlaneTable


def plane_list(request):
    # query_set = Plane.objects.annotate(num_services=Count("bikeservice"),
    #                                   first_service=Max("bikeservice__trip__time"),
    #                                   last_service=Min("bikeservice__trip__time"))
    query_set = Plane.objects
    query_set = query_set.order_by("tail_number").all()
    table = PlaneTable(query_set)
    RequestConfig(request).configure(table)
    return render(request, 'flight/planes.html', {'table': table})