from django.contrib import admin
# member 앱에서 models 파일안의 member 클래스를 가져옴
from member.models import Member


# Register your models here.

admin.site.register(Member)

