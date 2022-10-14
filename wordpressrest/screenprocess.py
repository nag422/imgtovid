import os
from django.conf import settings
import time
import sys
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
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

db = client.videorender
mycol=db["wordpressrest_seleniumimagestore"]
catname = "wordpressrest_wordpressbox"
from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.chrome.options import Options

import numpy
from lxml import html
import urllib.request
import requests
import json
import re
import math
import numpy as np
from urllib.parse import urlparse
from collections import Counter
from dateutil.relativedelta import relativedelta
from calendar import monthrange
#from fake_useragent import UserAgent

import nltk
import time
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags,ne_chunk
from pprint import pprint
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from wordcloud import WordCloud, STOPWORDS
from bs4 import BeautifulSoup
import threading

import datetime

import base64
from PIL import Image
from io import BytesIO
nlp = spacy.load('en_core_web_sm') 
location = "dotndot"
PARAMS = {'address':location} 
# ua = UserAgent()
# agents = {'ie': ua.ie, 'msie': ua.msie, 'opera': ua.opera,
#         'chrome': ua.chrome, 'google': ua.google, 'firefox': ua.firefox,
#         'safari': ua.safari, 'random': ua.random}
agents = {"random":"Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0"}    
headers = {'User-Agent': agents['random']}


chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=834,745")
chrome_path = r'C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\selenium\\webdriver\\chrome\\chromedriver.exe'


def selscrape(urls,selecttype):
    
    rotationnum = mycol.find().sort('id',-1)
    try:
        sortingnum=int(rotationnum[0]['id'])+1
    except Exception as e:
        print(e)
        sortingnum=1

    reslist = []
    if str(selecttype) == 'other':
        driver = webdriver.Chrome(chrome_path,options=chrome_options)
        
        # urls = ['https://www.reelnreel.com/','https://www.digitalndigital.com/','https://rankur.com']
        j=sortingnum
        for i in urls:
            try:
                responce = requests.get(i , headers=headers,verify=True)
                print(responce.status_code)
                if int(responce.status_code) >= 200 and int(responce.status_code) <400:
                    driver.set_page_load_timeout(30)
                    driver.get(i)
                    time.sleep(3)          
                            
                    png = driver.get_screenshot_as_png() 
                    im = Image.open(BytesIO(png))
                    width, height = im.size 
                    im = im.crop((0, 0, width-18, height)) # defines crop points
                    im.save('static/seleniumimages/screenshot'+str(j)+'.png',quality=30,optimize=True) # saves new cropped image
                    thisdict = {"id":j,"imagename":'static/seleniumimages/screenshot'+str(j)+'.png',"url":str(i),"title":'title',"description":'description',"type":selecttype}
                    mycol.insert_one(dict(thisdict))
                    j+=1
                    reslist.append(str(i))
            except Exception as e:
                print(e)
                pass
        driver.quit()
    elif str(selecttype) == "video":
        j=sortingnum        
        title =""
        for i in urls:       

            forvidid = i.replace('https://www.youtube.com/watch?v=','')
            
            try:
                title,description,image = videocreation(forvidid)
            except:
                title = "Video Not Available"
                description = "Video Not Available"

            if 'https://www.youtube.com/watch?v=' not in str(i):
                i = 'https://www.youtube.com/watch?v='+str(i)
            
            thisdict = {"id":j,"imagename":image,"url":str(i),"title":title,"description":description,"type":selecttype}
            mycol.insert_one(dict(thisdict))
            j+=1
            reslist.append(str(i))
    elif str(selecttype) == "channel":
        j=sortingnum
        driver = webdriver.Chrome(chrome_path,options=chrome_options)
        for i in urls:      
            if "https://www.youtube.com/channel/" in str(i):      
                channelId = i.replace('https://www.youtube.com/channel/','')
                title,description = createchannels(channelId)
            else:
                channelId = i.replace('https://www.youtube.com/user/','')
                title,description = createchannelsusers(channelId)
            
            
        
        # urls = ['https://www.reelnreel.com/','https://www.digitalndigital.com/','https://rankur.com']
        
            try:
                responce = requests.get(i , headers=headers,verify=True)
                print(responce.status_code)
                if int(responce.status_code) >= 200 and int(responce.status_code) <400:
                    
                    driver.get(i)
                    time.sleep(3)          
                            
                    png = driver.get_screenshot_as_png() 
                    im = Image.open(BytesIO(png))
                    width, height = im.size 
                    im = im.crop((0, 0, width-18, height)) # defines crop points
                    im.save('static/seleniumimages/screenshot'+str(j)+'.png',quality=30,optimize=True) # saves new cropped image
            except Exception as e:
                print(e)
                pass
            
            
            thisdict = {"id":j,"imagename":'static/seleniumimages/screenshot'+str(j)+'.png',"url":str(i),"title":title,"description":description,"type":selecttype}
            mycol.insert_one(dict(thisdict))
            j+=1
            reslist.append(str(i))
        driver.quit()

    return reslist

def image_determination(imgpath):
    # Opens a image in RGB mode 
    im = Image.open(imgpath) 
    
    # Size of the image in pixels (size of orginal image) 
    # (This is not mandatory) 
    width, height = im.size 
    
    # Setting the points for cropped image 
    left = 0
    top = 0
    right = -10
    bottom = 0
    
    # Cropped image of above dimension 
    # (It will not change orginal image) 
    im1 = im.crop((left, top, right, bottom)) 
    
    # Shows the image in image viewer 
    im1.save(imgpath) 

