from django.urls import path,include
from . import views

app_name='board'
urlpatterns = [
    path('list/', views.list, name='list'),
    path('write/', views.write, name='write'),
    path('view/<int:bno>/', views.view, name='view'),
    path('view2/<int:bno>/', views.view2, name='view2'),
    path('delete/<int:bno>/', views.delete, name='delete'),
    path('update/<int:bno>/', views.update, name='update'),
    path('reply/<int:bno>/', views.reply, name='reply'),
    # 차트그리기
    path('chart/', views.chart, name='chart'),
]
