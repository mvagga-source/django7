from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 1. 제목(title)을 가장 앞으로 보냅니다. (이제 제목을 클릭해서 상세 페이지 진입)
    list_display = ('title', 'is_notice', 'category', 'author', 'created_at')
    
    # 2. 리스트에서 바로 수정할 필드 지정
    list_editable = ('is_notice',)
    
    # 3. 제목을 클릭하면 상세 페이지로 이동하도록 명시 (선택 사항이지만 안전함)
    list_display_links = ('title',)
    
    list_filter = ('category', 'is_notice') 
    search_fields = ('title', 'author__username')

admin.site.register(Comment)