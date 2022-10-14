from django.db import models

# Create your models here.
def get_upload_path(instance, filename):
    sub_dir = instance.slug if hasattr(instance, 'slug') else str(instance.pk)
    return 'company_{0}/{1}'.format(instance.title, filename)

    #return os.path.join(instance.__class__.__name__.lower(), sub_dir, filename)
class ImageWriter(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image = models.FileField(upload_to='post_images')
    background = models.CharField(max_length=100)
    font = models.CharField(max_length=100,default="blank")
    pictype = models.CharField(max_length=100,default="blank")
    # multirefiles = models.ImageField(upload_to=get_upload_path)

    def __str__(self):
        return self.title

class ImageStore(models.Model):
    filename = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    

    def __str__(self):
        return self.filename

class ExcelFIleStore(models.Model):
    image = models.FileField(upload_to='post_images')
    
    

    def __str__(self):
        return self.image