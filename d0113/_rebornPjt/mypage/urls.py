from django.urls import path, include
from . import views

app_name = 'mypage'
urlpatterns = [
    path('mychange/', views.mychange, name='mychange'),
    path('myaccount/', views.myaccount, name='myaccount'),
    
    path('check-duplicate/', views.check_duplicate, name='check_duplicate'),
    path('update/', views.mychange_update, name='mychange_update'),
    
    path('check_password/', views.check_password, name='check_password'),
    path('delete/', views.delete_user, name='delete_user'),
    
]
