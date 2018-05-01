from django.urls import path

from . import views

app_name = 'shanghaimetro'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('train', views.TrainListView.as_view(), name='train'),
    path('train/l<line_number>', views.TrainListView.as_view(), name='train_per_line'),
    path('trip', views.IndexView.as_view(), name='trip'),
]
