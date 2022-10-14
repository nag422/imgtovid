from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.conf import settings
import os
import time
import sys
from .screenprocess import (selscrape,wordpresscreatepost,dbdeleter,
searchvideosofachannelkeyword,wordpress_api_request_fetching_data,retriever,entity_extraction_wp,wp_post_update_single,wordpress_api_Posts_single,wp_post_match_url,
wordpressupdatepost,filterretriever,docxwordpresscreate)
from .models import seleniumimagestore
from .serializers import seleniumimagestoreSerializer
import mammoth



class screencreator(APIView):
    def post(self, request, *args, **kwargs):
        links = request.data['textboxdata']
        selecttype = request.data['selecttype']
        linklist = links.split('\n')
        reslist =[]        
        
        try:
            
            linklist.remove('')
            
        except Exception as e: 
                       
            pass

        try:
            
            linklist.remove('null')
            
        except Exception as e:                        
            pass
        
        reslist = selscrape(linklist,selecttype)
        context = {
            'response':reslist
        }
        
        
        return Response(context)


class getimages(APIView):
    def get(self, request, *args, **kwargs):
        images = seleniumimagestore.objects.all()
        serializer = seleniumimagestoreSerializer(images,many=True)
        context = {
            'response':serializer.data
        }
        
        
        return Response(context)