def wordpresscreatepost(l,posttitle,selecttype):    
    imageidcollector = []
    imageidtitler = []
    imageurlcollector = []
    embedtitlecollector =[]
    embeddesccollector =[]
    formedesc =[]
    user = "reelnreel"
    # password = "kAs5 GQ7E Gojd bit7 npT3 IVGI" #Durvani
    password = "Nz74 ONBR Vlzt ar8R bJUS aw0F" #ReelnReel
    # password = "wtpZ K1uv RB4g hi8r pkpN Npe8" #localhost
    # password = "l17D O5GL kaf0 KaCS RXYw 49LT" #Dotndot
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())
    if str(selecttype) != "video":
        for i in l:
            vidurl = i['url']
            if "https://www.youtube.com/channel/" in str(vidurl):
                imgfilename = vidurl.replace('https://www.youtube.com/channel/','')                
            else:
                imgfilename = vidurl.replace('https://www.youtube.com/user/','')
                
            embedtitlecollector.append(i['title'])
            embeddesccollector.append(i['description'])     
            i = i['imagename']        
            imgPath = str(settings.IMAGE_PROCESSING_EXCEL)+'/'+str(i)        
            data = open(imgPath, 'rb').read()
            url = "https://reelnreel.com/wp-json/wp/v2/media"
            
            

            header = {'Authorization': 'Basic ' + token.decode('utf-8'),
                'Content-Type': 'image/png',                
                'Content-Disposition' : 'attatchment; filename="'+imgfilename+'.png"'} 
                            
            
            post = {
            
            'status'   : 'publish'        
            
            }
            

            responce = requests.post(url , data = data, headers=header, json=post, verify=True)
            jk = responce.json()
                    
            imageidcollector.append(jk['id'])
            imageurlcollector.append(vidurl)
            imageidtitler.append(jk['guid']['rendered'])
    elif str(selecttype) == "video":
        for i in l:
            vidurl = i['url']
            if "https://www.youtube.com/watch?v=" in str(vidurl):
                imgfilename = vidurl.replace('https://www.youtube.com/watch?v=','')                
            else:
                imgfilename = vidurl.replace('https://www.youtube.com/watch?v=','')
                
            embedtitlecollector.append(i['title'])
            embeddesccollector.append(imgfilename)
            formedesc.append(i['description'])
    

    strval = []
    strval1 = []

    if str(selecttype) == "video":
        for embedtitle,videourl,forme in zip(embedtitlecollector,embeddesccollector,formedesc):
            embedval = '<h2><b>'+embedtitle+'</b></h2><div style="margin:3%;text-align: center;"> <iframe width="560" height="315" src="https://www.youtube.com/embed/'+videourl+'" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
            embedval1 = '<h2><b>'+embedtitle+'</b></h2><div style="margin:3%;text-align: center;"> <iframe width="560" height="315" src="https://www.youtube.com/embed/'+videourl+'" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><br><p>'+str(forme)[:200]+'</p></div>'
            strval.append(embedval)
            strval1.append(embedval1)
    else:
        for imageid,imagename,videourl,embedtitle,embeddesc in zip(imageidcollector,imageidtitler,imageurlcollector,embedtitlecollector,embeddesccollector):
            if str(selecttype) == "other":
                embedval = '<div style="margin:3%;text-align: center;"> <img src="'+imagename+'" alt="" width="600" height="314" class="aligncenter size-full wp-image-"'+str(imageid)+'" />' \
                    '<br /><div style="text-align:center;padding:3%;"><h2><a href="'+videourl+'" target="_blank">'+videourl+'</a></h2></div></div>'
            
            elif str(selecttype) == "channel":
                embedval = '<h2><a href="'+str(videourl)+'" target="_blank">'+embedtitle+'</h2> <div style="margin:3%;text-align: center;"> <img src="'+imagename+'" alt="" width="600" height="314" class="aligncenter size-full wp-image-"'+str(imageid)+'" />' \
                    '<br /></div>'

            strval.append(embedval)
        
    
    url = "https://reelnreel.com/wp-json/wp/v2/posts"
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}

    post = {

     'title'    : str(posttitle),
     'status'   : 'draft',
     'content'  : ('\n').join(strval)    
     
    }

    
    # fo = open(str(posttitle)+'.txt','w',encoding="utf-8")
    # fo.write(str(('\n').join(strval1)))
    # fo.close()
    responce = requests.post(url , headers=header, json=post, verify=True)
    print(responce)

    return imageidcollector,imageidtitler


def docxwordpresscreate(contentlist,selecttype):    
    imageidcollector = []
    imageidtitler = []
    imageurlcollector = []
    embedtitlecollector =[]
    embeddesccollector =[]
    formedesc =[]
    user = "digitalndigital"
    # password = "kAs5 GQ7E Gojd bit7 npT3 IVGI" #Durvani
    # password = "rYMP qfXG 6X1J vhqZ x0en fGMr" #ReelnReel
    # password = "wtpZ K1uv RB4g hi8r pkpN Npe8" #localhost
    # password = "eIJS CUjq KIXV 3M0M JX0k 1BU0" #Dotndot
    password = "8etq NHLb aVFs 9LGo MMwi V4v4"   #Digitalndigital
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode()) 
      
    posttitle = contentlist[0].replace('</p>','')
    print(contentlist)
    url = "https://digitalndigital.com/wp-json/wp/v2/"+str(selecttype)
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
    str1=""    

    post = {

     'title'    : str(posttitle),
     'status'   : 'draft',
     'content'  : str((str1.join(contentlist[1:])).replace('\xc2\xa0',' '))    
     
    }

    
    # fo = open(str(posttitle)+'.txt','w',encoding="utf-8")
    # fo.write(str(('\n').join(strval1)))
    # fo.close()
    responce = requests.post(url , headers=header, json=post, verify=True)
    print(responce)

    return imageidcollector,imageidtitler

def wordpressupdatepost(l,posttitle,selecttype,textboxdata,operation,sitename):    
    imageidcollector = []
    imageidtitler = []
    imageurlcollector = []

    catname = 'wordpressrest_wordpressbox'
    mycol=db[catname]

    for i in l.split(','):
        for x in mycol.find({"type": str(selecttype),"postid":int(i),"url":sitename}):
            dbpostcontent = x['originalcontent']
            dbposttitle = x['title']
        
        url = str(sitename)+"/wp-json/wp/v2/posts/{}".format(str(i))
        
        user = "reelnreel"
        # password = "kAs5 GQ7E Gojd bit7 npT3 IVGI" #Durvani
        password = "Nz74 ONBR Vlzt ar8R bJUS aw0F" #ReelnReel
        # password = "wtpZ K1uv RB4g hi8r pkpN Npe8" #localhost
        # password = "l17D O5GL kaf0 KaCS RXYw 49LT" #Dotndot
        credentials = user + ':' + password
        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}           
        
        if operation == "substract":
            post = {
            'title': str(dbposttitle).replace(posttitle),
            'status'   : 'publish',
            'content'  : str(dbpostcontent).replace(textboxdata)          
            
            }
        elif operation == "prep":
            post = {
            'title': str(posttitle)+str(dbposttitle),
            'status'   : 'publish',
            'content'  : str(textboxdata) + str(dbpostcontent)         
            
            }

            
        else:
            post = {
            'title': str(dbposttitle) + str(posttitle),
            'status'   : 'publish',
            'content'  : dbpostcontent + str(textboxdata)          
            
            }
        

        responce = requests.put(url , headers=header, json=post)
        jk = responce.json()      
            
    return imageidcollector,imageidtitler

def retriever(sitename,selecttype,currentpage):
    single = []
    catname = 'wordpressrest_wordpressbox'
    mycol=db[catname]

    if int(currentpage) <= 1:
        currentpage = 0    
    

    for x in mycol.find({"type": selecttype,"url":sitename}).skip(int(currentpage) * 10).limit(10):  
        thisdict = x
        thisdict.pop("_id")
        single.append(thisdict)
    return single


def dbdeleter(l,sitename,selecttype):
    single = []
    catname = 'wordpressrest_wordpressbox'
    mycol=db[catname]
    # for every in l.split(','):
    #     myquery = ({"type": selecttype,"url":sitename,"postid":int(every)})
    #     mycol.delete_one(myquery)
    mycol.delete_many({})
    return single

def filterretriever(sitename,selecttype,currentpage,searchin,searchword):
    single = []
    catname = 'wordpressrest_wordpressbox'
    mycol=db[catname]
    
    for thisdict in mycol.find({"type": str(selecttype)}):        
        thisdict.pop("_id")
        if str(searchword).lower() in (thisdict[str(searchin)]).lower():
            single.append(thisdict)

    
    return single


