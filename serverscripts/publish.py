#! /c/Python27/ArcGIS10.2/python
print("\nRunning service publisher.\n")

import arcpy
from os import path, listdir
import sys
import httplib, urllib, json
import getpass

def main(argv=None):

  username = raw_input("Enter user name: ")
  password = getpass.getpass("Enter password: ")
  serverName = raw_input("Enter Server name (mrsbmapp...): ") or 'mrsbmapp21164'
  serverPort = 6080

  print("\nGetting token...\n")

  token = getToken(username,password,serverName,serverPort)
  print(token)
  if token == None:
    print("Could not generate a token with the username and password provided.")
    return

  folderPath = path.abspath(raw_input("Enter the path to the folder of MXDs: ") or '.')
  matchParam = raw_input("Enter filter for MXD names (or nothing for all MXDs): ")
  serverFolder = raw_input("Enter service folder: ") or "Public"
  gisConnection = raw_input("Enter name of GIS Server connection: ") or "prod"
  overrideProps = raw_input("Enter JSON updates to service properties: ")

  arcpy.env.overwriteOutput = True



  mxds = [i for i in listdir(folderPath) if i.endswith('.mxd') and (matchParam=='' or matchParam in i)]

  for mxd in mxds:
    print("Processing map: {}\n".format(mxd))
    name = mxd.split('.')[0]
    sdName = path.join(folderPath,name)
    draft = sdName+".sddraft"
    sd = sdName+".sd"

    print("Making Service Definition Draft: {}.\n".format(draft))

    analysis = arcpy.mapping.CreateMapSDDraft(path.join(folderPath,mxd),
                                              draft,
                                              name,
                                             "ARCGIS_SERVER",
                                             "",
                                             False,
                                             serverFolder
                                              )
    if analysis['errors'] == {}:
      print("Making Service Definition: {}.\n".format(sd))
      arcpy.StageService_server(draft,sd)
      print("Service Definition created.\n")
    else:
      print("Errors creating service definition",analysis['errors'])
      continue


    print("Getting service parameters.\n")

    serviceURL = "/arcgis/admin/services/" + serverFolder + "/" + name + ".MapServer"
    params = urllib.urlencode({'token': token, 'f': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
                    
    httpJSON = httplib.HTTPConnection(serverName,serverPort)
    httpJSON.request("POST", serviceURL, params, headers)

    response = httpJSON.getresponse()
    if (response.status != 200):
      httpJSON.close()
      print("Couldn't access the service {} in {} on {}. Check if it exists".format(name,serverFolder,serverName))
      continue
    data = response.read()
    httpJSON.close()
    if not assertJsonSuccess(data):          
      print("Error returned by operation. " + data)
      continue


    if overrideProps != "":
      overrideJSON = json.loads(overrideProps)
      dataJSON = json.loads(data)
      for key in overrideJSON:
        dataJSON[key] = overrideJSON[key]
      data = json.dumps(dataJSON)

    print("Service Parameters saved.\n")



    print("Removing old service.\n")

    httpDelete = httplib.HTTPConnection(serverName,serverPort)
    httpDelete.request("POST", serviceURL +"/delete", params, headers)

    response = httpDelete.getresponse()
    if (response.status != 200):
      httpDelete.close()
      print("Failed to delete")
      continue
    deleteRes = response.read()
    httpDelete.close()
    if not assertJsonSuccess(deleteRes):          
      print("Error returned by operation. " + deleteRes)
      continue
    print("Service Removed.\n")


    print("Publishing new service.\n")
    arcpy.UploadServiceDefinition_server(sd,"GIS Servers/"+gisConnection)
    print("{} published to {} folder on {}\n".format(name,serverFolder,serverName))

    print("Adding saved properties.\n")
    params = urllib.urlencode({'token': token, 'service':data, 'f': 'json'})
    httpPublish = httplib.HTTPConnection(serverName,serverPort)
    httpPublish.request("POST", serviceURL+"/edit", params, headers)

    response = httpPublish.getresponse()
    if (response.status != 200):
      httpPublish.close()
      print("Error while editing the service.")
      continue
    publishData = response.read()
    httpPublish.close()
    if not assertJsonSuccess(publishData):          
      print("Error returned by operation. " + publishData)
      continue
    print("Properties added.\n")
    print("{} successfully updated.\n".format(name))



def getToken(username, password, serverName, serverPort):
  tokenURL = "/arcgis/admin/generateToken"

  params = urllib.urlencode({'username': username, 'password': password, 'client': 'requestip', 'expiration':180,'f': 'json'})
  headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

  httpConn = httplib.HTTPConnection(serverName, serverPort)
  httpConn.request("POST", tokenURL, params, headers)

  response = httpConn.getresponse()
  if (response.status != 200):
    httpConn.close()
    print("Error while fetching tokens from admin URL. Please check the URL and try again.")
    return
  else:
    data = response.read()
    httpConn.close()

    if not assertJsonSuccess(data):            
      return

    token = json.loads(data)        
    return token['token']            
        

def assertJsonSuccess(data):
  obj = json.loads(data)
  if 'status' in obj and obj['status'] == "error":
    print("Error: JSON object returns an error. " + str(obj))
    return False
  else:
    return True
    
        
# Script start
if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))
