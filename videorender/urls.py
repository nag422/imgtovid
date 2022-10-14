from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404,handler500
# handler404 = 'videoapp.views.frontend'
# handler500 = 'videoapp.views.frontend'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('videoapp.urls')),
    path('', include('telegrambox.urls')),
    path('', include('livedash.urls')),
    path('', include('wordpressrest.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls'))
]

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL,serve,
                          document_root=settings.MEDIA_ROOT)
