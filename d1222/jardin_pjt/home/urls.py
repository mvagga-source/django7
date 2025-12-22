from django.urls import path,include
from . import views

app_name = ''
urlpatterns = [
    path('',views.index,name='index'),
    path('chart/',views.chart,name='chart'),
    path('chart_json/',views.chart_json,name='chart_json'),
    
    path('chart2/',views.chart2,name='chart2'),
    path('chart2_json/',views.chart2_json,name='chart2_json'),
]

