# Demonstrates how to stop or start all services in a folder

# For Http calls
import httplib, urllib, json

# For system tools
import sys

# For reading passwords without echoing
import getpass

# Defines the entry point into the script
def main(argv=None):
    # Print some info
    print
    print "This re-starts the following service:"
    print "http://mrsbmapp20982.ad.water.ca.gov/arcgis/rest/Public/WaterDistrictsTestMap.MapServer"
    print  
    
    # Ask for admin/publisher user name and password
    username = raw_input("Enter user name (water\username): ")
    password = getpass.getpass("Enter password: ")
    
    # Ask for server name
    #serverName = raw_input("Enter server name: ")
    serverName = "mrsbmapp20982.ad.water.ca.gov"
    serverPort = 6080
    #serverPort = 80

    #print "Enter the service name in the format <folder>/<name>.<type>"
    #service = raw_input("For example Public/WaterDistricts.MapServer: ")
    print "Restarting http://mrsbmapp20982.ad.water.ca.gov/arcgis/rest/Public/WaterDistrictsTestMap.MapServer"
    service = "Public/WaterDistrictsTestMap.MapServer"
 
    # Get a token
    token = getToken(username, password, serverName, serverPort)
    if token == "":
        print "Could not generate a token with the username and password provided."
        return
            
    # Construct URL to start a service - as an example the Geometry service
    #serviceStartURL = "/arcgis/admin/services/utilities/Geometry.GeometryServer/start"
    serviceStopURL = "/arcgis/admin/services/" + service + "/stop"
    serviceStartURL = "/arcgis/admin/services/" + service + "/start"

    
    # This request only needs the token and the response formatting parameter 
    params = urllib.urlencode({'token': token, 'f': 'json'})
    
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    
    # Connect to URL and post parameters    
    httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn.request("POST", serviceStopURL, params, headers)
    
    # Read response And return if error else proceed to start service
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Error while attempting to stop the service."
        return
    else:
        data = response.read()
        #httpConn.close()   # don't close here since used in next "start" request
        # Check that data returned is not an error object
        if not assertJsonSuccess(data):          
            print "Error returned by <stop> operation. " + data
            raw_input("Press enter to exit")
            return
        else:
            print "Operation <stop> completed successfully!"
        #return  # don't return here , we want the service to start again
    httpConn.request("POST", serviceStartURL, params, headers)    
    # Read response And return if error else proceed to start service
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Error while attempting to start the service."
        raw_input("Press enter to exit")
        return
    else:
        data = response.read()
        httpConn.close()
        # Check that data returned is not an error object
        if not assertJsonSuccess(data):          
            print "Error returned by <start> operation. " + data
            raw_input("Press enter to exit")
        else:
            print "Operation <start> completed successfully!"
            raw_input("Press enter to exit")
        return


# A function to generate a token given username, password and the adminURL.
def getToken(username, password, serverName, serverPort):
    # Token URL is typically http://server[:port]/arcgis/admin/generateToken
    tokenURL = "/arcgis/admin/generateToken"
    #tokenURL = "http://" + serverName + ":" + str(serverPort) + "/arcgis/admin/generateToken"
    
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
