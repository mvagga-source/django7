from django.urls import path,include
from . import views

app_name='member'
urlpatterns = [
    # html리턴
    path('step03/', views.step03, name='step03'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    # JSON 리턴 : id가 존재하는지 체크
    path('idCheck/', views.idCheck, name='idCheck'),
    
]