def wordpress_api_request_processor(URL,selecttype):
    if str(selecttype) == "posts":
        location = "echoice"
        import tldextract
        import datetime
        ext = tldextract.extract(URL)
        o_endpoint = (ext.domain)
        API_ENDPOINT = URL+"/wp-json"
        POST_API_ENDPOINT = URL+"/wp-json/wp/v2/posts"
        
        agents = {"random":"Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0"}

        headers = {'User-Agent': agents['random']}
            
        PARAMS = {'address':location}
        r = requests.get(url = POST_API_ENDPOINT,headers=headers, params = PARAMS)    
        data = r.json()  
        catname = 'wordpressrest_wordpressbox'
        mycol=db[catname]
        
        r = requests.get(url = POST_API_ENDPOINT, headers=headers,params = PARAMS)
        headers_r = json.dumps(dict(r.headers))
        y = json.loads(headers_r)
        try:
            Pages = (y['X-WP-TotalPages'])
        except:
            Pages = (y['x-wp-totalpages'])
        
        rotationnum = mycol.find().sort("id",-1)
        try:
            j=int(rotationnum[0]['id'])+1
        except:
            j=1
        
        
        def Posts_thread_1(from_range,numofpages_round):       
            Posts_thead_source(from_range,numofpages_round)
            return "done"
        def Posts_thread_2(from_range,numofpages_round):        
            Posts_thead_source(from_range,numofpages_round)
            return "done"

        def Posts_thead_source(from_range,numofpages_round):
            for iterationpost in range(int(from_range),int(numofpages_round)+1):
                API_ENDPOINT = POST_API_ENDPOINT+"?page="+str(iterationpost)
                try:
                    threadr = requests.get(url = API_ENDPOINT,headers=headers, params = PARAMS)
                    data = threadr.json()
                
                    for i in data:
                        internallinks = []
                        externallinks = []
                        internallinks_hash = []
                        postid = (i['id'])
                        date_pub = i['date']
                        
                        modified_date = i['modified']
                        guid = i['guid']['rendered']
                        slug = i['slug']
                        status = i['status']
                        type_post = i['type']
                        link = i['link']
                        title = i['title']['rendered']
                        titlesoup = BeautifulSoup(title,'lxml')
                        title = titlesoup.text
                        content = i['content']['rendered']
                        excerpt = i['excerpt']['rendered']
                        author = i['author']
                        
                        featured_media = i['featured_media']
                        comment_status = i['comment_status']
                        ping_status = i['ping_status']
                        format_post = i['format']
                        categories = i['categories']
                        tags = i['tags']
                        
                        formatingtime = "%Y-%m-%dT%H:%M:%S"
                        pubdate = datetime.datetime.strptime(date_pub, formatingtime)
                        modifieddate = datetime.datetime.strptime(modified_date, formatingtime)
                        soup = BeautifulSoup(content,'lxml')
                        ilink = ""
                        for i in soup.findAll('a',href=True):  
                            ilink = str(i.get('href'))               
                                        
                            try:
                                if "mailto:" not in str(ilink):
                                    if str(o_endpoint) in str(ilink) or str(ilink).startswith('.'):
                                        internallinks.append(str(ilink))
                                    elif '#' in ilink and str(o_endpoint) in str(ilink):                                
                                        internallinks_hash.append(str(ilink))
                                    elif 'http' in ilink and str(o_endpoint) not in str(ilink):
                                        externallinks.append(str(ilink))
                            except Exception as e:
                                print(e)
                                return
                        ############# <Title Analysis> ##############
                        spacecounter_title =  title.count(' ')  
                        titlewords = title.split(' ')          
                        titlecharslength = len(title)-(spacecounter_title)            
                        
                        ############# </Title Analysis> ##############
                        
                        ############# <Content Analysis> ##############
                        content_processor = re.sub("<.*?>", " ", content)
                        spacecounter_content = content_processor.count(' ')
                        contentwords = [x.strip() for x in content_processor.split(' ') if x.strip()]            
                        contentcharslength = len(content_processor)-(spacecounter_content)
                        ############# </Content Analysis> ##############
                        try:
                            soup = BeautifulSoup(content_processor,'lxml')
                        except:
                            content_processor = "none"
                            soup = BeautifulSoup(content_processor,'lxml')                        
                        rtime = (((len(contentwords))*0.36)/100)
                        
                        countdocs = 0  
                        if countdocs == 0:
                            autname = 'admin'
                            mydict = {"postid":postid,"date": pubdate,"modified_date":modifieddate,"guid":guid,"slug": slug,"url":URL,"titleprops":titlewords,
                            "contentprops":contentwords,"status":status,"type":"posts","link":link,"title":title,"author":author,
                            "featured_media":featured_media,"comment_status":comment_status,"ping_status":ping_status,
                            "format_post":format_post,"categories":categories,"tags":tags,"titlecharslength":titlecharslength,
                            "contentcharslength":contentcharslength,
                            "internallinks":internallinks,"internallinks_hash":internallinks_hash,"externallinks":externallinks,
                            "content":str(soup.text),"internallinks_count":len(internallinks),"externallinks_count":len(externallinks),
                            "rtime":rtime}             
                            mycol.insert_one(mydict)                
                                
                except Exception as e:
                    print("Posts Indecs Issue:",e)
                    pass
            print('Posts_thread_All Completed')
            return "Posts_thread_All Completed"
        
        numofpages_round = int(math.floor(int(Pages)/2))
        t1 = threading.Thread(target=Posts_thread_1,args = (1, numofpages_round), name='t1') 
        from_range = numofpages_round
        
        t2 = threading.Thread(target=Posts_thread_2,args = (from_range,int(math.floor(int(Pages)))), name='t2')  
        t1.start() 
        time.sleep(2)
        print("t1:  ", numofpages_round)
        t2.start() 
        print("t2:  "+str(from_range), int(math.floor(int(Pages))))
        time.sleep(2)
        t1.join() 
        t2.join()
    else:
        return 'done'

    return 'done'

########################################################################<Wordpress_api__Comments>#########################################################

########################################################################<Wordpress_api_Master_Handler>#################################################################

