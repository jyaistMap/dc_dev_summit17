# Demo 1: Create Database Connection File
#         The script is generalized to show what you'll have to enter
#         for your particular database. Examples of what was used for
#         live Demos have been included in comments. Throughout the rest
#         of the scripts, you'll have to change information to match
#         your system.
# If running outside of the Python window, uncomment the import
import arcpy

# allow python to overwrite existing data and files
arcpy.env.overwriteOutput = True

# Create the connection file
# Tool documented in the Workspace Toolset of the Data Management Toolbox
arcpy.CreateDatabaseConnection_management(r'<directory_path_for_connection_file>', #ex: C:\WorkArea\GDB
                                          '<file_name>', #ex dba_conn.sde
                                          '<platform>', # ex. "SQL_SERVER",
                                          '<database_instance>', #ex 'YAISTWIN8'
                                          'DATABASE_AUTH', # either DATABASE_AUTH or OPERATING_SYSTEM_AUTH
                                          'dba_username', # particular to your database
                                          'dba_password', # particular to your database
                                          '', # can enter SAVE_USERNAME or DO_NOT_SAVE_USERNAME
                                          "<database>") # only relevant to PostgreSQL and SQL Server

#for this example the path to describ wourld be r'C:\WorkArea\GDB\dba_conn.sde'
print('Database Name:\t' + arcpy.Describe(r'<full_path_to_connection_file>').connectionProperties.database)
print('Connected to {} version'.format(arcpy.Describe(r'<full_path_to_connection_file>').connectionProperties.version))
print('Authentication Mode:\t' + arcpy.Describe(r'<full_path_to_connection_file>').connectionProperties.authentication_mode)
print('Is this a Geodatabase?:\t' + arcpy.Describe(r'<full_path_to_connection_file>').connectionProperties.is_geodatabase)
print('Is this at the current Geodatabase Release?:\t' + str(arcpy.Describe(r'<full_path_to_connection_file>').currentRelease))
print('Type of Workspace:\t' + arcpy.Describe(r'<full_path_to_connection_file>').workspaceType)