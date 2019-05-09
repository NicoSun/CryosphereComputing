import numpy as np
import pandas
import csv
import matplotlib.pyplot as plt
import os



class NSIDC_area_south:

	def __init__  (self):
		self.year = 2017
		self.month = 1
		self.day = 1
		
		self.daycount = 366 #366year, 183summer
		
		self.name = 'MinimumofMinima' #MinimumofMinima MaximumofMaxima
		self.CSVDatum = ['Date']
		self.CSVArea =['Area']
		self.CSVExtent = ['Extent']
		self.CSVCompaction = ['Compaction']
		
		self.tarea_anom = ['Area Anomaly']
		self.textent_anom = ['Extent Anomaly']
		
		self.masksload()
		self.normalandanomaly()
		
		
		
		
	def masksload(self):
		'''Loads regionmask and pixel area mask
		option to display masks is commented out
		'''
		regionmaskfile = 'X:/NSIDC_south/Masks/region_s_pure.msk'
		with open(regionmaskfile, 'rb') as frmsk:
				mask = np.fromfile(frmsk, dtype=np.uint8)
		self.regmaskf = np.array(mask)
		
		areamaskfile = 'X:/NSIDC_south/Masks/pss25area_v3.dat'
		with open(areamaskfile, 'rb') as famsk:
				mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(mask2, dtype=float)/1000
		
#		self.maskview(self.areamaskf)
#		plt.show()
		
		
	def dayloop(self):
		'''for loop to load binary data files and pass them to the calculation function
		'''
		filepath = 'X:/NSIDC_south/DataFiles/'
		for count in range (0,self.daycount,1):
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			filename = 'NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
#			filenameMax = 'Max/NSIDC_Max_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenameMin = 'Minimum/NSIDC_Min_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filenameMean = 'Daily_Mean/NSIDC_Mean_{}{}_south.bin'.format(self.stringmonth,self.stringday)	
			
			
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
			with open(os.path.join(filepath,filenameMean), 'rb') as frr:
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

#			if count == (self.daycount-1):
#			self.normalshow(icemap_new,self.CSVArea[-1])
#			self.anomalyshow(icemapanomaly,area_anom)
			print(count)
			if count < self.daycount:
				self.datecalc()
		plt.show()
				
				
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
		areaanomaly = 0
		icemapanomaly = 1.1
		
		if regionmask < 10:
			icemapanomaly = icemap - iceaveragef
			if 0.15 <= icemap <=1:
				area = icemap*areamask
				extent = areamask
			if icemap > 1:
				icemapanomaly = 1.1
			if icemap <=1 and icemapanomaly <=1:
					areaanomaly = icemapanomaly*areamask
				
		return icemap_new,icemapanomaly,area,extent,areaanomaly
		
	def maskview(self,icemap):
		'''displays loaded masks'''
		icemap = icemap.reshape(332, 316)
		plt.imshow(icemap, interpolation='nearest', vmin=0, vmax=10, cmap=plt.cm.jet)

				

	def normalshow(self,icemap,icesum):		
		icemap = np.ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(332, 316)
		icesum = round(icesum,3)
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		self.ax.clear()
		self.ax.set_title('Minimum of Minima') #Maximum of Maxima, Minimum of Minima
