from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from member.models import MyUser
from restaurants.models import Restaurant

## 후기 테이블
class Review(models.Model):
    rno = models.AutoField(primary_key=True) # 후기 번호
    rcontent = models.TextField() # 후기 내용
    member = models.ForeignKey(MyUser,on_delete=models.SET_NULL,null=True) # 등록회원
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="reviews")  # 평가한 식당

    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) # 후기 별점
    rdate = models.DateTimeField(auto_now_add=True) # 등록 날짜
    
    def __str__(self):
        nickname = self.member.nick_nm if self.member else "탈퇴회원"
        return f'Review {self.rno} | {nickname} | ★{self.rating} | {self.rdate}'

## 리뷰 이미지
class ReviewImage(models.Model):
    ino = models.AutoField(primary_key=True) # 사진 번호
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images") # 첨부된 리뷰
    image = models.ImageField(upload_to="reviews/")
