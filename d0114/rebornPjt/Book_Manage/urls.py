from django.urls import path
from . import views

app_name='Book_Manage'
urlpatterns = [
    path('blist/', views.blist, name='blist'),
    path('bupdate/<str:bisbn>/', views.bupdate, name='bupdate'),
    path('bup_finish/<str:bisbn>/', views.bup_finish, name='bup_finish'),
    path('bview/<str:bisbn>/', views.bview, name='bview'),
    path('bdelete/<str:bisbn>/', views.bdelete, name='bdelete'),
    path('bwrite/', views.bwrite, name='bwrite'),
]