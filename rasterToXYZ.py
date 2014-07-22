import arcpy, os, zipfile
from addheader import addHeader

arcpy.CheckOutExtension('3D')

rast = arcpy.GetParameterAsText(0)
outLoc = arcpy.GetParameterAsText(1)
outName = arcpy.GetParameterAsText(2)

if not '.' in outName:
  outName+=".txt"

outPath = os.path.join(outLoc,outName)
outZip = os.path.join(outLoc,outName.split('.')[0]+'.zip')

arcpy.AddMessage("Running Raster to Point...")
point = arcpy.RasterToPoint_conversion(rast, r"in_memory\TEMPPOINT", "VALUE")
arcpy.AddMessage("Point feature created")

arcpy.AddMessage("Converting to 3D by Attribute...")
threed = arcpy.FeatureTo3DByAttribute_3d(point, r"in_memory\TEMPPOIINT3D","grid_code")
arcpy.Delete_management(r"in_memory\TEMPPOINT")
arcpy.AddMessage("3D conversion complete")

arcpy.AddMessage("Creating XYZ...")
xyz = arcpy.FeatureClassZToASCII_3d(threed,outLoc,outName,"XYZ","COMMA","FIXED",2)
arcpy.Delete_management(r"in_memory\TEMPPOINT3D")
arcpy.AddMessage("XYZ created")

arcpy.AddMessage("Adding header...")
addHeader(outPath)
arcpy.AddMessage("Header added")

arcpy.AddMessage("Zipping...")
with zipfile.ZipFile(outZip, 'w') as newzip:
  newzip.write(outPath, outName, zipfile.ZIP_DEFLATED)
arcpy.AddMessage("Zipped")

arcpy.AddMessage("Clearing in-memory workspace...")
arcpy.Delete_management("in_memory")
arcpy.AddMessage("In-memory workspace cleared")