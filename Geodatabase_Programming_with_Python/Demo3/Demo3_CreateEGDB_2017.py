# Demo 3
# Name: CreateGDB.py
# Description: This script will create an enterprise geodatabase,
#              create schema, users, roles, and versions. It will
#              also apply permissions to all data. The end result
#              is a geodatabase that is ready to use.
# Author: Esri
# You'll need to edit the particulars to get these scripts to run 
# on your system: file paths, database names, usernames, passwords
# all particular to the live demos.

import arcpy

#Allow Python to overwrite existing files and data.
arcpy.env.overwriteOutput = True

#Create variables - some of these will be reused a lot.
platform = '<your_platform'
instance = '<your_instance_name'
database = 'Demo3'
authentication = 'DATABASE_AUTH' #type of authentication
databaseAdmin = '<dba>'
databaseAdminPass = '<dba_password>'
schema = 'SDE_SCHEMA'
gdbAdmin = '<gdb_admin>'
adminPass = '<gdb_admin_password>'
tablespace = ''
authFile = r'<path_to_authorization_file>\<file_name>.ecp'


try:

    # Create Enterprise Geodatabase.
    print("Creating the enterprise geodatabase")
    arcpy.CreateEnterpriseGeodatabase_management(platform, instance, database,
                                                 authentication, databaseAdmin,
                                                 databaseAdminPass, schema, gdbAdmin,
                                                 adminPass, tablespace, authFile)

    # Once the database has been created we will create an admin
    # connection so that we can create users in it.
    print("Creating connection to geodatabase as the DBA user")
    adminConn = arcpy.CreateDatabaseConnection_management(r'<path_to_save_file>', '<file_name>.sde', platform, instance, authentication, \
                                                          databaseAdmin, databaseAdminPass,'', database, schema)


    # First create a few roles for data viewers and data editors.
    print("\tCreating the viewer and editor roles")
    arcpy.CreateRole_management(adminConn, 'viewers')
    arcpy.CreateRole_management(adminConn, 'editors')

    # Next create users and assign them to their proper roles.
    # Generate a list of users to be added as editors and a list to be added as viewers.
    print("\t\tCreating users")
    editors = ['matt', 'colin', 'andrew', 'gary']
    viewers = ['heather', 'jon', 'annie', 'shawn']
    for user in editors:
        arcpy.CreateDatabaseUser_management(adminConn, 'DATABASE_USER',
                                            user, '<your_choice_of_password>', 'editors')
    for user1 in viewers:
        arcpy.CreateDatabaseUser_management(adminConn, 'DATABASE_USER',
                                            user1, '<your_choice_of_password>', 'viewers')

    # Create a data owner user named 'gdb'
    print("Creating the data owner (gdb)")
    arcpy.CreateDatabaseUser_management(adminConn, 'DATABASE_USER', '<your_gdb_username>', '<your_gdb_password>')
    print("****Finished tasks as the DBA user**** \n\n")
    
    # Now connect as the gdb admin to import a custom configuration keyword
    print("Creating a connection to the geodatabase as the gdb admin user (sde)")
    gdbAdminConn = arcpy.CreateDatabaseConnection_management(r'<path_to_save_connection_file>',
                                                          '<file_name>.sde', platform, instance,
                                                          'DATABASE_AUTH', gdbAdmin, adminPass,
                                                          'SAVE_USERNAME', database)
    
    # Import a custom configuration keyword for the data owner to use
    # The file being imported had been exported from dbtune, modified, and now ready to import
    print("\tImport a new geodatabase configuration keyword named 'custom'")
    arcpy.ImportGeodatabaseConfigurationKeywords_management(gdbAdminConn,  r'<path_to_keyword_file>\<keyword_file_name')
    print("****Finished tasks as the gdb admin user (sde) ****\n")
    
    # Create schema and apply permissions.
    # Create a connection as the data owner.
    print("\nCreating a connection to the geodatabase as the data owner (gdb)")
    ownerConn = arcpy.CreateDatabaseConnection_management(r'<path_to_save_connection_file>',
                                                          'gdbDataOwner.sde', platform, instance,
                                                          'DATABASE_AUTH', 'gdb','gdb$DCDevSummit17',
                                                          'SAVE_USERNAME', database)
    
    # Import the data as the gdb user and specify the custom config keyword that the gdb admin has provided
    print("\tImporting the data as the data owner (gdb) using a config keyword named 'custom'")
    arcpy.ImportXMLWorkspaceDocument_management(ownerConn, r'<path_to_workspace_file>\<file_name>.xml', 'SCHEMA_ONLY', 'CUSTOM')

    # Get a list of feature classes, tables and feature datasets
    # and apply appropriate permissions.
    print("\tBuilding a list of feature classes, tables, and feature datasets in the geodatabase")
    arcpy.env.workspace = ownerConn[0] #note environments do not work with result objects.
    dataList = arcpy.ListTables() + arcpy.ListFeatureClasses() + arcpy.ListDatasets("", "Feature")

    # Use roles to apply permissions.
    print("\tGranting appropriate privileges to the data for the 'viewers' and 'editors' roles")
    arcpy.ChangePrivileges_management(dataList, 'viewers', 'GRANT')
    arcpy.ChangePrivileges_management(dataList, 'editors', 'GRANT', 'GRANT')

    # Register the data as versioned.
    print("\tRegistering the data as versioned")
    for dataset in dataList:
        arcpy.RegisterAsVersioned_management(dataset)

    # Finally, create a version for each editor.
    print("\tCreating a private version for each user in the editor role")
    for user3 in editors:
        verCreateConn = arcpy.CreateDatabaseConnection_management(r'<path_to_save_connection_file>',
                                                                  '<file_name>.sde', platform, instance,
                                                                  'DATABASE_AUTH', user3,
                                                                  '<your_password_choice>','SAVE_USERNAME',
                                                                  database)
        arcpy.CreateVersion_management(verCreateConn, 'sde.Default',
                                       '<your_choice_of_version_name>', 'PRIVATE')
        arcpy.ClearWorkspaceCache_management()
    print('\n****Done Creating Demo3 Geodatabase with roles, users, data and privileges.')

except:
    print('Script failure.\n')
    print(arcpy.GetMessages())




