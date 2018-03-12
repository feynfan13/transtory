import django_tables2 as tables
from .models import Bike


class BikeTable(tables.Table):
    class Meta:
        model = Bike
        fields = ("sn", "subtype.name", "num_services", "first_service", "last_service")
        template_name = "django_tables2/bootstrap.html"