class wordpresscrud(APIView):
    def post(self, request, *args, **kwargs):
        searchtype = kwargs['q']
        print(searchtype)
        images = seleniumimagestore.objects.all()
        serializer = seleniumimagestoreSerializer(images,many=True)
        context = {
            'response':serializer.data
        }
        if str(searchtype) == "create":
            reflist = []
            l = request.data['truebox']           
            posttitle = request.data['posttitle']
            selecttype = request.data['selecttype']
            for i in l.split(','):
                data = seleniumimagestore.objects.get(id=int(i))            
                reflist.append({"imagename":data.imagename,"url":data.url,"title":data.title,"description":data.description,"type":data.type})            

            if len(reflist) > 0:
                imageidcollector,imageidtitler = wordpresscreatepost(reflist,posttitle,selecttype)
                print(imageidcollector,imageidtitler)
            
        elif str(searchtype) == "imgdelete":  
            l = request.data['truebox']
        
            for i in l.split(','):
                data = seleniumimagestore.objects.get(id=int(i))
                try:
                    if 'constant' not in str(data.imagename):
                        os.remove(settings.IMAGE_PROCESSING_EXCEL+'/'+str(data.imagename))
                except:
                    pass
                data.delete()

           
        elif str(searchtype) == "deletedbfetch":  
            l = request.data['truebox']
            sitename = request.data['sitename']
            selecttype = request.data['selecttype']
            dbdeleter(l,sitename,selecttype)
        elif str(searchtype) == "getnfetch":                          
            
            sitename = request.data['sitename']
            selecttype = request.data['selecttype']       
            print(sitename,selecttype)     
            # wordpress_api_request_processor(sitename,selecttype)
            wordpress_api_request_fetching_data(sitename,selecttype)
        elif str(searchtype) == "getnfetchsingle":                         
            
            sitename = request.data['sitename']
            selecttype = request.data['selecttype']   
            numberofpages = request.data['numberofpages']
                
            print(sitename,selecttype)     
            # wordpress_api_request_processor(sitename,selecttype)
            wordpress_api_Posts_single(sitename,selecttype,numberofpages)
            
        elif str(searchtype) == "getentities":                         
            
            sitename = request.data['sitename']
            selecttype = request.data['selecttype']   
            truebox = request.data['truebox']              
            tagselection = request.data['tagselection']
            
            
            single,entities = entity_extraction_wp(sitename,selecttype,truebox,tagselection)
            
            context = {
                'response':single,
                'ents':entities
            }
        elif str(searchtype) == "matchurls":                         
            
            sitename = request.data['sitename']
            selecttype = request.data['selecttype']   
            truebox = request.data['truebox']   
            titledata = request.data['titledata']
            textboxdata = request.data['textboxdata']   
            operation = request.data['operation']           
            postid = request.data['postid']
            
            
            urlcollector,kwdcollector,urlstack = wp_post_match_url(sitename,selecttype,truebox,titledata,textboxdata,operation,postid)
            
            context = {
                'urls':urlcollector,
                'kwds':kwdcollector,
                'urlstack':urlstack
            }

        elif str(searchtype) == "updatepostsingle":                         
            
            sitename = request.data['sitename']
            selecttype = request.data['selecttype']   
            truebox = request.data['truebox']   
            keybox = request.data['keybox']             
            titledata = request.data['titledata']
            textboxdata = request.data['textboxdata']   
            operation = request.data['operation']           
            postid = request.data['postid']
            allurls = request.data['leftmatch']
            allkwds = request.data['rightmatch']
            finalarray1 =[]
            finalarray2 = []
            for j in (allurls.split(',')):
                finalarray1.append(j)
                
            for k in allkwds.split(','):
                
                finalarray2.append(k)
            for j in (truebox.split(',')):
                finalarray1.append(j)
                
            for k in keybox.split(','):
                
                finalarray2.append(k)

            urlnkwds = zip(finalarray1,finalarray2)
            
            single,entities = wp_post_update_single(sitename,selecttype,urlnkwds,titledata,textboxdata,operation,postid,allurls,allkwds)
            
            context = {
                'response':'single',
                'ents':'entities'
            }
            
                
        elif str(searchtype) == "retrieveposts":
            sitename = request.data['sitename']
            selecttype = request.data['selecttype']
            currentpage = request.data['currentpage']
            single = retriever(sitename,selecttype,currentpage)            
            context = {
                'response':single
            }
        
        elif str(searchtype) == "filterphase":
            sitename = request.data['sitename']
            selecttype = request.data['selecttype']
            currentpage = request.data['currentpage']
            searchin = request.data['searchin']
            searchword = request.data['searchword']
            single = filterretriever(sitename,selecttype,currentpage,searchin,searchword)         
            context = {
                'response':single
            }

        

        elif str(searchtype) == "ytubefetch":
            orderby = request.data['orderby']
            searchword = request.data['ytubekwd']
            maxResults = request.data['maxresults']        
            videos = searchvideosofachannelkeyword(searchword,orderby,maxResults)  
            print((videos))
            selscrape(videos,'video')   
            print('start reslist')
            print(reslist)
            context = {
                'response':'videos'
            }

        
        elif str(searchtype) == "docxparser":
            from io import BytesIO
            sitename = request.data['sitename']
            selecttype = request.data['selecttype']
            files = request.FILES.getlist('docxbunch')
            for docx_file in files:
                result = mammoth.convert_to_html(docx_file)
                html = result.value
                html = html.replace('<p>','<p style="text-align:justify">')
                html = html.replace('<ul>','<ul style="text-align:justify">')
                html = html.replace('<ol>','<ol style="text-align:justify">')
                # html = html.replace('<h1>','<h2>')
                # html = html.replace('</h1>','</h2>')
                contentlist = html.split('<p style="text-align:justify">')                
                while("" in contentlist) : 
                    contentlist.remove("")  
                contentlist[1] = '<p style="text-align:justify">'+contentlist[1]
                                       
                
                # imageidcollector,imageidtitler = docxwordpresscreate(contentlist,selecttype)
            # single = filterretriever(sitename,selecttype,filesfile)         
            context = {
                'response':'single'
            }

        
        elif str(searchtype) == "updatepost":
            sitename = request.data['sitename']
            selecttype = request.data['selecttype']
            posttitle = request.data['titledata']
            textboxdata = request.data['textboxdata']    
            operation = request.data['operation']     
            l = request.data['truebox']    
            wordpressupdatepost(l,posttitle,selecttype,textboxdata,operation,sitename)       
            
            


                    
        
        
        
        return Response(context)
