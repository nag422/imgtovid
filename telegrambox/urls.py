from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from . import views

urlpatterns = [
    path('telegram',views.telegram,name="telegram"),
    path('telegram/add/',views.telegramadd.as_view(),name="telegramadd"),
    path('telegram/post/',views.telegrampostViw.as_view(),name="telegrampost"),
    path('telegram/schedule/',views.telegramscheduleViw.as_view(),name="telegramschedule"),
    path('scrape/',views.scraperview.as_view(),name="scraper"),
    path('scht/<slug:act>',views.scht,name="scht"),
    
    
]

