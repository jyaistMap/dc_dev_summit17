"""Refresh the Database to make sure it's accepting connections again."""

import arcpy

# connect to the database as the dba admin
arcpy.env.overwriteOutput = True
arcpy.AcceptConnections(r'<path_to_connection_file>\<file_name>.sde', True)
print("\tDatabase accepting Connections.")

