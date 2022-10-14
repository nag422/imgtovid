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
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import AddTelegram,ExcelFIleShedule
from .serializers import AddTelegramSerializer,ExcelFIleScheduleSerializer
from .schedulerbck import start,msgjobstart
from .scraping import scrapingurl,gefile,delfile
import urllib.parse

from telegram import bot
import requests
from telegram.ext import Updater


# from telegram import MessageEntity
from telegram.ext import CommandHandler, MessageHandler, Filters
urls = 'https://api.telegram.org/bot912095520:AAElRterw1tIshRFFVK4gbw42LaPcYMtheA/'
def telegram(request):
    if request.method == "POST":
        ct = (request.POST['chat'])
        # TELEGRAM_BOT_TOKEN="912095520:AAElRterw1tIshRFFVK4gbw42LaPcYMtheA"        
        # updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
        # https://api.telegram.org/bot912095520:AAElRterw1tIshRFFVK4gbw42LaPcYMtheA/sendPhoto?chat_id=@videosofd&photo=https://www.filmibeat.com/ph-big/2020/03/rashmika-mandanna_158407715140.jpg
        # https://api.telegram.org/bot912095520:AAElRterw1tIshRFFVK4gbw42LaPcYMtheA/sendPhoto?chat_id=g422683669&photo=https://www.filmibeat.com/ph-big/2020/03/rashmika-mandanna_158407715140.jpg
        
         
       
        return HttpResponse('done')

        
    else:
        return render(request,'telegram.html')


class telegramadd(APIView):
    def post(self, request, *args, **kwargs):        
        addtype = request.data['title']
        textdata = request.data['textboxdata']          
          
        Telegramadd_serializer = AddTelegramSerializer(data=request.data)   
        
        
        if Telegramadd_serializer.is_valid():
            Telegramadd_serializer.save()
            return Response(Telegramadd_serializer.data, status=status.HTTP_201_CREATED)        
        
        return Response(Telegramadd_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):        
        group = []        
        channels = []        
        incr = 1
        for groups in AddTelegram.objects.filter(title="group"):
            val = (groups.textboxdata).split(',')
            for i in val:
                if str(i) != 'null':
                    group.append({'id':incr,'dbid':groups.id,'val':i})            
                    incr +=1
        
        incr =1  
        for channel in AddTelegram.objects.filter(title="channel"):            
            val = (channel.textboxdata).split('\n')
            for i in val:
                if str(i) != 'null':
                    channels.append({'id':incr,'dbid':channel.id,'val':i})            
                    incr +=1

       
        

        context = {
            'group':group,
            'channels':channels

        }

            
        
        return Response(context, status=status.HTTP_201_CREATED)


# class telegramadd(APIView):
    


class telegrampostViw(APIView):
    def post(self, request, *args, **kwargs):        
        title = request.data['sendnowtitle']
        cgvalue = request.data['groupdatatab2']
        messagetype = request.data['masgtyptab2']
        msg = request.data['msg']   
        arrayofids = cgvalue.split(',')

        
        params = {"text":msg}
        fintal_text = urllib.parse.urlencode(params, doseq=True)

        PARAMS = {'address':'home'}
        agents = {"random":"Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0"}
        headers = {'User-Agent': agents['random']}
        for cgvalue in arrayofids:
            if title == "group":
                if str(messagetype) == "photoupload":                
                    jq = urls+'sendPhoto'+'?chat_id=-'+str(cgvalue)+'&photo=https://www.filmibeat.com/ph-big/2020/03/rashmika-mandanna_158407715140.jpg'
                                
                else:
                    jq = urls+'sendMessage'+'?chat_id=-'+str(cgvalue)+'&'+str(fintal_text)
                    r = requests.get(url = jq,headers=headers, params = PARAMS)
                    print(jq)
            elif title == "channel":
                if str(messagetype) == "photoupload":
                    jq = urls+'sendPhoto'+'?chat_id=@'+str(cgvalue)+'&photo=https://www.filmibeat.com/ph-big/2020/03/rashmika-mandanna_158407715140.jpg'
                    print(jq)
                else: 
                    jq = urls+'sendMessage'+'?chat_id=@'+str(cgvalue)+'&'+str(fintal_text)
                    r = requests.get(url = jq,headers=headers, params = PARAMS)
                
                
          
        # Telegramadd_serializer = AddTelegramSerializer(data=request.data)   
        
        
        # if Telegramadd_serializer.is_valid():
        #     Telegramadd_serializer.save()
        context = {
            'group':'group',
            'channels':'channels'

        }
        return Response(context, status=status.HTTP_201_CREATED)        
        
        # return Response(Telegramadd_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class telegramscheduleViw(APIView):
    def post(self, request, *args, **kwargs):        
        title = request.data['scheduletitle']
        cgvalue = request.data['groupdatatab2']
        messagetype = request.data['masgtyptab2']
        timenow = 1 
        endtime = 1   
        gap = int(request.data['gap'])
        maxtime = int(request.data['maxtime'])
        arrayofids = cgvalue.split(',')
        
