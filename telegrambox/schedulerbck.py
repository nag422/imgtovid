from telegram import bot
import requests
from telegram.ext import Updater
from django.conf import settings
import os
import math
import numpy as np
import pandas as pd

import urllib.parse
# from telegram import MessageEntity
from telegram.ext import CommandHandler, MessageHandler, Filters

import requests
from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import register_events
urls = 'https://api.telegram.org/bot912095520:AAElRterw1tIshRFFVK4gbw42LaPcYMtheA/'

def msgjobstart(gap,timenow,endtime,jq,filenaming_excel,title,maxtime,arrayofids,symbs):
    def update_textmessage():
        x = datetime.now()
        js = (x.strftime("%d"))
        excel_printing(filenaming_excel,jq,gap,arrayofids,symbs)   
        print('schedule started')      

        # if int(js) >= int(endtime):
        #     scheduler.remove_job('kumaren')
        #     print('schedule closed')

    print('schedule Called')
    scheduler = BackgroundScheduler()   
    scheduler.add_job(update_textmessage, 'interval', hours = int(maxtime), id="kumaren")  
    scheduler.start()
    update_textmessage()
    return 'done'

def start(gap,timenow,endtime,jq,filenaming,filenaming_excel,title,maxtime):
    # print(gap,timenow)
    # print(endtime,jq)
    print(filenaming)
    
    def update_forecast():
        x = datetime.now()
        js = (x.strftime("%d"))
        excel_printing(filenaming,jq,filenaming_excel)         
        if int(js) >= int(endtime):
            scheduler.remove_job('kumaren')
    
    def update_photocast():
        
        x = datetime.now()
        js = (x.strftime("%M"))
        photo_printing(filenaming,jq,filenaming_excel)         
        if int(js) >= int(endtime):
            scheduler.remove_job('kumaren')

    def video_printing():
        
        x = datetime.now()
        js = (x.strftime("%M"))
        photo_printing(filenaming,jq,filenaming_excel)         
        if int(js) >= int(endtime):
            scheduler.remove_job('kumaren')



    
    scheduler = BackgroundScheduler()    
    # scheduler.add_job(update_forecast, 'interval',[scheduler], seconds=1, id="kumaren")

    if title == "photoupload":
        scheduler.add_job(update_photocast, 'interval', hours=int(maxtime), id="kumaren")
    elif title == "videoupload":
        scheduler.add_job(video_printing, 'interval', hours=int(maxtime), id="kumaren") 
    elif title == "textmessage":
        scheduler.add_job(update_forecast, 'interval', hours=int(maxtime), id="kumaren")       
    scheduler.start()        
     
  
def excel_printing(filenaming_excel,jq,gap,arrayofids,symbs):
    PARAMS = {'address':'home'} 
    agents = {"random":"Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0"}
    headers = {'User-Agent': agents['random']}
    

    df = pd.read_excel(settings.IMAGE_PROCESSING_EXCEL+'/'+filenaming_excel, encoding='utf-8')

    for cols_in in (df.columns).values.flatten():
        single = []
        texts = df[cols_in].tolist()
    print(texts)
    for alls in texts:
        params_text = {"text":alls}
        final_text = urllib.parse.urlencode(params_text, doseq=True)  
         
        for cgvalue in arrayofids:
            jq = urls+'sendMessage'+'?chat_id='+str(symbs)+str(cgvalue)+'&'    
            requests.get(url = jq+final_text+'&parse_mode=HTML',headers=headers, params = PARAMS)
            time.sleep(2)
        time.sleep(gap+2)
    return 'done'

def photo_printing(filenaming,jq,filenaming_excel,gap):
    PARAMS = {'address':'home'} 
    agents = {"random":"Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0"}
    headers = {'User-Agent': agents['random'],'content-type': 'multipart/form-data'}   
    print('trigger photo printing',filenaming)
    # Excel Processing
    df = pd.read_excel(settings.IMAGE_PROCESSING_EXCEL+'/'+filenaming_excel, encoding='utf-8')

    for cols_in in (df.columns).values.flatten():
        single = []
        texts = df[cols_in].tolist()

    for alls in zip(filenaming,texts):   
        final_text = 'http://localhost:8099/'+alls[0]+'&caption='+alls[1]+'&parse_mode=HTML'
        requests.get(url = jq+final_text,headers=headers, params = PARAMS)
        time.sleep(gap)
    return 'done'

def video_printing(filenaming,jq,filenaming_excel,gap):
    PARAMS = {'address':'home'} 
    agents = {"random":"Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0"}
    headers = {'User-Agent': agents['random'],'content-type': 'multipart/form-data'}   
    print('trigger photo printing',filenaming)
    # Excel Processing
    df = pd.read_excel(settings.IMAGE_PROCESSING_EXCEL+'/'+filenaming_excel, encoding='utf-8')

    for cols_in in (df.columns).values.flatten():
        single = []
        texts = df[cols_in].tolist()

    for alls in zip(filenaming,texts):   
        final_text = 'http://localhost:8099/'+alls[0]+'&caption='+alls[1]+'&parse_mode=HTML'
        requests.get(url = jq+final_text,headers=headers, params = PARAMS)
        time.sleep(gap)
    return 'done'