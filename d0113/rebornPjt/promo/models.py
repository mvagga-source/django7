from django.db import models
from restaurants.models import Restaurant

class Promo(models.Model):
    promo_id = models.AutoField(primary_key=True)

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="promos"
    )

    kicker = models.CharField(max_length=30, blank=True, default="")
    title = models.CharField(max_length=60)
    sub = models.CharField(max_length=80, blank=True, default="")
    cta_text = models.CharField(max_length=20, blank=True, default="자세히 보기")

    # 노출/정렬/기간(확장용)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-updated_at"]

    def __str__(self):
        return f"[{self.promo_id}] {self.restaurant.res_name} - {self.title}"
