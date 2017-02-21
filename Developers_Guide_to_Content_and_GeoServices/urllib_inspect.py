"""Script for examining the services accessible from an arcgis portal instance.
   Changing the root url allows you to examine either an ArcGIS Online
   Organization or  your own Portal for ArcGIS installation."""

import urllib.parse
import urllib.request
import urllib.error
import json
import os # can't use os.sep with tasks...enters in \ instead of /

# Create variable for proper URI separator since os.sep on windows is \
uri_sep = "/"
# Set up parameters, including headers, for the request object
params = {
    'username': '<org/portal_user_name>',
    'password': '<org/portal_password>',
    'referer': 'http://www.arcgis.com',
    'f': 'json'
}

headers = {}

# Variable for the root url of the portal. You know the url of your own
# otherwise can use http://www.arcgis.com/sharing/rest for ArcGIS Online
root = "<particular_to_your_org/portal>"

# create a portals-url variable to get access to the portal's Self resource
portals_url = root + uri_sep + "portals"
print("Portals URL: {}".format(portals_url))

# create a variable to the Self resource representing portal's view to current user
portal_view = portals_url + uri_sep + "self"
print("\tPortal View url: {}".format(portal_view))
print("{:-<100}\n".format(""))

# Generate a token for additional requests
# variable representing the generate token task
op = "generateToken"

# construct the request object:
# encode the params dictionary to url
uparams = urllib.parse.urlencode(params)
# encode the params string to bytes for use in post to avoid TypeError
params_post = uparams.encode()
# construct the request object
req = urllib.request.Request(root + "/" + op, params_post)
# send the request
resp = urllib.request.urlopen(req)
# resp is an HTTPResponse object whose read method returns a byte string
# that needs decoded to a string and loaded to an object
content = resp.read().decode('utf-8')
json_resp = json.loads(content)
token = json_resp.get('token')

# Use the token to generate a list of services accessible from the portal
# first add the token to the parameters
params['token'] = token

# encode params to url, then to utf-8 byte stream to POST
params_post = urllib.parse.urlencode(params).encode()
# construct request object
self_req = urllib.request.Request(portal_view, params_post)
# send the request
resp = urllib.request.urlopen(self_req)
# decode the returned HTTPResponse object to byte stream and load into json obj
Self_Resource = json.loads(resp.read().decode('utf-8'))

# print out information about the available Helper Services in the portal
try:
    for svc in Self_Resource['helperServices'].items():
        print(svc[0].capitalize())
        if isinstance(svc[1], list):
            for member in svc[1]:
                print("\t{}".format(member))
        elif isinstance(svc[1], dict):
            for key, value in svc[1].items():
                print("\t{}:\t{}".format(key, value))
except KeyError as e:
    print("The helperServices object was not found.")

## list of Federated servers
#s_parameters = urllib.parse.urlencode(params)
#s_url_byte_encoded = s_parameters.encode()
#req = urllib.request.Request(portals_url + uri_sep + Self_Resource['id'] + uri_sep + "servers", s_url_byte_encoded)
#print(portals_url + uri_sep + Self_Resource['id'] + uri_sep + "servers")
#resp = urllib.request.urlopen(req)
#with resp as response:
    #response_decoded = response.read().decode('utf-8')
    #response_json = json.loads(response_decoded)
    #for key, value in response_json.items():
        #server_obj = value
        #print(server_obj)
        #print("\n{:*<50}".format(""))
        #print("\t{}:\t".format(server_obj[0]['name']))
        #print("\t{}:\t".format(server_obj[0]['serverRole']))
        #print("\t{}:\t".format(server_obj[0]['url']))