import itertools
import django_tables2 as tables

from .models import Train


class TrainTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name="Index")

    class Meta:
        model = Train
        # fields = ("sn", "train_type.name", "num_services", "first_service", "last_service")
        fields = ("row_number", "sn", "type.name")
        template_name = "django_tables2/bootstrap.html"

    def __init__(self, *args, **kwargs):
        super(TrainTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)
