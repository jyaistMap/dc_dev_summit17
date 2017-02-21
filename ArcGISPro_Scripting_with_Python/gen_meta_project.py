"""Python script to examing the contents of an ArcGIS Pro Project."""

# import the appropriate modules
import arcpy
import os

# set the working environment
arcpy.env.workspace = r"<path_to_directory_with_project>"
work_path = arcpy.env.workspace

# instantiate the Project
aprx = arcpy.mp.ArcGISProject(work_path + os.sep + "<project_name>.aprx")

# use os.path and string functions to create variable for project name
base = os.path.basename(aprx.filePath)
project_name = base.split(".")[0].replace("_", " ")

# get a list of the views and layouts in the Project
vw_list = aprx.listMaps()
lyt_list = aprx.listLayouts()
# print the type of view, the basemap, and layers in the view
print("The {} Project has {} view(s) and {} layout(s):".format(project_name, len(vw_list), 
                                                               len(lyt_list)))
print("{:*<25}".format("The Views"))
for vw in vw_list:
    print("\n\t{} is a {} with {} layers:".format(vw.name, vw.mapType.capitalize(),
                                                len(vw.listLayers())))
    print("\t{:-<50}".format(""))
    lyrs = vw.listLayers()
    basemaps = [lyr.name for lyr in lyrs if lyr.isBasemapLayer]
    if basemaps:
        print("\t\t{}:".format("Basemaps".upper()))
        for basemap in basemaps:
            print("\t\t\t{}".format(basemap))
    print("\t\t{}:".format("Layers".upper()))
    for lyr in lyrs:
        if not lyr.isBasemapLayer:
            print("\t\t\t{}".format(lyr.name))
print("\n{:*<25}".format("The Layouts"))
for lyt in lyt_list:
    print("\t{} is a layout with {} elements:".format(lyt.name, len(lyt.listElements())))
    print("\t{:-<100}".format(""))
    for elem in lyt.listElements():
        print("\t\t{} Element is a {} of {} page units wide.".
              format(elem.name, elem.type, elem.elementWidth))