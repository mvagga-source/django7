from django.urls import path,include
from . import views

app_name='stuscore'
urlpatterns = [
    path('slist/', views.slist, name='slist'),
   
]