def wordpress_api_request_fetching_data(URL,selecttype):
    print('its called')
    breaking_thread = 0
    if breaking_thread == 0:        
        breaking_thread+=1
        location = "echoice"
        PARAMS = {'address':location}
        # agents = {'ie': ua.ie, 'msie': ua.msie, 'opera': ua.opera,
        #         'chrome': ua.chrome, 'google': ua.google, 'firefox': ua.firefox,
        #         'safari': ua.safari, 'random': ua.random}
        agents = {'random': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"}
        headers = {'User-Agent': agents['random']}

        #API_ENDPOINT = "https://www.reelnreel.com/wp-json/wp/v2/posts?orderby=date&order=desc"
        
        import tldextract
        ext = tldextract.extract(URL)
        o_endpoint = (ext.domain)
        API_ENDPOINT = URL+"/wp-json"
        MEDIA_API_ENDPOINT = URL+"/wp-json/wp/v2/media"
        TAGS_API_ENDPOINT = URL+"/wp-json/wp/v2/tags"
        POST_API_ENDPOINT = URL+"/wp-json/wp/v2/posts"
        CAT_API_ENDPOINT = URL+"/wp-json/wp/v2/categories"
        PAGE_API_ENDPOINT = URL+"/wp-json/wp/v2/pages"
        USER_API_ENDPOINT = URL+"/wp-json/wp/v2/users"
        COMMENTS_API_ENDPOINT = URL+"/wp-json/wp/v2/comments"
        
        
        def resp_user_thread():
            resp_users = wordpress_api_users(USER_API_ENDPOINT,URL,location)
            if resp_users == "done":
                print("Pages Fetched")
            return "Pages Fetched"
            
        def resp_pages_thread():
            resp_pages = wordpress_api_pages(PAGE_API_ENDPOINT,URL,location,o_endpoint) 
            if resp_pages == "done":
                print("Pages Fetched")
            return "Pages Fetched"
    
        def resp_posts_thread():
            resp_posts = wordpress_api_request_processor(URL,selecttype) 
            if resp_posts == "done":
                print("Posts Fetched")  
            return "Posts Fetched"  
    
        def resp_media_thread():
            resp_media = wordpress_api_media(MEDIA_API_ENDPOINT,URL,location)
            if resp_media == "done":
                print("Media Fetched") 
            return "Media Fetched"
    
        def resp_tags_thread():
            resp_tags = wordpress_api_tags(TAGS_API_ENDPOINT,URL,location)
            if resp_tags == "done":
                print("Tags Fetched")
            return "Tags Fetched"
    
        def resp_cat_thread():
            resp_cat = wordpress_api_authors_categories(CAT_API_ENDPOINT,URL,location)
            if resp_cat == "done":
                print("Categories Fetched")
            return "Categories Fetched"
    
        def resp_comments_thread():
            resp_comments = wordpress_api_comments(COMMENTS_API_ENDPOINT,URL,location)   
            if resp_comments == "done":
                print("Comments Fetched")
            return "Comments Fetched"
        
        
        
        t1 = threading.Thread(target=resp_user_thread, name='t1')
        t2 = threading.Thread(target=resp_pages_thread, name='t2')   
        t3 = threading.Thread(target=resp_posts_thread, name='t3')
        t4 = threading.Thread(target=resp_media_thread, name='t4') 
        t5 = threading.Thread(target=resp_tags_thread, name='t5')   
        t6 = threading.Thread(target=resp_cat_thread, name='t6') 
        t7 = threading.Thread(target=resp_comments_thread, name='t7') 

        # starting threads 
       
        time.sleep(2)
        if str(selecttype) == "pages":
            t2.start() 
            time.sleep(2)
        elif str(selecttype) == "posts":    
            t3.start() 
            time.sleep(2)
        elif str(selecttype) == "media":
            t4.start() 
            time.sleep(2)             
        elif str(selecttype) == "tags":
            t5.start()
            time.sleep(2)
        elif str(selecttype) == "categories":
            t6.start() 
            time.sleep(2)
        elif str(selecttype) == "comments":
            t7.start() 
        elif str(selecttype) == "users":
            t1.start() 


        # wait until all threads finish 
        # time.sleep(2)
        # t2.join() 
        # t3.join() 
        # t4.join()
        
        # t6.join() 
        # t7.join() 
        # t5.join()
    else:
        return 0
    return 'data'
########################################################################</Wordpress_api_Master_Handler>#################################################################



########################################################################<Wordpress_api__Comments>#########################################################

def wordpress_api_comments(COMMENTS_API_ENDPOINT,URL,location):
    PARAMS = {'address':location} 
    r = requests.get(url = COMMENTS_API_ENDPOINT,headers=headers, params = PARAMS)
    headers_r = json.dumps(dict(r.headers))
    y = json.loads(headers_r)
    Pages = (y['X-WP-TotalPages'])
    mycol=db[catname]
    rotationnum = mycol.find().sort("id",-1)
    try:
        j=int(rotationnum[0]['id'])+1
    except:
        j=1
    for iterationpost in range(1,int(Pages)+1):
        try:
            API_ENDPOINT = COMMENTS_API_ENDPOINT+"?page="+str(iterationpost)
            r = requests.get(url = API_ENDPOINT,headers=headers,params = PARAMS)
            data = r.json()
            for i in data:            
                commentid = int(i['id'])
                comment_post = int(i['post'])
                comment_name = i['author_name']
                comment_author = i['author_url']
                comment_date = i['date']
                comment_content= i['content']['rendered']
                comment_link= i['link']
                comment_status= i['status']
                comment_url = i['author_avatar_urls']
                myquery = { "comment_post": int(comment_post) }
                
                
                mydict = {"id":j,"url":URL,"comment_post":comment_post,"comment_name":comment_name,"comment_author":'admin',
                "comment_date":comment_date,"comment_content":comment_content,"comment_link":comment_link,"comment_status":comment_status,
                "comment_url":comment_url,"type": "comments"}
                mycol.insert_one(mydict)
                j+=1
        except Exception as e:
            print('comments',e)
            pass
    return 'done'



########################################################################</Wordpress_api__Comments>########################################################
########################################################################<API_Categories>#################################################################
def wordpress_api_authors_categories(CAT_API_ENDPOINT,URL,location):
    
    PARAMS = {'address':location} 
    r = requests.get(url = CAT_API_ENDPOINT,headers=headers, params = PARAMS)
    headers_r = json.dumps(dict(r.headers))
    y = json.loads(headers_r)
    try:
        Pages = (y['X-WP-TotalPages'])
    except:
        Pages = (y['x-wp-totalpages'])
    mycol=db[catname]
    rotationnum = mycol.find().sort("id",-1)
    try:
        j=int(rotationnum[0]['id'])+1
    except:
        j=1
    for iterationpost in range(1,int(Pages)+1):
        try:
            API_ENDPOINT = CAT_API_ENDPOINT+"?page="+str(iterationpost)
            r = requests.get(url = API_ENDPOINT,headers=headers,params = PARAMS)
            data = r.json()
            for i in data:            
                catid = int(i['id'])
                cat_count = int(i['count'])
                cat_desc = i['description']
                cat_name = i['name']
                cat_slug = i['slug']
                cat_parent= i['parent']
                cat_link= i['link']
                cat_links = i['_links']["self"]
                myquery = { "catid": int(catid) }
               
                mydict = {"id":j,"url":URL,"catid": catid,"cat_count":cat_count,"cat_desc":cat_desc,"cat_name":cat_name,"cat_slug":cat_slug,"cat_parent":cat_parent,
                "cat_link":cat_link,"cat_links":cat_links,"type": "categories"}
                mycol.insert_one(mydict)
                j+=1
        except Exception as e:
            print('categories',e)
            pass
    return 'done'
########################################################################</API_Categories>#################################################################
########################################################################<API_Media>#######################################################################

def wordpress_api_media(MEDIA_API_ENDPOINT,URL,location):    
    PARAMS = {'address':location} 
    # ua = UserAgent()
    # agents = {'ie': ua.ie, 'msie': ua.msie, 'opera': ua.opera,
    #         'chrome': ua.chrome, 'google': ua.google, 'firefox': ua.firefox,
    #         'safari': ua.safari, 'random': ua.random}
    agents = {"random":"Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0"}    
    headers = {'User-Agent': agents['random']}
    r = requests.get(url = MEDIA_API_ENDPOINT,headers=headers,params = PARAMS)
    headers_r = json.dumps(dict(r.headers))
    y = json.loads(headers_r)
    try:
        Pages = (y['X-WP-TotalPages'])
    except:
        Pages = (y['x-wp-totalpages'])
    mycol=db[catname]
    rotationnum = mycol.find().sort("id",-1)
    try:
        j=int(rotationnum[0]['id'])+1
    except:
        j=1
    
    def media_thread_1(from_range,numofpages_round):       
        media_thead_source(from_range,numofpages_round,headers)
        return "done"
    def media_thread_2(from_range,numofpages_round):        
        media_thead_source(from_range,numofpages_round,headers)
        return "done"

    def media_thead_source(from_range,numofpages_round,headers):
        for iterationpost in range(from_range,int(numofpages_round)+1):
            API_ENDPOINT = MEDIA_API_ENDPOINT+"?page="+str(iterationpost)       
            try:
                               
                r = requests.get(url = API_ENDPOINT,headers=headers, params = PARAMS)
                data = r.json()
                for i in data:            
                    mediaid = int(i['id'])
                    media_date = (i['date'])
                    media_title = i['title']['rendered']
                    media_slug = i['slug']
                    alt_text = i['alt_text']
                    image_post = i['post']
                    source_url= i['source_url']
                    media_type= i['mime_type']
                    media_author = i['author']
                    
                    # ua = UserAgent()
                    # agents = {'ie': ua.ie, 'msie': ua.msie, 'opera': ua.opera,
                    #         'chrome': ua.chrome, 'google': ua.google, 'firefox': ua.firefox,
                    #         'safari': ua.safari, 'random': ua.random}
                    agents = {"random":"Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0"}
                    headers = {'User-Agent': agents['random']}
                    
                    try:
                        r = requests.get(source_url, headers = headers, stream=True) 
                        if r.status_code == 200:                   
                            filesize = math.floor(int(r.headers['content-length'])/1024)
                        else:
                            filesize = 0
                            
                    except:
                        filesize = 0  
                    
                    formatingtime = "%Y-%m-%dT%H:%M:%S"
                    media_date = datetime.datetime.strptime(media_date, formatingtime)     
                    mydict = {"url":URL,"mediaid":mediaid,"date":media_date,"media_title":media_title,
                    "media_slug":media_slug,"alt_text":alt_text,"image_post":image_post,"source_url":source_url,"media_type":media_type,
                    "media_author":media_author,"filesize":filesize,"type": "media"}
                    mycol.insert_one(mydict)
                    
            except Exception as e:
                print('media:',e)
                pass
        return "media fetched"
    numofpages_round = int(math.floor(int(Pages)/2))
    t1 = threading.Thread(target=media_thread_1,args = (1, numofpages_round), name='t1') 
    from_range = numofpages_round    
    t2 = threading.Thread(target=media_thread_2,args = (from_range,int(math.floor(int(Pages)))), name='t2')  
    time.sleep(2)
    t1.start() 
    time.sleep(2)
    print("t1:  ", numofpages_round)
    t2.start() 
    print("t2:  "+str(from_range), int(math.floor(int(Pages))))
    time.sleep(2)
    t1.join() 
    t2.join() 
    return 'done'
########################################################################</API_Media>######################################################################
def wordpress_api_tags(TAGS_API_ENDPOINT,URL,location):
    PARAMS = {'address':location} 
    r = requests.get(url = TAGS_API_ENDPOINT,headers=headers, params = PARAMS)
    headers_r = json.dumps(dict(r.headers))
    y = json.loads(headers_r)
    try:
        Pages = (y['X-WP-TotalPages'])
    except:
        Pages = (y['x-wp-totalpages'])
    mycol=db[catname]
    rotationnum = mycol.find().sort("id",-1)
    try:
        j=int(rotationnum[0]['id'])+1
    except:
        j=1
    def tags_thread_1(from_range,numofpages_round):       
        tags_thead_source(from_range,numofpages_round,headers)
        return "done"
    def tags_thread_2(from_range,numofpages_round):        
        tags_thead_source(from_range,numofpages_round,headers)
        return "done"
    def tags_thead_source(from_range,numofpages_round,headers):
        
        for iterationpost in range(from_range,int(numofpages_round)+1):
            try:
                API_ENDPOINT = TAGS_API_ENDPOINT+"?page="+str(iterationpost)
                r = requests.get(url = API_ENDPOINT,headers=headers, params = PARAMS)
                data = r.json()
                for i in data:            
                    catid = int(i['id'])
                    cat_count = int(i['count'])
                    cat_desc = i['description']
                    cat_name = i['name']
                    cat_slug = i['slug']
                    cat_type= i['taxonomy']
                    cat_link= i['link']
                    cat_links = i['_links']["self"]
                    
                    mydict = {"url":URL,"catid": catid,"cat_count":cat_count,"cat_desc":cat_desc,"cat_name":cat_name,"cat_slug":cat_slug,
                    "cat_link":cat_link,"cat_links":cat_links,"type": 'tags'}
                    mycol.insert_one(mydict)
                    
            except Exception as e:
                print('tags: ',e)
                pass
        return "Done"
    
    numofpages_round = int(math.floor(int(Pages)/2))
    t1 = threading.Thread(target=tags_thread_1,args = (1, numofpages_round), name='t1') 
    from_range = numofpages_round
    
    t2 = threading.Thread(target=tags_thread_2,args = (from_range,int(math.floor(int(Pages)))), name='t2')  
    t1.start() 
    time.sleep(2)
    print("t1:  ", numofpages_round)
    t2.start() 
    print("t2:  "+str(from_range), int(math.floor(int(Pages))))
    time.sleep(2)
    t1.join() 
    t2.join()

    return 'done'



########################################################################API_Pages#################################################################
def wordpress_api_pages(PAGE_API_ENDPOINT,URL,location,o_endpoint):    
    PARAMS = {'address':location}
    r = requests.get(url = PAGE_API_ENDPOINT,headers=headers, params = PARAMS)    
    headers_r = json.dumps(dict(r.headers))
    y = json.loads(headers_r)
    try:
        Posts = (y['X-WP-Total'])
    except:
        Posts = (y['x-wp-total'])
    try:
        Pages = (y['X-WP-TotalPages'])
    except:
        Pages = (y['x-wp-totalpages'])
    mycol=db[catname]
    rotationnum = mycol.find().sort("id",-1)
    try:
        j=int(rotationnum[0]['id'])+1
    except:
        j=1
    for iterationpost in range(1,int(Pages)+1):
        try:
            API_ENDPOINT = PAGE_API_ENDPOINT+"?page="+str(iterationpost)
            r = requests.get(url = API_ENDPOINT,headers=headers,params = PARAMS)        
            data = r.json()

            for i in data:
                internallinks = []
                externallinks = []
                internallinks_hash = []
                postid = (i['id'])
                date_pub = i['date']
                modified_date = i['modified']
                guid = i['guid']['rendered']
                slug = i['slug']
                status = i['status']
                type_post = i['type']
                link = i['link']
                title = i['title']['rendered']
                titlesoup = BeautifulSoup(title,'lxml')
                title = titlesoup.text
                content = i['content']['rendered']
                excerpt = i['excerpt']['rendered']
                author = i['author']
                featured_media = i['featured_media']
                comment_status = i['comment_status']
                ping_status = i['ping_status']            
                
                formatingtime = "%Y-%m-%dT%H:%M:%S"
                pubdate = datetime.datetime.strptime(date_pub, formatingtime)
                modifieddate = datetime.datetime.strptime(modified_date, formatingtime)
                soup = BeautifulSoup(content,'lxml')
                ilink = ""
                for i in soup.findAll('a',href=True):  
                    ilink = str(i.get('href'))               
                                
                    try:
                        if "mailto:" not in str(ilink):
                            if str(o_endpoint) in str(ilink) or str(ilink).startswith('.'):
                                internallinks.append(str(ilink))
                            elif '#' in ilink and str(o_endpoint) not in str(ilink):                                
                                internallinks_hash.append(str(ilink))
                            elif 'http' in ilink and str(o_endpoint) not in str(ilink):
                                externallinks.append(str(ilink))
                    except Exception as e:
                        print(e)
                        pass
                
            
                ############# <Title Analysis> ###############

                spacecounter_title =  title.count(' ')  
                titlewords = title.split(' ')          
                titlecharslength = len(title)-(spacecounter_title)            
                
                ############# </Title Analysis> ##############
                
                ############# <Content Analysis> ###############

                content_processor = re.sub("<.*?>", " ", content)
                spacecounter_content = content_processor.count(' ')
                contentwords = [x.strip() for x in content_processor.split(' ') if x.strip()]            
                contentcharslength = len(content_processor)-(spacecounter_content)

                ################## </Content Analysis> ################

                try:
                    soup = BeautifulSoup(content_processor,'lxml')
                except:
                    content_processor = "none"
                    soup = BeautifulSoup(content_processor,'lxml') 

                rtime = (((len(contentwords))*0.36)/100)
                
                autname = 'admin'
                mydict = {"id":j,"postid":postid,"date": pubdate,"modified_date":modifieddate,"guid":guid,"slug": slug,"url":URL,"titleprops":titlewords,
                "contentprops":contentwords,"titlecharslength":titlecharslength,"contentcharslength":contentcharslength,
                "internallinks":internallinks,"internallinks_hash":internallinks_hash,"externallinks":externallinks,
                "status":status,"type":"pages","link":link,"title":title,"author":author,"featured_media":featured_media,"comment_status":comment_status,
                "ping_status":ping_status, "content":str(soup.text),"internallinks_count":len(internallinks),
                "rtime":rtime,"externallinks_count":len(externallinks),"type":"pages"}             
                mycol.insert_one(mydict)
                j+=1
        except Exception as e:
            print(e)
            pass
    return 'done'
########################################################################</API_Pages>#################################################################


########################################################################<API_USERS>#################################################################
def wordpress_api_users(USER_API_ENDPOINT,URL,location):
    PARAMS = {'address':location}
    r = requests.get(url = USER_API_ENDPOINT, headers=headers,params = PARAMS)    
    headers_r = json.dumps(dict(r.headers))
    y = json.loads(headers_r)
  
    try:
        Posts = (y['X-WP-Total'])
    except:
        try:
            Posts = (y['x-wp-total'])
        except:
            Posts = 0
    try:
        Pages = (y['X-WP-TotalPages'])
    except:
        try:
            Pages = (y['x-wp-totalpages'])
        except:
            Pages = 0
    
    mycol=db[catname]
    rotationnum = mycol.find().sort("id",-1)
    try:
        j=int(rotationnum[0]['id'])+1
    except:
        j=1
    for iterationpost in range(1,int(Pages)+1):
        try:
            API_ENDPOINT = USER_API_ENDPOINT+"?page="+str(iterationpost)
            r = requests.get(url = API_ENDPOINT, headers=headers,params = PARAMS)        
            data = r.json()

            for i in data:
                postid = (i['id'])
                name = (i['name'])
                description = (i['description'])
                avatar_urls = (i['avatar_urls'])
                mydict = {"id":j,"postid":postid,"name":name,"description":description,"avatar_urls":avatar_urls,"url":URL,"type":"users"}
                mycol.insert_one(mydict)
                j+=1
        except Exception as e:
            print('users: ',e)
            pass
    return 'done'

                
########################################################################</API_USERS>#################################################################

########################################################################<wordpress results front end>#################################################################


def videocreation(forvideoid):
    
    somes =[]
    countofvids = 0
    
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client    
    #DEVELOPER_KEY = "AIzaSyChnnGVkXth2ojo5Xx_KpZqXrlXWOnQAwU"
    DEVELOPER_KEY = 'AIzaSyCL6tw_6D1gjKZr9WKKwxirJtELxQ20y94'
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey = DEVELOPER_KEY)

    try:
        
            
        
        
        request = youtube.videos().list(
            part="snippet",
            id=str(forvideoid),
                    
        )
        response = request.execute()

        for i in response.get("items", []):            
            
            
        
            upload_date = i['snippet']['publishedAt']
            channelId = i['snippet']['channelId']
            
            title = i['snippet']['title']
            description = i['snippet']['description']
            image = i['snippet']['thumbnails']['default']['url']
            st = 'https://www.youtube.com/watch?v='+str(forvideoid)


            try:
                image = i['snippet']['thumbnails']['maxres']['url']
            except:
                try:
                    image = i['snippet']['thumbnails']['standard']['url']
                except:
                    try:
                        image = i['snippet']['thumbnails']['high']['url']
                    except:
                        try:
                            image = i['snippet']['thumbnails']['medium']['url']
                        except:                                
                            image = i['snippet']['thumbnails']['default']['url']

                    
                            
            
            
                
                
    except Exception as e:       
        print(e)
        title = "Video Not Available"
        description = "Video Not Available"
        pass
            
    return title,description,image




