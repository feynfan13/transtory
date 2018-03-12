import django_tables2 as tables
from .models import Plane


class PlaneTable(tables.Table):
    class Meta:
        model = Plane
        fields = ("tail_number", "airline.iata", "model.name")
        template_name = "django_tables2/bootstrap.html"
