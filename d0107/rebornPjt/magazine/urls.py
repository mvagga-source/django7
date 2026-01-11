from django.urls import path, include
from . import views

app_name = 'magazine'
urlpatterns = [
    path('mlist/', views.mlist, name='mlist'),
    path('mview/<int:mno>/', views.mview, name='mview'),
    path('mlike/', views.mlike, name='mlike'),
    path('mhit/<int:mno>/', views.mhit, name='mhit'),
    path('mnaver/', views.mnaver, name='mnaver'),
    path('mtest/', views.mtest, name='mtest'),
    path('mmnge/', views.mmnge, name='mmnge'),
    path('mcategoryChart/', views.mcategoryChart, name='mcategoryChart'),
    path('myearChart/', views.myearChart, name='myearChart'),
    path('mupdate/', views.mupdate, name='mupdate'),
    path('mlogin/', views.mlogin, name='mlogin'),
]
