import pandas
import numpy as np
import matplotlib.pyplot as plt

def looop():
	#year = 2016
	month = 2
	day = 29
	
	#Poleholelist
	Columns = ['hole']
	csvdata = pandas.read_csv('Tools/2008_polehole.csv', names=Columns,dtype=int)
	icepole = csvdata.hole.tolist()
		
	Columns = ['edge']
	csvdata = pandas.read_csv('Tools/2008_poleholeedge.csv', names=Columns,dtype=int)
	icepoleedge = csvdata.edge.tolist()	
	
	
	for count in range (0,1,1): #366
		filenamedav = 'DataFiles/Daily_Mean/NSIDC_Mean_'+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		filename7 = 'DataFiles/NSIDC_2007'+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		filename8 = 'DataFiles/NSIDC_2008'+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		filename9 = 'DataFiles/NSIDC_2009'+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		filename10 = 'DataFiles/NSIDC_2010'+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		filename11 = 'DataFiles/NSIDC_2011'+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		filename12 = 'DataFiles/NSIDC_2012'+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		filename13 = 'DataFiles/NSIDC_2013'+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		filename14 = 'DataFiles/NSIDC_2014'+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		filename15 = 'DataFiles/NSIDC_2015'+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		filename16 = 'DataFiles/NSIDC_2016'+str(month).zfill(2)+str(day).zfill(2)+'.bin'
		
		try:
			with open(filename7, 'rb') as fr7:
				ice7 = np.fromfile(fr7, dtype=np.uint8)
			with open(filename8, 'rb') as fr8:
				ice8 = np.fromfile(fr8, dtype=np.uint8)
			with open(filename9, 'rb') as fr9:
				ice9 = np.fromfile(fr9, dtype=np.uint8)
			with open(filename10, 'rb') as fr10:
				ice10 = np.fromfile(fr10, dtype=np.uint8)
			with open(filename11, 'rb') as fr11:
				ice11 = np.fromfile(fr11, dtype=np.uint8)	
			with open(filename12, 'rb') as fr12:
				ice12 = np.fromfile(fr12, dtype=np.uint8)
			with open(filename13, 'rb') as fr13:
				ice13 = np.fromfile(fr13, dtype=np.uint8)
			with open(filename14, 'rb') as fr14:
				ice14 = np.fromfile(fr14, dtype=np.uint8)	
			with open(filename15, 'rb') as fr15:
				ice15 = np.fromfile(fr15, dtype=np.uint8)
			with open(filename16, 'rb') as fr16:
				ice16 = np.fromfile(fr16, dtype=np.uint8)
				
		except:
			print('cant read')
		
		icedavf = np.zeros(136192, dtype=float)
		ice7f = np.array(ice7, dtype=float)
		ice8f = np.array(ice8, dtype=float)
		ice9f = np.array(ice9, dtype=float)
		ice10f = np.array(ice10, dtype=float)
		ice11f = np.array(ice11, dtype=float)
		ice12f = np.array(ice12, dtype=float)
		ice13f = np.array(ice13, dtype=float)
		ice14f = np.array(ice14, dtype=float)
		ice15f = np.array(ice15, dtype=float)
		ice16f = np.array(ice16, dtype=float)
		
		icepolecon = 0
		
		
		for x in range (0,136192):
			icelist = [ice7f[x],ice8f[x],ice9f[x],ice10f[x],ice11f[x],ice12f[x],ice13f[x],ice14f[x],ice15f[x],ice16f[x]]
			icedavf[x] = np.mean(icelist)
		
		for val in range(0,len(icepoleedge),1):
			icepolecon = icepolecon+icedavf[icepoleedge[val]] /len(icepoleedge)
		
		for val2 in range(0,len(icepole),1):
			icedavf[icepole[val2]] = icepolecon	

		
		export = np.array(icedavf, dtype=np.uint8)
				
		try:
			with open(filenamedav, 'wb') as frr:
				icewr = frr.write(export)
			
		except:
			print('cant write')
		day = day+1
		count = count+1
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
		


looop()

#plt.imshow(ice) 
#plt.colorbar()
#plt.show()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
