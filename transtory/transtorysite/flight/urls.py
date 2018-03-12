from django.urls import path

from . import views

app_name = 'flight'

urlpatterns = [
    # path('', views.BikeListView.as_view(), name='bike list'),
    path('planes', views.plane_list, name='plane_list'),
]
