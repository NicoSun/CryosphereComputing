import numpy as np
import numpy.ma as ma
import pandas
import csv
import matplotlib.pyplot as plt
import os



class NSIDC_area:

	def __init__  (self):
		self.year = 2000
		self.month = 1
		self.day = 1
		
		self.daycount = 10 #366year, 186summer
		
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
		'''Loads regionmask and pixel area mask
		option to display masks is commented out
		'''
		regionmaskfile = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		with open(regionmaskfile, 'rb') as frmsk:
				mask = np.fromfile(frmsk, dtype=np.uint32)
		self.regmaskf = np.array(mask)
		
		areamaskfile = 'X:/NSIDC/Masks/psn25area_v3.dat'
		with open(areamaskfile, 'rb') as famsk:
				mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(mask2, dtype=float)/1000
		
#		self.maskview(self.regmaskf)
#		plt.show()
		
		
	def dayloop(self):
		'''for loop to load binary data files and pass them to the calculation function
		'''
		filepath = 'X:/NSIDC/DataFiles/'
		for count in range (0,self.daycount,1):
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			filename = 'NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
#			filenameMax = 'Max/NSIDC_Max_{}{}.bin'.format(self.stringmonth,self.stringday)
#			filenameMin = 'Min/NSIDC_Min_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenamedav = 'Daily_Mean/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)	
			
			
			try:
				#loads data file
				with open(os.path.join(filepath,filename), 'rb') as fr:
					ice = np.fromfile(fr, dtype=np.uint8)
					icef = np.array(ice, dtype=float)/250
			except:
				#exception if date is unavailable
				self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
				self.CSVArea.append('N/A')			
				self.CSVExtent.append ('N/A')
				self.CSVCompaction.append ('N/A')
				break
			
			# loads the mean data file
			with open(os.path.join(filepath,filenamedav), 'rb') as frr:
				iceaverage = np.fromfile(frr, dtype=np.uint8)
				iceaveragef = np.array(iceaverage, dtype=float)/250
		
				#area & extent calculation
				aaa = np.vectorize(self.calculateAreaExtent)
				icemap_new,icemapanomaly,area,extent,areaanomaly = aaa(icef,iceaveragef,self.areamaskf,self.regmaskf)
			

				self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
				self.CSVArea.append((np.sum(area))/1e6)
				self.CSVExtent.append (np.sum(extent)/1e6)
				self.CSVCompaction.append((np.sum(area)/np.sum(extent))*100)
			
				area_anom = np.sum(areaanomaly)/1e6

				if count == (self.daycount-1):
					self.normalshow(icemap_new,self.CSVArea[-1])
					self.anomalyshow(icemapanomaly,area_anom)
			
			count += 1
			if count < self.daycount:
				self.datecalc()
				
				
	def datecalc(self):
		''' calculates the day-month for a 366 day year'''
		self.day = self.day+1
		if self.day==32 and (self.month==1 or self.month==3 or self.month==5 or self.month==7 or self.month==8 or self.month==10):
			self.day=1
			self.month = self.month+1
		elif self.day==31 and (self.month==4 or self.month==6 or self.month==9 or self.month==11):
			self.day=1
			self.month = self.month+1
		elif self.day==30 and self.month==2:
			self.day=1
			self.month = self.month+1
		elif  self.day==32 and self.month == 12:
			self.day = 1
			self.month = 1
			self.year = self.year+1
					
	def calculateAreaExtent(self,icemap,iceaveragef,areamask,regionmask):
		'''area & extent calculation & remove lake ice'''
		area = 0
		extent = 0
		icemap_new = icemap
		icemapanomaly = icemap - iceaveragef
		areaanomaly = 0
		
		if regionmask < 2:
			icemap_new = 0.0
			icemapanomaly = 0.0
		if 1 < regionmask < 16:
			if 0.15 <= icemap <=1:
				area = icemap*areamask
				extent = areamask
		if regionmask > 16:
			icemapanomaly = 5
		if icemap <=1 and icemapanomaly <=1:
				areaanomaly = icemapanomaly*areamask
				
		return icemap_new,icemapanomaly,area,extent,areaanomaly
		
	def maskview(self,icemap):
		'''displays loaded masks'''
		icemap = icemap.reshape(448, 304)
		plt.imshow(icemap, interpolation='nearest', vmin=0, vmax=16, cmap=plt.cm.jet)


	def normalshow(self,icemap,icesum):
		'''displays sea ice data'''
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
		'''creates separate figures for sea ice data'''
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
		'''creates separate figures for sea ice data'''
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

			
	def writetofile(self):
		'''writes data to a csv file'''
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