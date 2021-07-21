from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from geo.Geoserver import Geoserver
from .models import Sentinel, Groups, ChangeOutputsPNG, ClusteringOutput
from django.contrib.messages import get_messages
from django.contrib import messages
import environ
from django.core.mail import send_mail
import time
from sklearn.cluster import KMeans 
import numpy as np 
import os
from django.core.mail import EmailMessage,EmailMultiAlternatives
from email.mime.image import MIMEImage
import sys

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

## ----------------------------Completed------------------------------------------

#  Geoserver Variables
geo = Geoserver('http://127.0.0.1:'+env('GEOSERVER_PORT')+'/geoserver', username='admin', password='geoserver')
 # layers = geo.get_layers(workspace='App')['layers']['layer']

def index(request):

    db_layers = Sentinel.objects.all()
    colors = Sentinel.COLOR_RAMPS_CHOICES
    messages = get_messages(request)
    tim = time.strftime("%H:%M", time.localtime())
    context = {
        'db_layers': db_layers, 
        'cluster_layers': db_layers, 
        'change_layers': db_layers, 
        'colors': colors, 
        'time':tim,
        'messages': messages,
        }

    return render(request, "index.html", context)

def upload(request):

    name = request.POST['mapName']
    desc = request.POST['desc']
    c_ramp = request.POST['c_ramp']
    raster = request.FILES['raster']
    group_name = request.POST['group_name']
    print(group_name)
    if group_name not in Groups.objects.all():
        g = Groups.objects.create(name=group_name)
        print(group_name, g)
        if c_ramp=='None':
            file = Sentinel.objects.create(name=name, description=desc, color_ramps=None, file=raster, group_name=g)
            print(group_name, g.id, file)
            file.save()
        else:
            file = Sentinel.objects.create(name=name, description=desc, color_ramps=c_ramp, file=raster, group_name=g)
            print(group_name, g.id, file)
            file.save()
    else:
        if c_ramp=='None':
            file = Sentinel.objects.create(name=name, description=desc, color_ramps=None, file=raster)
            file.save()
        else:
            file = Sentinel.objects.create(name=name, description=desc, color_ramps=c_ramp, file=raster)
            file.save()
    messages.add_message(request, messages.SUCCESS, 'File '+name+' is succesfully uploaded!')
    return HttpResponse('Uploaded')

list = []
def search(request):
    print(request)
    if request.POST:
        list.clear()
        print(request.POST)
        name = request.POST["search"]
        list.append(name)
        return HttpResponse("Posted")
    else:
        print(list)
        postresult = Sentinel.objects.filter(name__contains=list[0])
        l = list.pop()
        json = []
        count = 0
        print(postresult)
        for i in postresult:
            print(i.name, i.description, i.color_ramps, i.uploaded_date)
            json.append({"name":i.name, "description":i.description, "color_ramps":i.color_ramps, "uploaded_date":i.uploaded_date})
            count+=1
        print(JsonResponse(json, safe=False))
        return JsonResponse(json, safe=False)


def mail(email_id, subject, content_text, html_text, file_loc, attach=None):
    html_content = """
        <html lang="en">
        <head>
            <style>
            html, body, #map {
                height: 100vh;
            }
            </style>
        </head>
        <body>
            <div id="map" class="map" style="padding: 2vh">
                <h1>Map</h1>
                <p>{{html_text}}</p>
                <img src="cid:logo" style="height: 25vh; width:25vh;"/>
            </div>
        </body>
        </html>
        """
    text_content = content_text
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email = settings.EMAIL_HOST_USER,
        to=[email_id],
    )
    # finders.find('emails/logo.png')
    with open(r'D:\PS-1\Django GIS\geodjango\uploads\Raster\2021\07\13\L1C_T42QZH_A022625_20210706T054240_3BTdFgY.tif', 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<logo>')
    email.attach_alternative(html_content,"text/html")
    # os.path.join(settings.MEDIA_URL, file_path)
    email.attach_file(logo)
    email.send()

## -------------------------------------Pending-----------------------------------

def cluster(request, id):

    return redirect("/")

def change(request):

    return redirect("/")