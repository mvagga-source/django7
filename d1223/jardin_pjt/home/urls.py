from django.urls import path,include
from . import views

app_name=''
urlpatterns = [
    path('', views.index, name='index'),
    path('chart2/', views.chart2, name='chart2'),
    path('my_map/', views.my_map, name='my_map'),
    
    # 카카오페이
    path('kakao_pay/', views.kakao_pay, name='kakao_pay'),
    path('prepare_payment/', views.prepare_payment, name='prepare_payment'),
    path('paySuccess/', views.paySuccess, name='paySuccess'),
    path('payFail/', views.payFail, name="payFail"), 
    path('payCancel/', views.payCancel, name="payCancel"), 

    
    
    path('chart_json/', views.chart_json, name='chart_json'),
    path('chart_json2/', views.chart_json2, name='chart_json2'),
    
]

