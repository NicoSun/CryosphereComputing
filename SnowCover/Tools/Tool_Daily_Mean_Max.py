import numpy as np

def looop():
	#day_of_year = 50
	
	# options Max,Min,Mean
	mode = 'Max'
	
	filename = 'Masks/Landmask.msk'
	with open(filename, 'rb') as fr:
		Landmask = np.fromfile(fr, dtype='uint8')

	
	for day_of_year in range (1,366): #366
		
		data = []
		stringday = str(day_of_year).zfill(3)
		filename_out = 'DataFiles/{}/NOAA_{}_{}_24km.bin'.format(mode,mode,stringday)
		
		for year in range(2000,2020):
			filename = 'DataFiles/NOAA_{}{}_24km.bin'.format(year,stringday)
			with open(filename, 'rb') as fr:
				ice = np.fromfile(fr, dtype=np.uint8)
				icef = np.array(ice, dtype=float)
				data.append(icef)
		
		
		snow_new = Landmask*10
		
		if mode =='Min':
			data2 = calcMinimum(data)
		if mode =='Max':
			data2 = calcMaximum(data)
		if mode =='Mean':
			data2 = calcMean(data)
					
		for x in range (0,len(Landmask)):
			if Landmask[x] == 2:
				snow_new[x] = (3 + (data2[x]-2)/2)*10
				
			elif Landmask[x] == 1:
				snow_new[x] = (1 + (data2[x]-1)/2)*10
		
		export = np.array(snow_new, dtype=np.float16)
		writefile(filename_out,export)
		print(day_of_year)
		
		
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

def writefile(filepath,export):
	'''writes output file'''
	with open(filepath, 'wb') as frr:
		frr.write(export)
		


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