from django.db import models

class ChartData(models.Model):
    cno = models.AutoField(primary_key=True)
    cyear = models.CharField(max_length=4)
    cdata = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.cno},{self.cyear},{self.cdata}'
