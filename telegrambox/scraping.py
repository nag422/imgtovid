import requests
from bs4 import BeautifulSoup
import re
import numpy
import pandas as pd
from lxml import html

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
mycol=db["videoapp_scrapestore"]

PARAMS = {'address':'home'} 
agents = {"random":"Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0"}
headers = {'User-Agent': agents['random']}

def scrapingurl(url):
    
    single = []
    # url="https://biteable.com/blog/tips/video-marketing-statistics/"
    
    try:
        r = requests.get(url, headers=headers, verify=False,timeout=(10, 15))       
        print(url)
        soup = BeautifulSoup(r.text, 'lxml')

        rotationnum = mycol.find().sort('id',-1)
        try:
            sortingnum=int(rotationnum[0]['id'])+1
        except:
            sortingnum=1

        gain = soup.find_all('li')

        for alls in gain:
            isvalidtext = (alls.get_text()).strip()
            if len(isvalidtext.split(' ')) > 5:             
                thisdict = {"id":sortingnum,"url":url,"stats":str(isvalidtext)}
                mycol.insert_one(dict(thisdict))
                sortingnum+=1
    except Exception as e:
        print(e)        
        pass

    return 'done'
def gefile():
    pages = []
    for autname in mycol.find({}):
        pages.append(dict(autname))
    df = pd.DataFrame(pages)
    df.to_excel("static/scrape/scraping.xlsx",sheet_name="postsheet")
    return 'done'

def delfile():
    mycol.delete_many({})
    return 'done'

    



