from django.db import models
from member.models import MyUser

class MagazineCode(models.Model):
    mtype = models.CharField(max_length=2)
    mtype_desc = models.CharField(max_length=100)
    mdate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.mtype},{self.mtype_desc}'

class Magazine(models.Model):
    mno = models.AutoField(primary_key=True)
    mtitle = models.CharField(max_length=1000)
    mcontent = models.TextField(null=True,blank=True)
    mthumbnail = models.TextField(null=True,blank=True)
    magazinecode = models.ForeignKey(MagazineCode,on_delete=models.SET_NULL,null=True)
    mfile = models.FileField(default='',null=True,blank=True,upload_to='magazine/')
    mhit = models.IntegerField(default=0)
    mdate = models.DateTimeField(auto_now_add=True)
    
    # mlike = models.ManyToManyField(MyUser,related_name='like_myuser',null=True,blank=True)
    
    def __str__(self):
        return f'{self.mno},{self.mtitle},{self.magazinecode}'
    

