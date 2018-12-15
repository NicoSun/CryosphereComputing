import numpy as np
from datetime import date
from datetime import timedelta
import time

def looop():
	year = 2016
	month = 1
	day = 1
	loopday = date(year, month, day)
	starttime = time.time()
		
	for count in range (0,366,1): #366
		stringmonth = str(month).zfill(2)
		stringday = str(day).zfill(2)
		filenameStdv = 'DataFiles/Stdv/NSIDC_Stdv_{}{}_south.bin'.format(stringmonth,stringday)
		filename6 = 'DataFiles/NSIDC_2006{}{}_south.bin'.format(stringmonth,stringday)
		filename7 = 'DataFiles/NSIDC_2007{}{}_south.bin'.format(stringmonth,stringday)
		filename8 = 'DataFiles/NSIDC_2008{}{}_south.bin'.format(stringmonth,stringday)
		filename9 = 'DataFiles/NSIDC_2009{}{}_south.bin'.format(stringmonth,stringday)
		filename10 = 'DataFiles/NSIDC_2010{}{}_south.bin'.format(stringmonth,stringday)
		filename11 = 'DataFiles/NSIDC_2011{}{}_south.bin'.format(stringmonth,stringday)
		filename12 = 'DataFiles/NSIDC_2012{}{}_south.bin'.format(stringmonth,stringday)
		filename13 = 'DataFiles/NSIDC_2013{}{}_south.bin'.format(stringmonth,stringday)
		filename14 = 'DataFiles/NSIDC_2014{}{}_south.bin'.format(stringmonth,stringday)
		filename15 = 'DataFiles/NSIDC_2015{}{}_south.bin'.format(stringmonth,stringday)
		filename16 = 'DataFiles/NSIDC_2016{}{}_south.bin'.format(stringmonth,stringday)
		filename17 = 'DataFiles/NSIDC_2017{}{}_south.bin'.format(stringmonth,stringday)
		
		try:
			with open(filename6, 'rb') as fr6:
				ice6 = np.fromfile(fr6, dtype=np.uint8)
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
			with open(filename17, 'rb') as fr:
				ice17 = np.fromfile(fr, dtype=np.uint8)
				
		except:
			print('cant read')
		
		icestdv = np.zeros(len(ice6), dtype=float)
		ice6f = np.array(ice6, dtype=float)
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
		ice17f = np.array(ice17, dtype=float)
		
# =============================================================================
# 		for x in range (0,len(ice6)):
# 			icelist = [ice6f[x],ice7f[x],ice8f[x],ice9f[x],ice10f[x],ice11f[x],ice12f[x],ice13f[x],ice14f[x],ice15f[x],ice16f[x],ice17f[x]]
# 			icestdv[x] = np.std(icelist)
# =============================================================================
			
		aaa = np.vectorize(standard_deviation)
		icestdv = aaa(ice6f,ice7f,ice8f,ice9f,ice10f,ice11f,ice12f,ice13f,ice14f,ice15f,ice16f,ice17f)
			
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
	end = time.time()
	print(end-starttime)

def standard_deviation(ice6,ice7,ice8,ice9,ice10,ice11,ice12,ice13,ice14,ice15,ice16,ice17):
	
	bbb = [ice6,ice7,ice8,ice9,ice10,ice11,ice12,ice13,ice14,ice15,ice16,ice17]
	icestdv = np.std(bbb)
	return icestdv
	

looop()


# =============================================================================
# import matplotlib.pyplot as plt
# plt.imshow(ice) 
# plt.colorbar()
# plt.show()
# =============================================================================
