from django.db.models import Count, Max, Min
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django_tables2 import RequestConfig

from .models import Train
from .tables import TrainTable

from transtory.shanghaimetro import ShmPublicDataApp


class IndexView(TemplateView):
    template_name = 'shanghaimetro/index.html'


class TrainListView(ListView):
    model = Train
    template_name = 'shanghaimetro/trains.html'
    context_object_name = 'train_list'  # context_object_name is a friendly name used in template
    ordering = ['sn']

    def get_context_data(self, **kwargs):
        context = super(TrainListView, self).get_context_data(**kwargs)
        context['nav_customer'] = True
        # Specific to train list
        line_train_mode = 'line_number' in self.kwargs.keys()
        query_set = Train.objects.annotate(num_services=Count("route"),
                                           first_service=Min("route__departure__time"),
                                           last_service=Max("route__departure__time"))
        if line_train_mode:
            query_set = query_set.filter(line__name='Line {:02d}'.format(int(self.kwargs['line_number'])))
        query_set = query_set.order_by('sn').all()
        # Form data dictionary for table and append missing trains
        data_dict_list, train_set = list(), set()
        for train in query_set:
            data_dict = dict()
            data_dict['sn'] = train.sn
            data_dict['train_type'] = train.train_type.name
            data_dict['num_services'] = train.num_services
            data_dict['first_service'] = train.first_service
            data_dict['last_service'] = train.last_service
            data_dict_list.append(data_dict)
            train_set.add(train.sn)
        if line_train_mode:  # append trains not taken for line mode
            train_df = ShmPublicDataApp.get_instance().get_trains_of_line(self.kwargs['line_number'])
            for _, train in train_df.iterrows():
                if not train['train'] in train_set:
                    data_dict = dict()
                    data_dict['sn'] = train['train']
                    data_dict['train_type'] = train['type']
                    data_dict['num_services'] = 0
                    data_dict['first_service'] = None
                    data_dict['last_service'] = None
                    data_dict_list.append(data_dict)
        data_dict_list.sort(key=lambda x: x['sn'])
        table = TrainTable(data_dict_list)
        RequestConfig(self.request, paginate={'per_page': 1000}).configure(table)
        context['table'] = table
        return context
