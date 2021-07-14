from django.http import HttpResponse
from django.shortcuts import render, redirect
from geo.Geoserver import Geoserver
from .models import Sentinel
import sys
import environ
from django.views.decorators.csrf import csrf_exempt

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

geo = Geoserver('http://127.0.0.1:'+env('GEOSERVER_PORT')+'/geoserver', username='admin', password='geoserver')

def index(request):
    layers = geo.get_layers(workspace='App')['layers']['layer']
    db_layers = Sentinel.objects.all()
    colors = Sentinel.COLOR_RAMPS_CHOICES
    context = {'db_layers': db_layers, 'cluster_layers': db_layers, 'change_layers': db_layers, 'colors': colors}
    return render(request, "index.html", context)

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

    layers = geo.get_layers(workspace='App')['layers']['layer']
    print("Cluster ", layers, id)
    db_layers = Sentinel.objects.all()
    colors = Sentinel.COLOR_RAMPS_CHOICES

    return redirect("/", {'db_layers': db_layers, 'colors': colors})

def change(request, id):
    
    layers = geo.get_layers(workspace='App')['layers']['layer']
    print("Change ", layers, id)
    db_layers = Sentinel.objects.all()
    colors = Sentinel.COLOR_RAMPS_CHOICES

    return redirect("/", {'db_layers': db_layers, 'colors': colors})

# @csrf_exempt
def upload(request):
    print(request.POST)
    print(request.FILES)
    # if request.method=='POST' and request.FILES['raster']:
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
    print(name, desc, c_ramp, raster)
    return HttpResponse('Uploaded')