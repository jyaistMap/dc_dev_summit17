# Author:  ESRI
# Date:    July 5, 2010
# Version: ArcGIS 10.0
# Summary: This script will add a layer file into a map view within a project 
#          document. This script should be compared to gen_AddLayerFile_DT.py 
#          to see the different classes and methods used to accommplish the same
#          task in ArcGIS Pro. Error trapping included.

import arcpy

try:
    # Set parameters
    layerFile = r'<path_to_a_layer_file>\<layer-file.lyr>'
    position = 'TOP'
    
    #Have to reference the project in ArcGIS pro
    #The ArcGISProject class is in the mp module
    aprx = arcpy.mp.ArcGISProject(r'<path_to_ArcGIS Pro Project>\<project_name>.aprx')

    #retrieve a list of Map(s) from the Project
    #and place the first Map object into a variable
    mapx = aprx.listMaps()[0]
    
    #Reference the layer file on disk
    #noting the mapping module is now mp
    #and using the LayerFile class
    addLayer = arcpy.mp.LayerFile(layerFile)
    
    mapx.addLayer(addLayer, position)
    aprx.save() # 

#   del mxd, addLayer
    del mapx, addLayer

except Exception as e:
    import traceback
    list(map(arcpy.AddError, traceback.format_exc().split("\n"))) #fixed with Python 2to3.py utility
    arcpy.AddError(str(e))
