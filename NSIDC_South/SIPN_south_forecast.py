import numpy as np
import numpy.ma as ma
import csv
import matplotlib.pyplot as plt
import os

from datetime import date
from datetime import timedelta

class NSIDC_prediction:

	def __init__  (self):
		self.start = date(2016, 1, 1)
		self.loopday = self.start
		self.year = self.start.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		
		self.daycount = 1 #366year, 186summer
		
		self.masksload()
		self.map_create()
		
		self.CSVDatum = ['Date']
		self.CSVVolume =  ['Volume']
		self.CSVExtent = ['Extent']
		self.CSVArea = ['Area']
		self.meltfactor = 0.82 # MJ reduction
		self.sic_cutoff = 0.12 #cm
		
		self.CSVVolumeHigh =  ['Volume']
		self.CSVExtentHigh = ['Extent']
		self.CSVAreaHigh = ['Area']
		
		self.CSVVolumeLow =  ['Volume']
		self.CSVExtentLow = ['Extent']
		self.CSVAreaLow = ['Area']
		
		
	def masksload(self):
	
		filename = 'X:/NSIDC_South/Masks/region_s_pure.msk'
		with open(filename, 'rb') as frmsk:
				mask = np.fromfile(frmsk, dtype=np.uint8)
		self.regmaskf = np.array(mask, dtype=float)
		
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
		
		self.latitudelist = np.loadtxt('X:/NSIDC_South/Masks/Lattable_south_MJ_all_year.csv', delimiter=',')
		
	
	def prediction(self):		
		filepath = 'X:/NSIDC_South/DataFiles/'	
		filename = 'NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
		countmax = self.index+self.daycount
		
		with open(os.path.join(filepath,filename), 'rb') as frr:
			iceforecast = np.fromfile(frr, dtype=np.uint8)
		iceforecast = np.array(iceforecast, dtype=float)/250
		
		self.iceMean = np.array(self.iceLastDate, dtype=float)
		self.iceHigh = np.array(self.iceLastDate, dtype=float)
		self.iceLow = np.array(self.iceLastDate, dtype=float)
		

		for count in range (self.index,countmax,1):
			filename = 'NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
			filenameAvg = 'DataFiles/Daily_Mean/NSIDC_Mean_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filenameChange = 'DataFiles/Daily_change/NSIDC_SIC_Change_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filenameStdv = 'DataFiles/Stdv/NSIDC_Stdv_{}{}_south.bin'.format(self.stringmonth,self.stringday)

		
			#normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16						
			
			if count <= 500: #change date of year to last available date
				with open(os.path.join(filepath,filename), 'rb') as frr:
					ice2 = np.fromfile(frr, dtype=np.uint8)
				iceforecast = np.array(ice2, dtype=float)/250
				iceforecast = iceforecast
				
				self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecast,self.iceMean)
# =============================================================================
# 				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh = np.array(self.iceMean),sicmap,extent,area,calcvolume
# 				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow = np.array(self.iceMean),sicmap,extent,area,calcvolume
# =============================================================================
				
			else:
				with open(filenameChange, 'rb') as fr:
					icechange = np.fromfile(fr, dtype=np.int8)
				icechange = np.array(icechange, dtype=float)/250
				with open(filenameAvg, 'rb') as fr:
					iceAvg = np.fromfile(fr, dtype=np.uint8)
				iceAvg = np.array(iceAvg, dtype=float)/250
				
				with open(filenameStdv, 'rb') as frr:
					iceStdv = np.fromfile(frr, dtype=np.float16)
				iceStdv = np.array(iceStdv, dtype=float)/250
			
				iceforecast = iceforecast + icechange
				iceforecastMean = (2*iceforecast+iceAvg)/3
				iceforecastHigh = np.array(iceforecastMean + iceStdv*0.25)
				iceforecastLow = np.array(iceforecastMean - iceStdv*0.5)
				
				self.iceMean,sicmap,extent,area,calcvolume = self.meltcalc(iceforecastMean,self.iceMean)
				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh = self.meltcalc(iceforecastHigh,self.iceHigh)
				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow = self.meltcalc(iceforecastLow,self.iceLow)
			

			self.CSVVolume.append(int(calcvolume))
			self.CSVExtent.append(int(extent)/1e6)
			self.CSVArea.append(int(area)/1e6)
			
