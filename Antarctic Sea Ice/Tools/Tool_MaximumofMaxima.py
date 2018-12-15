import winsound
import numpy as np
import matplotlib.pyplot as plt

def looop():
	#year = 2016
	month = 1
	day = 1
	daycount = 366
	asdf = input('Confirm action by pressing enter')
		
	for count in range (0,daycount,1): 
		filenamemax = 'Maximum/NSIDC_Max_'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		filename6 = 'DataFiles/NSIDC_2007'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		filename7 = 'DataFiles/NSIDC_2007'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		filename8 = 'DataFiles/NSIDC_2008'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		filename9 = 'DataFiles/NSIDC_2009'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		filename10 = 'DataFiles/NSIDC_2010'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		filename11 = 'DataFiles/NSIDC_2011'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		filename12 = 'DataFiles/NSIDC_2012'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		filename13 = 'DataFiles/NSIDC_2013'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		filename14 = 'DataFiles/NSIDC_2014'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		filename15 = 'DataFiles/NSIDC_2015'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		filename16 = 'DataFiles/NSIDC_2016'+str(month).zfill(2)+str(day).zfill(2)+'_south.bin'
		
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
				
		except:
			print('cant read')
		
		icedmaxf = np.zeros(104912, dtype=float)
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
		
		
		for x in range (0,104912):
			icedmaxf[x] = max(ice6f[x],ice7f[x],ice8f[x],ice9f[x],ice10f[x],ice11f[x],ice12f[x],ice13f[x],ice14f[x],ice15f[x],ice16f[x])
		
	
		export = np.array(icedmaxf, dtype=np.uint8)
		
		try:
			with open(filenamemax, 'wb') as frr:
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
	endmelody()

		
def endmelody():
	winsound.Beep(333, 200)#frequency in Hz and length in ms
	winsound.Beep(4000, 200)
	winsound.Beep(333, 200)
	winsound.Beep(4000, 200)
	winsound.Beep(333, 200)


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
