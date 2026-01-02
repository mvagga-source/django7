from django.urls import path, include
from . import views

app_name = 'magazine'
urlpatterns = [
    path('mlist/', views.mlist, name='mlist'),
    path('mview/<int:mno>/', views.mview, name='mview'),
    # path('mlike/', views.mlike, name='mlike'),
    path('mnaver/', views.mnaver, name='mnaver'),
]
