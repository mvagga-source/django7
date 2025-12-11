from django.db import models

# Create your models here.

class Student(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=1)
    grade = models.IntegerField(default=1)
    gender = models.CharField(max_length=10)
    hobby = models.CharField(max_length=100,default='게임')
    
    def __str__(self):
        return f"{self.sno},{self.name},{self.age},{self.grade}"
    

