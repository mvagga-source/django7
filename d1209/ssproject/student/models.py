from django.db import models

# Create your models here.


class Student(models.Model):
    
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