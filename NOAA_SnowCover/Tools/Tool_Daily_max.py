import numpy as np

def looop():
	#day_of_year = 50
	
	filename_land = 'Masks/Landmask.msk'
	with open(filename_land, 'rb') as fr:
		Landmask = np.fromfile(fr, dtype='uint8')

	
	for day_of_year in range (1,366): #366
		print(day_of_year)
		stringday = str(day_of_year).zfill(3)
		filename_export = 'DataFiles/Max/NOAA_Max_{}_24km.bin'.format(stringday)
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
			print('cant read: ',day_of_year)
		
		snow_export = np.zeros(len(ice16), dtype=float)
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
		
		for x in range (0,len(ice16)):
			snow_export[x] = np.max([ice7f[x],ice8f[x],ice9f[x],ice10f[x],ice11f[x],ice12f[x],ice13f[x],ice14f[x],ice15f[x],ice16f[x]])

		export = np.array(snow_export, dtype=np.uint8)
				
		try:
			with open(filename_export, 'wb') as fwr:
				fwr.write(export)
			
		except:
			print('cant write')
	print('Done')
		

def maxofmax():
	maxextent = np.zeros(610*450, dtype=np.uint8)
	for day_of_year in range (1,366): #366
		print(day_of_year)
		stringday = str(day_of_year).zfill(3)
		filename = 'DataFiles/Max/NOAA_Max_{}_24km.bin'.format(stringday)

		with open(filename, 'rb') as fr:
			ice = np.fromfile(fr, dtype=np.uint8)

		for x,y in enumerate(ice):
			if y > 2:
				maxextent[x] = 5
		
	export = np.array(maxextent, dtype=np.uint8)
	filename_export = 'Masks/Max_SnowCover.msk'
	with open(filename_export, 'wb') as fwr:
		fwr.write(export)
	

#looop()
maxofmax()

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