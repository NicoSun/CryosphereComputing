import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from datetime import timedelta

def looop():
	year = 2016
	month = 1
	day = 1
	loopday = date(year, month, day)
		
	for count in range (0,366,1): #366
		stringmonth = str(month).zfill(2)
		stringday = str(day).zfill(2)
		filenameStdv = 'DataFiles/Stdv/NSIDC_Stdv_{}{}.bin'.format(stringmonth,stringday)
		filename7 = 'DataFiles/NSIDC_2007{}{}.bin'.format(stringmonth,stringday)
		filename8 = 'DataFiles/NSIDC_2008{}{}.bin'.format(stringmonth,stringday)
		filename9 = 'DataFiles/NSIDC_2009{}{}.bin'.format(stringmonth,stringday)
		filename10 = 'DataFiles/NSIDC_2010{}{}.bin'.format(stringmonth,stringday)
		filename11 = 'DataFiles/NSIDC_2011{}{}.bin'.format(stringmonth,stringday)
		filename12 = 'DataFiles/NSIDC_2012{}{}.bin'.format(stringmonth,stringday)
		filename13 = 'DataFiles/NSIDC_2013{}{}.bin'.format(stringmonth,stringday)
		filename14 = 'DataFiles/NSIDC_2014{}{}.bin'.format(stringmonth,stringday)
		filename15 = 'DataFiles/NSIDC_2015{}{}.bin'.format(stringmonth,stringday)
		filename16 = 'DataFiles/NSIDC_2016{}{}.bin'.format(stringmonth,stringday)
		
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
		
		icestdv = np.zeros(136192, dtype=np.float16)
		
		for x in range (0,136192):
			a = [ice7[x],ice8[x],ice9[x],ice10[x],ice11[x],ice12[x],ice13[x],ice14[x],ice15[x],ice16[x]]
			icestdv[x] = np.std(a)

		export = np.array(icestdv, dtype=np.float16)
		
		try:
			with open(filenameStdv, 'wb') as frr:
				icewr = frr.write(export)
			
		except:
			print('cant write')
			
		print('{}-{}'.format(stringmonth,stringday))
		loopday = loopday+timedelta(days=1)
		year = loopday.year
		month = loopday.month
		day = loopday.day
		stringmonth = str(month).zfill(2)
		stringday = str(day).zfill(2)



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
