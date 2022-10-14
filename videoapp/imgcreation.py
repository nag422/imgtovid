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

def trailer():
    # print(settings.MEDIA_ROOT)
    # df = pd.read_excel("E:/imgtovid/videorender/media/post_images/ft_NEoai2A.xlsx", encoding='utf-8')
    # print(df)
    #mycol.delete_many({})
    return "done"
def write_image(text, windowwidth,output_filename,output_filename_final,IMAGE_WIDTH,IMAGE_HEIGHT,IF,SPACING,changetext,author,temporaryfilename,background_img):
    
    # setup
    text = wrap_text(text,windowwidth)
    img = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))

    # background
    back = Image.open(background_img, 'r')
    img_w, img_h = back.size
    bg_w, bg_h = img.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    img.paste(back, offset)

    # text
    font = IF
    draw = ImageDraw.Draw(img)
    img_w, img_h = img.size
    x = (img_w // 2)
    y = img_h // 2
    textsize = draw.multiline_textsize(text, font=IF, spacing=SPACING)

    text_w, text_h = textsize
    x -= (text_w // 2)
    y -= (text_h // 2)-changetext
    # het=int(input("enter + for top and enter - for down alignment"))
    # y -= text_h+(het)
    draw.multiline_text(align="center", xy=(x, y), text=text, fill=(255, 255, 255), font=font, spacing=SPACING)
    draw = ImageDraw.Draw(img)

    # output
    
    img.save(settings.IMAGE_PROCESSING_URL+temporaryfilename)

    #  Second Version

    # setup
    text = wrap_text(text,windowwidth)
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (255, 255, 255))

    # background
    back = Image.open(background_img, 'r')
    img_w, img_h = back.size
    bg_w, bg_h = img.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    img.paste(back, offset)

    # text
    font = IF
    draw = ImageDraw.Draw(img)
    img_w, img_h = img.size
    x = (img_w // 2)
    y = img_h // 2
    textsize = draw.multiline_textsize(text, font=IF, spacing=SPACING)

    text_w, text_h = textsize
    x -= (text_w // 2)
    y -= (text_h // 2)-changetext
    # het=int(input("enter + for top and enter - for down alignment"))
    # y -= text_h+(het)
    draw.multiline_text(align="center", xy=(x, y), text=text, fill=(255, 255, 255), font=font, spacing=SPACING)
    draw = ImageDraw.Draw(img)

    # output
    img.save(settings.IMAGE_PROCESSING_URL+output_filename)
    # rotationnum = mycol.find().sort('id',-1)
    # try:
    #     sortingnum=int(rotationnum[0]['id'])+1
    # except:
    #     sortingnum=1
    # thisdict = {"id":sortingnum,"author":author,"filename":temporaryfilename}
    # mycol.insert_one(dict(thisdict))

    return output_filename


def image_trigger(image_name,typeofpost,author,fontref,pciname_dyn):
    
    
    path_source = settings.IMAGE_PROCESSING_URL
    print(image_name,typeofpost)
    print(author,fontref)
    print(pciname_dyn)
    
    if typeofpost == "YouTubeV":
        IMAGE_WIDTH = 1920
        IMAGE_HEIGHT = 1080
        # pciname_dyn = "YouTubeV"
        windowwidth = 40
    elif typeofpost == "InstagramS":
        IMAGE_WIDTH = 720
        IMAGE_HEIGHT = 1280
        # pciname_dyn = "InstagramS"
        windowwidth = 26
    elif typeofpost == "FacebookS":
        IMAGE_WIDTH = 1080
        IMAGE_HEIGHT = 1920
        # pciname_dyn = "FacebookS"
        windowwidth = 22
    elif typeofpost == "FacebookV":
        IMAGE_WIDTH = 1280
        IMAGE_HEIGHT = 720
        # pciname_dyn = "FacebookV"
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
        # pciname_dyn = "WhatsappS"
        windowwidth = 24
    else:
        return "none"


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

        for text in texts:
            FONT_SIZE,changetext,windowwidth = recommend_font_size(text,typeofpost)
            FONT = str(path_source) + 'font/'+fontref+'.ttf'
            select_background_image = str(path_source) +"curatedrefs/"+ str(pciname_dyn)

            IF = ImageFont.truetype(FONT, FONT_SIZE)

            COLOR = (255, 255, 255)
            SPACING = 16

            temporaryfilename = str(author) + "/"+str(cols_in)+"/pic" + str(i) + ".png"
            output_filename =  str(author) + "/"+str(cols_in)+"/pic" + str(i) + ".jpg"
            output_filename_final = str(path_source) + str(author) + "/" +str(cols_in)+"/pic" + str(i) + ".jpg".format(int(time.time()))
            write_image(text,windowwidth,output_filename, output_filename_final, IMAGE_WIDTH, IMAGE_HEIGHT, IF, SPACING,changetext,author,temporaryfilename,
                              background_img=select_background_image)
            i += 1


        # dir = joining_path+str(cols_in)

        # for item in os.listdir(dir):
        #     if item.endswith(".png"):
        #         single.append((dir , item))
        # custom_dir = path_source+"backgrounds"
        # custom_item = str(pciname_dyn)+".jpg"
        # single.append((custom_dir,custom_item))
        # forextra_requriement = 1
        # if len(single) > 0:
        #     final_img_to_vid(single,forextra_requriement,cols_in,path_source)






def recommend_font_size(text,pciname_dyn):
    
    l = len(text)
    print(l)

    # resize_heuristic = 0.9
    # resize_actual = 0.985
    # while l > 1:
    #     l = l * resize_heuristic
    #     size = size * resize_actual
    if pciname_dyn == "YouTubeV":
        windowwidth = 40
        if l > 0 and l <= 15:
            size = 9 * l
            changetext = -15
            windowwidth = 40

        elif l > 15 and l <= 28:
            size = 4 * l
            changetext = -15
            windowwidth = 40

        elif l > 28 and l <= 68:
            if l < 40:
                size = 3 * l
            else:
                size = 1.1 * l
            changetext = 0
            windowwidth = 40
        elif l > 68 and l <=98:
            size = 0.7 * l
            changetext = 25
            windowwidth = 40
        elif l >= 99 and l <=200:
            size = 0.4 * l
            changetext = -15
            windowwidth = 40
        elif l > 200 and l <= 300:
            size = 0.2 * l
            changetext = -15
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
            changetext = -15
            windowwidth = 10
        elif l > 15 and l <= 28:
            size = 4 * l
            changetext = -15
            windowwidth = 5
        elif l > 28 and l <= 67:
            size = 1.3 * l
            changetext = -45
            windowwidth = 5
        elif l > 68 and l <=98:
            size = 0.8 * l
            changetext = -45
            windowwidth = 10
        elif l > 99 and l <=200:
            size = 0.28 * l
            changetext = -15
            windowwidth = 15
        elif l > 200 and l <= 300:
            size = 0.18 * l
            changetext = -15
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
            changetext = -60
            windowwidth = 40
        elif l > 15 and l <= 28:
            size = 6 * l
            changetext = -80
            windowwidth = 10
        elif l > 28 and l <= 67:
            size = 1.2 * l
            changetext = -45
            windowwidth = 20
        elif l > 68 and l <= 98:
            size = 0.9 * l
            changetext = -45
            windowwidth = 10
        elif l > 99 and l <= 200:
            size = 0.4 * l
            changetext = -15
            windowwidth = 10
        elif l > 200 and l <= 300:
            size = 0.25 * l
            changetext = -20
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





    return int(size), changetext,windowwidth


def wrap_text(text, windowwidth):
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


def file_retrieve_user_folder(joining_path,cols_in,particular_path,stype):
    single = []
    
    dir = joining_path+str(cols_in)
    if particular_path == "detailed":
        if stype == "folders":
            for item in os.listdir(dir):
                single.append({"id":item,"source":item,"author":cols_in})
            
    else:
        if stype == "images":                        
            for item in os.listdir(os.path.join(dir, particular_path)):
                if item.endswith(".png"):
                    
                    single.append({"id":item,"source":item,"author":cols_in})
        
        elif stype == "excelfiles":
            for item in os.listdir(settings.IMAGE_PROCESSING_EXCEL+'/media/post_images'):
                if item.endswith(".xlsx"):                    
                    single.append({"id":item,"source":item,"author":cols_in})
        
        else:
            for item in os.listdir(os.path.join(dir, particular_path)):
                if item.endswith(".mp4") and 'with' in str(item):                    
                    single.append({"id":item,"source":item,"author":cols_in})



    #     if item.endswith(".png"):
    #         single.append((dir , item))
    # custom_dir = path_source+"backgrounds"
    # # custom_item = str(pciname_dyn)+".jpg"
    # single.append(custom_dir)
    # forextra_requriement = 1
    # if len(single) > 0:
    #     final_img_to_vid(single,forextra_requriement,cols_in,path_source)
    return single






def final_img_to_vid(pathsource,username,foldername,datalist,foritercount):
    cins = []
    checkingnum = 1
    incnum = 4

    
    for inum, ext in datalist:        
        input = str(inum)+str(username)+"/"+str(foldername)+"/"+str(ext)
        output = str(inum)+str(username)+"/" +str(foldername)+"/"+str(ext.split('.')[0]) + '_video.mp4'
        outputvid = str(inum)+str(username)+"/" +str(foldername)+"/"+ str(foldername) +str(foritercount)+'_withoutaudio.mp4'
####################        
##        if "background" in str(inum):
##            clips = ImageClip(input).set_duration(3)
        if checkingnum == 1:
            
            clips = ImageClip(input).set_duration(4)
            
            
        else:
            clips = ImageClip(input).set_duration(6)
            
        clips.write_videofile(output, fps=24,preset="ultrafast",threads=6)
        clips.close()

#####################
        finclip = VideoFileClip(output)


        if int(checkingnum) != 1:
            cinsdtring = finclip.set_start(incnum - 1).crossfadein(1)
            incnum += 5

        else:
            cinsdtring = finclip

        checkingnum += 1
        cins.append(cinsdtring)
        

    # outputvid = str(inum)+str(username)+"/"+str(foldername)+"/"+str(foritercount)+"withoutaudio.mp4"


    final_clip = CompositeVideoClip(cins, bg_color=[232, 252, 253])

    final_clip.write_videofile(outputvid, fps=24,preset="ultrafast",threads=4)

    #composition_extra(cins,inum,cols_in,forextra_requriement,originalpath)
    final_clip.close()
    for alls in cins:
        alls.close()

#     # finclip1 = VideoFileClip('C:/Users/Dell/Desktop/imgtovid/output/pic1.mp4')
#     # finclip2 = VideoFileClip('C:/Users/Dell/Desktop/imgtovid/output/pic2.mp4')
#     # finclip3 = VideoFileClip('C:/Users/Dell/Desktop/imgtovid/output/pic3.mp4')
#     # cins=[finclip1,finclip2.set_start(6 - 1).crossfadein(1),finclip3.set_start(11 - 1).crossfadein(1)]


    return outputvid







def image_trigger_custome(imwidth,imheight,picname,font,fontsize,windowposition,changetext,excel_file,author,windowwidth):
    
    
    path_source = settings.IMAGE_PROCESSING_URL
    
    
    IMAGE_WIDTH = int(imwidth)
    IMAGE_HEIGHT = int(imheight)
    pciname_dyn = picname
    fontref = font
    FONT_SIZE = fontsize
    windowwidth = windowwidth    
    image_name = excel_file
    

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

        for text in texts:
            # FONT_SIZE,changetext,windowwidth = recommend_font_size(text,pciname_dyn)
            FONT = str(path_source) + 'font/'+fontref+'.ttf'
            select_background_image = str(path_source) +"curatedrefs/"+ str(pciname_dyn)

            IF = ImageFont.truetype(FONT, FONT_SIZE)

            COLOR = (255, 255, 255)
            SPACING = 16

            temporaryfilename = str(author) + "/"+str(cols_in)+"/pic" + str(i) + ".png"
            output_filename = str(author) + "/"+str(cols_in)+"/pic" + str(i) + ".jpg"
            output_filename_final = str(path_source) + str(author) + "/" +str(cols_in)+"/pic" + str(i) + ".jpg".format(int(time.time()))
            write_image(text,windowwidth,output_filename, output_filename_final, IMAGE_WIDTH, IMAGE_HEIGHT, IF, SPACING,changetext,author,temporaryfilename,
                              background_img=select_background_image)
            i += 1
    return "done"

        







# Audio Mixing

def composition(soundclip,pathing,exactpath,incnum):

    # outputvid = str(inum)+"/"+str(cols_in)+"withoutaudio.mp4"
    try:
        # outputvid = str(inum)+"/"+str(cols_in)+"withoutaudio.mp4"
        videoclip = VideoFileClip(pathing)
        audioclip = AudioFileClip(str(soundclip)).set_duration(videoclip.duration)
        videoclip.audio = audioclip
        output_withaudio = str(exactpath)+str(incnum)+"withaudio_final.mp4"
        videoclip.write_videofile(output_withaudio,fps=24,preset="ultrafast",threads=4)
        videoclip.close()
        audioclip.close()
    except Exception as e:
        print(e)
        pass
    return "done"

def composition_combine(soundclip,pathing,exactpath,incnum,username,foldername):
    
    # outputvid = str(inum)+"/"+str(cols_in)+"withoutaudio.mp4"
    cins = []
    try:
        for pic in pathing:
            path_source = settings.IMAGE_PROCESSING_URL+str(username)+"/"+foldername+'/'+pic  
            finclip = VideoFileClip(path_source)
            cins.append(finclip)
        final_clip = concatenate(cins)
        combinedvid = str(exactpath)+str(incnum)+"combine.mp4"
        final_clip.write_videofile(combinedvid,fps=24,preset="ultrafast",threads=4)
        final_clip.close()
            

       
        # outputvid = str(inum)+"/"+str(cols_in)+"withoutaudio.mp4"
        videoclip = VideoFileClip(combinedvid)
        audioclip = AudioFileClip(str(soundclip)).set_duration(videoclip.duration)
        videoclip.audio = audioclip
        output_withaudio = str(exactpath)+str(incnum)+"withaudio_final.mp4"
        videoclip.write_videofile(output_withaudio,fps=24,preset="ultrafast",threads=4)
        videoclip.close()
        audioclip.close()
    except Exception as e:
        print(e)
        pass
    return "done"