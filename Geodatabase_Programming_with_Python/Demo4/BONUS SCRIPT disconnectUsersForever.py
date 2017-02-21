#Disconnect users every 'x' minutes until time is up.

import time
import datetime
import arcpy

#Set Variables
hour = 16      #Hour of the day to stop (24 hour).
minute = 30    #Minute of that hour to stop.
sdeCon = r'<path_to_gdb_admin_connection_file\<file_name>.sde'
computerName = '<instance_name>'
pauseMinutes = .5

#Figure out when to stop and how long to pause
stop = datetime.time(hour, minute)
now = datetime.datetime.now()
finishTime = datetime.datetime.combine(now, stop)

pause = pauseMinutes * 60

while finishTime > datetime.datetime.now():
  userList = arcpy.ListUsers(sdeCon)
  idList = [(user.ID, user.Name) for user in userList if user.ClientName.lower()!=computerName.lower()]
  if len(idList)==0:
    print "Nobody else is connected"
  for id in idList:
    print 'Disconnecting user {0}'.format(id[1])
    arcpy.DisconnectUser(sdeCon, id[0])
  time.sleep(pause)
else:
  print "Quittin' time"