from django.db import models
from member.models import Member

# Create your models here.

# id -> ORM방식 객체저장이 가능해짐
#    member = models.ForeignKey(Member,on_delete=models.DO_NOTHING,null=True)

# 답변달기 사용에 필요한 컬럼
# bgroup, bstep, bindent
# 파일첨부
# bfile

class Board(models.Model):
    bno = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member,on_delete=models.DO_NOTHING,null=True)
    btitle = models.CharField(max_length=1000)
    bcontent = models.TextField()
    bhit = models.IntegerField(default=0)
    bdate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.bno},{self.btitle}'