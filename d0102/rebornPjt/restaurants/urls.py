from django.urls import path, include
from . import views

app_name = 'restaurants'
urlpatterns = [
    path('reslist/', views.reslist, name='reslist'),
]
