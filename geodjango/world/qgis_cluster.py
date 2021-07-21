import sys

def perform_cluster(input_path, output_path):
    #path modification to disable the virtual env
    prev_sys_path = sys.path
    prev_executable_path  = sys.executable
    sys.path = ['C:\\Users\\Admin\\Desktop', 'c:\\users\\admin\\appdata\\local\\programs\\python\\python39\\python39.zip', 'c:\\users\\admin\\appdata\\local\\programs\\python\\python39\\DLLs', 'c:\\users\\admin\\appdata\\local\\programs\\python\\python39\\lib', 'c:\\users\\admin\\appdata\\local\\programs\\python\\python39']
    sys.executable = r"C:\Users\Admin\AppData\Local\Programs\Python\Python39\python.exe"
    path_list = ['C:/PROGRA~1/QGIS32~1.0/apps/qgis/./python', 'C:/Users/Admin/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python', 'C:/Users/Admin/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python/plugins', 'C:/PROGRA~1/QGIS32~1.0/apps/qgis/./python/plugins', 'C:\\Program Files\\QGIS 3.20.0\\bin\\python39.zip', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\DLLs', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\lib', 'C:\\Program Files\\QGIS 3.20.0\\bin', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\lib\\site-packages', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\lib\\site-packages\\win32', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\lib\\site-packages\\win32\\lib', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\lib\\site-packages\\Pythonwin', 'C:/Users/Admin/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python'] 
    for i in path_list:
        sys.path.append(i)

    from qgis.core import QgsApplication, QgsRasterLayer, QgsProcessingFeedback
    from qgis import processing

    QgsApplication.setPrefixPath("C:\\Program Files\\QGIS 3.20.0\\apps\\qgis", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    from plugins.processing.core.Processing import Processing

    Processing.initialize()
    input_raster = QgsRasterLayer(input_path,'olayer')
    out_path = output_path[:-3]+"sdat"
    cluster_params = {
        'CLUSTER':out_path,
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

    convert_params = {
        'INPUT':out_path,
        'OUTPUT':output_path
    }
    processing.run("gdal:translate", convert_params)
    
    qgs.exitQgis()

    #restore path variables
    sys.path = prev_sys_path
    sys.executable = prev_executable_path