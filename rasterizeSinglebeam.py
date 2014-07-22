#IDW -> Con -> Raster to Polygon -> Buffer (negative length) -> erase (from rast domain) -> clip (data_mgmt)

#Create a raster from relatively dense singlebeam points, optionally clipping it to provided multibeam
#3,8 for num,rad if pretty dense data, could calculate to remove judgment
def rasterizeSinglebeam (points, mb, out="__rast",number=6,radius=18,overWrite=False):
  import arcpy
  from arcpy.sa import *
  if overWrite:
    arcpy.env.overwriteOutput = True
  outIDW = Idw(points, "bottom_elevation", 3, 2, RadiusVariable(number, radius))
  if mb:
    conRast = Con(outIDW, 1, '', '')
    poly = arcpy.RasterToPolygon_conversion(conRast, "_poly"+points, "SIMPLIFY", "")
    buff = arcpy.Buffer_analysis(poly, "buff_"+points, "-15 feet", "FULL","","","")
    footprint = arcpy.Erase_analysis(buff, mb, "footprint_"+points, "")
    finalRast = arcpy.Clip_management(outIDW,"","rast_"+points, footprint, "", "ClippingGeometry")
    arcpy.Delete_management(poly)
    arcpy.Delete_management(buff)
    arcpy.Delete_management(footprint)
  else:
    outIDW.save(arcpy.Describe(points).catalogPath+out)