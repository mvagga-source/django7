from django.contrib import admin
from magazine.models import Magazine, MagazineCode, MagazineAdmin

# Register your models here.

admin.site.register(Magazine)
admin.site.register(MagazineCode)
admin.site.register(MagazineAdmin)
