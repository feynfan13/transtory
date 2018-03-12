from django.urls import path

from . import views

app_name = 'mobike'

urlpatterns = [
    # path('', views.BikeListView.as_view(), name='bike list'),
    path('bikes', views.bike_list, name='bike_list'),
]
