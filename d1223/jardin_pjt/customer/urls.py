from django.urls import path,include
from . import views

# http://127.0.0.1:8000/customer/clistJson/
# http://localhost:8000/customer/clistJson/
app_name='customer'
urlpatterns = [
    # html리턴
    path('clist/', views.clist, name='clist'),
    
    # 리엑트 - 게시판리스트
    path('clistJson/', views.clistJson, name='clistJson'),
    path('cwriteJson/', views.cwriteJson, name='cwriteJson'),
    path('cdeleteJson/<int:bno>/', views.cdeleteJson, name='cdeleteJson'),
    
    
    path('cview/<int:bno>/', views.cview, name='cview'),
    path('cwrite/', views.cwrite, name='cwrite'),
    path('clikes/', views.clikes, name='clikes'),
    
]

