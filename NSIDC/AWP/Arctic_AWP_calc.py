from multiprocessing import Pool
import numpy as np
import csv
import matplotlib.pyplot as plt

from datetime import date
from datetime import timedelta

import time

class AWP_calc:

	def __init__ (self):
		
		self.iceMJ = 0.15
		self.datum = ['Date']
		self.Daily_all_regions = ['Daily MJ/m2']
		self.Accu_all_regions = ['Accumulated MJ/m2']
		
		self.Daily_central_regions = ['Daily MJ/m2']
		self.Accu_central_regions = ['Accumulated MJ/m2']
		
		self.SoO = ['Sea of Okhotsk']
		self.Bers = ['Bering Sea']
		self.HB = ['Hudson Bay']
		self.BB = ['Baffin Bay']
		self.EG = ['East Greenland Sea']
		self.BaS = ['Barents Sea']
		self.KS = ['Kara Sea']
		self.LS = ['Laptev Sea']
		self.ES = ['East Siberian Sea']
		self.CS = ['Chukchi Sea']
		self.BeaS = ['Beaufort Sea']
		self.CA = ['Canadian Archipelago']
		self.AB = ['Central Arctic']
		
		self.SoO_daily = ['Sea of Okhotsk']
		self.Bers_daily = ['Bering Sea']
		self.HB_daily = ['Hudson Bay']
		self.BB_daily = ['Baffin Bay']
		self.EG_daily = ['East Greenland Sea']
		self.BaS_daily = ['Barents Sea']
		self.KS_daily = ['Kara Sea']
		self.LS_daily = ['Laptev Sea']
		self.ES_daily = ['East Siberian Sea']
		self.CS_daily = ['Chukchi Sea']
		self.BeaS_daily = ['Beaufort Sea']
		self.CA_daily = ['Canadian Archipelago']
		self.AB_daily = ['Central Arctic']
		
		self.labelfont = {'fontname':'Arial'}
		self.plottype = 'cumu' #daily, cumu, both
		self.masksload()
		
		self.starttime = time.time()
		
	def startdate(self,year):
		self.start = date(year, 3, 20)
		self.year = self.start.year
		self.stringmonth = str(self.start.month).zfill(2)
		self.stringday = str(self.start.day).zfill(2)
		self.daycount = 38 # 187summer
		self.dailyorcumu()
		self.dayloop()
		
		return self.Daily_all_regions , self.Accu_all_regions

	def masksload(self):
		'''Loads regionmask, pixel area mask, latitudemask and
		AWP values for southern latitudes
		'''
		
		regionmaskfile = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		with open(regionmaskfile, 'rb') as frmsk:
			self.mask = np.fromfile(frmsk, dtype=np.uint32)
		self.regmaskf = np.array(self.mask, dtype=float)
		
		areamaskfile = 'X:/NSIDC/Masks/psn25area_v3.dat'
		with open(areamaskfile, 'rb') as famsk:
			self.mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(self.mask2, dtype=float)/1000
		
		latmaskfile = 'Masks/psn25lats_v3.dat'
		with open(latmaskfile, 'rb') as flmsk:
			self.mask3 = np.fromfile(flmsk, dtype=np.uint32)
		self.latmaskf = np.array(self.mask3, dtype=float)/100000
		
		icemaskfile = 'X:/NSIDC/Masks/Max_AWP_extent.bin'
		with open(icemaskfile, 'rb') as frmsk:
			self.Icemask = np.fromfile(frmsk, dtype=np.uint8)
			
		self.latitudelist = np.loadtxt('Masks/Lattable_MJ.csv', delimiter=',')
		
#		self.maskview(self.Icemask)
#		plt.show()
		
	def maskview(self,icemap):
		'''displays loaded masks'''
		icemap = icemap.reshape(448, 304)
		plt.imshow(icemap, interpolation='nearest', vmin=0, vmax=3, cmap=plt.cm.jet)
		
		
		
	def dayloop(self):
		'''for loop to load binary data files and pass them to the calculation function
		'''
		AWPdaily = np.zeros(len(self.regmaskf), dtype=float)
		AWPcumulative = np.zeros(len(self.regmaskf), dtype=float)
		loopday	= self.start

		
		for count in range (0,self.daycount,1):
