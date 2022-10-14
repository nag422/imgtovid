from django.db import models


class AddTelegram(models.Model):
    title = models.CharField(max_length=100)
    textboxdata = models.CharField(max_length=100)    

    def __str__(self):
        return self.title

class ExcelFIleShedule(models.Model):
    multirefiles = models.FileField(upload_to='schedule')
    
    

    def __str__(self):
        return self.multirefiles