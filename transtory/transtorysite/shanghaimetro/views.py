from django.db.models import Count, Max, Min
from django.shortcuts import render
from django.views.generic import ListView
from django_tables2 import RequestConfig

from .models import Train
from .tables import TrainTable

#
# def train_list(request):
#     query_set = Train.objects.annotate(num_services=Count("route"),
#                                        first_service=Min("route__departure__time"),
#                                        last_service=Max("route__departure__time"))
#     query_set = query_set.order_by("sn").all()
#     table = TrainTable(query_set)
#     RequestConfig(request).configure(table)
#     table.paginate(page=request.GET.get('page', 1), per_page=100)
#     return render(request, 'shanghaimetro/trains.html', {'table': table})


class TrainListView(ListView):
    model = Train
    template_name = 'shanghaimetro/trains.html'
    context_object_name = 'train_list'  # context_object_name is a friendly name used in template
    ordering = ['sn']

    def get_context_data(self, **kwargs):
        context = super(TrainListView, self).get_context_data(**kwargs)
        context['nav_customer'] = True
        query_set = Train.objects.annotate(num_services=Count("route"),
                                           first_service=Min("route__departure__time"),
                                           last_service=Max("route__departure__time"))
        query_set = query_set.order_by("sn").all()
        table = TrainTable(query_set)
        RequestConfig(self.request, paginate={'per_page': 100}).configure(table)
        context['table'] = table
        return context
