from django.contrib import admin
from django.urls import path , include
from django.conf.urls import url    
from cloudx import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$',views.home, name='home'),
    url(r'^login/',views.login, name='login'),
    url(r'^logout/',views.logout, name='logout'),
    url(r'^index/',views.index, name='index'),
    url(r'^register/',views.register, name='register'),
    url(r'^forgot-password/',views.forgot_password, name='forgot_password'),
    url(r'^profile/',views.profile, name='profile'),
    url(r'^cloudX/',views.cloud, name='cloudx'),
    url(r'^upload/',views.upload, name='upload'),
    url(r'^uploadProfile/',views.uploadProfile, name='uploadProfile'),
    url(r'^updatedetails/',views.updatedetails,name='updatedetails'),
    url(r'^updatedetails2/',views.updatedetails2,name='updatedetails2'),
    url(r'^newfile/',views.newfile,name='newfile'),
    url(r'^download/',views.download,name='download'),
    url(r'^delete/',views.delete,name='delete'),
    url(r'^view/',views.view_file,name='view'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
