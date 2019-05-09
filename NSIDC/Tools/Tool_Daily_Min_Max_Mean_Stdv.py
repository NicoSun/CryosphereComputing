import numpy as np
import pandas

def looop():
	'''iterates through a 366 day year'''
	month = 1
	day = 1
	daycount = 10
	
	# options Max,Min,Mean,Stdv
	mode = 'Stdv'

	
	Columns = ['hole']
	csvdata = pandas.read_csv('Tools/2008_polehole.csv', names=Columns,dtype=int)
	icepole = csvdata.hole.tolist()
	 		
	Columns = ['edge']
	csvdata = pandas.read_csv('Tools/2008_poleholeedge.csv', names=Columns,dtype=int)
	icepoleedge = csvdata.edge.tolist()
		
	for count in range (0,daycount,1): #366
		stringmonth = str(month).zfill(2)
		stringday = str(day).zfill(2)
		
		data = []
		filename_out = 'test/NSIDC_{}_{}{}.bin'.format(mode,stringmonth,stringday)
		
		for year in range(2007,2019):
			filename = 'DataFiles/NSIDC_{}{}{}.bin'.format(year,stringmonth,stringday)
			with open(filename, 'rb') as fr:
				ice = np.fromfile(fr, dtype=np.uint8)
				icef = np.array(ice, dtype=float)
				data.append(icef)

		if mode =='Min':
			ice_new = calcMinimum(data)
		if mode =='Max':
			ice_new = calcMaximum(data)
		if mode =='Mean':
			ice_new = calcMean(data)
		if mode =='Stdv':
			ice_new = calcStdv(data)
		
		ice_new = polehole(ice_new,icepole,icepoleedge)
		export = np.array(ice_new, dtype=np.uint8)
		writefile(filename_out,export)
		
			
		print(month,day)
		
		day = day+1
		if day==32 and (month==1 or 3 or 5 or 7 or 8 or 10 or 12):
			day=1
			month = month+1
		elif day==31 and (month==4 or month==6 or month==9 or month==11):
			day=1
			month = month+1
		elif day==30 and month==2:
			day=1
			month = month+1
	print('Done')
	
def calcMinimum(data):
	'''calculates the minimum grid cell concentration'''
	result = np.asarray(data).min(0)
	return result

def calcMaximum(data):
	'''calculates the minimum grid cell concentration'''
	result = np.asarray(data).max(0)
	return result

def calcMean(data):
	'''calculates the minimum grid cell concentration'''
	result = np.asarray(data).mean(0)
	return result

def calcStdv(data):
	'''calculates the minimum grid cell concentration'''
	result = np.asarray(data).std(0)
	return result
	
def polehole(ice,icepole,icepoleedge):
	'''calculates the pole hole'''
	
	icepolecon = []
	for val in icepoleedge:
		icepolecon.append (ice[val])
		
	icepolecon = np.mean(icepolecon)
	
	for val2 in icepole:
		ice[val2] = icepolecon
	
	return ice

def writefile(filepath,export):
	'''writes output file'''
	with open(filepath, 'wb') as frr:
		frr.write(export)



looop()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