api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

# Get credentials and create an API client    
#DEVELOPER_KEY = "AIzaSyChnnGVkXth2ojo5Xx_KpZqXrlXWOnQAwU"
DEVELOPER_KEY = 'AIzaSyCL6tw_6D1gjKZr9WKKwxirJtELxQ20y94'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
developerKey = DEVELOPER_KEY)
def createchannels(channelId):
    channel_title = "Not Available"
    channel_Ion = "Not Available"
    try:
        request = youtube.channels().list(
        part="snippet",
        id=str(channelId)
        )
        response = request.execute()
        for i in response.get("items", []):                
            channel_Ion = i['snippet']['thumbnails']['default']['url']
            channel_title = i['snippet']['title']                       
    except Exception as e:
        print(e)
        pass
    
    
    return channel_title,channel_Ion

def createchannelsusers(channelId):
    channel_title = "Not Available"
    channel_Ion = "Not Available"
    try:
        request = youtube.channels().list(
        part="snippet",
        forUsername=str(channelId)
        )
        response = request.execute()
        for i in response.get("items", []):                
            channel_Ion = i['snippet']['thumbnails']['default']['url']
            channel_title = i['snippet']['title'] 
    except Exception as e:
        print(e)
        pass                      
    
    
    return channel_title,channel_Ion



