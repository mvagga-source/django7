from django.db import models
from member.models import Member

# Create your models here.
# sno,id,kor,eng,math,total,avg,sdate

class Stuscore(models.Model):
    sno = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member,on_delete=models.CASCADE,null=True,blank=True)
    kor = models.IntegerField(default=0)
    eng = models.IntegerField(default=0)
    math = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    avg = models.FloatField(default=0)
    sdate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.sno},{self.member.id},{self.kor},{self.total},{self.avg},{self.sdate}'
    