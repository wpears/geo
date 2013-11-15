#! c:python26/ArcGIS10.0/python.exe
import arcpy, os, sys, correctElevations
arcpy.CheckOutExtension('3D')

overwrite = "N"
filterElevs = "Y"
spread = 0.1

if len(sys.argv) == 1:
  input = raw_input("Input file: ")
  feat = raw_input("Output feature class name: ")
  zone = raw_input("State Plane Zone: ")
  overwrite = raw_input("Overwrite output? y/n: ")
  filterElevs = raw_input("Filter elevations? y/n: ")
  if filterElevs[:1].upper() =="Y":
    spread = float(raw_input("Elevation spread: "))
else:
  args = len(sys.argv)
  if args < 4:
    arcpy.AddMessage("You must enter a valid input file, feature class name, and State Plane Zone.")
    exit(1)
  input = sys.argv[1]
  feat = sys.argv[2]
  zone = sys.argv[3]
  if args > 4:
    overwrite = sys.argv[4]
  if args > 5:  
    filterElevs = sys.argv[5]
  if args > 6:
    spread = float(sys.argv[6])

if not input or not feat or not zone:
  arcpy.AddMessage("You must enter a valid input file, feature class name, and State Plane Zone.")
  exit(1)

inpPath = os.path.realpath(input)
pathArr = inpPath.split('\\')
gdbPath = ''
if overwrite[:1].upper() =="Y" or overwrite == True:
  arcpy.env.overwriteOutput = True
  arcpy.AddMessage("Overwriting output: "+str(arcpy.env.overwriteOutput))


if pathArr[0].find(':'):
  del pathArr[0]
  inpPath = '\\'+'\\'.join(pathArr)

for i, piece in enumerate(pathArr):
  if piece.upper() == 'DATA_OTHER':
    gdbPath = ('\\'+'\\'.join(pathArr[:i])+'\\DATA_GIS\\Data.gdb')
    break

if inpPath[:4].upper() == '\PCD':
  inpPath = '\\'+inpPath
if gdbPath[:4].upper() == '\PCD':
  gdbPath = '\\'+gdbPath

if gdbPath == '':
  raise IOError("This script can only operate on files in DATA_OTHER folders. Follow the folder structure.")
inp = open(inpPath)
out = open('TEMPFILE.csv','w');


if len(zone)<4:
  sr = r'C:\Program Files (x86)\ArcGIS\Desktop10.0\Coordinate Systems\Projected Coordinate Systems\State Plane\NAD 1983 (US Feet)\NAD 1983 StatePlane California III FIPS 0403 (US Feet).prj'
else:
  sr = zone
if zone == '2' or zone == 'II':
  sr.replace('III FIPS 0403','II FIPS 0402')


out.write("y,x,Elevation,Depth,bottom_elevation\n")
inp.readline() #skip starting lines
inp.readline() #skip 

for line in inp:
  arr= line.split(',')
  if(len(arr[4])):
    out.write(','.join(arr[1:5])+","+str(float(arr[3])-float(arr[4]))+'\n')
inp.close()
out.close()


if filterElevs[:1].upper() =="Y" or filterElevs == True:
  correctElevations.run('TEMPFILE.csv','TEMPFILE2.csv',spread)
  arcpy.MakeXYEventLayer_management('TEMPFILE2.csv','x','y','temppoint',sr,'bottom_elevation')
else:
  arcpy.MakeXYEventLayer_management('TEMPFILE.csv','x','y','temppoint',sr,'bottom_elevation')


arcpy.FeatureClassToFeatureClass_conversion("temppoint",gdbPath,feat)

arcpy.Delete_management('temppoint')
try:
  os.unlink("TEMPFILE.csv")
  os.unlink("TEMPFILE2.csv")
except OSError: pass 