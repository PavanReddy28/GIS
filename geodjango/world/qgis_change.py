import sys

def perform_change(request, input_path1, input_path2, output_path):
    path_list = ['C:/PROGRA~1/QGIS32~1.0/apps/qgis/./python', 'C:/Users/Admin/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python', 'C:/Users/Admin/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python/plugins', 'C:/PROGRA~1/QGIS32~1.0/apps/qgis/./python/plugins', 'C:\\Program Files\\QGIS 3.20.0\\bin\\python39.zip', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\DLLs', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\lib', 'C:\\Program Files\\QGIS 3.20.0\\bin', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\lib\\site-packages', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\lib\\site-packages\\win32', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\lib\\site-packages\\win32\\lib', 'C:\\PROGRA~1\\QGIS32~1.0\\apps\\Python39\\lib\\site-packages\\Pythonwin', 'C:/Users/Admin/AppData/Roaming/QGIS/QGIS3\\profiles\\default/python']
    for i in path_list:
        sys.path.append(i)

    from qgis.core import QgsApplication, QgsRasterLayer
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

    from django.contrib import messages
    messages.add_message(request, messages.SUCCESS, 'Change is detected! Check output in the Change Detection section.')
