from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from geo.Geoserver import Geoserver
from .models import Sentinel
from django.contrib.messages import get_messages
from django.contrib import messages
import environ
from django.core.mail import send_mail
import time
from sklearn.cluster import KMeans 
from osgeo import gdal 
import numpy as np 
import os

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

## -------------------------------------Pending-----------------------------------

def cluster(request, id):

    # QGIS Application
    path = env.list('QGIS_PATH')
    print(path[0])

    # for i in path:
    #     sys.path.append(i)
        
    # QgsApplication.setPrefixPath("",True)
    # sys.path.append("C:\OSGeo4W\apps\qgis-ltr\python\plugins")
    # qgs = QgsApplication([], False)
    # qgs.initQgis()

    # from qgis import processing
    # from processing.core.Processing import Processing
    # Processing.initialize()
    # path = layer.file.path
    # # processing.algorithmHelp("saga:kmeansclusteringforgrids")
    # rlayer = QgsRasterLayer("file = "+path, "RasterLayer")
    # print(rlayer.bandCount())
    # cluster_params = {'GRIDS':[path],'METHOD':1,'NCLUSTER':3,'NORMALISE':0,'OLDVERSION':0,'UPDATEVIEW':1,'CLUSTER':os.path.join('C:/Users/YVM Reddy/Downloads' , layer.name+'_clustering.sdat'),'STATISTICS':os.path.join('C:/Users/YVM Reddy/Downloads' , layer.name+'_clustering.shp')}
    # processing.run("saga:kmeansclusteringforgrids",cluster_params)
    # qgs.exitQgis()

    ## USING GDAL TO PERFORM CLUSTERING
    raster_file = Sentinel.objects.get(id=id)
    file_path = str(raster_file.file)
    
    naip_fn = os.path.join(settings.MEDIA_URL, file_path)
    driverTiff = gdal.GetDriverByName('GTiff') 
    naip_ds = gdal.Open(naip_fn) 
    nbands = naip_ds.RasterCount 
    data = np.empty((naip_ds.RasterXSize*naip_ds.RasterYSize, nbands))

    for i in range(1, nbands+1): 
        band = naip_ds.GetRasterBand(i).ReadAsArray() 
        data[:, i-1] = band.flatten()

    km = KMeans(n_clusters=7) 
    km.fit(data) 
    km.predict(data)
    
    out_dat = km.labels_.reshape((naip_ds.RasterYSize,naip_ds.RasterXSize))
    clfds = driverTiff.Create(os.path.join(settings.MEDIA_URL, file_path[:11], 'classified_'+raster_file.name+'.tif'), naip_ds.RasterXSize, naip_ds.RasterYSize, 1, gdal.GDT_Float32)
    clfds.SetGeoTransform(naip_ds.GetGeoTransform())
    clfds.SetProjection(naip_ds.GetProjection())
    clfds.GetRasterBand(1).SetNoDataValue(-9999.0)
    clfds.GetRasterBand(1).WriteArray(out_dat)
    clfds = None

    return redirect("/")

def change(request):

    send_mail(
        'Trial',
        'Uploaded',
        'ypavan2802@gmail.com',
        ['ypavan2802@gmail.com'],
        html_message="""
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
                <img src='http://127.0.0.1:8085/geoserver/App/wms?service=WMS&version=1.1.0&request=GetMap&layers=App%3AHyderabad&bbox=799980.0%2C1890240.0%2C909780.0%2C2000040.0&width=768&height=768&srs=EPSG%3A32643&styles=&format='/>
            </div>
        </body>
        </html>
        """
    )

    return redirect("/")