# =============================================================================
# 			self.CSVVolumeHigh.append(int(calcvolumeHigh))
# 			self.CSVExtentHigh.append(int(extentHigh)/1e6)
# 			self.CSVAreaHigh.append(int(areaHigh)/1e6)
# 			
# 			self.CSVVolumeLow.append(int(calcvolumeLow))
# 			self.CSVExtentLow.append(int(extentLow)/1e6)
# 			self.CSVAreaLow.append(int(areaLow)/1e6)
# =============================================================================
			
			#save last date as arrary in mm
			self.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean')
			self.concentrationshow(sicmap,int(area),int(extent),'Mean')
#			self.thicknessshow(self.iceHigh,int(calcvolumeHigh),int(extentHigh),'High')
#			self.thicknessshow(self.iceLow ,int(calcvolumeLow),int(extentLow),'Low')
			iceLastDateMean = self.iceMean*1000
			iceLastDateMean = np.array(iceLastDateMean,dtype=np.uint16)
# =============================================================================
# 			iceLastDateHigh = self.iceHigh*1000
# 			iceLastDateHigh = np.array(iceLastDateHigh,dtype=np.uint16)
# 			iceLastDateLow = self.iceLow*1000
# 			iceLastDateLow = np.array(iceLastDateLow,dtype=np.uint16)
# =============================================================================

			with open('X:/Sea_Ice_Forecast/SIPN_south/SIPN2_Thickness_Mean_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
				writecumu.write(iceLastDateMean)
# =============================================================================
# 				with open('X:/Sea_Ice_Forecast/SIPN_south/SIPN2_Thickness_midHigh_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
# 					writecumu.write(iceLastDateHigh)
# 				with open('X:/Sea_Ice_Forecast/SIPN_south/SIPN2_Thickness_midLow_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
# 					writecumu.write(iceLastDateLow)
# =============================================================================
			with open('X:/Sea_Ice_Forecast/SIPN_south/SIPN2_SIC_Mean_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
				writecumu.write(sicmap)
# =============================================================================
# 				with open('X:/Sea_Ice_Forecast/SIPN_south/SIPN2_SIC_midHigh_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
# 					writecumu.write(sicmapHigh)
# 				with open('X:/Sea_Ice_Forecast/SIPN_south/SIPN2_SIC_midLow_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
# 					writecumu.write(sicmapLow)
# =============================================================================
			
			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			print(self.year,count)
			print(self.yearday)
			if count < countmax:
				self.advanceday(1)
			
	def advanceday(self,delta):	
		self.loopday = self.loopday+timedelta(days=delta)
		self.year = self.loopday.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		self.yearday = self.loopday.timetuple().tm_yday
					
				

	def meltcalc(self,iceforecast,icearray):
		arraylength = len(iceforecast)
		np.seterr(divide='ignore', invalid='ignore')
		icemeltenergy = 333.55*1000*0.92/1000 #Meltenergy per m3, KJ/kg*1000(m3/dm)*0.92(density)/1000(MJ/KJ)
		gridvolumefactor = 625*0.001
		
		sicmapg = np.array(np.zeros(len(icearray),dtype=np.uint8))
		extent = 0
		area = 0
		calcvolume = 0
		for x in range (0,arraylength):
			if  1 < self.regmaskf[x] < 16:
				if 0 < icearray[x] < 5:
					pixlat = min(-50,self.latmaskf[x])
					indexx = int(round((pixlat+50)*(-5)))
					MJ = self.latitudelist[indexx][self.yearday]*(1-min(1,max(0,iceforecast[x])))*self.meltfactor
					icearray[x] = max(0,icearray[x]-MJ/icemeltenergy)
					calcvolume = calcvolume + gridvolumefactor*icearray[x]
				if self.sic_cutoff < icearray[x] < 5:
					sicmapg[x] = min(250,(icearray[x]**1.3)/0.004)
					extent = extent + self.areamaskf[x]
					area = area + min(1,icearray[x])*0.82 * self.areamaskf[x]
					
					
		return icearray,sicmapg,extent,area,calcvolume
		

	def thicknessshow(self,icemap,Volumevalue,extentvalue,outlooktype):		
		icemap = ma.masked_greater(icemap, 5)
		icemap = icemap.reshape(332, 316)
		
#		areavalue = int(areavalue*1e6)
#		extentvalue = int(extentvalue*1e6)
		Volumevalue = '{:,}'.format(Volumevalue)+' 'r'$km^3$'
		extentvalue = '{:,}'.format(extentvalue)+' 'r'$km^2$'
	
		
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		
		self.ax.clear()
		self.ax.set_title('{}_Forecast , Date: {}-{}-{}'.format(outlooktype,self.year,self.stringmonth,self.stringday))
		#self.ax.set_title('Average Forecast')
		self.ax.set_xlabel('Volume: {} / Extent: {}'.format(Volumevalue,extentvalue), fontsize=14)
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=3, cmap=cmap)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 8, r'Data: NSIDC', fontsize=10,color='white',fontweight='bold')
		self.ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.ax.text(-0.04, 0.48, 'https://sites.google.com/site/cryospherecomputing/forecast',
        transform=self.ax.transAxes,rotation='vertical',color='grey', fontsize=10)
		self.fig.tight_layout(pad=1)
		self.fig.subplots_adjust(left=0.05)
