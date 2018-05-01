from django.urls import path

from . import views

app_name = 'crh'

urlpatterns = [
    path('trains', views.train_list, name='train_list'),
]
