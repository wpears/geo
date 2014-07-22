import os
from webproducts import webProducts
from rasterizemb import rasterizeMB
from addheader import addHeader
from makecsv import makeCSV

def walkXYZs (dir,excluded):
  walk = os.walk(dir)
  exList = list(excluded)
  for item in walk:
    for ex in exList:
      if not ex in item[0]:
        for xyz in item[2]:
          if xyz.lower().endswith('.txt'):
            print os.path.join(item[0],xyz)
            webProducts(rasterizeMB(addHeader(makeCSV(os.path.join(item[0],xyz)))))