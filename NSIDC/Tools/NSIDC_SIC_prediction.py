import numpy as np
import numpy.ma as ma
import pandas
import csv
import matplotlib.pyplot as plt
import os



class NSIDC_prediction:

	def __init__  (self):
		self.year = 2012
		self.month = 4
		self.day = 15
		
		self.daycount = 1 #366year, 186summer
		
		self.masksload()
		self.normalandanomaly()
		
		
	def masksload(self):
	
		self.regionmask = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		with open(self.regionmask, 'rb') as frmsk:
				self.mask = np.fromfile(frmsk, dtype=np.uint32)
		self.regmaskf = np.array(self.mask, dtype=float)
		
		self.areamask = 'X:/NSIDC/Masks/psn25area_v3.dat'
		with open(self.areamask, 'rb') as famsk:
				self.mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(self.mask2, dtype=float)
		self.areamaskf = self.areamaskf /1000
		
	def loadLastDate(self,lastday):		
		filepath = 'X:/NSIDC/DataFiles/'	
		filename = 'NSIDC_{}.bin'.format(lastday)
		
		with open(os.path.join(filepath,filename), 'rb') as fr:
				ice = np.fromfile(fr, dtype=np.uint8)
		self.iceLastDate = np.array(ice, dtype=float)/250
		
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
		#self.normalshow(self.iceLastDate,self.CSVArea[-1],self.CSVExtent[-1],'Mean')
	
	def prediction(self):		
		filepath = 'X:/NSIDC/DataFiles/'	
		filename = 'NSIDC_{}{}{}.bin'.format(self.year,str(self.month).zfill(2),str(self.day).zfill(2))
		
		iceMean = np.array(self.iceLastDate, dtype=float)
		iceHigh = np.array(self.iceLastDate, dtype=float)
		iceLow = np.array(self.iceLastDate, dtype=float)
		
		arraylength = len(iceMean)
		np.seterr(divide='ignore', invalid='ignore')
		
		for count in range (0,self.daycount,1): 
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			
			filenameAvg = 'DataFiles/Daily_Mean/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameChange = 'DataFiles/Daily_change/NSIDC_SIC_Change_{}{}.bin'.format(self.stringmonth,self.stringday)
			#filenameMax = 'DataFiles/Maximum/NSIDC_Max_{}{}.bin'.format(self.stringmonth,self.stringday)
			#filenameMin = 'DataFiles/Minimum/NSIDC_Min_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameStdv = 'DataFiles/Stdv/NSIDC_Stdv_{}{}.bin'.format(self.stringmonth,self.stringday)
		
			#normal dtype:uint8 , filenameChange:int8 , filenameStdv: np.float16						
			with open(filenameChange, 'rb') as fr:
				iceforecast = np.fromfile(fr, dtype=np.int8)
			
			with open(filenameAvg, 'rb') as fr:
				iceAvg = np.fromfile(fr, dtype=np.uint8)			
			with open(filenameStdv, 'rb') as frr:
				iceStdv = np.fromfile(frr, dtype=np.float16)
				iceStdv = np.array(iceStdv, dtype=float)				
			
			self.areaHigh=[]
			self.area=[]
			self.areaLow=[]
			self.extentHigh = []
			self.extent = []
			self.extentLow = []
			
			iceforecast = iceforecast/250
			iceAvg = iceAvg/250
			iceStdv = iceStdv/250
			
			for x in range (0,arraylength):
				if  1 < self.regmaskf[x] < 16:
					iceStdvChange = abs(iceforecast[x])*(1-iceStdv[x])*0.5
					iceMax = [iceAvg[x]+iceStdv[x],iceHigh[x]-iceStdvChange]
					iceMax = np.mean(iceMax)
					
					if count < 30:
						iceMin = min(iceAvg[x]-iceStdv[x],self.iceLastDate[x])
					else:
						iceMin = iceAvg[x]-iceStdv[x]
					
					iceHigh[x] = max(min(iceHigh[x]+iceforecast[x]+iceStdvChange*0.33,iceMax,1),iceMin,0)
					iceMean[x] = max(min(iceMean[x]+iceforecast[x],iceMax,1),iceMin,0)					
					iceLow[x] = max(min(iceLow[x]+iceforecast[x]-iceStdvChange,iceMax,1),iceMin,0)

					if 0.15 < iceHigh[x] <=1:
						self.areaHigh.append  (iceHigh[x]*self.areamaskf[x])
						self.extentHigh.append (self.areamaskf[x])
					if 0.15 < iceMean[x] <=1:
						self.area.append  (iceMean[x]*self.areamaskf[x])
						self.extent.append (self.areamaskf[x])
					if 0.15 < iceLow[x] <=1:
						self.areaLow.append  (iceLow[x]*self.areamaskf[x])
						self.extentLow.append (self.areamaskf[x])
					
				elif  0 <= self.regmaskf[x] < 2:
					iceHigh[x] = 0
					iceMean[x] = 0
					iceLow[x] = 0


			self.CSVAreaHigh.append((sum(self.areaHigh))/1e6)			
			self.CSVArea.append((sum(self.area))/1e6)			
			self.CSVAreaLow.append((sum(self.areaLow))/1e6)			
			self.CSVExtentHigh.append (sum(self.extentHigh)/1e6)
			self.CSVExtent.append (sum(self.extent)/1e6)
			self.CSVExtentLow.append (sum(self.extentLow)/1e6)
						
			if count == (self.daycount-1):
				self.normalshow(iceHigh,self.CSVAreaHigh[-1],self.CSVExtentHigh[-1],'III-High')
				self.normalshow(iceMean,self.CSVArea[-1],self.CSVExtent[-1],'II-Mean')
				self.normalshow(iceLow,self.CSVAreaLow[-1],self.CSVExtentLow[-1],'I-Low')

					
			
			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			count = count+1
			#print(count)
			if count < self.daycount:
				self.day = self.day+1
				if self.day==32 and (self.month==1 or self.month==3 or self.month==5 or self.month==7 or self.month==8 or self.month==10):
					self.day=1
					self.month = self.month+1
				elif self.day==31 and (self.month==4 or self.month==6 or self.month==9 or self.month==11):
					self.day=1
					self.month = self.month+1
				elif self.day==29 and self.month==2:
					self.day=1
					self.month = self.month+1
				elif  self.day==32 and self.month == 12:
					self.day = 1
					self.month = 1
					self.year = self.year+1
			
		

	def normalshow(self,icemap,areavalue,extentvalue,outlooktype):		
		icemap = ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		
		areavalue = int(areavalue*1e6)
		extentvalue = int(extentvalue*1e6)
		areavalue = '{:,}'.format(areavalue)+' 'r'$km^2$'
		extentvalue = '{:,}'.format(extentvalue)+' 'r'$km^2$'
	
		
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		
		self.ax.clear()
		self.ax.set_title('{}_Forecast , Date: {}-{}-{}'.format(outlooktype,self.year,self.stringmonth,self.stringday))
		#self.ax.set_title('Average Forecast')
		self.ax.set_xlabel('Area: {} / Extent: {}'.format(areavalue,extentvalue), fontsize=14)
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=1, cmap=cmap)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 8, r'Data: NSIDC', fontsize=10,color='white',fontweight='bold')
		self.ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.ax.text(-0.04, 0.48, 'https://sites.google.com/site/cryospherecomputing/forecast',
        transform=self.ax.transAxes,rotation='vertical',color='grey', fontsize=10)
		self.fig.tight_layout(pad=1)
		self.fig.subplots_adjust(left=0.05)
		self.fig.savefig('X:/Upload/SIC_prediction/{}_day_forecast_{}.png'.format(self.daycount,outlooktype))
		#plt.pause(0.01)	
		
	def normalandanomaly(self):
		self.icenull = np.zeros(136192, dtype=float)
		self.icenull = self.icenull.reshape(448, 304)
		
		self.fig, self.ax = plt.subplots(figsize=(8, 10))
		self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=100,cmap = plt.cm.jet)
		self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Sea Ice concentration in %')
			
		
			
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
		legend = plt.legend(loc=4, shadow=True, fontsize='medium')
		
		ax.text(0.20, 0.07, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.20, 0.04, r'Calculation by Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.subplots_adjust(bottom=0.08)
		
		fig.savefig('X:/Upload/SIC_prediction/Arctic_{}day_Forecast.png'.format(self.daycount))


	def writetofile(self):
		
		with open('X:/Upload/SIC_prediction/Arctic_'+str(self.daycount)+'days_forecast_II-Mean_'+str(self.year)+'.csv', "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for writeing in range(0,len(self.CSVArea)):
				writer.writerow([self.CSVDatum[writeing],self.CSVArea[writeing],self.CSVExtent[writeing]])
				
		with open('X:/Upload/SIC_prediction/Arctic_'+str(self.daycount)+'days_forecast_I-Low_'+str(self.year)+'.csv', "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for writeing in range(0,len(self.CSVAreaLow)):
				writer.writerow([self.CSVDatum[writeing],self.CSVAreaLow[writeing],self.CSVExtentLow[writeing]])
				
		with open('X:/Upload/SIC_prediction/Arctic_'+str(self.daycount)+'days_forecast_III-High_'+str(self.year)+'.csv', "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for writeing in range(0,len(self.CSVAreaHigh)):
				writer.writerow([self.CSVDatum[writeing],self.CSVAreaHigh[writeing],self.CSVExtentHigh[writeing]])

	
	def loadCSVdata (self):
		
		#NRT Data
		Yearcolnames = ['Date', 'Area', 'Extent','Compaction']
		Yeardata = pandas.read_csv('X:/Upload/AreaData/Arctic_NSIDC_Area_NRT_'+str(self.year)+'.csv', names=Yearcolnames)
		self.CSVDatum = Yeardata.Date.tolist()
		self.CSVArea =  Yeardata.Area.tolist()
		self.CSVExtent = Yeardata.Extent.tolist()
				
		self.CSVAreaHigh = list(self.CSVArea)
		self.CSVAreaLow = list(self.CSVArea)
		self.CSVExtentHigh = list(self.CSVExtent)
		self.CSVExtentLow = list(self.CSVExtent)
		
		#Climate Data
		Climatecolnames = ['Date','Max','C1980s','C1990s','C2000s','Min', 'C2007', 'C2008', 'C2009', 'C2010', 'C2011', 'C2012', 'C2013', 'C2014', 'C2015', 'C2016', 'C2017']
		Climatedata = pandas.read_csv('X:/Upload/AreaData/Arctic_climate_full.csv', names=Climatecolnames,header=0)
		self.C1980s = Climatedata.C1980s.tolist()
		self.C1990s = Climatedata.C1990s.tolist()
		self.C2000s = Climatedata.C2000s.tolist()
		self.Max = Climatedata.Max.tolist()
		self.Min = Climatedata.Min.tolist()
		self.C2007 = Climatedata.C2007.tolist()
		self.C2008 = Climatedata.C2008.tolist()
		self.C2009 = Climatedata.C2009.tolist()
		self.C2010 = Climatedata.C2010.tolist()
		self.C2011 = Climatedata.C2011.tolist()
		self.C2012 = Climatedata.C2012.tolist()
		self.C2013 = Climatedata.C2013.tolist()
		self.C2014 = Climatedata.C2014.tolist()
		self.C2015 = Climatedata.C2015.tolist()
		self.C2016 = Climatedata.C2016.tolist()
		self.C2017 = Climatedata.C2017.tolist()
		#del self.C1980s[0],self.C1990s[0],self.C2000s[0]
		#del self.C2007[0],self.C2008[0],self.C2009[0],self.C2010[0],self.C2011[0],self.C2012[0],self.C2013[0],self.C2014[0],self.C2015[0],self.C2016[0]
		
	
	
	def automated (self,daycount,day,month,year):
			
		self.year = year
		self.month = month
		self.day = day
		lastday = '{}{}{}'.format(self.year,str(self.month).zfill(2),str(self.day).zfill(2))
		
		self.daycount = daycount
		self.loadCSVdata()
		self.loadLastDate(lastday)
		self.prediction()
		self.makegraph(self.CSVAreaHigh,self.CSVArea,self.CSVAreaLow)
		self.writetofile()

action = NSIDC_prediction()
if __name__ == "__main__":
	print('main')
	#action.loadCSVdata()
	#action.prediction()
	action.automated(30,25,6,2018)
	#action.makegraph()
	#action.makegraph_compaction()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA