import django_tables2 as tables
from .models import Train


class TrainTable(tables.Table):
    class Meta:
        model = Train
        # fields = ("sn", "train_type.name", "num_services", "first_service", "last_service")
        fields = ("sn", "type.name")
        template_name = "django_tables2/bootstrap.html"
