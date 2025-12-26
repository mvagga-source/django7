from django.urls import path,include
from . import views

app_name='comment'
urlpatterns = [
    # html리턴
    path('colist/', views.colist, name='colist'),
    path('cowrite/', views.cowrite, name='cowrite'),
    path('codelete/', views.codelete, name='codelete'),
    
]

