from django.urls import path,include
from . import views

app_name = 'member'
urlpatterns = [
    
    # html 리턴
    path('step03/',views.step03,name='step03'),
    
    # JSON 리턴 : id 존재 확인
    path('idCheck/',views.idCheck,name='idCheck'),

]

