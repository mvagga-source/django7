from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('member/', include('member.urls')),
    path('board/', include('board.urls')),
    path('comment/', include('comment.urls')),
    path('stuscore/', include('stuscore.urls')),
]


# 파일업로드시 url구성, urlpatterns에 추가 설정
urlpatterns += static(settings.MEDIA_URL,
             document_root = settings.MEDIA_ROOT )