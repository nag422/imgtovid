from django.db import models

# Create your models here.
class seleniumimagestore(models.Model):    
    imagename = models.CharField(max_length=100)
    url = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=100)
    def __str__(self):
        return self.imagename