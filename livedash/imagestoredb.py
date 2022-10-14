import numpy as np
import pandas as pd
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
mycol=db["livedash_backgroundimagesstore"]

def imagestore(request,filesfile):
    print('called')
    rotationnum = mycol.find().sort('id',-1)
    try:
        sortingnum=int(rotationnum[0]['id'])+1
    except Exception as e:
        print(e)
        sortingnum=1
   

    incr = sortingnum
    try:
        for f in filesfile:
            
            filenaming = 'static/livestreams/images/'+str(incr)+str(f.name).replace(" ", "_")            
            with open(filenaming, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            incr+=1
            thisdict = {"id":incr,"image":str(filenaming)}
            mycol.insert_one(dict(thisdict))
    except Exception as e:
        print(e)
    return 'done'

def Excelstore(request,filesfile,sourcetype,language):
    print('called')
    mycol=db["livedash_excelfilestore"]
    rotationnum = mycol.find().sort('id',-1)
    try:
        sortingnum=int(rotationnum[0]['id'])+1
    except Exception as e:
        print(e)
        sortingnum=1
   

    incr = sortingnum
    if str(sourcetype) == 'excel':
        try:
            for f in filesfile:                
                filenaming = 'static/livestreams/excels/'+str(incr)+str(f.name).replace(" ", "_")            
                with open(filenaming, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                incr+=1
            df = pd.read_excel(settings.IMAGE_PROCESSING_EXCEL+"/"+str(filenaming), encoding='utf-8')
            for cols_in in (df.columns).values.flatten():
                single = []
                texts = df[cols_in].tolist()
            
            thisdict = {"id":sortingnum,"language":language,"sourcetype":sourcetype,"data":texts}
            mycol.insert_one(dict(thisdict))
        except Exception as e:
            print(e)
    else:
        try:            
            thisdict = {"id":sortingnum,"language":language,"sourcetype":sourcetype,"data":filesfile.split('\n')}
            mycol.insert_one(dict(thisdict))
        except Exception as e:
            print(e)
        
    return 'done'