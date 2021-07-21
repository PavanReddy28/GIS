import sys

def perform_change(input_path1, input_path2, output_path):
    path_list = ['C:/OSGeo4W/apps/qgis-ltr/./python', 'C:/Users/YVM Reddy/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python', 'C:/Users/YVM Reddy/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python/plugins', 'C:/OSGeo4W/apps/qgis-ltr/./python/plugins', 'C:\\Program Files\\QGIS 3.18\\apps\\qgis\\python', 'C:\\OSGeo4W\\bin\\python39.zip', 'C:\\OSGeo4W\\apps\\Python39\\DLLs', 'C:\\OSGeo4W\\apps\\Python39\\lib', 'C:\\OSGeo4W\\bin', 'C:\\Users\\YVM Reddy\\AppData\\Roaming\\Python\\Python39\\site-packages', 'C:\\OSGeo4W\\apps\\Python39', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages\\win32', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages\\win32\\lib', 'C:\\OSGeo4W\\apps\\Python39\\lib\\site-packages\\Pythonwin', 'C:/Users/YVM Reddy/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python']
    for i in path_list:
        sys.path.append(i)

    from qgis.core import QgsApplication, QgsRasterLayer, QgsProcessingFeedback
    from qgis import processing

    QgsApplication.setPrefixPath("C:\\Program Files\\QGIS 3.20.0\\apps\\qgis", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    from plugins.processing.core.Processing import Processing

    Processing.initialize()

    rlayer1 = QgsRasterLayer(input_path1, 'layer1')
    rlayer2 = QgsRasterLayer(input_path2, 'layer2')

    diff_params = {
        'INPUT_A':rlayer1,
        'INPUT_B':rlayer2,
        'BAND_A':1,
        'BAND_B':1,
        'FORMULA':'A-B',
        'OUTPUT':output_path
    }

    processing.run("gdal:rastercalculator",diff_params)