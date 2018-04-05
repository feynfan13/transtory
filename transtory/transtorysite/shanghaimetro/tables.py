import itertools
import django_tables2 as tables

from .models import Train, shanghaimetro_city
from transtory.common import dt_wrapper


class TrainTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="Index")

    class Meta:
        model = Train
        fields = ("row_number", "sn", "train_type.name", "num_services", "first_service", "last_service")
        template_name = "django_tables2/bootstrap.html"

    def __init__(self, *args, **kwargs):
        super(TrainTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)

    def render_first_service(self, value):
        return dt_wrapper.get_local_datetime_str_from_utc_datetime_str(value, shanghaimetro_city)

    def render_last_service(self, value):
        return dt_wrapper.get_local_datetime_str_from_utc_datetime_str(value, shanghaimetro_city)