#		if self.loopday.month > 9:
#			self.fig.savefig('X:/Sea_Ice_Forecast/SIPN_south/SIPN_{}{}{}.png'.format(self.year,self.stringmonth,self.stringday))
		plt.pause(0.01)
		
	def concentrationshow(self,icemap,Areavalue,extentvalue,outlooktype):
		icemap = icemap/250
		icemap = ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(332, 316)
		
#		areavalue = int(areavalue*1e6)
#		extentvalue = int(extentvalue*1e6)
		Areavalue = '{:,}'.format(Areavalue)+' 'r'$km^2$'
		extentvalue = '{:,}'.format(extentvalue)+' 'r'$km^2$'
	
		
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		
		self.ax2.clear()
		self.ax2.set_title('{}_Forecast , Date: {}-{}-{}'.format(outlooktype,self.year,self.stringmonth,self.stringday))
		#self.ax.set_title('Average Forecast')
		self.ax2.set_xlabel('Area: {} / Extent: {}'.format(Areavalue,extentvalue), fontsize=14)
		self.cax2 = self.ax2.imshow(icemap, interpolation='nearest', vmin=0, vmax=1, cmap=cmap)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 8, r'Data: NSIDC', fontsize=10,color='white',fontweight='bold')
		self.ax2.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.ax2.text(-0.04, 0.48, 'https://sites.google.com/site/cryospherecomputing/forecast',
        transform=self.ax2.transAxes,rotation='vertical',color='grey', fontsize=10)
		self.fig2.tight_layout(pad=1)
		self.fig2.subplots_adjust(left=0.05)
