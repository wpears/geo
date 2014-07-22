import os

def addHeader(file,header='x y z\n'):
  temp = file + "TEMPFILE"
  os.rename(file, temp)
  with open(temp) as inp:
    with open(file,'w') as out:
      firstLine=inp.readline()
      if len(firstLine.split(' ')) == 1:
        header = 'x,y,z\n'
      out.write(header)
      out.write(firstLine)
      for line in inp:
        out.write(line)
  try: os.unlink(temp)
  except OSError: pass
  print "\nHeader added.\n"
  return file  