#		self.ax.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
		self.ax.set_xlabel('Area: '+str(icesum)+' million km2', fontsize=14)
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=1,cmap=cmap)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 8, r'Data: NSIDC', fontsize=10,color='white',fontweight='bold')
		self.ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.fig.tight_layout(pad=1)
		#self.fig.savefig('Animation/MaxofMax'+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		plt.pause(0.01)
		
	def anomalyshow(self,icemap,icesum):		
		icemap = icemap.reshape(332, 316)
		icesum = round(icesum,3)
		self.ax2.clear()
		self.ax2.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
		cmap2 = plt.cm.coolwarm_r
		cmap2.set_bad('black',0.6)
		self.ax2.set_xlabel('Area: '+str(icesum)+' million km2', fontsize=14)
		self.cax = self.ax2.imshow(icemap, interpolation='nearest', vmin=-0.75, vmax=0.75, cmap=cmap2)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 8, r'Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 18, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.fig2.tight_layout(pad=1)
		#self.fig2.savefig('Animation/MaxofMax_anom'+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		plt.pause(0.01)	
		
	def normalandanomaly(self):		
		self.icenull = np.zeros(104912, dtype=float)
		self.icenull = self.icenull.reshape(332, 316)
		

		self.fig, self.ax = plt.subplots(figsize=(8,8))
		self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=100,cmap = plt.cm.jet)
		self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Sea Ice concentration in %')
		#self.title = self.fig.suptitle('Antarctic Maximum of Maxima', fontsize=14, fontweight='bold', x=0.45)
		self.title = self.fig.suptitle('Antarctic Sea Ice Concentration', fontsize=14, fontweight='bold', x=0.45)

# =============================================================================
# 		self.fig2, self.ax2 = plt.subplots(figsize=(8,8))
# 		self.cax = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=-75, vmax=75, cmap=plt.cm.coolwarm_r)
# 		self.cbar = self.fig2.colorbar(self.cax, ticks=[-75,-50,-25,0,25,50,75]).set_label('Sea Ice concentration anomaly in %')
# 		#self.title = self.fig2.suptitle('Antarctic Sea Ice Concentration Anomaly', fontsize=14, fontweight='bold', x=0.4)
# =============================================================================
		
			
		
	def writetofile(self):
		filename = str(self.year-1) # self.name
		try:
			with open(filename+'.csv','w') as output: 
				writer = csv.writer(output, lineterminator='\n') #str(self.year)
				for writeing in range(0,len(self.CSVArea)):
					writer.writerow([self.CSVDatum[writeing],self.CSVArea[writeing],self.CSVExtent[writeing],self.CSVCompaction[writeing]])
				
		except Exception as e:
			print(str(e))
	

	def loadCSVdata (self):
		
		Yearcolnames = ['Date', 'Area', 'Extent']
		Yeardata = pandas.read_csv('D:/CryoComputing/CC_upload/AreaData/Antarctic_NSIDC_Area_NRT_2017.csv', names=Yearcolnames)
		self.CSVDatum = Yeardata.Date.tolist()
		self.CSVArea = Yeardata.Area.tolist()
		self.CSVExtent = Yeardata.Extent.tolist()
		del self.CSVDatum[-(self.daycount-1):]
		del self.CSVArea[-(self.daycount-1):]
		del self.CSVExtent[- (self.daycount-1):]
		
		Climatecolnames = ['Date','Average', 'C1986', 'C1993' ,'C2006','C2007', 'C2008', 'C2009', 'C2010',
		'C2011', 'C2012', 'C2013', 'C2014', 'C2015', 'C2016']
		Climatedata = pandas.read_csv('D:/CryoComputing/CC_upload/AreaData/Antarctic_climate.csv', names=Climatecolnames)
		
		self.C1986= Climatedata.C1986.tolist()
		self.C1993 = Climatedata.C1993.tolist()
		self.C2006 = Climatedata.C2006.tolist()
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
		
		del self.C1986[0],self.C1993[0],self.C2006[0],self.C2013[0],self.C2014[0],self.C2015[0],self.C2016[0]
		
	
	def automated (self,day,month,year):
		
		self.mode = 'man'
	
		self.year = year
		self.month = month
		self.day = day
		
		self.daycount = 366
		
		self.loadCSVdata()
		self.dayloop()
		self.writetofile()


		
action = NSIDC_area_south()
if __name__ == "__main__":
	print('main')
	#action.automated(1,1,2017)
	#action.loadCSVdata()
	action.dayloop()
	action.writetofile()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA