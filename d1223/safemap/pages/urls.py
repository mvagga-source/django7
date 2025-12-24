from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('board/', views.board_list, name='board_list'),
    path('api/kr-admin/', views.kr_admin, name='kr_admin'),
]