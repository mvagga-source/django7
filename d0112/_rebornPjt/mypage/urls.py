from django.urls import path, include
from . import views

app_name = 'mypage'
urlpatterns = [
    path('mychange/', views.mychange, name='mychange'),
    path('myaccount/', views.myaccount, name='myaccount'),

    path('check-duplicate/', views.check_duplicate, name='check_duplicate'),
    path('update/', views.mychange_update, name='mychange_update'),
    
]
