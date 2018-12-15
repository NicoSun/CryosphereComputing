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
		self.loopday	= self.start
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
		self.CSVAlaska = ['Alaska']
		
		self.CSVVolumeLow =  ['Volume']
		self.CSVExtentLow = ['Extent']
		self.CSVAreaLow = ['Area']
		
		
	def masksload(self):
	
		self.regionmask = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		with open(self.regionmask, 'rb') as frmsk:
				mask = np.fromfile(frmsk, dtype=np.uint32)
		self.regmaskf = np.array(mask, dtype=float)
		
		self.areamask = 'X:/NSIDC/Masks/psn25area_v3.dat'
		with open(self.areamask, 'rb') as famsk:
				mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(mask2, dtype=float)
		self.areamaskf = self.areamaskf /1000
		
		self.latmask = 'X:/NSIDC/Masks/psn25lats_v3.dat'
		with open(self.latmask, 'rb') as flmsk:
				mask3 = np.fromfile(flmsk, dtype=np.uint32)
		self.latmaskf = np.array(mask3, dtype=float)
		self.latmaskf = self.latmaskf /100000
		
		self.lonmask = 'X:/NSIDC/Masks/psn25lons_v3.dat'
		with open(self.lonmask, 'rb') as flmsk:
				mask4 = np.fromfile(flmsk, dtype=np.uint32)
		self.lonmaskf = np.array(mask4, dtype=float)
		self.lonmaskf = self.lonmaskf /100000
		
		self.latitudelist = [40,40.2,40.4,40.6,40.8,41,41.2,41.4,41.6,41.8,42,42.2,42.4,42.6,42.8,43,43.2,43.4,43.6,43.8,44,44.2,44.4,44.6,44.8,45,45.2,45.4,45.6,45.8,46,46.2,46.4,46.6,46.8,47,47.2,47.4,47.6,47.8,48,48.2,48.4,48.6,48.8,49,49.2,49.4,49.6,49.8,50,50.2,50.4,50.6,50.8,51,51.2,51.4,51.6,51.8,52,52.2,52.4,52.6,52.8,53,53.2,53.4,53.6,53.8,54,54.2,54.4,54.6,54.8,55,55.2,55.4,55.6,55.8,56,56.2,56.4,56.6,56.8,57,57.2,57.4,57.6,57.8,58,58.2,58.4,58.6,58.8,59,59.2,59.4,59.6,59.8,60,60.2,60.4,60.6,60.8,61,61.2,61.4,61.6,61.8,62,62.2,62.4,62.6,62.8,63,63.2,63.4,63.6,63.8,64,64.2,64.4,64.6,64.8,65,65.2,65.4,65.6,65.8,66,66.2,66.4,66.6,66.8,67,67.2,67.4,67.6,67.8,68,68.2,68.4,68.6,68.8,69,69.2,69.4,69.6,69.8,70,70.2,70.4,70.6,70.8,71,71.2,71.4,71.6,71.8,72,72.2,72.4,72.6,72.8,73,73.2,73.4,73.6,73.8,74,74.2,74.4,74.6,74.8,75,75.2,75.4,75.6,75.8,76,76.2,76.4,76.6,76.8,77,77.2,77.4,77.6,77.8,78,78.2,78.4,78.6,78.8,79,79.2,79.4,79.6,79.8,80,80.2,80.4,80.6,80.8,81,81.2,81.4,81.6,81.8,82,82.2,82.4,82.6,82.8,83,83.2,83.4,83.6,83.8,84,84.2,84.4,84.6,84.8,85,85.2,85.4,85.6,85.8,86,86.2,86.4,86.6,86.8,87,87.2,87.4,87.6,87.8,88,88.2,88.4,88.6,88.8,89,89.2,89.4,89.6,89.8,90]
		self.latitudelist = np.loadtxt('X:/NSIDC/Masks/Lattable_MJ_all_year.csv', delimiter=',')
		
	
	def prediction(self):		
		filepath = 'X:/NSIDC/DataFiles/'	
		filename = 'NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
		countmax = self.index+self.daycount
		
		with open(os.path.join(filepath,filename), 'rb') as frr:
			iceforecast = np.fromfile(frr, dtype=np.uint8)
		iceforecast = np.array(iceforecast, dtype=float)/250
		
		self.iceMean = np.array(self.iceLastDate, dtype=float)
		self.iceHigh = np.array(self.iceLastDate, dtype=float)
		self.iceLow = np.array(self.iceLastDate, dtype=float)
		

		for count in range (self.index,countmax,1):		
			filename = 'NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
			filenameAvg = 'DataFiles/Daily_Mean/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameChange = 'DataFiles/Daily_change/NSIDC_SIC_Change_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameStdv = 'DataFiles/Stdv/NSIDC_Stdv_{}{}.bin'.format(self.stringmonth,self.stringday)

		
			#normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16						
			
			if count <= 222: #change date of year to last available date
				with open(os.path.join(filepath,filename), 'rb') as frr:
					ice2 = np.fromfile(frr, dtype=np.uint8)
				iceforecast = np.array(ice2, dtype=float)/250
				iceforecast = iceforecast
				
				self.iceMean,sicmap,extent,area,calcvolume,alaska = self.meltcalc(iceforecast,self.iceMean,count)
				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh = np.array(self.iceMean),sicmap,extent,area,calcvolume
				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow = np.array(self.iceMean),sicmap,extent,area,calcvolume
				
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
				
				self.iceMean,sicmap,extent,area,calcvolume,alaska = self.meltcalc(iceforecastMean,self.iceMean,count)
				self.iceHigh,sicmapHigh,extentHigh,areaHigh,calcvolumeHigh,alaskaHigh = self.meltcalc(iceforecastHigh,self.iceHigh,count)
				self.iceLow ,sicmapLow,extentLow,areaLow,calcvolumeLow,alaskaLow = self.meltcalc(iceforecastLow,self.iceLow,count)
			

			self.CSVVolume.append(int(calcvolume))
			self.CSVExtent.append(int(extent)/1e6)
			self.CSVArea.append(int(area)/1e6)
			
			self.CSVVolumeHigh.append(int(calcvolumeHigh))
			self.CSVExtentHigh.append(int(extentHigh)/1e6)
			self.CSVAreaHigh.append(int(areaHigh)/1e6)
			
			self.CSVVolumeLow.append(int(calcvolumeLow))
			self.CSVExtentLow.append(int(extentLow)/1e6)
			self.CSVAreaLow.append(int(areaLow)/1e6)
			self.CSVAlaska.append((int(alaska)/1e6))
			
			#save last date as arrary in mm
