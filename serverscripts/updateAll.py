# Demonstrates how to stop or start all services in a folder

# For Http calls
import httplib, urllib, json

# For system tools
import sys

#for regex splitting
import re
# For reading passwords without echoing
import getpass


# Defines the entry point into the script
def main(argv=None):
    # Print some info
    print
    print "This tool updates all the max/min instances on a server."
    print  
    
    # Ask for admin/publisher user name and password
    username = raw_input("Enter user name: ")
    password = getpass.getpass("Enter password: ")
    
    # Ask for server name
    serverName = raw_input("Enter server name: ")
    serverPort = 6080
    excluded = re.split('[,\s]+',raw_input("Enter excluded folders: ").upper())

    # stopOrStart = raw_input("Enter whether you want to START or STOP all services: ")
    minInstances = raw_input("Enter the new minimum: ")
    maxInstances = raw_input("Enter the new maximum: ")

    # Check to make sure the minimum and maximum are numerical
    try:
        minInstancesNum = int(minInstances)
        maxInstancesNum = int(maxInstances)
    except ValueError:
        print "Numerical value not entered for minimum, maximum, or both."
        return

    # Check to make sure stop/start parameter is a valid value
    #if str.upper(stopOrStart) != "START" and str.upper(stopOrStart) != "STOP":
    #    print "Invalid STOP/START parameter entered"
    #    return
    
    # Get a token
    token = getToken(username, password, serverName, serverPort)
    if token == "":
        print "Could not generate a token with the username and password provided."
        return
    
            
    folderURL = "/arcgis/admin/services/"
    
    # This request only needs the token and the response formatting parameter 
    params = urllib.urlencode({'token': token, 'f': 'json'})
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    # Connect to URL and post parameters    
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn.request("POST", folderURL, params, headers)
    
    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Could not read folder information."
        return
    else:
        data = response.read()
        
        # Check that data returned is not an error object
        if not assertJsonSuccess(data):          
            print "Error when reading folder information. " + str(data)
        else:
            print "Processed folder information successfully. Now processing services..."

        # Deserialize response into Python object
        dataObj = json.loads(data)
        httpConn.close()
        for folder in dataObj['folders']:
            if folder.upper() in excluded:
                continue

            folderURL = "/arcgis/admin/services/" + folder
    
    # This request only needs the token and the response formatting parameter 
            params = urllib.urlencode({'token': token, 'f': 'json'})
    
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    # Connect to URL and post parameters    
            httpConn = httplib.HTTPConnection(serverName, serverPort)
            httpConn.request("POST", folderURL, params, headers)
    
    # Read response
            response = httpConn.getresponse()
            if (response.status != 200):
                httpConn.close()
                print "Could not read folder information."
                return
            else:
                data = response.read()
                
                # Check that data returned is not an error object
                if not assertJsonSuccess(data):          
                    print "Error when reading folder information. " + str(data)
                else:
                    print "Processed current folder information successfully. Now processing services..."

                # Deserialize response into Python object
                dataObj2 = json.loads(data)
                httpConn.close()

                # Loop through each service in the folder and update instances    
                for item in dataObj2['services']:
                    fullSvcName = item['serviceName'] + "." + item['type']
                    serviceURL = "/arcgis/admin/services/" + folder + "/" + fullSvcName
                    
                    # This request only needs the token and the response formatting parameter 
                    params = urllib.urlencode({'token': token, 'f': 'json'})
                    
                    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                    
                    # Connect to service to get its current JSON definition    
                    httpConn = httplib.HTTPConnection(serverName, serverPort)
                    httpConn.request("POST", serviceURL, params, headers)
                    
                    # Read response
                    response = httpConn.getresponse()
                    if (response.status != 200):
                        httpConn.close()
                        print "Could not read service information."
                        return
                    else:
                        data = response.read()
                        
                        # Check that data returned is not an error object
                        if not assertJsonSuccess(data):          
                            print "Error when reading service information. " + str(data)
                        else:
                            print "Service information read successfully. Now changing properties..."

                        # Deserialize response into Python object
                        dataObj = json.loads(data)
                        httpConn.close()

                        # Edit desired properties of the service
                        dataObj["minInstancesPerNode"] = minInstancesNum
                        dataObj["maxInstancesPerNode"] = maxInstancesNum

                        # Serialize back into JSON
                        updatedSvcJson = json.dumps(dataObj)

                        # Call the edit operation on the service. Pass in modified JSON.
                        editSvcURL = serviceURL + "/edit"
                        params = urllib.urlencode({'token': token, 'f': 'json', 'service': updatedSvcJson})
                        httpConn.request("POST", editSvcURL, params, headers)
                        
                        # Read service edit response
                        editResponse = httpConn.getresponse()
                        if (editResponse.status != 200):
                            httpConn.close()
                            print "Error while executing edit."
                            return
                        else:
                            editData = editResponse.read()
                            
                            # Check that data returned is not an error object
                            if not assertJsonSuccess(editData):
                                print "Error returned while editing service" + str(editData)        
                            else:
                                print "Service edited successfully."

                        httpConn.close()   
                
        return

        # A function to generate a token given username, password and the adminURL.
def getToken(username, password, serverName, serverPort):
    # Token URL is typically http://server[:port]/arcgis/admin/generateToken
    #tokenURL = "http://localhost:6080/arcgis/admin/generateToken"
    tokenURL = "/arcgis/admin/generateToken"
    
    params = urllib.urlencode({'username': username, 'password': password, 'client': 'requestip', 'f': 'json'})
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    # Connect to URL and post parameters
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn.request("POST", tokenURL, params, headers)
    
    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Error while fetching tokens from admin URL. Please check the URL and try again."
        return
    else:
        data = response.read()
        httpConn.close()
        
        # Check that data returned is not an error object
        if not assertJsonSuccess(data):            
            return
        
        # Extract the token from it
        token = json.loads(data)        
        return token['token']            
        

# A function that checks that the input JSON object 
#  is not an error object.
def assertJsonSuccess(data):
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        print "Error: JSON object returns an error. " + str(obj)
        return False
    else:
        return True
    
        
# Script start
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))