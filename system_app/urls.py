from django.urls import path
from . import views

app_name = 'system_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('load_data', views.load_data, name='load_data'),
    path('show_data', views.show_data, name='show_data'),
    path('data_timeline', views.data_timeline, name='data_timeline'),
    path('data_pie', views.data_pie, name='data_pie'),
]