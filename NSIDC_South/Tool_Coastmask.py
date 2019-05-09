import numpy as np
import matplotlib.pyplot as plt

def costmask_calc():
	
	regionmaskfile = 'X:/NSIDC_south/Masks/region_s_pure.msk'
	with open(regionmaskfile, 'rb') as frmsk:
		mask = np.fromfile(frmsk, dtype=np.uint8)
	
	
	coastlist = []
	newmask = np.zeros(len(mask), dtype='uint8')
	mask = mask.reshape((332, 316))
	newmask = newmask.reshape((332, 316))
	for x in range (0,332):
		for y in range (0,316):
			coastlist.append([x,y])
			newmask[x,y] = mask[x,y]
			
	for x in range (0,332):
		print(x)
		for y in range (0,316):
			if GetNearest_coast_pixel(coastlist,x,y):
				newmask[x,y] = newmask[x,y]+20
			
	
	with open('Coastmask_new', 'wb') as export:
		export.write(newmask)
	plt.imshow(newmask)
	plt.show()

def GetNearest_coast_pixel(coastlist,x,y):
	#calculates the distance of new sample to all existing points
	dlist = [((pixel[0] - x)** 2 + (pixel[1] - y)** 2)**0.5 for pixel in coastlist]

	if min(dlist) < 10:
		return True
	else:
		return False



costmask_calc()

'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

arraylength: 104912 (332, 316)

#Regionmask:
2: Weddel Sea
3: Indian Ocean
4: Pacific Ocean
5: Ross Sea
6: Bellingshausen Amundsen Sea
11: Land
12: Coast
'''