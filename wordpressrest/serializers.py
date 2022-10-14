from rest_framework import serializers
from .models import seleniumimagestore

class seleniumimagestoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = seleniumimagestore
        fields = '__all__'