#			self.stringmonth = str(loopday.month).zfill(2)
#			self.stringday = str(loopday.day).zfill(2)
			filename = 'DataFiles/NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
			filenameMean = 'DataFiles/Daily_Mean/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)
#			filenameDecMean = 'S:/Temp/Mean_80_{}{}.bin'.format(self.stringmonth,self.stringday)
						
			with open(filenameMean, 'rb') as fr:
				iceMean = np.fromfile(fr, dtype=np.uint8)
			with open(filename, 'rb') as frr:
				ice = np.fromfile(frr, dtype=np.uint8)
		
			iceMeanfloat = np.array(iceMean, dtype=float) / 250
			icef = np.array(ice, dtype=float) / 250
			
			#define lists for regional area calculation
			self.SoO_daily_calc = []
			self.SoO_calc = []
			self.SoOarea = []
			self.Bers_daily_calc = []
			self.Bers_calc = []
			self.Bersarea = []
			self.HB_daily_calc = []
			self.HB_calc = []
			self.HBarea = []
			self.BB_daily_calc = []
			self.BB_calc = []
			self.BBarea = []
			self.EG_daily_calc = []
			self.EG_calc = []
			self.EGarea = []
			self.BaS_daily_calc = []
			self.BaS_calc = []
			self.BaSarea = []
			self.KS_daily_calc = []
			self.KS_calc = []
			self.KSarea = []
			self.LS_daily_calc = []
			self.LS_calc = []
			self.LSarea = []
			self.ES_daily_calc = []
			self.ES_calc = []
			self.ESarea = []
			self.CS_daily_calc = []
			self.CS_calc = []
			self.CSarea = []
			self.BeaS_daily_calc = []
			self.BeaS_calc = []
			self.BeaSarea = []
			self.CA_daily_calc = []
			self.CA_calc = []
			self.CAarea = []
			self.AB_daily_calc = []
			self.AB_calc = []
			self.ABarea = []
			
			#calculate the map
			aaa = np.vectorize(self.energycalc)
			AWPdaily,AWPcumulative,AWPdaily_areaweighted,AWPcumulative_areaweighted,AWPdaily_oceanarea,AWPcumulative_oceanarea = aaa(
					count,icef,iceMeanfloat,AWPcumulative,self.Icemask,self.regmaskf,self.areamaskf,self.latmaskf)
			
			#append pan Arctic lists
			self.datum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			self.Daily_all_regions.append (round(np.nansum(AWPdaily_areaweighted) / np.nansum(AWPdaily_oceanarea),3))
			self.Accu_all_regions.append (round(np.nansum(AWPcumulative_areaweighted) / np.nansum(AWPcumulative_oceanarea),3))
			
			#create a single central Arctic list from regions
			central_arctic_daily = [np.sum(self.AB_daily_calc),np.sum(self.CA_daily_calc),np.sum(self.BeaS_daily_calc),np.sum(self.CS_daily_calc),
						np.sum(self.ES_daily_calc),np.sum(self.LS_daily_calc),np.sum(self.KS_daily_calc)]
			central_arctic = [np.sum(self.AB_calc),np.sum(self.CA_calc),np.sum(self.BeaS_calc),np.sum(self.CS_calc),np.sum(self.ES_calc),
							np.sum(self.LS_calc),np.sum(self.KS_calc)]
			central_arctic_area = [np.sum(self.ABarea),np.sum(self.CAarea),np.sum(self.BeaSarea),np.sum(self.CSarea),
								np.sum(self.ESarea),np.sum(self.LSarea),np.sum(self.KSarea)]
			
			#append central Arctic Lists
			self.Daily_central_regions.append (round(np.sum(central_arctic_daily)/np.sum(central_arctic_area),3))
			self.Accu_central_regions.append (round(np.sum(central_arctic)/np.sum(central_arctic_area),3))
			
			
			#append regional lists
			self.SoO.append (round((np.sum(self.SoO_calc)/np.sum(self.SoOarea)),3))
			self.Bers.append (round((np.sum(self.Bers_calc)/np.sum(self.Bersarea)),3))
			self.HB.append (round((np.sum(self.HB_calc)/np.sum(self.HBarea)),3))
			self.BB.append (round((np.sum(self.BB_calc)/np.sum(self.BBarea)),3))
			self.EG.append (round((np.sum(self.EG_calc)/np.sum(self.EGarea)),3))
			self.BaS.append (round((np.sum(self.BaS_calc)/np.sum(self.BaSarea)),3))
			self.KS.append (round((np.sum(self.KS_calc)/np.sum(self.KSarea)),3))
			self.LS.append (round((np.sum(self.LS_calc)/np.sum(self.LSarea)),3))
			self.ES .append (round((np.sum(self.ES_calc)/np.sum(self.ESarea)),3))
			self.CS.append (round((np.sum(self.CS_calc)/np.sum(self.CSarea)),3))
			self.BeaS.append (round((np.sum(self.BeaS_calc)/np.sum(self.BeaSarea)),3))
			self.CA.append (round((np.sum(self.CA_calc)/np.sum(self.CAarea)),3))
			self.AB.append (round((np.sum(self.AB_calc)/np.sum(self.ABarea)),3))
		
			#append daily regional lists
			self.SoO_daily.append (round((np.sum(self.SoO_daily_calc)/np.sum(self.SoOarea)),3))
			self.Bers_daily.append (round((np.sum(self.Bers_daily_calc)/np.sum(self.Bersarea)),3))
			self.HB_daily.append (round((np.sum(self.HB_daily_calc)/np.sum(self.HBarea)),3))
			self.BB_daily.append (round((np.sum(self.BB_daily_calc)/np.sum(self.BBarea)),3))
			self.EG_daily.append (round((np.sum(self.EG_daily_calc)/np.sum(self.EGarea)),3))
			self.BaS_daily.append (round((np.sum(self.BaS_daily_calc)/np.sum(self.BaSarea)),3))
			self.KS_daily.append (round((np.sum(self.KS_daily_calc)/np.sum(self.KSarea)),3))
			self.LS_daily.append (round((np.sum(self.LS_daily_calc)/np.sum(self.LSarea)),3))
			self.ES_daily.append (round((np.sum(self.ES_daily_calc)/np.sum(self.ESarea)),3))
			self.CS_daily.append (round((np.sum(self.CS_daily_calc)/np.sum(self.CSarea)),3))
			self.BeaS_daily.append (round((np.sum(self.BeaS_daily_calc)/np.sum(self.BeaSarea)),3))
			self.CA_daily.append (round((np.sum(self.CA_daily_calc)/np.sum(self.CAarea)),3))
			self.AB_daily.append (round((np.sum(self.AB_daily_calc)/np.sum(self.ABarea)),3))
			
			