#			if count == (countmax-1):
#			self.thicknessshow(self.iceMean,int(calcvolume),int(extent),'Mean')
#			self.concentrationshow(sicmap,int(area),int(extent),'Mean')
#			self.thicknessshow(self.iceHigh,int(calcvolumeHigh),int(extentHigh),'High')
#			self.thicknessshow(self.iceLow ,int(calcvolumeLow),int(extentLow),'Low')
			iceLastDateMean = self.iceMean*1000
			iceLastDateMean = np.array(iceLastDateMean,dtype=np.uint16)
			iceLastDateHigh = self.iceHigh*1000
			iceLastDateHigh = np.array(iceLastDateHigh,dtype=np.uint16)
			iceLastDateLow = self.iceLow*1000
			iceLastDateLow = np.array(iceLastDateLow,dtype=np.uint16)
			if self.loopday.month > 5:
#				with open('X:/Forecast/August_test/SIPN2_Thickness_Mean_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
#					writecumu.write(iceLastDateMean)
				with open('X:/Forecast/August_test/SIPN2_Thickness_midHigh_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
					writecumu.write(iceLastDateHigh)
				with open('X:/Forecast/August_test/SIPN2_Thickness_midLow_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
					writecumu.write(iceLastDateLow)
					
#				with open('X:/Forecast/August_test/SIPN2_SIC_Mean_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
#					writecumu.write(sicmap)
				with open('X:/Forecast/August_test/SIPN2_SIC_midHigh_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
					writecumu.write(sicmapHigh)
				with open('X:/Forecast/August_test/SIPN2_SIC_midLow_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday),'wb') as writecumu:
					writecumu.write(sicmapLow)
			
			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			count = count+1
			print(count)
			if count < countmax:
				self.advanceday(1)
			
	def advanceday(self,delta):	
		self.loopday = self.loopday+timedelta(days=delta)
		self.year = self.loopday.year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
					
				

	def meltcalc(self,iceforecast,icearray,count):
		arraylength = len(iceforecast)
		np.seterr(divide='ignore', invalid='ignore')
		icemeltenergy = 333.55*1000*0.92/1000 #Meltenergy per m3, KJ/kg*1000(m3/dm)*0.92(density)/1000(MJ/KJ)
		gridvolumefactor = 625*0.001
		
		sicmapg = np.array(self.sicmap)
		extent = 0
		area = 0
		alaska = 0
		calcvolume = 0
		for x in range (0,arraylength):
			if  1 < self.regmaskf[x] < 16:
				if 0 < icearray[x] < 5:
					pixlat = max(40,self.latmaskf[x])
					indexx = int(round((pixlat-40)*5))
					MJ = self.latitudelist[indexx][count+1]*(1-min(1,max(0,iceforecast[x])))*self.meltfactor
					icearray[x] = max(0,icearray[x]-MJ/icemeltenergy)
					calcvolume = calcvolume + gridvolumefactor*icearray[x]
				if self.sic_cutoff < icearray[x] < 5:
					sicmapg[x] = min(250,(icearray[x]**1.3)/0.004)
					extent = extent + self.areamaskf[x]
					area = area + min(1,icearray[x])*0.82 * self.areamaskf[x]
					if self.regmaskf[x] == 12 or self.regmaskf[x] == 13:
						alaska = alaska + self.areamaskf[x]
					
					
		return icearray,sicmapg,extent,area,calcvolume,alaska
		

	def thicknessshow(self,icemap,Volumevalue,extentvalue,outlooktype):		
		icemap = ma.masked_greater(icemap, 5)
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		
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
		if self.loopday.month > 9:
			self.fig.savefig('X:/Forecast/August_test/SIPN_{}{}{}.png'.format(self.year,self.stringmonth,self.stringday))
		plt.pause(0.01)
		
	def concentrationshow(self,icemap,Areavalue,extentvalue,outlooktype):
		icemap = icemap/250
		icemap = ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		
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
		if self.loopday.month > 9:
			self.fig2.savefig('X:/Forecast/August_test/SIPN_SIC_{}{}{}.png'.format(self.year,self.stringmonth,self.stringday))
		plt.pause(0.01)
		
	def map_create(self):
		self.icenull = np.zeros(136192, dtype=float)
		self.icenull = self.icenull.reshape(448, 304)
		
		self.fig, self.ax = plt.subplots(figsize=(8, 10))
		self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=3,cmap = plt.cm.jet)
		self.cbar = self.fig.colorbar(self.cax, ticks=[0,0.5,1,1.5,2,2.5,3]).set_label('Sea Ice Thickness in m')
		
		self.fig2, self.ax2 = plt.subplots(figsize=(8, 10))
		self.cax2 = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=3,cmap = plt.cm.jet)
		self.cbar = self.fig2.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Sea Ice concentration in %')
			
		
			
	def makegraph(self,forecastHigh,forecastMean,forecastLow):
		#del self.CSVArea[0]
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('Forecast Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday) ,fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,31,60,91,121,152,182,213,244,274,305,335]
		plt.xticks(x,labels)

		ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.6, -0.06, 'https://sites.google.com/site/cryospherecomputing/forecast',
        transform=ax.transAxes,color='grey', fontsize=10)
		
		ax.grid(True)
		CSVAreaPast = forecastHigh[:(len(forecastHigh)-(self.daycount))]
		
		
		plt.plot( self.C1980s, color=(0.8,0.8,0.8),label='1980s',lw=1,ls='--')
		plt.plot( self.C1990s, color=(0.6,0.6,0.6),label='1990s',lw=1,ls='--')
		plt.plot( self.C2000s, color=(0.4,0.4,0.4),label='2000s',lw=1,ls='--')
		plt.plot( self.C2007, color='red',label='2007',lw=1)
		plt.plot( self.C2012, color='orange',label='2012',lw=1)
		plt.plot( self.C2013, color='purple',label='2013',lw=1)
		plt.plot( self.C2014, color='blue',label='2014',lw=1)
		#plt.plot( self.C2015, color='green',label='2015',lw=1)
		plt.plot( self.C2016, color='green',label='2016',lw=1)
		plt.plot( self.C2017, color='brown',label='2017',lw=1)
		plt.plot( CSVAreaPast, color='black',label='2018',lw=2)
		plt.plot( forecastHigh, color='black',lw=2,ls=':')
		plt.plot( forecastMean, color='black',lw=2,ls=':')
		plt.plot( forecastLow, color='black',lw=2,ls=':')
		
		last_value_High =  int(forecastHigh[-1]*1e6)
		last_value_Mean =  int(forecastMean[-1]*1e6)
		last_value_Low =  int(forecastLow[-1]*1e6)
		ax.text(0.01, 0.07, 'High: '+'{:,}'.format(last_value_High)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
		ax.text(0.01, 0.04, 'Mean: '+'{:,}'.format(last_value_Mean)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
		ax.text(0.01, 0.01, 'Low: '+'{:,}'.format(last_value_Low)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
		
		startdate = int(self.day+(self.month-1)*30.5-(self.daycount+5))
		ymin = min(forecastLow[-1]-1,forecastLow[startdate]-1)
		ymax = max(forecastHigh[startdate]+1,forecastHigh[-1]+1)
		plt.axis([startdate,len(forecastLow)+20,ymin,ymax])
		plt.legend(loc=4, shadow=True, fontsize='medium')
		
		ax.text(0.20, 0.07, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.20, 0.04, r'Calculation by Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.subplots_adjust(bottom=0.08)
		
#		fig.savefig('X:/Upload/SIC_prediction/Arctic_{}day_Forecast.png'.format(self.daycount))


	def writetofile(self):
		
		with open('X:/Forecast/August_test/___SIPN_forecast_{}.csv'.format(self.year), "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for x in range(0,len(self.CSVVolume)):
				writer.writerow([self.CSVDatum[x],self.CSVVolume[x],self.CSVExtent[x],self.CSVArea[x],self.CSVAlaska[x]])
				
		with open('X:/Forecast/August_test/___SIPN_forecast_High_{}.csv'.format(self.year), "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for x in range(0,len(self.CSVVolumeHigh)):
				writer.writerow([self.CSVDatum[x],self.CSVVolumeHigh[x],self.CSVExtentHigh[x],self.CSVAreaHigh[x]])
				
		with open('X:/Forecast/August_test/___SIPN_forecast_Low_{}.csv'.format(self.year), "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for x in range(0,len(self.CSVVolumeLow)):
				writer.writerow([self.CSVDatum[x],self.CSVVolumeLow[x],self.CSVExtentLow[x],self.CSVAreaLow[x]])


		
	def getvolume (self,thickness,daycount,day,month,year):
		self.daycount = daycount
		self.start = date(year,month,day)
		self.loopday	= self.start
		self.year = year
		self.stringmonth = str(self.loopday.month).zfill(2)
		self.stringday = str(self.loopday.day).zfill(2)
		lastday = '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		self.index = self.loopday.timetuple().tm_yday
		
		self.daycount = daycount
		
		print(thickness,'meter')
		
		filepath = 'X:/NSIDC/DataFiles/'	
		filename = 'NSIDC_{}.bin'.format(lastday)
		
		with open(os.path.join(filepath,filename), 'rb') as fr:
				ice = np.fromfile(fr, dtype=np.uint8)
		self.iceLastDate = np.array(ice, dtype=float)/250
		self.sicmap = np.zeros(len(self.iceLastDate),dtype=np.uint8)
		
		for x in range (0,len(self.iceLastDate)):
			if self.regmaskf[x] > 15:
				self.iceLastDate[x] = 9
				self.sicmap [x] = 255
		
		for x in range (0,len(self.iceLastDate)):
			if 1 < self.regmaskf[x] < 16:
				if self.iceLastDate[x] > 0.15:
					self.iceLastDate[x] = thickness*self.iceLastDate[x]*(self.latmaskf[x]/75)
			if self.regmaskf[x] < 2:
				self.iceLastDate[x] = 0

		
#		self.normalshow(self.iceLastDate,volume,area,'Mean')
		self.prediction()
		if self.year > 2016:
			self.writetofile()
		plt.show()
	
thicknesslist =1.5#2.02# [2.25,2.46,2.32,1.98,1.87,1.82,1.93,2.11,1.99,2.02,1.98]#,2.02] , 2007 start
#thicknesslistAug18 =1.5
year = 2018


action = NSIDC_prediction()
if __name__ == "__main__":
	print('main')
#	action.loadCSVdata()
	#action.prediction()
	#action.makegraph()
	#action.makegraph_compaction()
#	for x in range(0,len(thicknesslist)):
	action.getvolume(thicknesslist,40,10,8,year)
#	year = year+1

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA