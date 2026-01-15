from django.urls import path
from . import views

app_name='store'
urlpatterns = [
    path('slist/', views.slist, name='slist'),
    path('sview/<str:bisbn>/', views.sview, name='sview'),
]