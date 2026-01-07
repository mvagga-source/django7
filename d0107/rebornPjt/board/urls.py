from django.urls import path, include
from . import views

app_name = 'board'
urlpatterns = [
    path('blist/', views.blist, name='blist'),
    path('bwrite/', views.bwrite, name='bwrite'),
    path('bview/<int:bno>/', views.bview, name='bview'),
    path('bview/<int:bno>/comment/', views.comment_write, name='comment_write'),
    path('bview/<int:bno>/comment/<int:cno>/delete/', views.comment_delete, name='comment_delete'),
    path('bview/<int:bno>/like/', views.post_like, name='post_like'),
    
    path('notice/', views.notice, name='notice'),
    
]
