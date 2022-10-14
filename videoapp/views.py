from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.conf import settings
import os
import math
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import Permission, User
from .serializers import ImageWriterSerializer,ImageStoreSerializer,ExcelFIleStoreSerializer
from .models import ImageWriter,ImageStore,ExcelFIleStore
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .imgcreation import image_trigger,trailer,file_retrieve_user_folder,final_img_to_vid,image_trigger_custome,composition,composition_combine
from .imagecreationdynamic import image_trigger_dynamic
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile

def frontend(request):
    return render(request, 'index.html')



@csrf_exempt
def home(request,user,spath,stype):
    #trailer()
    print(stype)
    if str(stype) == "folders":
        joining_path = settings.IMAGE_PROCESSING_URL
        cols_in = str(user)+"/"
        single = file_retrieve_user_folder(joining_path,cols_in,spath,stype)
        context = {
            "response": single
        }
    elif str(stype) == "images":
        joining_path = settings.IMAGE_PROCESSING_URL
        cols_in = str(user)+"/"
        single = file_retrieve_user_folder(joining_path,cols_in,spath,stype)
        context = {
            "response": single
        }
    
    elif str(stype) == "excelfiles":
        joining_path = settings.IMAGE_PROCESSING_URL
        cols_in = str(user)+"/"
        single = file_retrieve_user_folder(joining_path,cols_in,spath,stype)
        context = {
            "response": single
        }

    elif str(stype) == "deletes":
        pic = (((request.body).decode('utf-8')))
        
        path_source = settings.IMAGE_PROCESSING_URL+str(user)+"/"+spath+'/'+pic
        

        if 'reference_backs' not in str(path_source):
            os.remove(path_source)           
        

        context = {
            "response": 'single'
        }
    elif str(stype) == "videos":
        joining_path = settings.IMAGE_PROCESSING_URL
        cols_in = str(user)+"/"
        single = file_retrieve_user_folder(joining_path,cols_in,spath,stype)
        context = {
            "response": single
        }
    else:
        context = {
            "response": 'fail'
        }
    

    return JsonResponse(context)

