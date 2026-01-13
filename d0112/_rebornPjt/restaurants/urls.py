from django.urls import path, include
from . import views

app_name = 'restaurants'
urlpatterns = [
    path('reslist/', views.reslist, name='reslist'),
    path('resview/<int:resno>/', views.resview, name='resview'),
]
