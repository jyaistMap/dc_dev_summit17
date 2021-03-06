"""Python Script to import mxds into ArcGIS Pro Projects."""


# import modules
import arcpy
import os

# set the workspace
arcpy.env.workspace = r'<path_to_directory_to_search_for_mxds>'
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
    for file in files:
        if file[-4:] == '.mxd' and file not in mxds:
            mxds.append(file)
for mxd in mxds:
    print("\t" + mxd)

# create a new project
aprx = arcpy.mp.ArcGISProject(r"<path_to_project>\<project_name>.aprx")

#import mxds to project
for mxd in mxds:
    aprx.importDocument(work_path + os.sep + mxd, True)
    print("\t\tAdded {} to <project_name> Project.".format(mxd))
aprx.save()
print("\n****** Script Complete. *********")    
