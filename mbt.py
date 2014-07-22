import arcpy
from arcpy.sa import *
from os import rename
from os import unlink
arcpy.CheckOutExtension('Spatial')
arcpy.overwriteOutput = True

def makeCSV (ssv, skipHeader):
  temp = ssv + "TEMPFILE"
  rename(ssv, temp)
  with open(temp) as inp:
    with open(ssv, 'w') as out:

      if skipHeader == True:
        inp.readline()
      arcpy.AddMessage("Header added.")
      out.write('x,y,z\n') 
      for line in inp.read():
        out.write(','.join(line.split(' ')))
  try:
    unlink(temp)
  except OSError:
    pass
  arcpy.AddMessage("Transformed to CSV")
  return ssv

def checkHeader(file):
  with open(file) as inp:
    checkLine = inp.readline()
    if checkLine == 'x,y,z\n':
      return file
    else:
      skipHeader = checkLine == 'x y z\n'
  return makeCSV(file, skipHeader)

xyz = arcpy.GetParameterAsText(0)
outRast = arcpy.GetParameterAsText(1)
gridSize = arcpy.GetParameterAsText(2)
sr= arcpy.GetParameterAsText(3)

rastNames = outRast.split('\\')
lastName = rastNames[len(rastNames)-1]
if(rastNames[len(rastNames)-1][0] in '0123456789'):
  rastNames[len(rastNames)-1] = 'a'+lastName
  outRast = '\\'.join(rastNames)
  arcpy.AddMessage("Can't begin file names with a number. Changing name to "+outRast)

arcpy.MakeXYEventLayer_management(checkHeader(xyz), 'x', 'y', 'temprastpoints', sr, 'z')

rast = Idw('temprastpoints', "z", gridSize, 2, RadiusVariable(1, float(gridSize)/2.))
arcpy.Delete_management('temprastpoints')
rast.save(outRast)
arcpy.AddMessage("Raster created.")  
