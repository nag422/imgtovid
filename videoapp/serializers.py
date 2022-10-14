from rest_framework import serializers
from .models import ImageWriter,ImageStore,ExcelFIleStore

class ImageWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageWriter
        fields = '__all__'

class ImageStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageStore
        fields = '__all__'

class ExcelFIleStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFIleStore
        fields = '__all__'