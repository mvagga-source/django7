from django.urls import path, include
from . import views

app_name = 'promo'
urlpatterns = [
    path('admin/', views.promo_admin, name='admin'),# 프로모션 관리페이지
    
    # ✅ AJAX API
    path("api/list/", views.promo_list_api, name="api_list"),
    path("api/save/", views.promo_save_api, name="api_save"),
    path("api/delete/<int:promo_id>/", views.promo_delete_api, name="api_delete"),
]
