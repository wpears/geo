#! c:python26/ArcGIS10.0/python.exe
import arcpy, os, sys
arcpy.CheckOutExtension('3D')


if len(sys.argv) == 4:
  input = sys.argv[1]
  feat = sys.argv[2]
  zone = sys.argv[3]
else:
  input = raw_input("Input file: ")
  feat = raw_input("Output feature class name: ")
  zone = raw_input("State Plane Zone: ")

inpPath = os.path.realpath(input)
pathArr = inpPath.split('\\')
gdbPath = ''

if pathArr[0].find(':'):
  del pathArr[0]
  inpPath = '\\\\'+'\\'.join(pathArr)

for i, piece in enumerate(pathArr):
  if piece == 'DATA_OTHER':
    gdbPath = ('\\\\'+'\\'.join(pathArr[:i])+'\\DATA_GIS\\Data.gdb')
    break

if gdbPath == '':
  raise IOError("This script can only operate on files in DATA_OTHER folders. Follow the folder structure.")
inp = open(inpPath)
out = open('TEMPFILE.csv','w');
sr = r'C:\Program Files (x86)\ArcGIS\Desktop10.0\Coordinate Systems\Projected Coordinate Systems\State Plane\NAD 1983 (US Feet)\NAD 1983 StatePlane California III FIPS 0403 (US Feet).prj'
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

arcpy.MakeXYEventLayer_management('TEMPFILE.csv','x','y','temppoint',sr,'bottom_elevation')

arcpy.FeatureClassToFeatureClass_conversion("temppoint",gdbPath,feat)

arcpy.Delete_management('temppoint')