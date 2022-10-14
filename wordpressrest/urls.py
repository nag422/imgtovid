from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from . import views

urlpatterns = [
    
    path('screencreator',views.screencreator.as_view(),name="livepost"),
    path('getimages',views.getimages.as_view(),name="getimages"),
    path('wordpresscrud/<slug:q>',views.wordpresscrud.as_view(),name="wpcreate"),
  
    
    
    
    
]