#		if self.loopday.month > 9:
#			self.fig2.savefig('X:/Sea_Ice_Forecast/SIPN_south/SIPN_SIC_{}{}{}.png'.format(self.year,self.stringmonth,self.stringday))
		plt.pause(0.01)
		
	def map_create(self):
		self.icenull = np.zeros(104912, dtype=float)
		self.icenull = self.icenull.reshape(332, 316)
		
		self.fig, self.ax = plt.subplots(figsize=(8, 10))
		self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=3,cmap = plt.cm.jet)
		self.cbar = self.fig.colorbar(self.cax, ticks=[0,0.5,1,1.5,2,2.5,3]).set_label('Sea Ice Thickness in m')
		
		self.fig2, self.ax2 = plt.subplots(figsize=(8, 10))
		self.cax2 = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=3,cmap = plt.cm.jet)
		self.cbar = self.fig2.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Sea Ice concentration in %')
			

	def writetofile(self):
		
		with open('X:/Sea_Ice_Forecast/SIPN_south/___SIPN_forecast_{}.csv'.format(self.year), "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for x in range(0,len(self.CSVVolume)):
				writer.writerow([self.CSVDatum[x],self.CSVVolume[x],self.CSVExtent[x],self.CSVArea[x]])
				
# =============================================================================
# 		with open('X:/Sea_Ice_Forecast/SIPN_south/___SIPN_forecast_High_{}.csv'.format(self.year), "w") as output: 
# 			writer = csv.writer(output, lineterminator='\n') #str(self.year)
# 			for x in range(0,len(self.CSVVolumeHigh)):
# 				writer.writerow([self.CSVDatum[x],self.CSVVolumeHigh[x],self.CSVExtentHigh[x],self.CSVAreaHigh[x]])
# 				
# 		with open('X:/Sea_Ice_Forecast/SIPN_south/___SIPN_forecast_Low_{}.csv'.format(self.year), "w") as output: 
# 			writer = csv.writer(output, lineterminator='\n') #str(self.year)
# 			for x in range(0,len(self.CSVVolumeLow)):
# 				writer.writerow([self.CSVDatum[x],self.CSVVolumeLow[x],self.CSVExtentLow[x],self.CSVAreaLow[x]])
# =============================================================================


		
	def getvolume (self,thickness,daycount,day,month,year):
		self.daycount = daycount
		self.start = date(year,month,day)
		self.loopday	= self.start
		self.year = year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		lastday = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		self.index = self.loopday.timetuple().tm_yday
		self.yearday = self.loopday.timetuple().tm_yday
		
		self.daycount = daycount
		
		print(thickness,'meter')
		
		filepath = 'X:/NSIDC_south/DataFiles/'	
		filename = 'NSIDC_{}_south.bin'.format(lastday)
		
		with open(os.path.join(filepath,filename), 'rb') as fr:
				ice = np.fromfile(fr, dtype=np.uint8)
		self.iceLastDate = np.array(ice, dtype=float)/250
		
		for x in range (0,len(self.iceLastDate)):
			if self.regmaskf[x] > 7:
				self.iceLastDate[x] = 9
		
		for x in range (0,len(self.iceLastDate)):
			if 1 < self.regmaskf[x] < 7:
				if self.iceLastDate[x] > 0.15:
					self.iceLastDate[x] = thickness*self.iceLastDate[x]*(self.latmaskf[x]/(-60))
			if self.regmaskf[x] < 1:
				self.iceLastDate[x] = 0

		
#		self.normalshow(self.iceLastDate,volume,area,'Mean')
		self.prediction()
#		self.thicknessshow(self.iceLastDate,5,4,'dfh')
#		self.concentrationshow(ice,5,4,'dfh')
		self.writetofile()
		plt.show()
	
thicknesslist =1.5 #[1.422,1.589,1.344,1.470,1.555,1.407,1.553,1.414,1.521,1.446,1.465,1.408,1.537,1.626,1.609,1.624,1.538] 2000-2017
year = 2015


action = NSIDC_prediction()
if __name__ == "__main__":
	print('main')
#	action.loadCSVdata()
	#action.prediction()
	#action.makegraph()
	#action.makegraph_compaction()
#	for x in range(0,len(thicknesslist)):
	action.getvolume(thicknesslist,92,1,12,year)
#	year = year+1

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA