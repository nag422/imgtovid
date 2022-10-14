import os
import sys
import subprocess
import psutil
import math
from typing import Any
import time
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip, AudioClip, \
    CompositeVideoClip
import moviepy.video.fx.all as vfx
from moviepy.video.fx.resize import resize
from moviepy.video.tools.segmenting import findObjects
import numpy as np
from moviepy.editor import *
import pandas as pd
from PIL import Image, ImageFont, ImageDraw
import random
import time
from django.conf import settings
import pymongo
from pymongo import MongoClient
from pymongo.errors import (BulkWriteError,
                            ConfigurationError,
                            InvalidName,
                            OperationFailure)
from pymongo.results import (BulkWriteResult,
                             DeleteResult,
                             InsertOneResult,
                             InsertManyResult,
                             UpdateResult)

client = MongoClient(settings.MONGO_URL)      

db = client.videorender
mycol=db["videoapp_imagestore"]

staticdirectory = settings.STATIC_DIR
cpucores = 5

def wrap_text_extras(text, windowwidth):
    new_text = ""
    new_sentence = ""
    for word in text.split(" "):
        delim = " " if new_sentence != "" else ""
        new_sentence = new_sentence + delim + word
        if len(new_sentence) > windowwidth:
            new_text += "\n" + new_sentence
            new_sentence = ""
    new_text += "\n" + new_sentence
    return new_text