def searchvideosofachannelkeyword(searchword,orderby,maxResults):
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
    # Get credentials and create an API client    
    # DEVELOPER_KEY = 'AIzaSyAR6brMGXiuz1vhG3CLhWTidVi1--9zV-o'
    DEVELOPER_KEY = 'AIzaSyBng2XO28RZPHGgQ1zzPOS6l-e8GAfc5c8'

    
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
    videos=[]  
    maxvideositer=1 
    maxvideos = int(maxResults)      
        
    request = youtube.search().list(
        part="snippet",
        maxResults=50,
        order=orderby,
        q=str(searchword)
        
        
    )
    response = request.execute()
    print(response)
    
    
    for i in response.get("items", []):  
        try:
            print(i['id']['videoId'])          
            videos.append(i['id']['videoId'])
        except Exception as e:    
            print(e)    
            pass
    try:
        token = response['nextPageToken']        
    except:
        token='None'
        pass
    if (token!='None') and int(maxvideos) >= 1:   
        while (token!='None'):
            returnedvideos,token = searchvideoprocessorkeyword(token,searchword,orderby)
            videos+=returnedvideos   
            print('loop : ',maxvideositer)         
            if (token == 'None') or int(maxvideositer) >= int(maxvideos):
                
                break
            maxvideositer+=1        
    
    return videos