class BulkProcessingView(APIView):
    def post(self, request, *args, **kwargs):
        username = kwargs['author']
        foldername = kwargs['foldername']
        stype = kwargs['stype']
        if stype == "images":
        
            piclist = request.data
            for pic in piclist:
                path_source = settings.IMAGE_PROCESSING_URL+str(username)+"/"+foldername+'/'+pic     
                os.remove(path_source)     

        elif stype == "videos":
            piclist = request.data
            
            # files = request.FILES.getlist('musicfiles')
            
            # print(request.data['piclist'])
            for pic in piclist:
                path_source = settings.IMAGE_PROCESSING_URL+str(username)+"/"+foldername+'/'+pic   
                print(path_source)
                os.remove(path_source)  
        
        elif stype == "exceldelete":
            piclist = request.data
            
            # files = request.FILES.getlist('musicfiles')
            
            # print(request.data['piclist'])
            for pic in piclist:
                path_source = settings.IMAGE_PROCESSING_EXCEL+"/media/post_images/"+pic   
                print(path_source)
                os.remove(path_source)  

        
        elif stype == "music":           
            
            files = request.FILES.getlist('musicfiles')
            incr = 1
            for f in files:
                extension = f.name[f.name.rfind("."):]
                filenaming = settings.IMAGE_PROCESSING_URL+str(username)+"/soundclips/"+str(f.name)
                with open((filenaming), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                    incr+=1
                soundclip = filenaming
            
            piclist = (request.data['piclist']).split(',')
            extranum = 1
            for pic in piclist:
                path_source = settings.IMAGE_PROCESSING_URL+str(username)+"/"+foldername+'/'+pic   
                exactpath = settings.IMAGE_PROCESSING_URL+str(username)+"/"+foldername+'/'
                composition(soundclip,path_source,exactpath,extranum)
                extranum+=1

        elif stype == "combine":           
            
            files = request.FILES.getlist('musicfiles')
            incr = 1
            for f in files:
                extension = f.name[f.name.rfind("."):]
                filenaming = settings.IMAGE_PROCESSING_URL+str(username)+"/soundclips/"+str(f.name)
                with open((filenaming), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                    incr+=1
                soundclip = filenaming
            
            piclist = (request.data['piclist']).split(',')
            extranum = 1
            # for pic in piclist:
            #     path_source = settings.IMAGE_PROCESSING_URL+str(username)+"/"+foldername+'/'+pic   
            exactpath = settings.IMAGE_PROCESSING_URL+str(username)+"/"+foldername+'/'
            composition_combine(soundclip,piclist,exactpath,extranum,username,foldername)
            extranum+=1
                
                

        

        context = {
            "response": 'request.data'
        }
        
        return Response(context)

    


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        
        user_name = request.data['username']
        password1 = request.data['password']
        email = request.data['email']
        
        try:
            User.objects.get(username=user_name)
            context = {
                "error": 'Already exists'
                
            }
        except User.DoesNotExist:        
            user = User.objects.create_user(username=user_name, password=password1)
            user.save()
            u = User.objects.get(username=user_name)
            Token.objects.create(user=u)
            temporary_path = settings.IMAGE_PROCESSING_URL+ str(user_name)
            try:
                #os.mkdir(os.path.join(joining_path, cols_in))
                os.mkdir(temporary_path)
                os.mkdir(os.path.join(temporary_path, 'reference_backs'))
                os.mkdir(os.path.join(temporary_path, 'soundclips'))
                os.mkdir(os.path.join(temporary_path, 'rendered_images'))
            except:
                pass
            context = {
                "username": user_name
            }
        
        return Response(context)
class VideoView(APIView):
    def post(self, request, *args, **kwargs):
        
        foritercount = 1
        single = []
        final_render = []
        # variation = 6
        username = kwargs['username']
        variation = int(kwargs['loopiter'])
        path_source = settings.IMAGE_PROCESSING_URL

        for foldername in request.data:            
            for subitem in os.listdir(path_source+username+"/"+foldername+"/"):            
                if subitem.endswith(".png"):
                    single.append((path_source, subitem))
            

            if len(single) >= variation:
                foritercount = 1
                i = variation
                custom_range = int(math.ceil(len(single))/variation)                
                for videos in range(0,custom_range+1):
                    datalist = single[i-variation:i]
                    #customizing_endslie.append(single[i-variation])    
                    if len(datalist) > 0:            
                        outputvid = final_img_to_vid(path_source,username,foldername,datalist,foritercount)
                        final_render.append(outputvid)
                        i+=variation
                        foritercount+=1
            elif len(single) > 0:
                outputvid = final_img_to_vid(path_source,username,foldername,single,foritercount)
            else:
                return

        context = {
            "response":'single'
        }
        return Response(context)
    def delete(self, request, *args, **kwargs):
        print('yes deleted')
        username = kwargs['username']
        foldername = kwargs['loopiter']
        print(foldername,username)
        print(request.data)
        path_source = settings.IMAGE_PROCESSING_URL+username+"/"+foldername+'/'
        os.rmdir(path_source)
        context = {
            "response":'username'
        }
        return Response(context)
        
class DeleteHandleall(APIView):
    
    def delete(self, request, *args, **kwargs):  
        import shutil      
        username = kwargs['username']
        foldername = kwargs['foldername']        
        path_source = settings.IMAGE_PROCESSING_URL+username+"/"+foldername+'/'
        shutil.rmtree(path_source)
        context = {
            "response":username
        }
        return Response(context)



class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = ImageStore.objects.all()
        serializer = ImageStoreSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        posts_serializer = ImageWriterSerializer(data=request.data)
        
        
        if posts_serializer.is_valid():
            posts_serializer.save()

            try:
                files = request.FILES.getlist('multirefiles')
            
                incr = 1
                for f in files:
                    extension = f.name[f.name.rfind("."):]
                    filenaming = 'static/'+str(posts_serializer.data['author'])+'/reference_backs/'+str(incr)+str(extension)
                    with open(filenaming, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                        incr+=1
            except:
                pass

            try:
                
                files = request.FILES.getlist('staticnewbg')
            
                incr = 1
                for f in files:
                    extension = f.name[f.name.rfind("."):]
                    
                    filenaming = 'static/'+str(posts_serializer.data['author'])+'/curatedrefs/'+str(f.name)
                    with open(filenaming, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                        incr+=1
            except:
                pass

            if str(posts_serializer.data['background']) == "static":
                
                puberty = int(request.data['bgpuburty'])
                print(puberty)
                if puberty == 0:
                    image_trigger(posts_serializer.data['image'],posts_serializer.data['pictype'],posts_serializer.data['author'],posts_serializer.data['font'],posts_serializer.data['title'])
                elif puberty == 1:
                    print(str(str(f.name).split('.')[0]))
                    image_trigger(posts_serializer.data['image'],posts_serializer.data['pictype'],posts_serializer.data['author'],posts_serializer.data['font'],str(str(f.name).split('.')[0]))
                
            else:
                image_trigger_dynamic(posts_serializer.data['image'],posts_serializer.data['pictype'],posts_serializer.data['author'],posts_serializer.data['font'],posts_serializer.data['title'])
                print("done")

            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        mymodel.my_file_field.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
staticdirectory = settings.STATIC_DIR
def trails(request):
    js = os.path.join(settings.STATIC_DIR,'haritha')
    
    return HttpResponse(js)


from zipfile import ZIP_DEFLATED
from django_zipfile import TemplateZipFile
import zipfile
from os.path import basename
staticdirectory = settings.STATIC_DIR
import base64
class ImageDownload(APIView):
    def post(self, request, *args, **kwargs):
        username = kwargs['username']
        foldername = kwargs['foldername']
        name = kwargs['name']
        
        with open('static/'+str(username)+'/'+str(foldername)+'/'+str(name)+'.png', 'rb') as fh:
            # base64.b64encode
            response = HttpResponse((fh.read()), content_type="image/*")
            # response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            response['Content-Disposition'] = 'attachment; filename=static/'+str(username)+'/'+str(foldername)+'/'+str(name)+'.png'
        return response

class CustomImage(APIView):
    def get(self, request, *args, **kwargs):   
        single = []
        foldername = kwargs['foldername']    
        for item in os.listdir('static/'+str(foldername)):        
            if item.endswith('jpg'):    
                single.append({"id":"pic","source":item})
                    
        
       
        return Response({"single":single})



class DownloadView(APIView):
    def post(self, request, *args, **kwargs):
        username = kwargs['username']
        dwntype = kwargs['dwntype']
        print(dwntype,username)
        for foldername in request.data:
            with zipfile.ZipFile('./static/'+str(username)+'/'+str(foldername)+'/spam.zip', 'w') as myzip:  
                try:      
                    for item in os.listdir('./static/'+str(username)+'/'+str(foldername)):     
                         
                        if item.endswith(dwntype):    
                            myzip.write('./static/'+str(username)+'/'+str(foldername)+'/'+item)
                finally:
                    myzip.close()
        with open('./static/'+str(username)+'/'+str(foldername)+'/spam.zip', 'rb') as fh:
            response = HttpResponse(ContentFile(fh.read()), content_type="application/zip")
            # response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            response['Content-Disposition'] = 'attachment; filename=spam.zip'
        return response
class ExcelDownloadView(APIView):
    def post(self, request, *args, **kwargs):
        username = kwargs['author']
        
        
        for foldername in request.data:
            with zipfile.ZipFile('./media/post_images/excels.zip', 'w') as myzip:  
                try:      
                    for item in os.listdir('./media/post_images/'):    
                         
                        if item.endswith('xlsx'):    
                            myzip.write('./media/post_images/'+item)
                finally:
                    myzip.close()
        with open('./media/post_images/excels.zip', 'rb') as fh:
            response = HttpResponse(ContentFile(fh.read()), content_type="application/zip")
            # response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            response['Content-Disposition'] = 'attachment; filename=spam.zip'
        return response

def trail(request):
    # obj = get_object_or_404(MyModel, pk=object_id)
    # context = {
    #     'object': obj
    # }
    # js = os.path.join(settings.STATIC_DIR,'reference_backs\haritha\\facebook\\')
    # js = "E:\\imgtovidvideorender/static/reference_backs/haritha/facebook/"
    # os.chdir(js)
    # my_zipfile = zipfile.ZipFile("myzip.zip", mode='w', compression=zipfile.ZIP_DEFLATED)
    # single = []
    # for item in os.listdir(js):
    #     # if item.endswith(".png"):
    #     filepath = os.path.join(js, item)
    #     single.append(filepath)
    with zipfile.ZipFile('spam.zip', 'w') as myzip:  
        try:      
            for item in os.listdir('media/post_images/'):            
                myzip.write('media/post_images/'+item)
        finally:
            myzip.close()
            # response = HttpResponse(content_type='application/zip')
            # response['Content-Disposition'] = 'attachment; filename=spam.zip'

    # myzip.close()
    # my_zipfile.write(js)
    # my_zipfile.close()
    # print(single)
    # file_path = "E:/imgtovid/videorender/myzip.zip"
    with open('spam.zip', 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/zip")
        # response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        response['Content-Disposition'] = 'attachment; filename=spams.zip'
        # return response
    # response = HttpResponse(content_type='application/zip')
    # response['Content-Disposition'] = 'attachment; filename=spam.zip'
 
    return response





class CustomPost(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        fontsize = int(request.data['fontsize'])
        username = request.data['author']
        imwidth = int(request.data['imwidth'])
        imheight = int(request.data['imheight'])
        font = (request.data['font'])
        title = request.data['title']
        excel_file = request.data['image']
        pictype = int(request.data['pictype'])
        # print(fontsize,username)
        # print(imwidth,imheight)
        # print(font,title)

        posts_serializer = ExcelFIleStoreSerializer(data=request.data)
        
        
        if posts_serializer.is_valid():
            posts_serializer.save()
        
        
        try:
            files = request.FILES.getlist('multirefiles')
        
            incr = 1
            for f in files:
                extension = f.name[f.name.rfind("."):]
                pictitled = str(f.name)
                filenaming = 'static/curatedrefs/'+str(f.name)
                with open(filenaming, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                    incr+=1
        except:
            pass
        if len(files) > 1:
            picname = pictitled
        else:
            picname = title
        windowposition = 40
        changetext = 0
        image_trigger_custome(imwidth,imheight,picname,font,fontsize,windowposition,changetext,posts_serializer.data['image'],username,pictype)
        return Response({"done":"done"})

    def get(self, request, *args, **kwargs):
        posts_serializer = ImageWriterSerializer(data=request.data)
        
        
        if posts_serializer.is_valid():
            posts_serializer.save()

            try:
                files = request.FILES.getlist('multirefiles')
            
                incr = 1
                for f in files:
                    extension = f.name[f.name.rfind("."):]
                    filenaming = 'static/'+str(posts_serializer.data['author'])+'/reference_backs/'+str(incr)+str(extension)
                    with open(filenaming, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                        incr+=1
            except:
                pass

            if str(posts_serializer.data['background'] == "static"):
                print("done")
               
                #image_trigger(posts_serializer.data['image'],posts_serializer.data['title'],posts_serializer.data['author'],posts_serializer.data['font'])
                
            else:
                #image_trigger_dynamic(posts_serializer.data['image'],posts_serializer.data['title'],posts_serializer.data['author'],posts_serializer.data['font'])
                print("done")

            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        mymodel.my_file_field.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
import img2pdf
class pdfViewPost(APIView):
    def post(self, request, *args, **kwargs):
        single = []
        # picslist = ['pic1.png','pic2.png']
        author = kwargs['author']
        folder = kwargs['foldername']
        picslist = (request.data)
        # author="kiran"
        # folder="tweep"
        # template_path = 'linkedinpdf.html'
        
        pdfdatapath = settings.STATIC_DIR+"\\"+str(author)+'\\'+str(folder)+'\\'
        for i in picslist:
            single.append(pdfdatapath+str(i.split('.')[0])+'.jpg')


        # for item in os.listdir(os.path.join(dir, particular_path)):
        #     if item.endswith(".png"):                
        #         single.append({"id":item,"source":item,"author":cols_in})
        # Create a Django response object, and specify content_type as pdf
        with open(pdfdatapath+"output.pdf", "wb") as f:
            f.write(img2pdf.convert(single))

        with open(pdfdatapath+"output.pdf", 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            # response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            # response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=spam.pdf'
        
        
        return response


# MultiLingual Images Creations
from PIL import Image, ImageFont, ImageDraw

class imgWalkView(APIView):
    def post(self, request, *args, **kwargs):
        context = {
            "width":640,
            "height":320
        }
        
        try:
            files = request.FILES.getlist('multirefiles')        
            
            for f in files:
                
                filenaming = 'static/'+str(request.data['author'])+'/reference_backs/'+str(f.name).replace(" ", "_")
                with open(filenaming, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                back = Image.open(filenaming, 'r')
                img_w, img_h = back.size
                    
        except:
            pass

        try:
            
            files = request.FILES.getlist('staticnewbg')
        
            
            for f in files:                
                
                filenaming = 'static/curatedrefs/'+str(f.name).replace(" ", "_")
                with open(filenaming, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                back = Image.open(filenaming, 'r')
                img_w, img_h = back.size
                    
        except:
            pass
        context = {
            "width":img_w,
            "height":img_h
        }
        return Response(context)

            
                   
