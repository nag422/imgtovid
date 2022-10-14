import os

DATABASES = {  
   
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'videorender',
        'HOST':'localhost',
        'PORT':27017,
        'USER':'',
        'PASSWORD':'',
        'AUTH_SOURCE': 'videorender',
        # 'AUTH_MECHANISM': 'SCRAM-SHA-1',        
 

        
    },
}


DATABASES1 = {  
   
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'mealbox',
        'HOST':'localhost',
        'PORT':27017,
        'USER':'',
        'PASSWORD':'',
        'AUTH_SOURCE': 'mealbox',
        # 'AUTH_MECHANISM': 'SCRAM-SHA-1',     
    }
   
}