#			print('Progress: ',100*count/self.daycount)
			print(self.year ,self.stringmonth, self.stringday)
		

			loopday = loopday+timedelta(days=1)
			self.year = loopday.year
			self.stringmonth = str(loopday.month).zfill(2)
			self.stringday = str(loopday.day).zfill(2)
				
		
		end = time.time()
		print(end-self.starttime)
		self.writetofile()
		with open('netcdf/AWP_energy_{}.bin'.format(self.year), 'wb') as writecumu:
			writecumu.write(AWPcumulative)
#		self.normalshow(AWPdaily,self.Daily_all_regions[-1])
		self.cumulativeshow(AWPcumulative,round(self.Accu_all_regions[-1],0))
		self.fig2.savefig('CSVexport/Final_{}.png'.format(self.year))
#		plt.show()
		
	def energycalc(self,count,ice,iceMean,AWPcumulative,icemask,regmaskf,areamask,latmask):
		'''AWP energy calculation & Regional breakdown'''
		AWPdaily_areaweighted = np.nan
		AWPdaily_oceanarea = np.nan
		AWPcumulative_areaweighted = np.nan
		AWPcumulative_oceanarea = np.nan
		
		if regmaskf < 16:
			if ice == 1.02: #value for missing data
				ice = iceMean
			pixlat = max(40,latmask)
			indexx = int(round((pixlat-40)*5))
			MJ = self.latitudelist[indexx][count+1]
			AWPdaily = ((1-ice) * MJ) + self.iceMJ * MJ * ice
			AWPcumulative = AWPcumulative + AWPdaily
			if icemask == 1:
				AWPdaily_areaweighted = AWPdaily * areamask
				AWPdaily_oceanarea = areamask
				AWPcumulative_areaweighted = AWPcumulative * areamask
				AWPcumulative_oceanarea = areamask
					
				if regmaskf == 2:
					self.SoO_daily_calc.append  (AWPdaily_areaweighted)
					self.SoO_calc.append  (AWPcumulative_areaweighted)
					self.SoOarea.append (areamask)
				elif regmaskf == 3:
					self.Bers_daily_calc.append  (AWPdaily_areaweighted)
					self.Bers_calc.append  (AWPcumulative_areaweighted)
					self.Bersarea.append (areamask)
				elif regmaskf == 4:
					self.HB_daily_calc.append  (AWPdaily_areaweighted)
					self.HB_calc.append  (AWPcumulative_areaweighted)
					self.HBarea.append (areamask)
				elif regmaskf == 6:
					self.BB_daily_calc.append  (AWPdaily_areaweighted)
					self.BB_calc.append  (AWPcumulative_areaweighted)
					self.BBarea.append (areamask)
				elif regmaskf == 7:
					self.EG_daily_calc.append  (AWPdaily_areaweighted)
					self.EG_calc.append  (AWPcumulative_areaweighted)
					self.EGarea.append (areamask)
				elif regmaskf == 8:
					self.BaS_daily_calc.append  (AWPdaily_areaweighted)
					self.BaS_calc.append  (AWPcumulative_areaweighted)
					self.BaSarea.append (areamask)
				elif regmaskf == 9:
					self.KS_daily_calc.append  (AWPdaily_areaweighted)
					self.KS_calc.append  (AWPcumulative_areaweighted)
					self.KSarea.append (areamask)
				elif regmaskf == 10:
					self.LS_daily_calc.append  (AWPdaily_areaweighted)
					self.LS_calc.append  (AWPcumulative_areaweighted)
					self.LSarea.append (areamask)
				elif regmaskf == 11:
					self.ES_daily_calc.append  (AWPdaily_areaweighted)
					self.ES_calc.append  (AWPcumulative_areaweighted)
					self.ESarea.append (areamask)
				elif regmaskf == 12:
					self.CS_daily_calc.append  (AWPdaily_areaweighted)
					self.CS_calc.append  (AWPcumulative_areaweighted)
					self.CSarea.append (areamask)
				elif regmaskf == 13:
					self.BeaS_daily_calc.append  (AWPdaily_areaweighted)
					self.BeaS_calc.append  (AWPcumulative_areaweighted)
					self.BeaSarea.append (areamask)
				elif regmaskf == 14:
					self.CA_daily_calc.append  (AWPdaily_areaweighted)
					self.CA_calc.append  (AWPcumulative_areaweighted)
					self.CAarea.append (areamask)
				elif regmaskf == 15:
					self.AB_daily_calc.append  (AWPdaily_areaweighted)
					self.AB_calc.append  (AWPcumulative_areaweighted)
					self.ABarea.append (areamask)
						

		else:
			AWPdaily = 9999.9
			AWPcumulative = 9999.9
			
		return AWPdaily,AWPcumulative,AWPdaily_areaweighted,AWPcumulative_areaweighted,AWPdaily_oceanarea,AWPcumulative_oceanarea
		

	def normalshow(self,icemap,icesum):
		'''displays daily AWP data'''
		icemap = icemap.reshape(448, 304)
		icemap = icemap[50:430,20:260]
		icemap = np.ma.masked_greater(icemap, 9000)
		cmap = plt.cm.coolwarm
		cmap.set_bad('black',0.8)
		
		self.ax.clear()
		self.ax.set_title('Albedo-Warming Potential',loc='left')
		self.ax.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),loc='right')
		#self.ax.set_title('Maximum of Maxima: {}-{}')
		
		
		self.ax.set_xlabel('Mean: '+str(icesum)+' [MJ / 'r'$m^2$]',**self.labelfont)
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=30, cmap=cmap)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 6, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax.text(2, 12, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.ax.text(-0.04, 0.25, 'cryospherecomputing.tk/awp',
        transform=self.ax.transAxes,rotation='vertical',color='grey', fontsize=10)
		self.fig.tight_layout(pad=1)
		plt.pause(0.01)
		
	def cumulativeshow(self,icemap,icesum):
		'''displays cumulative AWP data'''
		icemap = icemap.reshape(448, 304)
		icemap = icemap[50:430,20:260]
		icemap = np.ma.masked_greater(icemap, 9000)
		cmap2 = plt.cm.coolwarm
		cmap2.set_bad('black',0.8)
		
		self.ax2.clear()
		self.ax2.set_title('Albedo-Warming Potential',loc='left')
		self.ax2.set_title('Astronomical Summer '+str(self.year),loc='right')
#		self.ax2.set_title('Astronomical Summer without ice',loc='right')
		
		self.ax2.set_xlabel('Mean: '+str(icesum)+' [MJ / 'r'$m^2$]',**self.labelfont)
		self.cax = self.ax2.imshow(icemap, interpolation='nearest', vmin=0, vmax=5000, cmap=cmap2)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 6, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 12, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(-0.04, 0.25, 'cryospherecomputing.tk/awp',
        transform=self.ax2.transAxes,rotation='vertical',color='grey', fontsize=10)
		self.fig2.tight_layout(pad=1)
		plt.pause(0.01)
		
	def anomalyshow(self,icemap,year,icesum):
		'''displays anomaly AWP data'''
		cmap = plt.cm.coolwarm
		cmap.set_bad('black',0.66)
		
		for x,y in enumerate(self.regmaskf):
			if y > 15:
				icemap[x] = 9999
		
		icemap = np.ma.masked_outside(icemap,-5000,5000) 
		icemap = icemap.reshape(448, 304)
		icemap = icemap[50:430,20:260]
		fig = plt.figure(figsize=(7.5, 9))
		ax = fig.add_subplot(111)

		cax = ax.imshow(icemap, interpolation='nearest', vmin=-1000, vmax=1000, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[-1000,-500,0,500,1000]).set_label('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]')
		
		ax.imshow(icemap, interpolation='nearest', vmin=-1000, vmax=1000, cmap=cmap)
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.set_xlabel('Anomaly: '+str(icesum)+' [MJ / 'r'$m^2$]',**self.labelfont)
		ax.set_ylabel('cryospherecomputing.tk/awp',y=0.15)
		ax.set_title('Albedo-Warming Potential Anomaly: {}'.format(year),x=0.5)
		ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.text(160, 375,r'Anomaly Base: 2000-2018', fontsize=8,color='black',fontweight='bold')
		fig.tight_layout()

		fig.savefig('csvexport/AWP_anom_{}.png'.format(year))
		
	def percentshow(self,icemap,year,icesum):
		'''displays anomaly AWP data'''
		cmap = plt.cm.coolwarm
		cmap.set_bad('black',0.66)
		
		for x,y in enumerate(self.regmaskf):
			if y > 15:
				icemap[x] = 9999
		
		icemap = icemap*100
		icemap = np.ma.masked_outside(icemap,-5000,5000) 
		icemap = icemap.reshape(448, 304)
		icemap = icemap[50:430,20:260]
		fig = plt.figure(figsize=(7.5, 9))
		ax = fig.add_subplot(111)

		cax = ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=100, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[0,25,50,75,100]).set_label('percent of permanent icefree conditions')
		
		ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=100, cmap=cmap)
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.set_xlabel('Mean: '+str(icesum)+' %',**self.labelfont)
		ax.set_ylabel('cryospherecomputing.tk/awp',y=0.15)
		ax.set_title('Albedo-Warming Potential (percent of max): {}'.format(year),x=0.5)
		ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		fig.tight_layout()

		fig.savefig('csvexport/AWP_percent_{}.png'.format(year))
		
	def dailyorcumu(self):
		'''creates separate figures for sea ice data'''
		self.icenull = np.zeros(len(self.regmaskf), dtype=float)
		self.icenull = self.icenull.reshape(448, 304)
		
		if self.plottype == 'daily' or  self.plottype == 'both':
			self.fig, self.ax = plt.subplots(figsize=(7.5, 9))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=30, cmap=plt.cm.coolwarm)
			self.cbar = self.fig.colorbar(self.cax, ticks=[0,5,10,15,20,25,30]).set_label('clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		if self.plottype == 'cumu' or self.plottype == 'both':
			self.fig2, self.ax2 = plt.subplots(figsize=(7.5, 9))
			self.cax = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=5000, cmap=plt.cm.coolwarm)
			self.cbar = self.fig2.colorbar(self.cax, ticks=[0,1000,2000,3000,4000,5000]).set_label('clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
			
		
	def writetofile(self):
		
		with open('CSVexport/raw/_AWP_'+str(self.year)+'.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.Daily_all_regions))):
				writer.writerow([self.datum[x],self.Daily_all_regions[x],self.Accu_all_regions[x],self.Daily_central_regions[x],self.Accu_central_regions[x]])
						
		with open('CSVexport/raw/_AWP_regional_'+str(self.year)+'.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.datum))):
				writer.writerow([self.datum[x],self.SoO[x],self.Bers[x],self.HB[x],self.BB[x],self.EG[x],self.BaS[x],
				self.KS[x],self.LS[x],self.ES[x],self.CS[x],self.BeaS[x],self.CA[x],self.AB[x]])
				
		with open('CSVexport/raw/_AWP_regional_daily_'+str(self.year)+'.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.datum))):
				writer.writerow([self.datum[x],self.SoO_daily[x],self.Bers_daily[x],self.HB_daily[x],self.BB_daily[x],
					self.EG_daily[x],self.BaS_daily[x],self.KS_daily[x],self.LS_daily[x],self.ES_daily[x],self.CS_daily[x],
				self.BeaS_daily[x],self.CA_daily[x],self.AB_daily[x]])

	
	def calcanomaly(self):
		
		icemean = np.zeros(len(self.regmaskf))
		icelist = []
		icelist_mean = []
		valuelist = [-242,-227,-189,-268,-246,-205,-202,-208,-224,-178,-179,-91,-164,-202,-112,-175,-65,-182,-106,-102,-130,-94,-111,-85,-58,-78,-22,11,63,-4,-46,43,70,81,-15,5,44,107,49,40]

		for yearload in range(1979,2019):
			with open('netcdf/years/AWP_energy_{}.bin'.format(yearload), 'rb') as fr:
				file = np.fromfile(fr, dtype=np.float)
				icelist.append(file)
				if 1999 < yearload < 2020:
					icelist_mean.append(file)
		
		for x in icelist_mean:
			icemean = icemean + x/len(icelist_mean)
		
		year = 1979
		for x,y in enumerate(icelist):
			iceanomaly = y - icemean
			
			self.anomalyshow(iceanomaly,year,valuelist[x])
			year +=1
#		plt.show()
			
	def calpercentage(self):
		icelist = []
		
		with open('netcdf/AWP_energy_Icefree.bin', 'rb') as fr:
			noIcemap = np.fromfile(fr, dtype=np.float)
			
		for yearload in range(1979,2019):
			with open('netcdf/years/AWP_energy_{}.bin'.format(yearload), 'rb') as fr:
				file = np.fromfile(fr, dtype=np.float)
				icelist.append(file)
				
		year = 1979
		for x in icelist:
			Mean_percent = []
			icepercent = x / noIcemap
			for x,y in enumerate(self.Icemask):
				if y ==1:
					Mean_percent.append(icepercent[x])
			
			self.percentshow(icepercent,year,round(np.mean(Mean_percent)*100,1))
			year +=1
#		plt.show()
	
	
# =============================================================================
# def spawnprocess(year):
# 	action = AWP_calc()
# 	data = action.startdate(year)
# 	
# 	return data
# 	
# if __name__ == '__main__':
# 	yearlist = []
# 	for year in range(1979,2019):
# 		yearlist.append(year)
# 	
# 	p = Pool(processes=15)
# 	data = p.map(spawnprocess, yearlist)
# 	p.close()
# =============================================================================
	


action = AWP_calc()
#action.calcanomaly()
#action.calpercentage()
action.startdate(2019)


'''
#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA

Region mask
0: Lakes
1: Ocean
2: Sea of Okhotsk
3: Bering Sea
4: Hudson Bay
5: St Lawrence
6: Baffin Bay
7: East Greenland Sea
8: Barents Sea
9: Kara Sea
10: Laptev Sea
11: East Siberian Sea
12: Chukchi Sea
13: Beaufort Sea
14: Canadian Archipelago
15: Central Arctic
20: Land
21: Coast

Max Ice Extent:
0: Ocean
1: Ice
2: Land
3: Coast
'''