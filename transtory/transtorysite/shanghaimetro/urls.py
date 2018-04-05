from django.urls import path

from . import views

app_name = 'shanghaimetro'

urlpatterns = [
    # path('trains', views.train_list, name='train_list'),
    path('trains', views.TrainListView.as_view(), name='train_list'),
]
