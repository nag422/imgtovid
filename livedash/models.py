from django.db import models

# Create your models here.
class BackgroundImagesStore(models.Model):
    image = models.CharField(max_length=100)
    def __str__(self):
        return self.image

class ExcelFileStore(models.Model):    
    language = models.CharField(max_length=100)
    sourcetype = models.CharField(max_length=100)  
    data = models.CharField(max_length=100000)
    def __str__(self):
        return self.excel

class DataStore(models.Model):    
    language = models.CharField(max_length=100)
    sourcetype = models.CharField(max_length=100)
    data = models.CharField(max_length=100000)
    def __str__(self):
        return self.language