#######################################################################################
        # cgvalue = 'videosofd'
        # urllib.parse.urlencode(params, doseq=True)
        # title -- group or channel
        # grouptype -- channel value or group value
        # messagetype -- sendMessage send Photo
        # print(title,messagetype,cgvalue)
        # start(gap,timenow,endtime,)
########################################################################################
        urls = 'https://api.telegram.org/bot912095520:AAElRterw1tIshRFFVK4gbw42LaPcYMtheA/'
        
        if str(messagetype) != 'textmessage':
            try:
                files1 = (request.FILES.getlist('msg'))
                files = (request.FILES.getlist('msgimages'))            
                if str(messagetype) == 'videoupload':
                    filenamecuration = 'media/schedule/videos/'
                elif str(messagetype) == 'photoupload':
                    filenamecuration = 'media/schedule/photos/'


                incr = 1
                mediafiles = []
                for f in files:
                    extension = f.name[f.name.rfind("."):]
                    pictitled = str(f.name)
                    filenaming = filenamecuration+str(f.name)
                    with open(filenaming, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                            mediafiles.append(filenaming)
                        incr+=1
            

                incr = 1
                
                for f in files1:
                    extension = f.name[f.name.rfind("."):]
                    pictitled = str(f.name)
                    filenaming_excel = 'media/schedule/'+str(f.name)
                    with open(filenaming_excel, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)                          

                        incr+=1

            except:
                pass

        else:
            try:
                files1 = (request.FILES.getlist('msg'))
                incr = 1
                print("its excel block")
                    
                for f in files1:
                    extension = f.name[f.name.rfind("."):]
                    pictitled = str(f.name)
                    filenaming_excel = 'media/schedule/'+str(f.name)
                    with open(filenaming_excel, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)                          

                        incr+=1
            except Exception as e:
                print(e)
                pass




        if title == "group":
            if str(messagetype) == "photoupload":                
                jq = urls+'sendPhoto'+'?chat_id=-'+str(cgvalue)+'&photo='
                start(gap,timenow,endtime,jq,mediafiles,filenaming_excel,messagetype,maxtime)      
            elif str(messagetype) == "videoupload":
                jq = urls+'sendPhoto'+'?chat_id=-'+str(cgvalue)+'&video='
                start(gap,timenow,endtime,jq,mediafiles,filenaming_excel,messagetype,maxtime)         
                                 
            else:
                jq = urls+'sendMessage'+'?chat_id=-'+str(cgvalue)+'&'
                symbs = '@'
                msgjobstart(gap,timenow,endtime,jq,filenaming_excel,messagetype,maxtime,arrayofids,symbs)
                
        elif title == "channel":
            if str(messagetype) == "photoupload":
                jq = urls+'sendPhoto'+'?chat_id=@'+str(cgvalue)+'&photo='
                start(gap,timenow,endtime,jq,mediafiles,filenaming_excel,messagetype,maxtime)         
                
            elif str(messagetype) == "videoupload":
                jq = urls+'sendVideo'+'?chat_id=@'+str(cgvalue)+'&video='
                start(gap,timenow,endtime,jq,mediafiles,filenaming_excel,messagetype,maxtime)        
                       
            else:                
                jq = urls+'sendMessage'+'?chat_id=@'+str(cgvalue)+'&'   
                symbs = '@'                           
                msgjobstart(gap,timenow,endtime,jq,filenaming_excel,messagetype,maxtime,arrayofids,symbs)    
                

       
        

        
        context = {
            'group':'group',
            'channels':'channels'

        }
        return Response(context, status=status.HTTP_201_CREATED)        
        
        # return Response(Telegramadd_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class scraperview(APIView):
    def post(self, request, *args, **kwargs):
        links = request.data['textboxdata']
        linklist = links.split('\n')
        
        
        try:
            
            linklist.remove('')
            
        except Exception as e: 
                       
            pass

        try:
            
            linklist.remove('null')
            
        except Exception as e:                        
            pass
     
        for url in linklist:
            
            scrapingurl(url)


        
        context = {
            'group':'group',
            'channels':'channels'

        }
        return Response(context, status=status.HTTP_201_CREATED) 
    def get(self, request, *args, **kwargs):
        gefile()       
        with open("static/scrape/scraping.xlsx", 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=spam.xlsx'        
        
        return response

    def delete(self, request, *args, **kwargs):
        delfile()
        context = {
            'group':'group',
            'channels':'channels'

        }
        return Response(context, status=status.HTTP_201_CREATED) 
        



def scht(request,act):
    start(act)
   
    return HttpResponse('Done')