import numpy as np
import pandas
import matplotlib.pyplot as plt

from datetime import date
from datetime import timedelta

class AWP_calc_daily:

	def __init__ (self):
		
		self.iceMJ = 0.15
		self.labelfont = {'fontname':'Arial'}
		self.masksload()
		self.dailyorcumu()
		
		self.CSVDatum = ['Date']
		self.CSVDaily = ['Daily MJ/m2']
		self.CSVCumu = ['Accumulated MJ/m2']
		
		self.CSVDaily_central = ['Daily MJ/m2']
		self.CSVAccu_central = ['Accumulated MJ/m2']
		
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
		
		latmaskfile = 'X:/NSIDC/Masks/psn25lats_v3.dat'
		with open(latmaskfile, 'rb') as flmsk:
			self.mask3 = np.fromfile(flmsk, dtype=np.uint32)
		self.latmaskf = np.array(self.mask3, dtype=float)/100000
		
		icemaskfile = 'X:/NSIDC/Masks/Max_AWP_extent.bin'
		with open(icemaskfile, 'rb') as frmsk:
			self.Icemask = np.fromfile(frmsk, dtype=np.uint8)
			
		self.latitudelist = np.loadtxt('X:/NSIDC/Masks/Lattable_MJ.csv', delimiter=',')
		
