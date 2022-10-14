from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from . import views

urlpatterns = [
    
    path('livepost',views.livepost.as_view(),name="livepost"),
    path('livefilepost',views.livefilepost.as_view(),name="livefilepost"),
    path('livefileretrieve',views.livefileretrieve.as_view(),name="livefileretrieve"),
    path('livefileretrievetext',views.livefileretrievetext.as_view(),name="livefileretrievetext"),
    path('deleteimgs',views.deleteimgs.as_view(),name="deleteimgs"),
    path('deletetexts',views.deletetexts.as_view(),name="deletetexts")
  
    
    
    
    
]

