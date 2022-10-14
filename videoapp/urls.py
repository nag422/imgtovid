from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from . import views

urlpatterns = [
    path('',views.frontend,name="frontend"),
    path('home/<slug:user>/<slug:spath>/<slug:stype>', views.home,name="homeview"),
    path('posts/', views.PostView.as_view(), name= 'posts_list'),
    path('register', views.RegisterView.as_view(), name= 'registration'),
    path('video/<slug:username>/<int:loopiter>', views.VideoView.as_view(), name= 'video_process'),
    path('deleter/<slug:username>/<slug:foldername>', views.DeleteHandleall.as_view(), name= 'deletehandler'),
    path('trail',views.trail,name="trail"),
    path('download/<slug:username>/<slug:dwntype>',views.DownloadView.as_view(),name="download"),    
    path('imagedownload/<slug:username>/<slug:foldername>/<slug:name>',views.ImageDownload.as_view(),name="downloadimg"),
    path('customimage/<slug:foldername>',views.CustomImage.as_view(),name="custimg"),
    path('cp',views.CustomPost.as_view(),name="custompost"),
    path('pdf/<slug:author>/<slug:foldername>',views.pdfViewPost.as_view(),name="pdfviewpost"),
    path('excel/<slug:author>/<slug:foldername>',views.ExcelDownloadView.as_view(),name="exceldownload"),
    path('bulk/<slug:author>/<slug:foldername>/<slug:stype>',views.BulkProcessingView.as_view(),name="bulkviewpost"),
    path('imgwalk/', views.imgWalkView.as_view(), name= 'img_walk')
    
]

