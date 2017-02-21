# Demo 2: Create Enterprise Geodatabase, Users, and Roles

# If running outside of the Python window, uncomment the import
import arcpy

# allow python to overwrite existing data and files
arcpy.env.overwriteOutput = True

# Create the geodatabase
# Full tool documentation: Data Management Toolbox < Geodatabase Administration Toolset
# https://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-enterprise-geodatabase.htm
# different database platforms have different requirements so refer to documentation for 
# particulars to connect
arcpy.CreateEnterpriseGeodatabase_management('<your_platform>', 
                                             '<your_instance_name>', 
                                             '<database_name>', # see doc
                                             '<authentication_type>', # see doc
                                             '<your_dba_user_name>', 
                                             '<your_dba_password>', 
                                             '<sde_schema>', # see doc, only relevant to SQL Server 
                                             '<geodatabase_administrator_name>',
                                             '<geodatabase_administrator_password>', 
                                             '', r'<path_to_your_license_file>')

# Create database connection
arcpy.CreateDatabaseConnection_management(r'<full_path_to_connection_file>', '<file_name>.sde', '<platform>', '<your_instance_name>', '<authentication_type>', '<your_dba_user_name>', '<dba_password>', '<save_user_pass>', '<database>', 'schema')

# Create an editor role
arcpy.CreateRole_management(r'<full_path_to_connection_file>\<file_name>.sde', 'editor')

# Create list of users
userList = ['matt', 'tom', 'colin']

# Create users and assign to editor role
for user in userList:
    arcpy.CreateDatabaseUser_management(r'<full_path_to_connection_file>\<file_name>.sde', '<authentication_type>', user, '<your_choice_password>', 'editor')
        