def searchvideoprocessorkeyword(token,chids,orderby):
    videos = []
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
    # Get credentials and create an API client    
    DEVELOPER_KEY = 'AIzaSyCL6tw_6D1gjKZr9WKKwxirJtELxQ20y94'
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
    
    request = youtube.search().list(
        part="snippet",
        maxResults=50,
        order=orderby,
        q=str(chids),
        pageToken=token     
        )
    
    response = request.execute()
    
    for i in response.get("items", []):
        try:
            videos.append(i['id']['videoId'])
        except:
            pass
    try:
        token = response['nextPageToken']        
    except:
        token='None'
        pass                    
    
    return videos,token  


############################################################################## WordPress Posts ##############################################################################
def wordpress_api_Posts_single(URL,selecttype,numberofpages):
    if str(selecttype) != "":
        location = "Anonymous"
        import tldextract
        import datetime
        ext = tldextract.extract(URL)
        o_endpoint = (ext.domain)
        API_ENDPOINT = URL+"/wp-json"
        POST_API_ENDPOINT = URL+"/wp-json/wp/v2/"+str(selecttype)
        
        agents = {"random":"Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0"}

        headers = {'User-Agent': agents['random']}
            
        PARAMS = {'address':location}
        
        catname = 'wordpressrest_wordpressbox'
        mycol=db[catname]
        rotationnum = mycol.find().sort("id",-1)
        try:
            j=int(rotationnum[0]['id'])+1
        except:
            j=1      
        
        

        
        for iterationpost in range(1,int(numberofpages)+1):
            API_ENDPOINT = POST_API_ENDPOINT+"?page="+str(iterationpost)
            try:
                threadr = requests.get(url = API_ENDPOINT,headers=headers, params = PARAMS)
                data = threadr.json()
            
                for i in data:
                    internallinks = []
                    externallinks = []
                    internallinks_hash = []
                    postid = (i['id'])
                    date_pub = i['date']
                    
                    modified_date = i['modified']
                    guid = i['guid']['rendered']
                    slug = i['slug']
                    status = i['status']
                    type_post = i['type']
                    link = i['link']
                    title = i['title']['rendered']
                    titlesoup = BeautifulSoup(title,'lxml')
                    title = titlesoup.text
                    content = i['content']['rendered']
                    excerpt = i['excerpt']['rendered']
                    author = i['author']
                    
                    featured_media = i['featured_media']
                    comment_status = i['comment_status']
                    ping_status = i['ping_status']                    
                    # format_post = i['format']
                    try:
                        categories = i['categories']
                    except:
                        categories:"None"
                        pass
                    try:
                        tags = i['tags']
                    except:
                        tags:"None"
                        pass
                    
                    formatingtime = "%Y-%m-%dT%H:%M:%S"
                    pubdate = datetime.datetime.strptime(date_pub, formatingtime)
                    modifieddate = datetime.datetime.strptime(modified_date, formatingtime)
                    soup = BeautifulSoup(content,'lxml')
                    ilink = ""
                    for i in soup.findAll('a',href=True):  
                        ilink = str(i.get('href'))               
                                    
                        try:
                            if "mailto:" not in str(ilink):
                                if str(o_endpoint) in str(ilink) or str(ilink).startswith('.'):
                                    internallinks.append(str(ilink))
                                elif '#' in ilink and str(o_endpoint) in str(ilink):                                
                                    internallinks_hash.append(str(ilink))
                                elif 'http' in ilink and str(o_endpoint) not in str(ilink):
                                    externallinks.append(str(ilink))
                        except Exception as e:
                            print(e)
                            return
                    ############# <Title Analysis> ##############
                    spacecounter_title =  title.count(' ')  
                    titlewords = title.split(' ')          
                    titlecharslength = len(title)-(spacecounter_title)            
                    
                    ############# </Title Analysis> ##############
                    
                    ############# <Content Analysis> ##############
                    content_processor = re.sub("<.*?>", " ", content)
                    spacecounter_content = content_processor.count(' ')
                    contentwords = [x.strip() for x in content_processor.split(' ') if x.strip()]            
                    contentcharslength = len(content_processor)-(spacecounter_content)
                    ############# </Content Analysis> ##############
                    try:
                        soup = BeautifulSoup(content_processor,'lxml')
                    except:
                        content_processor = "none"
                        soup = BeautifulSoup(content_processor,'lxml')                        
                    rtime = (((len(contentwords))*0.36)/100)
                    try:
                        myquery = { "postid": int(postid),"url":str(URL),"type":str(selecttype) }
                        print(myquery)
                        cntdics = mycol.delete_many(myquery)
                        print(cntdics.deleted_count, " documents deleted.")
                    except Exception as e:
                        print(e)
                        pass
                    
                    countdocs = 0  
                    if selecttype == "posts":
                        autname = 'admin'
                        mydict = {"postid":postid,"date": pubdate,"modified_date":modifieddate,"guid":guid,"slug": slug,"url":URL,"titleprops":titlewords,
                        "contentprops":contentwords,"status":status,"type":str(selecttype),"link":link,"title":title,"author":author,
                        "featured_media":featured_media,"comment_status":comment_status,"ping_status":ping_status,
                        "format_post":"format_post","categories":categories,"tags":tags,"titlecharslength":titlecharslength,
                        "contentcharslength":contentcharslength,
                        "internallinks":internallinks,"internallinks_hash":internallinks_hash,"externallinks":externallinks,
                        "content":str(soup.text),"originalcontent":content,"internallinks_count":len(internallinks),"externallinks_count":len(externallinks),
                        "rtime":rtime}             
                        mycol.insert_one(mydict)     
                    if selecttype == "pages":
                        autname = 'admin'
                        mydict = {"id":j,"postid":postid,"date": pubdate,"modified_date":modifieddate,"guid":guid,"slug": slug,"url":URL,"titleprops":titlewords,
                        "contentprops":contentwords,"titlecharslength":titlecharslength,"contentcharslength":contentcharslength,
                        "internallinks":internallinks,"internallinks_hash":internallinks_hash,"externallinks":externallinks,
                        "status":status,"type":str(selecttype),"link":link,"title":title,"author":author,"featured_media":featured_media,"comment_status":comment_status,
                        "ping_status":ping_status, "content":str(soup.text),"originalcontent":content,"internallinks_count":len(internallinks),
                        "rtime":rtime,"externallinks_count":len(externallinks)}             
                        mycol.insert_one(mydict)           
                            
            except Exception as e:
                print("Posts Indecs Issue:",e)
                pass
        print('Posts_thread_All Completed')
            
        
       
    else:
        return 'done'

    return 'done'
