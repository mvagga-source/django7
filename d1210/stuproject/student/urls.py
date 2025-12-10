"""
URL configuration for sproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

app_name = 'student'
urlpatterns = [
    path('write/', views.write,name='write'),
    path('list/', views.list,name='list'),
    path('view/<int:sno>/<str:name>/', views.view,name='view'),
    # path('view/', views.view,name='view'),
    path('delete/', views.delete,name='delete'),
]
