from django.contrib import admin
from .models import Report

@admin.action(description="상태: 접수됨")
def mark_received(modeladmin, request, queryset):
    queryset.update(status=Report.STATUS_RECEIVED)

@admin.action(description="상태: 처리중")
def mark_processing(modeladmin, request, queryset):
    queryset.update(status=Report.STATUS_PROCESSING)

@admin.action(description="상태: 완료")
def mark_done(modeladmin, request, queryset):
    queryset.update(status=Report.STATUS_DONE)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "risk", "status", "created_at", "happened_at", "user")
    list_filter = ("status", "category", "risk", "created_at")
    search_fields = ("title", "content", "summary", "address_text", "sido", "sigungu", "dong")
    actions = [mark_received, mark_processing, mark_done]
