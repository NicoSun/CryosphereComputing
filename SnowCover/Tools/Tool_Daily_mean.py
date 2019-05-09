import numpy as np

def looop():
	#day_of_year = 50
	
	filename = 'Masks/Landmask.msk'
	with open(filename, 'rb') as fr:
		Landmask = np.fromfile(fr, dtype='uint8')

	
	for day_of_year in range (1,367): #366
		stringday = str(day_of_year).zfill(3)
		filenamedav = 'DataFiles/Mean/NOAA_Mean_{}_24km.bin'.format(stringday)
		filename5 = 'DataFiles/NOAA_2005{}_24km.bin'.format(stringday)
		filename6 = 'DataFiles/NOAA_2006{}_24km.bin'.format(stringday)
		filename7 = 'DataFiles/NOAA_2007{}_24km.bin'.format(stringday)
		filename8 = 'DataFiles/NOAA_2008{}_24km.bin'.format(stringday)
		filename9 = 'DataFiles/NOAA_2009{}_24km.bin'.format(stringday)
		filename10 = 'DataFiles/NOAA_2010{}_24km.bin'.format(stringday)
		filename11 = 'DataFiles/NOAA_2011{}_24km.bin'.format(stringday)
		filename12 = 'DataFiles/NOAA_2012{}_24km.bin'.format(stringday)
		filename13 = 'DataFiles/NOAA_2013{}_24km.bin'.format(stringday)
		filename14 = 'DataFiles/NOAA_2014{}_24km.bin'.format(stringday)
		filename15 = 'DataFiles/NOAA_2015{}_24km.bin'.format(stringday)
		filename16 = 'DataFiles/NOAA_2016{}_24km.bin'.format(stringday)
		filename17 = 'DataFiles/NOAA_2017{}_24km.bin'.format(stringday)
		filename18 = 'DataFiles/NOAA_2018{}_24km.bin'.format(stringday)
		
		try:
			with open(filename5, 'rb') as fr:
				ice5 = np.fromfile(fr, dtype=np.uint8)
			with open(filename6, 'rb') as fr:
				ice6 = np.fromfile(fr, dtype=np.uint8)
			with open(filename7, 'rb') as fr:
				ice7 = np.fromfile(fr, dtype=np.uint8)
			with open(filename8, 'rb') as fr:
				ice8 = np.fromfile(fr, dtype=np.uint8)
			with open(filename9, 'rb') as fr:
				ice9 = np.fromfile(fr, dtype=np.uint8)
			with open(filename10, 'rb') as fr:
				ice10 = np.fromfile(fr, dtype=np.uint8)
			with open(filename11, 'rb') as fr:
				ice11 = np.fromfile(fr, dtype=np.uint8)	
			with open(filename12, 'rb') as fr:
				ice12 = np.fromfile(fr, dtype=np.uint8)
			with open(filename13, 'rb') as fr:
				ice13 = np.fromfile(fr, dtype=np.uint8)
			with open(filename14, 'rb') as fr:
				ice14 = np.fromfile(fr, dtype=np.uint8)	
			with open(filename15, 'rb') as fr:
				ice15 = np.fromfile(fr, dtype=np.uint8)
			with open(filename16, 'rb') as fr:
				ice16 = np.fromfile(fr, dtype=np.uint8)
			with open(filename17, 'rb') as fr:
				ice17 = np.fromfile(fr, dtype=np.uint8)
			with open(filename18, 'rb') as fr:
				ice18 = np.fromfile(fr, dtype=np.uint8)
				
		except:
			print('cant read: ',day_of_year)
		
		snowmean = np.zeros(len(ice5), dtype=float)
		ice5f = np.array(ice5, dtype=float)
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
		ice18f = np.array(ice18, dtype=float)
		
		for x in range (0,len(ice16)):
			if Landmask[x] == 2:
				snowmean[x] = np.mean([max(3,ice5f[x]),max(3,ice6f[x]),max(3,ice7f[x]),max(3,ice8f[x]),max(3,ice9f[x]),max(3,ice10f[x]),
			max(3,ice11f[x]),max(3,ice12f[x]),max(3,ice13f[x]),max(3,ice14f[x]),max(3,ice15f[x]),max(3,ice16f[x]),max(3,ice17f[x]),max(3,ice18f[x])])*10
			if Landmask[x] == 1:
				snowmean[x] = np.mean([min(2,ice5f[x]),min(2,ice6f[x]),min(2,ice7f[x]),min(2,ice8f[x]),min(2,ice9f[x]),min(2,ice10f[x]),
			min(2,ice11f[x]),min(2,ice12f[x]),min(2,ice13f[x]),min(2,ice14f[x]),min(2,ice15f[x]),min(2,ice16f[x]),min(2,ice17f[x]),min(2,ice18f[x])])*10
		
		export = np.array(snowmean, dtype=np.float16)
				
		try:
			with open(filenamedav, 'wb') as fwr:
				fwr.write(export)
			
		except:
			print('cant write')
		print(stringday)
	print('Done')
		


looop()

#plt.imshow(ice) 
#plt.colorbar()
#plt.show()



'''
region_coding
0: Ocean
3: North America
4: Greenland
5: Europe
6: Asia
'''

'''
snowmap encoding
1: Ocean
2: Land
3: Ice
4: Snow
'''