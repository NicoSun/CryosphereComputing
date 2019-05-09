# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 12:10:55 2018

@author: NicoS
"""
from netCDF4 import Dataset
import numpy as np
import os


class NETCDF:
	def __init__  (self):
		self.year = 1979
		self.masksload()
		
	def masksload(self):
	
		filename = 'X:/NSIDC/Masks/psn25area_v3.dat'
		with open(filename, 'rb') as famsk:
				mask2 = np.fromfile(famsk, dtype=np.int32)
		self.areamaskf = np.array(mask2, dtype=float)/1000
		
		filename = 'X:/NSIDC/Masks/psn25lats_v3.dat'
		with open(filename, 'rb') as flmsk:
				mask3 = np.fromfile(flmsk, dtype=np.int32)
		self.latmaskf = np.array(mask3, dtype=float)/100000
		
		filename = 'X:/NSIDC/Masks/psn25lons_v3.dat'
		with open(filename, 'rb') as flmsk:
				mask4 = np.fromfile(flmsk, dtype=np.int32)
		self.lonmaskf = np.array(mask4, dtype=float)/100000
		
		filename = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		with open(filename, 'rb') as frmsk:
			mask = np.fromfile(frmsk, dtype=np.uint32)
		self.landmask = np.array(mask)
		for x,y in enumerate(self.landmask):
			if y==20 or y==21:
				self.landmask[x] = 100
			else:
				self.landmask[x] = 0

		


		
	def NETCDF_creater(self):
		rootgrp = Dataset("AWP_anomaly_Arctic.nc", "w", format="NETCDF4")
		rootgrp.description = 'Nico Sun cumulative Arctic Albedo Warming Potential (AWP)'


		fcstgrp = rootgrp.createGroup("forecasts")
		year = rootgrp.createDimension("year", None)
		xaxis = rootgrp.createDimension("xaxis", 448)
		yaxis = rootgrp.createDimension("yaxis", 304)
		
		times = rootgrp.createVariable("year","S1",("year",))
		latitude = rootgrp.createVariable("latitude","f4",("xaxis","yaxis",))
		longitude = rootgrp.createVariable("longitude","f4",("xaxis","yaxis",))
		areacello = rootgrp.createVariable("areacello","f4",("xaxis","yaxis",))
		sftof = rootgrp.createVariable("sftof","u1",("xaxis","yaxis",))
		
		areacello.units = "gridcell area in km^2"
		sftof.units = "land cover in precent"
		
		
		self.latmaskf = self.latmaskf.reshape(448, 304)
		self.lonmaskf = self.lonmaskf.reshape(448, 304)
		self.areamaskf = self.areamaskf.reshape(448, 304)
		self.landmask  = self.landmask.reshape(448, 304)
		
		latitude[:,:] = self.latmaskf
		longitude[:,:] = self.lonmaskf
		areacello[:,:] = self.areamaskf
		sftof[:,:] = self.landmask
		
		self.yearcount = 39
		filepath = 'X:/NSIDC/netcdf/'
		x = 0
		while x < self.yearcount:
			AWP_cumu = rootgrp.createVariable(varname="AWP_cumulative_{}".format(self.year),
				 datatype="f4",dimensions=("xaxis","yaxis",))
			AWP_cumu.units = "AWP anomaly in MJ/m2"
			filename = 'AWP_anomaly_{}.bin'.format(self.year)
			with open(os.path.join(filepath,filename), 'rb') as fr:
				AWP_cumu_load = np.fromfile(fr, dtype='float')
				AWP_cumu_load = AWP_cumu_load.reshape(448, 304)
				AWP_cumu[:,:] = AWP_cumu_load
			
			x += 1
			self.year += 1

		rootgrp.close()
		#print ('temp shape before adding data = ', temp.shape)
		


action = NETCDF()
action.NETCDF_creater()


'''
Values are coded as follows:
0-250 ice concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

#Regionmask:
0: lakes
1: Ocean
2: Sea of Okothsk
3: Bering Sea
4: Hudson bay
5: St Lawrence
6: Baffin Bay
7: Greenland Sea
8: Barents Sea
9: Kara Sea
10: Laptev Sea
11: East Siberian Sea
12: Chukchi Sea
13: Beaufort Sea
14: Canadian Achipelago
15: Central Arctic
20: Land
21: Coast
'''