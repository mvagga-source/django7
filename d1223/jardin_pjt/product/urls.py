from django.urls import path,include
from . import views

app_name='product'
urlpatterns = [
    path('detail/', views.detail, name='detail'),
    # 카카오 결제요청
    path('prepare_payment/', views.prepare_payment, name='prepare_payment'),
    # 카카오 결제승인창
    path('approve/', views.approve, name='approve'),
    # 카카오 결제후 이동
    path('success/', views.success, name='success'),
    path('fail/', views.fail, name='fail'),
    path('cancel/', views.cancel, name='cancel'),
    
    
]

