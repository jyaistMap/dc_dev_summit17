# Author:  ESRI
# Date:    July 5, 2010
# Version: ArcGIS 10.0
# Summary: This script will add a layer file into a map document. The script
#          must be run from within ArcMap because it references the CURRENT
#          map document.  The purpose of the script is to create a user
#          friendly tool that allows users to simply add a layer from a list
#          of existing layer files all stored in a common location. A validation
#          script is used to automatically populate two of the parameters.
#          The parameters are:
#               1) Browse to a folder that contains layer files. This could be
#                  hard coded within the validation script eliminating the need
#                  for entering this parameter.
#               2) Select a layer file from the list.  This is auto populated
#                  using a validation script.
#               3) Select a data frame.  This is also auto populated using a
#                  validation script.
#               4) Select one of 3 placement positions.
#
# Note: This script tool will only work if background processing is disabled.
#       because CURRENT is being used.
# Note: To run the script from ArcMap either run the script tool from the
#       Catalog window from within ArcMap or add the script tool into the UI
#       via the customize dialog box [Geoprocessing Tools].

import arcpy

try:
    #Read parameters from dialog
    layerFile = r'C:\StudentPy\PYTH\Schools.lyr'
    position = 'TOP'
    
    #Have to reference the project in ArcGIS pro
    #The ArcGISProject class is in the mp module
    aprx = arcpy.mp.ArcGISProject(r'C:\DCDevSummit\2017\pro_scripting_python\Two2Three.aprx')

    #retrieve a list of Map(s) from the Project
    #and place the first Map object into a variable
    mapx = aprx.listMaps()[0]
    
    #Reference the layer file on disk
    #noting the mapping module is now mp
    #and using the LayerFile class
    addLayer = arcpy.mp.LayerFile(layerFile)
    
    mapx.addLayer(addLayer, position)
    aprx.save()

#   del mxd, addLayer
    del mapx, addLayer

except Exception as e:
    import traceback
    list(map(arcpy.AddError, traceback.format_exc().split("\n"))) #fixed with Python 2to3.py utility
    arcpy.AddError(str(e))
