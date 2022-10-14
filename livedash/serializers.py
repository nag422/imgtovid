from rest_framework import serializers
from .models import BackgroundImagesStore,ExcelFileStore,DataStore

class BackgroundImagesStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundImagesStore
        fields = '__all__'

class ExcelFileStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFileStore
        fields = '__all__'

class DataStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataStore
        fields = '__all__'