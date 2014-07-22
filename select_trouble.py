
def select_trouble (feat1, out_feat="trouble", dist=0.5, troub=0.3):
  import arcpy
  import numpy

  feat = arcpy.CreateFeatureclass_management(arcpy.env.workspace,out_feat,"POINT",'','','ENABLED',feat1)

  arcpy.AddField_management(feat,'name',"TEXT",'','',5)
  arcpy.AddField_management(feat,'bottom_elevation',"DOUBLE")

  iCursor = arcpy.da.InsertCursor(feat,('SHAPE@X','SHAPE@Y','SHAPE@Z','name','bottom_elevation'))

  cursx = []
  with arcpy.da.SearchCursor(feat1,('SHAPE@X','SHAPE@Y','SHAPE@Z','name','bottom_elevation')) as sCursor:
    for row in sCursor:
      cursx.append(row)

  cursx = sorted(cursx, key=lambda tup: tup[0])
  length = len(cursx)
  lastAdded = 0
  for i, row in enumerate(cursx):
    x = row[0]
    y = row[1]
    elev = row[4]
    ind = i+1;
    while ind<length:
      row2 = cursx[ind]
      x2 = row2[0]
      y2 = row2[1]
      elev2 = row2[4]
      xdiff = abs(x - x2)
      if xdiff >= dist:
        break
      if x2>lastAdded and xdiff < dist and abs(y-y2) < dist and abs(elev-elev2) >= troub:
        lastAdded = x2
        iCursor.insertRow(row2)
      ind+=1
  del iCursor