from django.urls import path, include
from . import views

app_name = 'board'
urlpatterns = [
    path('blist/', views.blist, name='blist'),
    path('bwrite/', views.bwrite, name='bwrite'),
    path('bview/<int:bno>/', views.bview, name='bview'),
    path('bupdate/<int:bno>/', views.bupdate, name='bupdate'),
    path('bdelete/<int:bno>/', views.bdelete, name='bdelete'),
    path('bview/<int:bno>/comment/', views.comment_write, name='comment_write'),
    path('bview/<int:bno>/comment/<int:cno>/delete/', views.comment_delete, name='comment_delete'),
    path('bview/<int:bno>/comment/<int:cno>/update/', views.comment_update, name='comment_update'),
    path('bview/<int:bno>/like/', views.post_like, name='post_like'),
    
    path('noticelist/', views.noticelist, name='noticelist'),
    path('nwrite/', views.nwrite, name='nwrite'),
    
]
