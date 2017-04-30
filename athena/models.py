from django.db import models


class RTLS_times(models.Model):
    interaction_id = models.IntegerField(default=0)
    times = models.DateTimeField('rivER time')
    status = models.CharField(default="0", max_length=200)
    location = models.CharField(default="0", max_length=200)
        
        

class EHR_times(models.Model):
    interaction_id = models.IntegerField(default=0)
    times = models.DateTimeField('athena time')
    status = models.CharField(default="0", max_length=200)
    location = models.CharField(default="0", max_length=200)
