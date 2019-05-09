import numpy as np
import numpy.ma as ma
import pandas
import csv
import matplotlib.pyplot as plt
import os



class NSIDC_area:

	def __init__  (self):
		self.year = 1979
		self.month = 1
		self.day = 1
		
		self.daycount = 151 #366year, 186summer
		
		self.CSVDatum = ['Date']
		self.CSVArea =['Area']
		self.CSVExtent = ['Extent']
		self.CSVCompaction = ['Compaction']
		
		self.tarea_anom = ['Area Anomaly']
		self.textent_anom = ['Extent Anomaly']
		
		self.plottype = 'both' #normal, anomaly, both
		self.masksload()
		self.normalandanomaly()
		
		
	def masksload(self):
	
		regionmaskfile = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		with open(regionmaskfile, 'rb') as frmsk:
				mask = np.fromfile(frmsk, dtype=np.uint32)
		self.regmaskf = np.array(mask, dtype=float)
		
		areamaskfile = 'X:/NSIDC/Masks/psn25area_v3.dat'
		with open(areamaskfile, 'rb') as famsk:
				mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(mask2, dtype=float)
		self.areamaskf = self.areamaskf /1000
		
		
	def dayloop(self):		
		filepath = 'X:/NSIDC/DataFiles/'	
		for count in range (0,self.daycount,1): 
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			
			filename = 'NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
			filenamedav = 'Daily_Mean/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)	
			
			with open(os.path.join(filepath,filename), 'rb') as fr:
				ice = np.fromfile(fr, dtype=np.uint8)
			
			with open(os.path.join(filepath,filenamedav), 'rb') as frr:
				iceaverage = np.fromfile(frr, dtype=np.uint8)
			
			if len(ice) > 5000:
				self.icef = np.array(ice, dtype=float)
				iceaveragef = np.array(iceaverage, dtype=float)
				iceanomaly = np.zeros(136192, dtype=float)
		
				self.area=[]
				self.extent = []
	
				self.area_anom=[]
				self.extent_anom = []
			
			
				iceaveragef = iceaveragef/250
				icef = self.icef / 250
			
				for x in range (0,136192):
					if  1 < self.regmaskf[x] < 16:
						iceanomaly[x] = icef[x]-iceaveragef[x]
						if 0.15 <= icef[x] <=1:
							self.area.append  (icef[x]*self.areamaskf[x])
							self.extent.append (self.areamaskf[x])
						if  iceanomaly[x] <=1 and icef[x] <=1:
							self.area_anom.append  (iceanomaly[x]*self.areamaskf[x])
						
						
					elif  0 <= self.regmaskf[x] < 2:
						icef[x] = 0
						iceanomaly[x] = 0
					if  self.regmaskf[x] > 16 or icef[x]>1:
						iceanomaly[x] = 9


				self.CSVArea.append((sum(self.area))/1e6)			
				self.CSVExtent.append (sum(self.extent)/1e6)
				self.CSVCompaction.append ((sum(self.area)/sum(self.extent))*100)
			
				self.tarea_anom.append((sum(self.area_anom))/1e6)			
			
				if count == (self.daycount-1):
					self.normalshow(icef,self.CSVArea[-1])
					self.anomalyshow(iceanomaly,self.tarea_anom[-1])
					
			else:
				self.CSVArea.append('N/A')			
				self.CSVExtent.append ('N/A')
				self.CSVCompaction.append ('N/A')
			
			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			count = count+1
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
			
		

	def normalshow(self,icemap,icesum):		
		icemap = ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		icesum = round(icesum,3)
		icesum = '{0:.3f}'.format(icesum)
		
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		
		self.ax.clear()
		self.ax.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
		#self.ax.set_title('Minimum of Minima')
		self.ax.set_xlabel('Area: '+str(icesum)+' million km2', fontsize=14)
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=1, cmap=cmap)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 8, r'Data: NSIDC NRT', fontsize=10,color='white',fontweight='bold')
		self.ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.ax.text(-0.04, 0.48, 'https://sites.google.com/site/cryospherecomputing/daily-data',
        transform=self.ax.transAxes,rotation='vertical',color='grey', fontsize=10)
		self.fig.tight_layout(pad=1)
		self.fig.subplots_adjust(left=0.05)
		self.fig.savefig('X:/Upload/Arctic_yesterday.png')
		plt.pause(0.01)
	
	def anomalyshow(self,icemap,icesum):
		icemap = ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		icesum = round(icesum,3)
		icesum = '{0:.3f}'.format(icesum)
		
		self.ax2.clear()
		self.ax2.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday))		
		cmap2 = plt.cm.coolwarm_r
		cmap2.set_bad('black',0.6)
		
		self.ax2.set_xlabel('Area Anomaly: '+str(icesum)+' million km2', fontsize=14)
		self.cax = self.ax2.imshow(icemap, interpolation='nearest', vmin=-0.5, vmax=0.5, cmap=cmap2)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 8, r'Data: NSIDC NRT', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 18, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(-0.04, 0.48, 'https://sites.google.com/site/cryospherecomputing/daily-data',
        transform=self.ax2.transAxes,rotation='vertical',color='grey', fontsize=10)
		self.fig2.tight_layout(pad=1)
		self.fig2.subplots_adjust(left=0.05)
		self.fig2.savefig('X:/Upload/Arctic_yesterday_anomaly.png')
		plt.pause(0.01)
	
		
	def normalandanomaly(self):
		self.icenull = np.zeros(136192, dtype=float)
		self.icenull = self.icenull.reshape(448, 304)
		
		if self.plottype == 'normal' or self.plottype == 'both' :
			self.fig, self.ax = plt.subplots(figsize=(8, 10))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=100,cmap = plt.cm.jet)
			self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Sea Ice concentration in %')
			#self.title = self.fig.suptitle('Arctic Sea Ice Concentration', fontsize=14, fontweight='bold')
			
		if self.plottype == 'anomaly' or self.plottype == 'both':
			self.fig2, self.ax2 = plt.subplots(figsize=(8, 10))
			self.cax = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=-50, vmax=50, cmap=plt.cm.coolwarm_r)
			self.cbar = self.fig2.colorbar(self.cax, ticks=[-50,-25,0,25,50]).set_label('Sea Ice concentration anomaly in %')
			#self.title = self.fig2.suptitle('Arctic Sea Ice Concentration Anomaly', fontsize=14, fontweight='bold')
		
			
	def makegraph(self):
		#del self.CSVArea[0]
		fig = plt.figure(figsize=(8, 6))
		fig.suptitle('Arctic Sea Ice Area', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,31,60,91,121,152,182,213,244,274,305,335]
		plt.xticks(x,labels)

		ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
		
		ax.text(0.01, -0.08, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.35, -0.08, 'https://sites.google.com/site/cryospherecomputing/daily-data',
        transform=ax.transAxes,color='grey', fontsize=10)
		
		ax.grid(True)
		
		plt.plot( self.C1980s, color=(0.75,0.75,0.75),label='1980s',lw=2,ls='--')
		plt.plot( self.C1990s, color=(0.44,0.44,0.44),label='1990s',lw=2,ls='--')
		plt.plot( self.C2000s, color=(0.1,0.1,0.1),label='2000s',lw=2,ls='--')
		plt.plot( self.C2007, color='red',label='2007',lw=1)
		plt.plot( self.C2012, color='orange',label='2012',lw=1)
		plt.plot( self.C2013, color='purple',label='2013',lw=1)
		#plt.plot( self.C2014, color='blue',label='2014',lw=1)
		#plt.plot( self.C2015, color='green',label='2015',lw=1)
		plt.plot( self.C2016, color='green',label='2016',lw=1)
		plt.plot( self.C2017, color='brown',label='2017',lw=1)
		plt.plot( self.CSVArea, color='black',label='2018',lw=2)
		
		last_value =  int(self.CSVArea[-1]*1e6)
		ax.text(0.01, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
		
		ymin = max(0,float(self.CSVArea[-1])-4)
		ymax = min(15,float(self.CSVArea[-1])+4)
		plt.axis([(self.month-2.5)*30.5+self.day,self.day+(self.month)*30.5,ymin,ymax])
		legend = plt.legend(loc=4, shadow=True, fontsize='medium')
		
		ax.text(0.52, 0.07, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.52, 0.04, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.subplots_adjust(bottom=0.08)
		fig.savefig('X:/Upload/Arctic_Graph.png')

			
	def makegraph_full(self):
		#del self.CSVArea[0]
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('Arctic Sea Ice Area', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,31,60,91,121,152,182,213,244,274,305,335]
		plt.xticks(x,labels)

		ax.text(5, 0.5, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		ax.text(5, 0.2, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
		major_ticks = np.arange(0, 15, 1)
		ax.set_yticks(major_ticks)  

		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.6, -0.06, 'https://sites.google.com/site/cryospherecomputing/daily-data',
        transform=ax.transAxes,
        color='grey', fontsize=10)	
		
		ax.grid(True)
				
		plt.plot( self.C1980s, color=(0.75,0.75,0.75),label='1980s',lw=2,ls='--')
		plt.plot( self.C1990s, color=(0.44,0.44,0.44),label='1990s',lw=2,ls='--')
		plt.plot( self.C2000s, color=(0.1,0.1,0.1),label='2000s',lw=2,ls='--')
		plt.plot( self.C2007, color='red',label='2007',lw=1)
		plt.plot( self.C2012, color='orange',label='2012',lw=1)
		plt.plot( self.C2013, color='purple',label='2013',lw=1)
		#plt.plot( self.C2014, color='blue',label='2014',lw=1)
		#plt.plot( self.C2015, color='green',label='2015',lw=1)
		plt.plot( self.C2016, color='green',label='2016',lw=1)
		plt.plot( self.C2017, color='brown',label='2017',lw=1)
		plt.plot( self.CSVArea, color='black',label='2018',lw=2)
		
		last_value =  int(self.CSVArea[-1]*1e6)
		ax.text(0.72, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
		
		ymin = 0
		ymax = 15
		plt.axis([0,365,ymin,ymax])
		legend = plt.legend(loc=4, shadow=True, fontsize='medium')
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.subplots_adjust(bottom=0.06)
		fig.savefig('X:/Upload/Arctic_Graph_full.png')

			
	def makegraph_compaction(self):
		#del self.CSVCompaction[0]
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('Arctic Sea Ice Compaction (Area / Extent)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,31,60,91,121,152,182,213,244,274,305,335]
		plt.xticks(x,labels)
		
		ax.text(0.01, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.01, 0.03, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.set_ylabel('Compaction in %')
		major_ticks = np.arange(0, 100, 5)
		ax.set_yticks(major_ticks)     

		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.6, -0.06, 'https://sites.google.com/site/cryospherecomputing/daily-data',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		ax.grid(True)
		
		plt.plot( self.Compaction1980s, color=(0.8,0.8,0.8),label='1980s',lw=2,ls='--')
		plt.plot( self.Compaction1990s, color=(0.5,0.5,0.5),label='1990s',lw=2,ls='--')
		plt.plot( self.Compaction2000s, color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
		plt.plot( self.Compaction2010s, color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
		plt.plot( self.Compaction2007, color='red',label='2007',lw=1)
		plt.plot( self.Compaction2012, color='orange',label='2012',lw=1)
		plt.plot( self.Compaction2013, color='purple',label='2013',lw=1)
		#plt.plot( self.Compaction2014, color='blue',label='2014',lw=1)
		#plt.plot( self.Compaction2015, color='green',label='2015',lw=1)
		plt.plot( self.Compaction2016, color='green',label='2016',lw=1)
		plt.plot( self.Compaction2017, color='brown',label='2017',lw=1)
		plt.plot( self.CSVCompaction, color='black',label='2018',lw=2)
		
		last_value =  round(self.CSVCompaction[-1],2)
		ax.text(0.75, 0.01, 'Last value: '+str(last_value)+' %', fontsize=10,color='black',transform=ax.transAxes)
		
		yearday = int((self.month-1)*30.5+self.day)
		variance = [self.Compaction1980s[yearday],self.Compaction1990s[yearday],self.Compaction2000s[yearday],self.Compaction2010s[yearday]]
		variance_new = np.asarray(variance).astype(np.float32)
		deviation = np.std(variance_new)+1
		ymin = max(49,float(self.CSVCompaction[-1])-8*deviation)
		ymax = min(96,float(self.CSVCompaction[-1])+8*deviation)
		plt.axis([(self.month-2.5)*30.5+self.day,self.day+(self.month)*30.5,ymin,ymax])
		
		
		#ymin = 55
		#ymax = 96
		#plt.axis([0,365,ymin,ymax])
		
		
		legend = plt.legend(loc=4, shadow=True, fontsize='medium')
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.subplots_adjust(bottom=0.06)
		fig.savefig('X:/Upload/Arctic_Graph_Compaction.png')

			
	def writetofile(self):
		
		with open('X:/Upload/AreaData/Arctic_NSIDC_Area_NRT_'+str(self.year)+'.csv', "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for writeing in range(0,len(self.CSVArea)):
				writer.writerow([self.CSVDatum[writeing],self.CSVArea[writeing],self.CSVExtent[writeing],self.CSVCompaction[writeing]])	
	
	def loadCSVdata (self):
		
		#NRT Data
		Yearcolnames = ['Date', 'Area', 'Extent','Compaction']
		Yeardata = pandas.read_csv('X:/Upload/AreaData/Arctic_NSIDC_Area_NRT_'+str(self.year)+'.csv', names=Yearcolnames)
		self.CSVDatum = Yeardata.Date.tolist()
		self.CSVArea = Yeardata.Area.tolist()
		self.CSVExtent = Yeardata.Extent.tolist()
		self.CSVCompaction = Yeardata.Compaction.tolist()
		
		del self.CSVDatum[-(self.daycount-1):]
		del self.CSVArea[-(self.daycount-1):]
		del self.CSVExtent[- (self.daycount-1):]
		del self.CSVCompaction[- (self.daycount-1):]
		
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
		
		#Compaction Data
		Compactioncolnames = ['Date','C1980s','C1990s','C2000s','C2010s','C2007', 'C2008', 'C2009', 'C2010', 'C2011', 'C2012', 'C2013', 'C2014', 'C2015', 'C2016', 'C2017']
		Compactiondata = pandas.read_csv('X:/Upload/AreaData/Arctic_climate_compaction.csv', names=Compactioncolnames,header=0)
		self.Compaction1980s = Compactiondata.C1980s.tolist()
		self.Compaction1990s = Compactiondata.C1990s.tolist()
		self.Compaction2000s = Compactiondata.C2000s.tolist()
		self.Compaction2010s = Compactiondata.C2010s.tolist()
		self.Compaction2007 = Compactiondata.C2007.tolist()
		self.Compaction2008 = Compactiondata.C2008.tolist()
		self.Compaction2009 = Compactiondata.C2009.tolist()
		self.Compaction2010 = Compactiondata.C2010.tolist()
		self.Compaction2011 = Compactiondata.C2011.tolist()
		self.Compaction2012 = Compactiondata.C2012.tolist()
		self.Compaction2013 = Compactiondata.C2013.tolist()
		self.Compaction2014 = Compactiondata.C2014.tolist()
		self.Compaction2015 = Compactiondata.C2015.tolist()
		self.Compaction2016 = Compactiondata.C2016.tolist()
		self.Compaction2017 = Compactiondata.C2017.tolist()
		#del self.Compaction1980s[0],self.Compaction1990s[0],self.Compaction2000s[0],self.Compaction2010s[0],self.Compaction2007[0],self.Compaction2008[0],self.Compaction2009[0],self.Compaction2010[0],self.Compaction2011[0],self.Compaction2012[0],self.Compaction2013[0],self.Compaction2014[0],self.Compaction2015[0],self.Compaction2016[0]
		
	
	
	def automated (self,day,month,year,daycount):
		
		self.year = year
		self.month = month
		self.day = day
		
		self.daycount = daycount
		self.loadCSVdata()
		self.dayloop()
		self.writetofile()
		self.makegraph()
		self.makegraph_full()
		self.makegraph_compaction()

action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	#action.loadCSVdata()
	#action.dayloop()
	action.automated(1,1,2018,156) #note substract xxx days from last available day
	#action.makegraph()
	#action.makegraph_compaction()

'''
Values are coded as follows:
0-250  concentration
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
12: Chuckhi Sea
13:Beaufort Sea
14: Canadian Achipelago
15: Central Arctic
20: Land
21: Coast
'''