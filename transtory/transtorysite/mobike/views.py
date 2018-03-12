from django.db.models import Count, Max, Min
from django.shortcuts import render
from django.views import generic
from django_tables2 import RequestConfig

from .models import Bike
from .tables import BikeTable


def bike_list(request):
    query_set = Bike.objects.annotate(num_services=Count("bikeservice"),
                                      first_service=Max("bikeservice__trip__time"),
                                      last_service=Min("bikeservice__trip__time"))
    query_set = query_set.order_by("sn").all()
    table = BikeTable(query_set)
    RequestConfig(request).configure(table)
    return render(request, 'mobike/bikes.html', {'table': table})

#
# class BikeListView(generic.ListView):
#     template_name = 'mobike/bikes.html'
#     context_object_name = 'bike_list'
#
#     def get_queryset(self):
#         """
#         Return the last five published questions (not including those set to be
#         published in the future).
#         """
#         return Bike.objects.all().order_by("sn")
#
#
# class BikeDetailView(generic.DetailView):
#     model = Bike
