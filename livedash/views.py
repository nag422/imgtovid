from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.conf import settings
import os
import math
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import Permission, User
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.files.base import ContentFile
from .models import BackgroundImagesStore,ExcelFileStore,DataStore
from .serializers import BackgroundImagesStoreSerializer,ExcelFileStoreSerializer,DataStoreSerializer
from .forms import BackgroundImagesStoreForm
from .imagestoredb import imagestore,Excelstore
class livepost(APIView):
    def post(self, request, *args, **kwargs):
        try:
            filesfile = request.FILES.getlist('image')   
            imagestore(request,filesfile)     
            print(files)
            
        except Exception as e:
            print(e)
            pass         

        context = {
            "response": 'request.data'
        }
        
        return Response(context)

class livefilepost(APIView):
    def post(self, request, *args, **kwargs):
        language = request.data['language']
        sourcetype = request.data['sourcetype']
        if str(sourcetype) == 'excel':
            filesfile = request.FILES.getlist('excel')
            Excelstore(request,filesfile,sourcetype,language)
        else:
            filesfile = request.data['textboxdata']            
            
            Excelstore(request,filesfile,sourcetype,language)
             

        context = {
            "response": 'request.data'
        }
        
        return Response(context)
    
    def get(self, request, *args, **kwargs):
        data = BackgroundImagesStore.objects.all()
        
        serializer = BackgroundImagesStoreSerializer(data,many=True)

        data2 = ExcelFileStore.objects.all()
        
        serializer2 = ExcelFileStoreSerializer(data2,many=True)
        context = {
            "response": serializer.data,
            "result": serializer2.data,
        }
        
        return Response(context)


class livefileretrieve(APIView):
    def post(self, request, *args, **kwargs):
        l = request.data['imagelist']
        
        
        single = []
        for i in l:
            data = BackgroundImagesStore.objects.get(id=int(i))  
            single.append(str(data.image)) 
        print(single)
        
        
        context = {
            "response": single
        }
        
        return Response(context)
    
    def get(self, request, *args, **kwargs):
        
        l = request.data['imagelist']
        
        single = []
        for i in l:
            data = BackgroundImagesStore.objects.get(id=int(i))  
            single.append(str(data)) 
        
        print(single)
        context = {
            "response": single
        }
        
        return Response(context)

class livefileretrievetext(APIView):
    def post(self, request, *args, **kwargs):
        l = request.data['imagelist']       
        
        single = []
        for i in l:
            data = ExcelFileStore.objects.get(id=int(i)) 
             
      
        context = {
            "response": data.data
        }
        
        return Response(context)

class deleteimgs(APIView):
    def post(self, request, *args, **kwargs):
        l = request.data['imagelist']       
        import os       
        
        for i in l:
            data = BackgroundImagesStore.objects.get(id=int(i)).delete()
            os.remove(settings.IMAGE_PROCESSING_EXCEL+'/'+str(data))
            
      
        context = {
            "response": l
        }
        return Response(context)

class deletetexts(APIView):
    def post(self, request, *args, **kwargs):
        l = request.data['textlist'] 
        print(l.split(','))
        for i in l.split(','):
            data = ExcelFileStore.objects.get(id=int(i)).delete()
            
   
        context = {
            "response": l
        }
        return Response(context)
    
    



    


