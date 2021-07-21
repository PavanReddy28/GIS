import sys

def perform_cluster(input_path, output_path):
    path = ['C:/OSGeo4W/apps/qgis-ltr/./python', 'C:/Users/YVM Reddy/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python', 'C:/Users/YVM Reddy/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python/plugins', 'C:/OSGeo4W/apps/qgis-ltr/./python/plugins', 'C:\\Program Files\\QGIS 3.18\\apps\\qgis\\python', 'C:\\OSGeo4W\\bin\\python39.zip', 'C:\\OSGeo4W\\apps\\Python39\\DLLs', 'C:\\OSGeo4W\\apps\\Python39\\lib', 'C:\\OSGeo4W\\bin', 'C:\\Users\\YVM Reddy\\AppData\\Roaming\\Python\\Python39\\site-packages', 'C:\\OSGeo4W\\apps\\Python39', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages\\win32', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages\\win32\\lib', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages\\Pythonwin', 'C:/Users/YVM Reddy/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python']
    print(path[0], path[1])
    for i in path:
        sys.path.append(i)

    from qgis.core import QgsApplication, QgsRasterLayer, QgsProcessingFeedback
    from qgis import processing

    QgsApplication.setPrefixPath("C:\\Program Files\\QGIS 3.20.0\\apps\\qgis", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    from plugins.processing.core.Processing import Processing

    Processing.initialize()
    input_raster = QgsRasterLayer(input_path,'olayer')
    output_path = output_path
    cluster_params = {
        'CLUSTER':output_path,
        'GRIDS':[input_raster],
        'METHOD':1,
        'NCLUSTER':5,
        'MAXITER':5,
        'NORMALISE':False,
        'OLDVERSION':False,
        'UPDATEVIEW':True,
        'STATISTICS':'TEMPORARY_OUTPUT'
    }

    class MyFeedBack(QgsProcessingFeedback):

        def setProgressText(self, text):
            print(text)

        def pushInfo(self, info):
            print(info)

        def pushCommandInfo(self, info):
            print(info)

        def pushDebugInfo(self, info):

            print(info)

        def pushConsoleInfo(self, info):
            print(info)

        def reportError(self, error, fatalError=False):
            print(error)

    processing.run("saga:kmeansclusteringforrasters",cluster_params,feedback=MyFeedBack())

    qgs.exitQgis()