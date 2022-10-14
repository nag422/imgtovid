from django import forms
from .models import BackgroundImagesStore

class BackgroundImagesStoreForm(forms.ModelForm):
    class Meta:
        model = BackgroundImagesStore
        fields = ('image', )