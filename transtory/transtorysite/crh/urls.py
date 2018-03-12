from django.urls import path

from . import views

app_name = 'crh'

urlpatterns = [
    # path('', views.BikeListView.as_view(), name='bike list'),
    path('trains', views.train_list, name='train_list'),
]
