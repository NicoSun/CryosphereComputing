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
		self.year = 1978
		
		
		self.yearcount = 3 #366 year 183 austral summer
		self.masksload()
		
	def masksload(self):
	
		filename = 'X:/NSIDC_South/Masks/pss25area_v3.dat'
		with open(filename, 'rb') as famsk:
				mask2 = np.fromfile(famsk, dtype=np.int32)
		self.areamaskf = np.array(mask2, dtype=float)/1000
		
		filename = 'X:/NSIDC_South/Masks/pss25lats_v3.dat'
		with open(filename, 'rb') as flmsk:
				mask3 = np.fromfile(flmsk, dtype=np.int32)
		self.latmaskf = np.array(mask3, dtype=float)/100000
		
		filename = 'X:/NSIDC_South/Masks/pss25lons_v3.dat'
		with open(filename, 'rb') as flmsk:
				mask4 = np.fromfile(flmsk, dtype=np.int32)
		self.lonmaskf = np.array(mask4, dtype=float)/100000
		
		filename = 'X:/NSIDC_South/Masks/region_s_pure.msk'
		with open(filename, 'rb') as frmsk:
				mask = np.fromfile(frmsk, dtype=np.uint8)
		self.landmask = np.array(mask, dtype=float)
		for x,y in enumerate(self.landmask):
			if y==11 or y==12:
				self.landmask[x] = 100
			else:
				self.landmask[x] = 0

		


		
	def NETCDF_creater(self):
		rootgrp = Dataset("AWP_Antarctic.nc", "w", format="NETCDF4")
		rootgrp.description = 'Nico Sun cumulative Antarctic Albedo Warming Potential (AWP)'
		
		filepath = 'X:/NSIDC_South/netcdf/'

		fcstgrp = rootgrp.createGroup("forecasts")
		year = rootgrp.createDimension("year", None)
		xaxis = rootgrp.createDimension("xaxis", 332)
		yaxis = rootgrp.createDimension("yaxis", 316)
		
		times = rootgrp.createVariable("year","S1",("year",))
		latitude = rootgrp.createVariable("latitude","f4",("xaxis","yaxis",))
		longitude = rootgrp.createVariable("longitude","f4",("xaxis","yaxis",))
		areacello = rootgrp.createVariable("areacello","f4",("xaxis","yaxis",))
		sftof = rootgrp.createVariable("sftof","u1",("xaxis","yaxis",))
		
		areacello.units = "gridcell area in km^2"
		sftof.units = "land cover in precent"
		AWP_cumu.units = "AWP in MJ/m2"
		
		self.latmaskf = self.latmaskf.reshape(332, 316)
		self.lonmaskf = self.lonmaskf.reshape(332, 316)
		self.areamaskf = self.areamaskf.reshape(332, 316)
		self.landmask  = self.landmask.reshape(332, 316)
		
		latitude[:,:] = self.latmaskf
		longitude[:,:] = self.lonmaskf
		areacello[:,:] = self.areamaskf
		sftof[:,:] = self.landmask
		
		icelist = []
		timelist = []
		
		for file in os.listdir(filepath):
			AWP_cumu = rootgrp.createVariable("AWP_cumulative","f4",("year","xaxis","yaxis",),least_significant_digit=1)
			with open(os.path.join(filepath,file), 'rb') as fr:
				AWP_cumu_load = np.fromfile(fr, dtype='float')
				AWP_cumu_load = AWP_cumu_load.reshape(332, 316)
				icelist.append(AWP_cumu_load)
				timelist.append('{}-{}'.format(self.year,self.year+1))
				self.year += 1
			
		AWP_cumu[0:len(icelist),:,:] = icelist
#		times[:] = timelist
		
		
		rootgrp.close()
		#print ('temp shape before adding data = ', temp.shape)
		


action = NETCDF()
action.NETCDF_creater()
