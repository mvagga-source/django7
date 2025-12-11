from django.urls import path, include
from . import views

app_name = 'member'
urlpatterns = [
    path('write/',views.write,name='write'),
    path('list/',views.list,name='list'),
    path('login/',views.login,name='login'),
]
