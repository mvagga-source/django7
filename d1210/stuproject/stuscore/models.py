from django.db import models

# Create your models here.

class Stuscore(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    kor = models.IntegerField(default=0)
    eng = models.IntegerField(default=0)
    math = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    avg = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.sno},{self.name},{self.total}"