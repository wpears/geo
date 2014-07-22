#! c:python27/ArcGIS10.2/python.exe
import arcpy, sys

def getModeAvg (arr):
  counts = {}
  first = 0,0
  second = 0,0
  third = 0,0
  for line in arr:
    num = getElev(line)
    roundNum = int(round(num*100))
    if counts.get(roundNum):
      counts[roundNum]+=1
    else:
      counts[roundNum]=1
  for key, val in counts.iteritems():
    if val > first[1]:
      third = second
      second = first
      first = key,val
    elif val > second:
      third = second
      second = key,val
    elif val > third:
      third = key,val
  #print first,second,third
  #print abs(first[0] - second[0]) 
  #print abs(third[0] - second[0])
  #print abs(first[0] - third[0])

  if not second[0]:
    second = first
  if not third[0]:
    third = (first[0]*first[1]+second[0]*second[1])/(first[1]+second[1]), (first[1]+second[1])/2.
  if abs(first[0] - second[0]) > 15 or abs(third[0] - second[0]) > 15 or abs(first[0] - third[0]) > 15:
    return False
  return (first[0]*first[1]+second[0]*second[1]+third[0]*third[1])/(first[1]+second[1]+third[1])/100.

def filterOutliers (avg,lines,slope,spread):
  arcpy.AddMessage("Filtering with slope:"+str(slope))
  cleaned = []
  mid = len(lines)/2
  for i,line in enumerate(lines):
    elev = getElev(line)
   # corr = slope*(mid-i)
    if abs(elev-avg) <= spread:
      cleaned.append(line)
  return cleaned

def getElev(line):
  return float(line.split(',')[2])

def run(infile, outfile, spread=0.1):
  inp = open(infile)
  out = open(outfile, 'w')
  headers = inp.readline()
  out.write(headers)
  lines = [line for line in inp]
  count = 0
  chunks = []
  start = 0
  end = 100
  diff = 100 #diff allows splitting intervals if there is a large mode difference.

  while start < len(lines):
#    print start,end
    arr = lines[start:end]
    avg = getModeAvg(arr) #average of modes.. good proxy for 'true' elevation over short timespans
  # print avg
    if avg:
      chunks.append((avg,(start+end)/2,arr))
  #    print "advance", start,end,diff  
      start, end = end, end+diff
      if diff < 60:
        diff*=2
    #  print "advanced to", start,end,diff 
    else:
    #  print "failed", start,end,diff
      diff = int((end-start)/2)
      end = end-diff
   #   print "failed to", start,end,diff

  #chunks are [mode average, middle value, original array at this chunk's interval]
  for i,chunk in enumerate(chunks):
    if i == 0:
      slope = (chunk[0]-chunks[i+1][0])/(chunk[1]-chunks[i+1][1])
    elif i == len(chunks) -1:
      slope = (chunks[i-1][0]-chunk[0])/(chunks[i-1][1]-chunk[1])
    else:
      #print chunks[i-1][0],chunks[i-1][1],chunk[0],chunk[1],chunks[i+1][0],chunks[i+1][1]
      slope = ((chunks[i-1][0]-chunk[0])/(chunks[i-1][1]-chunk[1])+
              (chunk[0]-chunks[i+1][0])/(chunk[1]-chunks[i+1][1]))/2
    #print slope
    cleaned = filterOutliers(chunk[0],chunk[2],slope,spread)
    for line in cleaned:
      out.write(line)
      count+=1
  inp.close()    
  out.close()
  arcpy.AddMessage("\n\nStripped "+str(len(lines)-count)+" rows from "+str(len(lines))+" collected. This is "+str((len(lines)-count*1.0)/len(lines)*100.)+"%.\n\n")

if __name__ == "__main__":
  if len(sys.argv) > 2:
    run(sys.argv[1],sys.argv[2])
  else:
    input = raw_input("Input file: ")
    output = raw_input("Output file: ")
    run(input,output)

#import random
#(random.random()/25+1)*4 +num/4000.0 for num in range(1000)
# for first iteration random files.. Now operates on csv's.. Need to csv these elevs if needed again