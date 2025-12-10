
from django.urls import path, include
from . import views

app_name = 'student'
urlpatterns = [
    path('write/', views.write,name='write'),
    path('list/', views.list,name='list'),
]