############################################################################## End Wordpress Posts ##########################################################################

############################# Named Entity Extraction #############################
def entity_extraction_wp(sitename,selecttype,truebox,tagselection):
    single = []
    entities =[]    
    stcontent = ""
    catname = 'wordpressrest_wordpressbox'
    mycol=db[catname]
    searchstring = (truebox.split(','))[0]
    results = mycol.find({'url':str(sitename),'type':str(selecttype),'postid':int(searchstring)})
    for x in results:
        thisdict = x
        thisdict.pop("_id")
        single.append(thisdict)
    soup = BeautifulSoup(thisdict['originalcontent'],'lxml')
    for tk in soup.findAll('p'):
        ops = re.sub('<strong>.*?</strong>|<p.*?>|</p>|\,|\'|\"|\.|<a.*?>|</a>',' ',str(tk))
        stcontent+=str(ops.strip())
    if str(tagselection) == "p":
        doc = nlp(stcontent)
    elif str(tagselection) == "h":
        doc = nlp(thisdict['content'])
    for X in doc.ents:
        if str(X.text) != ' ':
            if str(X.text) not in entities:            
                entities.append(str(X.text))
    
    return single,entities
############################# End Named Entity Extraction #########################

############################# Single Posts Update ############################

def wp_post_update_single(sitename,selecttype,urlnkwds,titledata,textboxdata,operation,postid,allurls,allkwds):
    imageidcollector = []
    imageidtitler = []
    imageurlcollector = []
    # allurls = []

    catname = 'wordpressrest_wordpressbox'
    mycol=db[catname]
    #################  GET URLS ###################

    # for x in mycol.find({"type": str(selecttype),"url":sitename}):
    #     allurls.append(x['link'])        

    #################  End GET URLS ###############
    
    for x in mycol.find({"type": str(selecttype),"postid":int(postid),"url":sitename}):
        dbpostcontent = x['originalcontent']
        dbposttitle = x['title']
    
    url = str(sitename)+"/wp-json/wp/v2/{}/{}".format(str(selecttype),int(postid))
    if sitename == "https://www.digitalndigital.com":
        user = "digitalndigital"
        password = "8etq NHLb aVFs 9LGo MMwi V4v4"
    elif sitename == "https://www.reelnreel.com":
        user = "reelnreel"
        password = "Nz74 ONBR Vlzt ar8R bJUS aw0F"
    elif sitename == "https://www.dotndot.com":
        user = "dotndot"
        password = "l17D O5GL kaf0 KaCS RXYw 49LT" #Dotndot

    # password = "wtpZ K1uv RB4g hi8r pkpN Npe8"
    # password = "Nz74 ONBR Vlzt ar8R bJUS aw0F" #ReelnReel
    # password = "wtpZ K1uv RB4g hi8r pkpN Npe8" #localhost
    # password = "l17D O5GL kaf0 KaCS RXYw 49LT" #Dotndot
    
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}

    val = dbpostcontent.split('<p style="text-align: justify;">')
    stringcontent = ''
    for i in val[1:]:
        ptext = ('<p style="text-align: justify;">'+i)
        htext = re.sub('<h2 style="text-align: justify;">.*?</h2>','',ptext) 
        for alls,every in urlnkwds:        
            # for alls in allurls.split(','):            
            #     if ((every).lower()) in (alls).lower():
            cofirmedstring = '<a href=\"'+alls+'\" target=\"_blank\" rel=\"noopener noreferrer\">'+every+'</a>'                
            htext = htext.replace(every,cofirmedstring)

        x = re.findall('<h2 style="text-align: justify;">', ptext)  
        if len(x) >= 1:  
            h2text = re.sub('<p style="text-align: justify;">.*?</p>','',ptext)
            stringcontent+=(htext+h2text)
        else:
            stringcontent+=(htext)
         

    
    # for every in truebox.split(','):        
    #     for alls in allurls:            
    #         if ((every).lower()) in (alls).lower():
    #             cofirmedstring = '<a href=\"'+alls+'\" target=\"_blank\" rel=\"noopener noreferrer\">'+every+'</a>'
                
                # dbpostcontent = dbpostcontent.replace(every,cofirmedstring)
    

 
    # myquery = { "postid": int(postid) }
    # newvalues = { "$set": { "originalcontent": stringcontent } }

    # mycol.update_one(myquery, newvalues)
    
    # post = {
    # 'title': str(titledata),
    # 'status'   : 'publish',
    # 'content'  : stringcontent        
    
    # }
    

    # responce = requests.put(url , headers=header, json=post)
    
    # jk = responce.json()      
    print(stringcontent)
            
    return imageidcollector,imageidtitler









############################ End Single Posts Update #########################



############################# Single Match URLS ############################

def wp_post_match_url(sitename,selecttype,truebox,titledata,textboxdata,operation,postid):    
    
    kwdcollector = []
    urlcollector = []
    allurls = []
    urlstack = []


    catname = 'wordpressrest_wordpressbox'
    mycol=db[catname]
    #################  GET URLS ###################

    for x in mycol.find({"type": str(selecttype),"url":sitename}):
        allurls.append(x['link'])        

    #################  End GET URLS ###############
    
    for x in mycol.find({"type": str(selecttype),"postid":int(postid),"url":sitename}):
        dbpostcontent = x['originalcontent']
        dbposttitle = x['title']
    
    
    idno = 1
    for every in truebox.split(','):
        
        for alls in allurls:            
            if ((every).lower()) in (alls).lower():
                cofirmedstring = '<a href=\"'+alls+'\" target=\"_blank\" rel=\"noopener noreferrer\">'+every+'</a>'
                urlstack.append({"id":int(idno),"url":alls,"keyword":every})
                
                if every not in kwdcollector:  
                    urlcollector.append(alls)                  
                    kwdcollector.append(every)
            idno+=1
    
            
    return urlcollector,kwdcollector,urlstack









############################ End Single Match URLS #########################














