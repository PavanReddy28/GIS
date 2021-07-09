from django.shortcuts import render, redirect
from geo.Geoserver import Geoserver
from .models import Sentinel
import sys

# Create your views here.
def index(request):
    geo = Geoserver('http://127.0.0.1:8085/geoserver', username='admin', password='geoserver')
    layers = geo.get_layers(workspace='App')['layers']['layer']
    db_layers = Sentinel.objects.all()
    colors = Sentinel.COLOR_RAMPS_CHOICES
    return render(request, "index.html", {'db_layers': db_layers, 'colors': colors})

def cluster(request, id):

    # QGIS Application
    # path = ['C:/OSGeo4W/apps/qgis-ltr/./python', 'C:/Users/YVM Reddy/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python', 'C:/Users/YVM Reddy/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python/plugins', 'C:/OSGeo4W/apps/qgis-ltr/./python/plugins', 'C:\\Program Files\\QGIS 3.18\\apps\\qgis\\python', 'C:\\OSGeo4W\\bin\\python39.zip', 'C:\\OSGeo4W\\apps\\Python39\\DLLs', 'C:\\OSGeo4W\\apps\\Python39\\lib', 'C:\\OSGeo4W\\bin', 'C:\\Users\\YVM Reddy\\AppData\\Roaming\\Python\\Python39\\site-packages', 'C:\\OSGeo4W\\apps\\Python39', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages\\win32', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages\\win32\\lib', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages\\Pythonwin', 'C:/Users/YVM Reddy/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python']
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

    geo = Geoserver('http://127.0.0.1:8085/geoserver', username='admin', password='geoserver')
    layers = geo.get_layers(workspace='App')['layers']['layer']
    print("Cluster ", layers, id)
    db_layers = Sentinel.objects.all()
    colors = Sentinel.COLOR_RAMPS_CHOICES

    return redirect("/", {'db_layers': db_layers, 'colors': colors})

def change(request, id):
    
    geo = Geoserver('http://127.0.0.1:8085/geoserver', username='admin', password='geoserver')
    layers = geo.get_layers(workspace='App')['layers']['layer']
    print("Change ", layers, id)
    db_layers = Sentinel.objects.all()
    colors = Sentinel.COLOR_RAMPS_CHOICES

    return redirect("/", {'db_layers': db_layers, 'colors': colors})