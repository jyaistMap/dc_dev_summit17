# Demo 4: Connection Management

# If running outside of the Python window, uncomment the import
import arcpy

# allow Python to overwrite existing files and data
arcpy.env.overwriteOutput = True

# Block new connections to the geodatabase
arcpy.AcceptConnections(r'<path_to_connection_file>\<file_name>.sde', False)

# Get a list of users that are connected to the geodatabase
userList = arcpy.ListUsers(r'<path_to_connection_file>\<file_name>.sde')
print(userList)

# Clean up the output of the userList
for user in userList:
    print(user.Name, user.ID)
print('\n')

proc_id = input("ID of Process to Disconnect: ")

# Disconnect a single user
arcpy.DisconnectUser(r'<path_to_connection_file>\<file_name>.sde', int(proc_id))
print("ID {} disconnected.\n".format(proc_id))

# Regenerate list
userList = arcpy.ListUsers(r'<path_to_connection_file>\<file_name>.sde')
for user in userList:
    print(user.Name, user.ID)
print('\n')

# Disconnect all users
disconnect = input("Do you want to disconnect all users? y or n ")
if disconnect == 'y':
    arcpy.DisconnectUser(r'<path_to_connection_file>\<file_name>.sde', "ALL")
else:
    pass
print("All users disconnected.")

# Regenerate list
userList = arcpy.ListUsers(r'<path_to_connection_file>\<file_name>.sde')
for user in userList:
    print("Rmaining connection: {} {}".format(user.Name, user.ID))
