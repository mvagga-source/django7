from django.urls import path
from . import views

app_name = 'reports'
urlpatterns = [
    path('map/', views.map_view, name='map'),
    path('new/', views.new_report, name='new'),
    path('my/', views.my_reports, name='my'),
    path('<int:pk>/', views.detail, name='detail'),

    # API
    path('api/list/', views.api_list, name='api_list'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
