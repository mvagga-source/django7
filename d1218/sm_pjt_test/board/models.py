from django.db import models
from member.models import Member

class Board(models.Model):
    bno = models.AutoField(primary_key=True) 
    btitle = models.CharField(max_length=1000)
    bcontent = models.TextField()
    member = models.ForeignKey(Member,on_delete=models.SET_NULL,null=True)
    # 답변달기 사용컬럼
    bgroup = models.IntegerField(default=0)
    bstep = models.IntegerField(default=0)
    bindent = models.IntegerField(default=0)
    
    bhit = models.IntegerField(default=0) #조회수
    bfile = models.FileField(default='',null=True)
    bdate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.bno},{self.btitle},{self.member.id},{self.bgroup},{self.bdate}'
