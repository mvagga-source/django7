from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('traffic', '교통사고'),
    ('violence', '폭력/위협'),
    ('fire', '화재/연기'),
    ('lost', '분실/도난'),
    ('etc', '기타'),
]

class Report(models.Model):
    STATUS_RECEIVED = 'received'
    STATUS_PROCESSING = 'processing'
    STATUS_DONE = 'done'

    STATUS_CHOICES = [
        (STATUS_RECEIVED, '접수됨'),
        (STATUS_PROCESSING, '처리중'),
        (STATUS_DONE, '완료'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=120)
    content = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    # Optional: human-readable address picked from map
    address_text = models.CharField(max_length=255, blank=True)
    sido = models.CharField(max_length=50, blank=True)
    sigungu = models.CharField(max_length=50, blank=True)
    dong = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_RECEIVED)
    happened_at = models.DateTimeField()
    summary = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='etc')
    risk = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
