#Amy Zuber
#converts latitude in DMS to DD

def lat2DD(lat1):
        
	D = (lat1[0:2])
	M = (lat1[3:5])
	S  = (lat1[7:9])
	DD = (float(D) + float(M)/60 + float(S)/3600)
	return  DD

    





	 


