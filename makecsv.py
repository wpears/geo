import os, sys

def makeCSV (ssv):
  temp = ssv + "TEMPFILE"
  os.rename(ssv, temp)
  with open(temp) as inp:
    with open(ssv, 'w') as out:
      for line in inp.read():
        out.write(','.join(line.split(' ')))
  try:
    os.unlink(temp)
  except OSError:
    pass
  print "\nTransformed to CSV\n"
  return ssv

if __name__ == "__main__":
  makeCSV(sys.argv[1:])