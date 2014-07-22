# Amy Zuber
# this function converts Longitude in DMS to DD for field calculations it is a
# negative number

def long2DD(long1):
	D = (long1[0:4])
	M = (long1[5:7])
	S  = (long1[9:11])
	DD = (float(D) + float(M)/60 + float(S)/3600)*-1
	return DD
