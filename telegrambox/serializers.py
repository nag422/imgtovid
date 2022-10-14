from rest_framework import serializers
from .models import AddTelegram,ExcelFIleShedule

class AddTelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddTelegram
        fields = '__all__'


class ExcelFIleScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFIleShedule
        fields = '__all__'