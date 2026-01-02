from django.db import models

class Restaurant(models.Model):
    resno=models.AutoField(primary_key=True)
    locno=models.IntegerField(default=0)
    res_name=models.CharField(max_length=50,null=True)
    desc=models.TextField(null=True)
    addr=models.CharField(max_length=200,null=True)
    tel=models.CharField(max_length=13,null=True)
    lat=models.DecimalField(max_digits=10,decimal_places=7,default=0)
    lng=models.DecimalField(max_digits=10,decimal_places=7,default=0)
    date=models.DateTimeField(auto_now=True)
    mem_id=models.CharField(max_length=25,null=True)
    
    def __str__(self):
        return f"{self.resno},{self.res_name},{self.tel},{self.mem_id}"