import arcpy
import os
import sys

mxdDir = sys.argv[1]
serverConnection = sys.argv[2]
serverFolder = sys.argv[3]

mxds = [i for i in os.listdir(mxdDir) if 'mxd' in i]

arcpy.mapping.CreateGISServerConnectionFile("PUBLISH_GIS_SERVICES",
                                            mxdDir,
                                           "pythonpub.ags",
                                           "http://parcgis.water.ca.gov:6080/arcgis",
                                           "ARCGIS_SERVER",
                                            True,
                                            None
                                            )

for mxd in mxds:
  print(mxd)
  name = os.path.basename(mxd).split('.')[0]
  sdName = os.path.join(mxdDir,name)
  draft = sdName+".sddraft"
  sd = sdName+".sd"

  analysis = arcpy.mapping.CreateMapSDDraft(mxd,
                                            draft,
                                            name,
                                           "ARCGIS_SERVER"
                                            )
  if analysis['errors'] == {}:
    arcpy.StageService_server(draft,sd)
    arcpy.UploadServiceDefinition_server(sd,serverConnection)
  else:
    print("Errors",analysis['errors'])
