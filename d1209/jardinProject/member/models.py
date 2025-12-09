from django.db import models

# Create your models here.

# 테이블 생성 - 파이썬 명령어로 sql구문을 대체 : ORM방식

    # id varchar2(100) primary key,
    # pw varchar2(100) not null,
    # name varchar2(100),
    # phone char(13),
    # gender char(1),
    # hobby varchar2(100)
    
class Member(models.Model):
    
    id = models.CharField(max_length=100,primary_key=True)
    pw = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(default=0)
    hobby = models.CharField(max_length=100)
    
    # 객체출력 - 주소값, __str__ 객체를 문자열로 출력시켜줌
    def __str__(self):
        return f"{self.id},{self.name},{self.age},{self.gender}"
