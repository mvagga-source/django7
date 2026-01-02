from django.db import models

from django.db import models

class Book(models.Model):
    # 엑셀의 헤더(컬럼)를 만드는 과정입니다.
    btitle = models.CharField(max_length=200, verbose_name="책 제목")
    bauthor = models.CharField(max_length=100, verbose_name="저자")
    bpublisher = models.CharField(max_length=100, verbose_name="출판사")
    bpubdate= models.DateField(verbose_name="출판일", null=True, blank=True)
    bprice = models.IntegerField(verbose_name="가격", null=True, blank=True)
    bimage = models.URLField(verbose_name="이미지", null=True, blank=True)
    blink = models.URLField(verbose_name="구매 링크", null=True, blank=True)
    bdescription = models.TextField(verbose_name="책 소개", null=True, blank=True)
    bhit = models.IntegerField(default=0, verbose_name="조회수")
    
    # ★ 핵심: 중복 저장을 막기 위한 고유 번호 (ISBN)
    bisbn = models.CharField(max_length=50, unique=True, verbose_name="ISBN")
    
    # 언제 저장했는지 기록 (자동 입력)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
