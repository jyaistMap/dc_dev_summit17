# Author:  ESRI
# Date:    July 5, 2010
# Version: ArcGIS 10.0
# Summary: This script will add a layer file into a map view within a project 
#          document. This script should be compared to gen_AddLayerFile_Pro.py 
#          to see the different classes and methods used to accommplish the same
#          task in ArcGIS Pro. Error trapping included.

import arcpy

try:
    #Read parameters from dialog
    folderLocation = r'<path_to_a_directory>'
    layerFile = '<path_to_directory>\<layer_file_name>.lyr'
    dfName = 'Layers' #name of data frame in mxd
    position = 'TOP'

    #Reference map document from within ArcMap
    mxd = arcpy.mapping.MapDocument(r'<path_to_a_directory>\<mxd_name>.mxd')

    #Reference the layer file on disk and data frame
    addLayer = arcpy.mapping.Layer(layerFile)
    df = arcpy.mapping.ListDataFrames(mxd, dfName)[0]
    #Add layer file
    arcpy.mapping.AddLayer(df, addLayer, position)

    #Refresh TOC and ActiveView
    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()

    mxd.save()
    del mxd, addLayer

except Exception as e:
    import traceback
    map(arcpy.AddError, traceback.format_exc().split("\n"))
    arcpy.AddError(str(e))
