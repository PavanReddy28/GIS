from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from geo.Geoserver import Geoserver
from .models import Sentinel, Groups, ChangeOutputs, ClusteringOutput
from django.contrib.messages import get_messages
from django.contrib import messages
import environ
import time
import os
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from osgeo import gdal
from world.qgis_cluster import perform_cluster
from world.qgis_change import perform_change

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

## ----------------------------Completed------------------------------------------

#  Geoserver Variables
geo = Geoserver('http://127.0.0.1:'+env('GEOSERVER_PORT')+'/geoserver', username='admin', password='geoserver')
 # layers = geo.get_layers(workspace='App')['layers']['layer']

def index(request):

    db_layers = Sentinel.objects.all()
    change_layers = ChangeOutputs.objects.all()
    cluster_layers = ClusteringOutput.objects.all()
    all_groups = Groups.objects.all()
    groups = []
    for group in all_groups:
        temp = db_layers.filter(group_name=group)
        if len(temp)>1:
            groups.append({"name":group.name, "list": temp})
    colors = Sentinel.COLOR_RAMPS_CHOICES
    messages = get_messages(request)
    tim = time.strftime("%H:%M", time.localtime())
    context = {
        'db_layers': db_layers, 
        'cluster_layers': cluster_layers, 
        'change_layers': change_layers, 
        'colors': colors, 
        'time':tim,
        'messages': messages,
        'groups' : groups,
        'group_names':all_groups,
        }

    return render(request, "index.html", context)

def upload(request):

    name = request.POST['mapName']
    desc = request.POST['desc']
    c_ramp = request.POST['c_ramp']
    raster = request.FILES['raster']
    group_name = request.POST['group_name']
    print(group_name, type(raster))
    if group_name not in  Groups.objects.all().values_list('name', flat=True) :
        g = Groups.objects.create(name=group_name)
        if c_ramp=='None':
            file = Sentinel.objects.create(name=name, description=desc, color_ramps=None, file=raster, group_name=g)
            print(group_name, g.id, file)
            file.save()
        else:
            file = Sentinel.objects.create(name=name, description=desc, color_ramps=c_ramp, file=raster, group_name=g)
            print(group_name, g.id, file)
            file.save()
    else:
        g = Groups.objects.get(name=group_name)
        if c_ramp=='None':
            file = Sentinel.objects.create(name=name, description=desc, color_ramps=None, file=raster, group_name=g)
            file.save()
        else:
            file = Sentinel.objects.create(name=name, description=desc, color_ramps=c_ramp, file=raster, group_name=g)
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


def mail(email_id, subject, content_text, html_heading, html_text, file_loc, attach_tif_file_loc=None):
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
                <h1>"""+html_heading+"""</h1>
                <p>"""+html_text+"""</p>
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
    with open(file_loc, 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<logo>')
    email.attach_alternative(html_content,"text/html")
    if attach_tif_file_loc:
        email.attach_file(attach_tif_file_loc)
    email.attach(logo)
    email.send()

## -------------------------------------Pending-----------------------------------

def cluster(request):
    print("enter")
    id = int(request.POST['cluster_id'])
    raster = Sentinel.objects.get(id=id)
    name = "Cluster_"+str(raster.id)
    le = len(ClusteringOutput.objects.all().values_list('name', flat=True).filter(name=name))
    messages.add_message(request, messages.INFO, 'Clustering is taking place. Check for output '+name+' after sometime.')
    print(name, le)
    output = os.path.join(settings.BASE_DIR, 'outputs', 'cluster', name+"_"+str(le)+".tif")
    perform_cluster(request, raster.file.path, output)
    # output = r'D:\PS-1\Django GIS\geodjango\pungi.tif'
    file = ClusteringOutput.objects.create(name="Cluster_"+str(raster.id), sentinel_id=raster, file=output)
    file.save()
    print("done")
    return redirect("/")

def change(request):
    id1 = int(request.POST['change_id1'])
    raster1 = Sentinel.objects.get(id=id1)
    id2 = int(request.POST['change_id2'])
    raster2 = Sentinel.objects.get(id=id2)
    name = "Change_"+str(raster1.id)+"_"+str(raster2.id)
    le = len(ChangeOutputs.objects.all().values_list('name', flat=True).filter(name=name))
    if raster1.group_name == raster2.group_name:
        messages.add_message(request, messages.INFO, 'Chnage Detection is taking place. Check for output '+name+' after sometime.')
        output = os.path.join(settings.BASE_DIR, 'outputs', 'change', name+"_"+str(le)+".tif" )
        perform_change(request, raster1.file.path, raster2.file.path, output)
        # output = r'D:\PS-1\Django GIS\geodjango\pungi.tif'
        file = ChangeOutputs.objects.create(name=name, sentinel_1_id=raster1, sentinel_2_id=raster2, file=output, group_name=raster1.group_name)
        file.save()
        # if request.user.is_authenticated:
        #     email = request.user.email
        #     ds = gdal.Open(file.file.path)
        #     down_path = os.path.join(settings.BASE_DIR, 'outputs', 'change', name+"_"+str(le)+".png")
        #     xyz = gdal.Translate(down_path, ds)
        #     print(email)
        #     mail(email_id=email, subject="Change Detected in  group "+file.group_name.name, content_text="",
        #         html_heading="Change Detection - GIS World", 
        #         html_text="Change has been detected in the group "+file.group_name.name+", between the maps "+file.sentinel_1_id.name+" and "+file.sentinel_2_id.name+". Please view the change below.",
        #         file_loc=down_path,
        #         attach_tif_file_loc=file.file.path
        #     )
        return redirect("/")
    else:
        messages.add_message(request, messages.ERROR, 'Files choosen are of different groups. Please choose files from same group.')
        return redirect("/")