import arcpy
from arcpy import env
arcpy.CheckOutExtension("3D")
env.outputZFlag="Disabled"
env.outputMFlag="Disabled"
env.workspace=r"\\nasgisnp\NCRO\BATH\Testgeo.gdb"

def webProducts (rast, project=True, method="POINT_REMOVE", tolerance=15, minimumArea=3000 ):
  rastName=arcpy.Describe(rast).baseName
  if project:
    arcpy.ProjectRaster_management(rastName,"WEB"+rastName,r"Coordinate Systems/Projected Coordinate Systems/World/WGS 1984 Web Mercator (Auxiliary Sphere).prj","BILINEAR","","NAD_1983_to_WGS_1984_5")
    raster = "WEB"+rastName
  q=arcpy.RasterDomain_3d(raster, raster+"q", "POLYGON")
  qq=arcpy.Union_analysis(q,raster+"qq","ALL",0.1,"NO_GAPS")
  qqq=arcpy.Dissolve_management(qq,raster+"qqq")
  qqqq=arcpy.cartography.SimplifyPolygon(qqq, raster+"qqqq", method, tolerance, minimumArea, "NO_CHECK", "NO_KEEP")
  arcpy.Buffer_analysis(qqqq, "out_"+raster, "30 Feet", "FULL", "", "NONE")
  print "Products created."

  arcpy.Delete_management(rast)
  arcpy.Delete_management(raster+"q")
  arcpy.Delete_management(raster+"qq")
  arcpy.Delete_management(raster+"qqq")
  arcpy.Delete_management(raster+"qqqq")