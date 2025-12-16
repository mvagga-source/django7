from django.db import models

# Create your models here.

class Board(models.Model):
    bno = models.AutoField(primary_key=True)
    btitle = models.CharField(max_length=1000)
    bfile = models.FileField(default='',null=True)
    
    def __str__(self):
        return f'{self.bno},{self.btitle},{self.bfile}'
    