#		self.maskview(self.Icemask)
#		plt.show()
		
	def maskview(self,icemap):
		'''displays loaded masks'''
		icemap = icemap.reshape(448, 304)
		plt.imshow(icemap, interpolation='nearest', vmin=0, vmax=3, cmap=plt.cm.jet)
		
	def dayloop(self):
		
		self.AWPcumulative = np.zeros(len(self.regmaskf), dtype=float)
		self.AWPanomaly_acumu = np.zeros(len(self.regmaskf), dtype=float)
		
		loopday = date(2019, 3, 20)
		self.year = loopday.year
		self.stringmonth = str(loopday.month).zfill(2)
		self.stringday = str(loopday.day).zfill(2)
		for count in range (1,188):
			print(self.year ,self.stringmonth, self.stringday)
			self.daycalc(count,4.7,1946.01)
		
			loopday = loopday+timedelta(days=1)
			self.year = loopday.year
			self.stringmonth = str(loopday.month).zfill(2)
			self.stringday = str(loopday.day).zfill(2)
		self.export_data()
		
	def daycalc(self,DayofYear,AWP_Daily_mean,AWP_Accu_mean):
		'''for loop to load binary data files and pass them to the calculation function
		'''

		filename = 'X:/NSIDC/DataFiles/NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
		filenameMean = 'X:/NSIDC/DataFiles/Mean_00_19/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)
						
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
		AWPdaily,self.AWPcumulative,AWPanomaly,self.AWPanomaly_acumu,AWPdaily_areaweighted,AWPcumulative_areaweighted,AWPdaily_oceanarea,AWPcumulative_oceanarea = aaa(
				DayofYear,icef,iceMeanfloat,self.AWPcumulative,self.AWPanomaly_acumu,self.Icemask,self.regmaskf,self.areamaskf,self.latmaskf)
			
		#append pan Arctic lists
		self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
		self.CSVDaily.append (round(np.nansum(AWPdaily_areaweighted) / np.nansum(AWPdaily_oceanarea),3))
		self.CSVCumu.append (round(np.nansum(AWPcumulative_areaweighted) / np.nansum(AWPcumulative_oceanarea),3))
		
		#create a single central Arctic list from regions
		central_arctic_daily = [np.sum(self.AB_daily_calc),np.sum(self.CA_daily_calc),np.sum(self.BeaS_daily_calc),np.sum(self.CS_daily_calc),
						np.sum(self.ES_daily_calc),np.sum(self.LS_daily_calc),np.sum(self.KS_daily_calc)]
		central_arctic = [np.sum(self.AB_calc),np.sum(self.CA_calc),np.sum(self.BeaS_calc),np.sum(self.CS_calc),np.sum(self.ES_calc),
							np.sum(self.LS_calc),np.sum(self.KS_calc)]
		central_arctic_area = [np.sum(self.ABarea),np.sum(self.CAarea),np.sum(self.BeaSarea),np.sum(self.CSarea),
								np.sum(self.ESarea),np.sum(self.LSarea),np.sum(self.KSarea)]
		
		#append central Arctic Lists
		self.CSVDaily_central.append (round(np.sum(central_arctic_daily)/np.sum(central_arctic_area),3))
		self.CSVAccu_central.append (round(np.sum(central_arctic)/np.sum(central_arctic_area),3))
		
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
		
		if DayofYear > 186:
			self.normalshow(AWPdaily,self.CSVDaily[-1])
			self.cumulativeshow(self.AWPcumulative,round(self.CSVCumu[-1],0))
	# =============================================================================
	# 		plt.close()
	# 		plt.close()
	# =============================================================================
				
			AWP_Daily_anom = self.CSVDaily[-1] - float(AWP_Daily_mean)
			AWP_Accu_anom = self.CSVCumu[-1] - float(AWP_Accu_mean)
			self.anomalyshow(AWPanomaly,round(AWP_Daily_anom,2))
			self.anomalyshow_accu(self.AWPanomaly_acumu,round(AWP_Accu_anom,2))


		
	def energycalc(self,DayofYear,ice,iceMean,AWPcumulative,AWPanomaly_acumu,icemask,regmaskf,areamask,latmask):
		'''AWP energy calculation & Regional breakdown'''
		AWPdaily_areaweighted = np.nan
		AWPdaily_oceanarea = np.nan
		AWPcumulative_areaweighted = np.nan
		AWPcumulative_oceanarea = np.nan
		AWPanomaly = np.nan
		anomalymap = iceMean - ice
		
		if regmaskf < 16:
			if ice == 1.02: #value for missing data
				ice = iceMean
				anomalymap = iceMean - ice
			pixlat = max(40,latmask)
			indexx = int(round((pixlat-40)*5))
			MJ = self.latitudelist[indexx][DayofYear]
			AWPdaily = ((1-ice) * MJ) + self.iceMJ * MJ * ice
			AWPcumulative = AWPcumulative + AWPdaily
			AWPanomaly = anomalymap * MJ * 0.8
			AWPanomaly_acumu = AWPanomaly_acumu + AWPanomaly
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
			
		return AWPdaily,AWPcumulative,AWPanomaly,AWPanomaly_acumu,AWPdaily_areaweighted,AWPcumulative_areaweighted,AWPdaily_oceanarea,AWPcumulative_oceanarea
		

	def normalshow(self,icemap,icesum):
		'''displays daily AWP data'''
		icemap = icemap.reshape(448, 304)
		icemap = icemap[50:430,20:260]
		icemap = np.ma.masked_greater(icemap, 9000)
		
		cmap = plt.cm.coolwarm
		cmap.set_bad('black',0.8)
		
		cbarmax = min(30,int(np.amax(icemap)))
		
		self.ax.clear()
		self.ax.set_title('Albedo-Warming Potential',loc='left')
		self.ax.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),loc='right')
		#self.ax.set_title('Maximum of Maxima: {}-{}')
		
		
		self.ax.set_xlabel('Pan Arctic Mean: '+str(icesum)+' [MJ / 'r'$m^2$]',**self.labelfont)
		cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=cbarmax, cmap=cmap)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 6, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax.text(2, 12, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.ax.text(-0.04, 0.25, 'cryospherecomputing.tk/awp',
        transform=self.ax.transAxes,rotation='vertical',color='grey', fontsize=10)
		
		cbar = self.fig.colorbar(cax, ticks=[0,cbarmax*0.25,cbarmax*0.5,cbarmax*0.75,cbarmax]).set_label('clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		
		self.fig.tight_layout(pad=1)
		plt.pause(0.01)
		self.fig.savefig('X:/Upload/AWP/North_AWP_Map1.png')
		
		
	def cumulativeshow(self,icemap,icesum):
		'''displays cumulative AWP data'''
		icemap = icemap.reshape(448, 304)
		icemap = icemap[50:430,20:260]
		icemap = np.ma.masked_greater(icemap, 9000)
		cmap2 = plt.cm.coolwarm
		cmap2.set_bad('black',0.8)
		
		cbarmax = min(5000,int(np.amax(icemap)))
		
		self.ax2.clear()
		self.ax2.set_title('Accumulated AWP',loc='left')
		self.ax2.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),loc='right')

		
		self.ax2.set_xlabel('Pan Arctic Mean: '+str(int(icesum))+' [MJ / 'r'$m^2$]',**self.labelfont)
		cax = self.ax2.imshow(icemap, interpolation='nearest', vmin=0, vmax=cbarmax, cmap=cmap2)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 6, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 12, r'AWP Model: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(-0.04, 0.25, 'cryospherecomputing.tk/awp',
        transform=self.ax2.transAxes,rotation='vertical',color='grey', fontsize=10)
		
		cbar = self.fig2.colorbar(cax, ticks=[0,cbarmax*0.25,cbarmax*0.5,cbarmax*0.75,cbarmax]).set_label('clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		
		self.fig2.tight_layout(pad=1)
		plt.pause(0.01)
		self.fig2.savefig('X:/Upload/AWP/North_AWP_Map2.png')
		
	def anomalyshow(self,icemap,icesum):
		'''displays anomaly AWP data'''
		for x,y in enumerate(self.regmaskf):
			if y > 15:
				icemap[x] = 99
		icemap = np.ma.masked_outside(icemap,-50,50) 
		icemap = icemap.reshape(448, 304)
		icemap = icemap[50:430,20:260]
		cmap = plt.cm.coolwarm
		cmap.set_bad('black',0.66)
		
		lowestAWP = np.amin(icemap)
		highestAWP = np.amax(icemap)
		
		cbarmax = int(max(abs(lowestAWP),highestAWP,10))
		
		fig = plt.figure(figsize=(7.5, 9))
		ax = fig.add_subplot(111)

		cax = ax.imshow(icemap, interpolation='nearest', vmin=-cbarmax, vmax=cbarmax, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[-cbarmax,-0.5*cbarmax,0,0.5*cbarmax,cbarmax]).set_label('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]')
				
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.set_xlabel('Pan Arctic Anomaly: '+str(icesum)+' [MJ / 'r'$m^2$]',**self.labelfont)
		ax.set_ylabel('cryospherecomputing.tk/awp',y=0.15)
		ax.set_title('Albedo-Warming Potential Anomaly',loc='left')
		ax.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),loc='right')
		
		ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.text(160, 375,r'Anomaly Base: 2000-2019', fontsize=8,color='black',fontweight='bold')
		fig.tight_layout()
		plt.pause(0.01)
		fig.savefig('X:/Upload/AWP/North_AWP_Map3.png')
		plt.close()
		
	def anomalyshow_accu(self,icemap,icesum):
		'''displays anomaly AWP data'''
		for x,y in enumerate(self.regmaskf):
			if y > 15:
				icemap[x] = 9999
		icemap = np.ma.masked_outside(icemap,-5000,5000) 
		icemap = icemap.reshape(448, 304)
		icemap = icemap[50:430,20:260]
		cmap = plt.cm.coolwarm
		cmap.set_bad('black',0.66)
		
		lowestAWP = np.amin(icemap)
		highestAWP = np.amax(icemap)
		
		cbarmax = int(min(abs(lowestAWP),highestAWP,1000))
		
		fig = plt.figure(figsize=(7.5, 9))
		ax = fig.add_subplot(111)

		cax = ax.imshow(icemap, interpolation='nearest', vmin=-cbarmax, vmax=cbarmax, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[-cbarmax,-0.5*cbarmax,0,0.5*cbarmax,cbarmax]).set_label('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]')
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.set_xlabel('Pan Arctic Anomaly: '+str(icesum)+' [MJ / 'r'$m^2$]',**self.labelfont)
		ax.set_ylabel('cryospherecomputing.tk/awp',y=0.15)
		ax.set_title('Accumulated AWP Anomaly',loc='left')
		ax.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),loc='right')
		
		ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.text(160, 375,r'Anomaly Base: 2000-2019', fontsize=8,color='black',fontweight='bold')
		fig.tight_layout()
		plt.pause(0.01)
		fig.savefig('X:/Upload/AWP/North_AWP_Map4.png')
		plt.close()
		
	def dailyorcumu(self):
		'''creates separate figures for sea ice data'''	
		self.fig, self.ax = plt.subplots(figsize=(7.5, 9))
		self.fig2, self.ax2 = plt.subplots(figsize=(7.5, 9))
			
			
	def csvexport(self,filename,filedata):
		np.savetxt(filename, np.column_stack((filedata)), delimiter=",", fmt='%s')
		
	def export_data(self):
		self.csvexport('X:/Upload/AWP_data/Arctic_AWP_NRT.csv'.format(self.year),
				[self.CSVDatum,self.CSVDaily,self.CSVCumu,self.CSVDaily_central,self.CSVAccu_central])
		self.csvexport('X:/Upload/AWP_data/Arctic_AWP_NRT_regional.csv'.format(self.year),
				[self.CSVDatum,self.SoO,self.Bers,self.HB,self.BB,self.EG,self.BaS,
				self.KS,self.LS,self.ES,self.CS,self.BeaS,self.CA,self.AB])
		self.csvexport('X:/Upload/AWP_data/Arctic_AWP_NRT_regional_daily.csv'.format(self.year),
				[self.CSVDatum,self.SoO_daily,self.Bers_daily,self.HB_daily,self.BB_daily,self.EG_daily,self.BaS_daily,self.KS_daily,
				 self.LS_daily,self.ES_daily,self.CS_daily,self.BeaS_daily,self.CA_daily,self.AB_daily])
		
		#save binary accumulative files
		with open('X:/Upload/AWP_data/Arctic_AWP_Accu.bin', 'wb') as writecumu:
			writecumu.write(self.AWPcumulative)
		with open('X:/Upload/AWP_data/Arctic_AWP_Accu_anom.bin', 'wb') as writecumu:
			writecumu.write(self.AWPanomaly_acumu)
	
	def loadCSVdata (self):
		Yearcolnames = ['Date','B','C','D','E']
		Yeardata = pandas.read_csv('X:/Upload/AWP_data/Arctic_AWP_NRT.csv', names=Yearcolnames)
		self.CSVDatum = Yeardata.Date.tolist()
		self.CSVDaily = Yeardata.B.tolist()
		self.CSVCumu = Yeardata.C.tolist()
		self.CSVDaily_central = Yeardata.D.tolist()
		self.CSVAccu_central = Yeardata.E.tolist()
		
		AWP_mean = ['A','B','C','D']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Climatology/Arctic_AWP_mean.csv', names=AWP_mean)
		self.AWP_Daily_mean = Climatedata.A.tolist()
		self.AWP_Accu_mean = Climatedata.B.tolist()

	
	
	def loadCSVRegiondata (self):
		Yearcolnames = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
		Yeardata = pandas.read_csv('X:/Upload/AWP_data/Arctic_AWP_NRT_regional.csv', names=Yearcolnames)
		self.SoO = Yeardata.Sea_of_Okhotsk.tolist()
		self.Bers = Yeardata.Bering_Sea.tolist()
		self.HB = Yeardata.Hudson_Bay.tolist()
		self.BB = Yeardata.Baffin_Bay.tolist()
		self.EG = Yeardata.East_Greenland_Sea.tolist()
		self.BaS = Yeardata.Barents_Sea.tolist()
		self.KS = Yeardata.Kara_Sea.tolist()
		self.LS = Yeardata.Laptev_Sea.tolist()
		self.ES = Yeardata.East_Siberian_Sea.tolist()
		self.CS = Yeardata.Chukchi_Sea.tolist()
		self.BeaS = Yeardata.Beaufort_Sea.tolist()
		self.CA = Yeardata.Canadian_Archipelago.tolist()
		self.AB = Yeardata.Central_Arctic.tolist()
		
		Yearcolnames_daily = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
		Yeardata_daily = pandas.read_csv('X:/Upload/AWP_data/Arctic_AWP_NRT_regional_daily.csv', names=Yearcolnames_daily)
		self.SoO_daily = Yeardata_daily.Sea_of_Okhotsk.tolist()
		self.Bers_daily = Yeardata_daily.Bering_Sea.tolist()
		self.HB_daily = Yeardata_daily.Hudson_Bay.tolist()
		self.BB_daily = Yeardata_daily.Baffin_Bay.tolist()
		self.EG_daily = Yeardata_daily.East_Greenland_Sea.tolist()
		self.BaS_daily = Yeardata_daily.Barents_Sea.tolist()
		self.KS_daily = Yeardata_daily.Kara_Sea.tolist()
		self.LS_daily = Yeardata_daily.Laptev_Sea.tolist()
		self.ES_daily = Yeardata_daily.East_Siberian_Sea.tolist()
		self.CS_daily = Yeardata_daily.Chukchi_Sea.tolist()
		self.BeaS_daily = Yeardata_daily.Beaufort_Sea.tolist()
		self.CA_daily = Yeardata_daily.Canadian_Archipelago.tolist()
		self.AB_daily = Yeardata_daily.Central_Arctic.tolist()
	
	
	def automated (self,year,stringmonth,stringday):
		self.year = year
		self.stringmonth = stringmonth
		self.stringday = stringday
		
		print(self.year,self.stringmonth,self.stringday)
		self.loadCSVdata()
		self.loadCSVRegiondata()
		
		#load accumulative files
		with open('X:/Upload/AWP_data/Arctic_AWP_Accu.bin', 'rb') as readcumu:
			self.AWPcumulative = np.fromfile(readcumu, dtype=float)
		with open('X:/Upload/AWP_data/Arctic_AWP_Accu_anom.bin', 'rb') as readcumu:
			self.AWPanomaly_acumu = np.fromfile(readcumu, dtype=float)
		
		index = len(self.CSVDaily)
#		print(self.AWP_Daily_mean[index])
		self.daycalc(index,self.AWP_Daily_mean[index],self.AWP_Accu_mean[index])
		self.export_data()
		
		import Arctic_Daily_AWP_Graphs
		Arctic_Daily_AWP_Graphs.action.automated(self.year,stringmonth,stringday)


action = AWP_calc_daily()
	

	
if __name__ == '__main__':
#	action.automated(2019,'08','27')
	action.dayloop()
	


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