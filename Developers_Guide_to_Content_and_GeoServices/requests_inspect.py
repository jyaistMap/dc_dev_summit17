"""Script for examining the services accessible from an arcgis portal instance.
   Changing the root url allows you to examine either an ArcGIS Online
   Organization or  your own Portal for ArcGIS installation. This script uses
   the higher-level requests module over the urllib.parse/error/request modules.
   Script would need edited to use security in the requests module."""



import requests
import json
import os

root_url = "<particular_to_your_portal/org>"

# Ininitialize a session as a context manager to 
# persist variables across requests
with requests.Session() as s:
    # Generate the token    
    # not sure how to handle verifying the cerificate, get ssl error if
    # set verify=\path\to\cert as in doc at http://requests.readthedocs.io/en/master/user/advanced
    # import portal or server's self-signed certificate as trusted cert? web server's cert?
    auth = {'username': '<your_user_name>', 'password': 'your_user_password', 'referer': 'http://www.arcgis.com','f': 'json'}
    op = "generateToken"
    r = s.post(root_url + os.sep + op, data = auth, verify = False)
    #json of response accessible through r.json() or using json.loads(r.text)
    token = r.json()['token']
    #Get the analysis url from the portal self resource helperServices
    #append token to the auth dict
    auth['token'] = token
    #construct the url to the self resource
    portals_url = root_url + os.sep + "portals"
    self_view = portals_url + os.sep + "self"
    print("Self Resource: {}".format(self_view))
    #issue request
    r = s.post(self_view, data = auth, verify = False)
    print("\n\tUsing {} encoding for this request.\n".format(r.encoding))
    #convert the response to json
    r_json = json.loads(r.text)
    #extract dictionary of all services accessible with the portal
    if 'helperServices' in r_json:
        portal_services =  r_json.get('helperServices')
        #retrieve the analysis service and its url from the Services dictionary
        #if 'analysis' in portal_services:
            #analysis_service_info = portal_services.get('analysis')
            #if 'url' in analysis_service_info:
                #analysis_url = analysis_service_info.get('url')
    else:
        raise Exception("Unable to obtain the Analysis URL.")
    # how do I find out the tasks on the service from the REST API?

    print("List of Services Available from root url:")
    print("\t\t{}.".format(root_url))
    print("{:*<50}".format(""))
    for service_item in portal_services.items():
        if isinstance(service_item[1], dict):
            print(service_item[0].capitalize())
            for key, value in service_item[1].items():
                print("\t{}:\t{}".format(key, value))
        elif isinstance(service_item[1], list):
            print(service_item[0].capitalize())
            if isinstance(service_item[1][0], dict):
                for key2, value2 in service_item[1][0].items():
                    print("\t\t{}:\t{}".format(key2, value2))