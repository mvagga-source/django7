from django.urls import path, include
from . import views

app_name = 'review'
urlpatterns = [
    path('write/', views.write_review, name='write'),
    path('delete/', views.delete_review, name='delete'),
    path('update/', views.update_review, name='update'),
    path('list/', views.list_review, name='list'),
]