def write_image_extras(text, windowwidth,output_filename,output_filename_final,IMAGE_WIDTH,IMAGE_HEIGHT,IF,SPACING,changetext,effectbackground_img,temporaryfilename,background_img):
    
    try:
        
        # setup
        if windowwidth == 0:
            windowwidth = IMAGE_HEIGHT - int(IMAGE_HEIGHT/4)
            
        text = wrap_text_extras(text,windowwidth)
        img = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))

        # background
        try:
            back = Image.open(background_img, 'r')
        except:
            
            back = Image.open(background_img, 'r')
        img_w, img_h = back.size
        bg_w, bg_h = img.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        img.paste(back, offset)

        #Effect Paste
        try:
            back = Image.open(effectbackground_img, 'r')
            img_w, img_h = back.size
            bg_w, bg_h = img.size
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
            img.alpha_composite(back, offset)
        except:
            pass

        # text
        font = IF
        draw = ImageDraw.Draw(img)
        img_w, img_h = img.size
        x = (img_w // 2)
        y = img_h // 2
        textsize = draw.multiline_textsize(text, font=IF, spacing=SPACING)
        
##
        text_w, text_h = textsize
        x -= (text_w // 2)
        y -= (text_h // 2)- changetext
        # het=int(input("enter + for top and enter - for down alignment"))
        # y -= text_h+(het)
        draw.multiline_text(align="center", xy=(x+5, y+5), text=text, fill=(0, 0, 0), font=font, spacing=SPACING)
        draw.multiline_text(align="center", xy=(x, y), text=text, fill=(255, 255, 255), font=font, spacing=SPACING)
        
        
        draw = ImageDraw.Draw(img)

        # output
        img.save(settings.IMAGE_PROCESSING_URL+temporaryfilename)

        #Second Edition
        # 
        # setup
        if windowwidth == 0:
            windowwidth = IMAGE_HEIGHT - int(IMAGE_HEIGHT/4)
            
        text = wrap_text_extras(text,windowwidth)
        img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))

        # background
        try:
            back = Image.open(background_img, 'r')
        except:
            
            back = Image.open(background_img, 'r')
        img_w, img_h = back.size
        bg_w, bg_h = img.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        img.paste(back, offset)

        #Effect Paste
        try:
            back = Image.open(effectbackground_img, 'r')
            img_w, img_h = back.size
            bg_w, bg_h = img.size
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
            img.alpha_composite(back, offset)
        except:
            pass

        # text
        font = IF
        draw = ImageDraw.Draw(img)
        img_w, img_h = img.size
        x = (img_w // 2)
        y = img_h // 2
        textsize = draw.multiline_textsize(text, font=IF, spacing=SPACING)
        
##
        text_w, text_h = textsize
        x -= (text_w // 2)
        y -= (text_h // 2)- changetext
        # het=int(input("enter + for top and enter - for down alignment"))
        # y -= text_h+(het)
        draw.multiline_text(align="center", xy=(x+5, y+5), text=text, fill=(0, 0, 0), font=font, spacing=SPACING)
        draw.multiline_text(align="center", xy=(x, y), text=text, fill=(255, 255, 255), font=font, spacing=SPACING)
        
        
        draw = ImageDraw.Draw(img)

        # output
        img.save(settings.IMAGE_PROCESSING_URL+output_filename)        
    except Exception as e:
        print("this is: ",e)
        

    # for converting to jpeg

    # im = Image.open(output_filename)
    # rgb_im = im.convert('RGB')
    # rgb_im.save(output_filename_final)

    # END for converting to jpeg

    return output_filename

def recommend_font_size_extra(text,pciname_dyn):
    l = len(text)
    print(l)

    # resize_heuristic = 0.9
    # resize_actual = 0.985
    # while l > 1:
    #     l = l * resize_heuristic
    #     size = size * resize_actual
    if pciname_dyn == "YouTubeV":
        
        if l > 0 and l <= 15:
            size = 9 * l
            changetext = 200
            windowwidth = 40

        elif l > 15 and l <= 28:
            size = 4 * l
            changetext = 200
            windowwidth = 40

        elif l > 28 and l <= 68:
            if l < 40:
                size = 3 * l
            else:
                size = 1.1 * l
            changetext = 200
            windowwidth = 40
        elif l > 68 and l <=98:
            size = 0.7 * l
            changetext = 200
            windowwidth = 40
        elif l > 98 and l <=200:
            size = 0.4 * l
            changetext = 200
            windowwidth = 40
        elif l > 200 and l <= 300:
            size = 0.2 * l
            changetext = 200
            windowwidth = 40

    elif pciname_dyn == "WhatsappS":
        size = 60
        # resize_heuristic = 3
        # resize_actual = 3
        # while l > 1:
        #     l = l * resize_heuristic
        #     size = size * resize_actual
        if l > 0 and l <= 15:
            size = 9 * l
            changetext = 300
            windowwidth = 10
        elif l > 15 and l <= 28:
            size = 4 * l
            changetext = 300
            windowwidth = 5
        elif l > 28 and l <= 67:
            if l < 40:
                size = 3 * l
            else:
                size = 1.2 * l
            changetext = 210
            windowwidth = 5
        elif l > 68 and l <=98:
            size = 0.8 * l
            changetext = 150
            windowwidth = 10
        elif l > 99 and l <=200:
            size = 0.28 * l
            changetext = 150
            windowwidth = 15
        elif l > 200 and l <= 300:
            size = 0.18 * l
            changetext = 150
            windowwidth = 15
    elif pciname_dyn == "FacebookS":
        size = 60

        if l > 0 and l <= 15:
            size = 9 * l
            changetext = -15
            windowwidth = 10
        elif l > 15 and l <= 28:
            size = 4 * l
            changetext = -15
            windowwidth = 5
        elif l > 28 and l <= 67:
            if l < 40:
                size = 7 * l
            else:
                size = 1.7 * l
            changetext = -45
            windowwidth = 10
        elif l > 68 and l <= 98:
            size = 0.9 * l
            changetext = -45
            windowwidth = 10
        elif l > 99 and l <= 200:
            size = 0.4 * l
            changetext = -15
            windowwidth = 10
        elif l > 200 and l <= 300:
            size = 0.2 * l
            changetext = -15
            windowwidth = 25

    elif pciname_dyn == "FacebookV":
        size = 60
        if l > 0 and l <= 15:
            size = 9 * l
            changetext = -60
            windowwidth = 40
        elif l > 15 and l <= 28:
            size = 4 * l
            changetext = -80
            windowwidth = 40
        elif l > 28 and l <= 67:
            size = 0.8 * l
            changetext = -45
            windowwidth = 40
        elif l > 68 and l <= 98:
            size = 0.5 * l
            changetext = -45
            windowwidth = 40
        elif l > 99 and l <= 200:
            size = 0.2 * l
            changetext = -15
            windowwidth = 50
        elif l > 200 and l <= 300:
            size = 0.12 * l
            changetext = -15
            windowwidth = 50
    elif pciname_dyn == "InstagramS":
        windowwidth = 40
        if l > 0 and l <= 15:
            size = 11 * l
            changetext = 300
            windowwidth = 40
        
        elif l > 15 and l <= 28:            
            size = 6 * l
            changetext = 300
            windowwidth = 10
        elif l > 28 and l <= 67:
            if l < 40:
                size = 3 * l
            else:
                size = 1.2 * l
            
            changetext = 300
            windowwidth = 20
        elif l > 68 and l <= 98:
            size = 0.9 * l
            changetext = 300
            windowwidth = 10
        elif l > 99 and l <= 200:
            size = 0.4 * l
            changetext = 300
            windowwidth = 10
        elif l > 200 and l <= 300:
            size = 0.25 * l
            changetext = 350
            windowwidth = 20
    elif pciname_dyn == "TIktokS":
        if l > 0 and l <= 15:
            size = 11 * l
            changetext = -60
            windowwidth = 40
        elif l > 15 and l <= 28:
            size = 6 * l
            changetext = -80
            windowwidth = 10
        elif l > 28 and l <= 67:
            size = 1.5 * l
            changetext = -45
            windowwidth = 10
        elif l > 68 and l <= 98:
            size = 0.9 * l
            changetext = -45
            windowwidth = 20
        elif l > 99 and l <= 200:
            size = 0.4 * l
            changetext = -15
            windowwidth = 13
        elif l > 200 and l <= 300:
            size = 0.25 * l
            changetext = -20
            windowwidth = 20
    elif pciname_dyn == "TwitterV":
        size = 60
        if l > 0 and l <= 15:
            size = 9 * l
            changetext = -60
            windowwidth = 40
        elif l > 15 and l <= 28:
            size = 4 * l
            changetext = -80
            windowwidth = 40
        elif l > 28 and l <= 67:
            size = 0.8 * l
            changetext = -45
            windowwidth = 40
        elif l > 68 and l <= 98:
            size = 0.5 * l
            changetext = -45
            windowwidth = 40
        elif l > 99 and l <= 200:
            size = 0.2 * l
            changetext = -15
            windowwidth = 50
        elif l > 200 and l <= 300:
            size = 0.12 * l
            changetext = -15
            windowwidth = 50
    else:        
        resize_heuristic = 0.9
        resize_actual = 0.985
        changetext = 0
        windowwidth = 0
        while l > 1:            
            l = l * resize_heuristic
            size = size * resize_actual
        
    return int(size), changetext,windowwidth



def extra_image_on_text_trigger(search_path,username):
    path_source = settings.IMAGE_PROCESSING_URL
    originalpath = settings.IMAGE_PROCESSING_URL
    # joining_path = path_source +str(username)+"/"+"reference_backs/"+str(search_path)+'/'
    joining_path = path_source +str(username)+"/"+"reference_backs/"
    pciname_dyn =[]
    
    dir = joining_path
    single = []
    for item in os.listdir(dir):               
        
        if item.endswith(".png"):
            single.append((joining_path,item))

    
    return single  







def image_trigger_dynamic(image_name,typeofpost,author,fontref,typeofsubmit):
    starttime = time.time()
    path_source = settings.IMAGE_PROCESSING_URL
    originalpath = settings.IMAGE_PROCESSING_URL
    
    
    if typeofpost == "YouTubeV":
        IMAGE_WIDTH = 1920
        IMAGE_HEIGHT = 1080
        # typeofsubmit = "YouTubeV"
        windowwidth = 40
    elif typeofpost == "InstagramS":
        IMAGE_WIDTH = 1080
        IMAGE_HEIGHT = 1920
        # typeofsubmit = "InstagramS"
        windowwidth = 26
    elif typeofpost == "FacebookS":
        IMAGE_WIDTH = 1080
        IMAGE_HEIGHT = 1920
        # pciname_dyn = "FacebookS"
        windowwidth = 22
    elif typeofpost == "FacebookV":
        IMAGE_WIDTH = 1280
        IMAGE_HEIGHT = 720
        # typeofsubmit = "FacebookV"
        windowwidth = 40
    elif typeofpost == "TwitterV":
        IMAGE_WIDTH = 1280
        #IMAGE_HEIGHT = 1024
        IMAGE_HEIGHT = 720
        # pciname_dyn = "TwitterV"
        windowwidth = 40
    elif typeofpost == "TIktokS":
        IMAGE_WIDTH = 1080
        IMAGE_HEIGHT = 1920
        # pciname_dyn = "TIktokS"
        windowwidth = 30
    elif typeofpost == "WhatsappS":
        IMAGE_WIDTH = 750
        IMAGE_HEIGHT = 1334
        # typeofsubmit = "WhatsappS"
        windowwidth = 24
    else:
        return
        
        
        
    
    df = pd.read_excel(settings.IMAGE_PROCESSING_EXCEL+str(image_name), encoding='utf-8')
    

    for cols_in in (df.columns).values.flatten():
        single = []
        texts = df[cols_in].tolist()
        joining_path = path_source + str(author) + "/"
        
        temporary_path = settings.IMAGE_PROCESSING_URL+ str(author) + "/"
        try:
            #os.mkdir(os.path.join(joining_path, cols_in))
            os.mkdir(os.path.join(temporary_path, cols_in))
        except:
            pass


        i = 1
        single_array = extra_image_on_text_trigger(cols_in,author)
        for text in texts:
            FONT_SIZE,changetext,windowwidth = recommend_font_size_extra(text,typeofsubmit)
            FONT = str(path_source) + 'font/'+fontref+'.ttf'
            try:
                
                try:
                    pciname_dyn = single_array[i]
                except:
                    
                    pciname_dyn = single_array[random.randint(1, len(single_array))]
                    
                select_background_image = str(pciname_dyn[0])+ str(pciname_dyn[1])
##                print("background:  ",select_background_image)
                if i == 1:
                    FONT_SIZE = 70
                IF = ImageFont.truetype(FONT, FONT_SIZE)

                COLOR = (255, 255, 255)
                SPACING = 16

                temporaryfilename = str(author) + "/"+str(cols_in)+"/pic" + str(i) + ".png"
                output_filename =  str(author) + "/"+str(cols_in)+"/pic" + str(i) + ".jpg"
                output_filename_final = str(path_source) + "output/"+str(author)+"/"+str(cols_in)+"/pic" + str(i) + ".jpg".format(int(time.time()))
                effectbackground_img = str(path_source) + "Effects/effect.png"
                print(write_image_extras(text,windowwidth,output_filename, output_filename_final, IMAGE_WIDTH, IMAGE_HEIGHT, IF, SPACING,changetext,effectbackground_img,temporaryfilename,
                                  background_img=select_background_image))
            except Exception as e:
                print(e)
                pass


            i += 1

    #readymade_images_and_video("rendered_images",cols_in)
    seconds = time.time() - starttime
    print('Time Taken:', time.strftime("%H:%M:%S",time.gmtime(seconds)))

    return 'none'
