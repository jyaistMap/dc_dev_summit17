"""Python Script to import mxds into ArcGIS Pro Projects."""


# import modules
import arcpy
import os

# set the workspace
arcpy.env.workspace = r'C:\StudentPy\PYTH\Geometry_objects'
wkspace = arcpy.Describe(arcpy.env.workspace)
work_path = arcpy.env.workspace

# allow owverwrite
arcpy.env.overwriteOutput = True

print("The {} Workspace is a {} type space.".format(wkspace.name, wkspace.workspaceType))
print("{:-<50}\n".format(""))

# create list of mxds in the directory
print("Map Documents in Current Directory:")
print("{:-<50}".format(""))
mxds = []
for dir, subdir, files in os.walk(work_path):
    #print("{} has {} subdirectories and {} files.".format(dir, len(subdir), len(
        #files)))
    for file in files:
        if file[-4:] == '.mxd' and file not in mxds:
            mxds.append(file)
for mxd in mxds:
    print("\t" + mxd)

# create a new project
aprx = arcpy.mp.ArcGISProject(r"C:\DCDevSummit\2017\pro_scripting_python\Importation\Importation.aprx")

#import mxds to project
for mxd in mxds:
    aprx.importDocument(work_path + os.sep + mxd, True)
    print("\t\tAdded {} to Importation Project.".format(mxd))
aprx.save()
print("\n****** Script Complete. *********")    
