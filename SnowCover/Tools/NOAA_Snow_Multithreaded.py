'''
NOAA Daily Snow Extent / Ice Extent Data


array size: 247500 (550:450)
'''
from multiprocessing import Pool
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import csv

class NOAA_Snow_Cover:


	def __init__  (self):
		self.year = 2019
		self.daycount = 366 #366 year,39 years
		self.day_of_year = 1
		
		self.threads = 16
		
		self.plottype = 'daily' # daily ,  mask
		self.dailyorcumu()
		self.masksload()
		self.mode = 'Mean'
		
		self.CSVDatum = ['Date']
		self.IceExtent = ['IceExtent']
		self.NorthAmericaExtent =['NorthAmericaExtent']
		self.GreenlandExtent =['GreenlandExtent']
		self.EuropeExtent =['EuropeExtent']
		self.AsiaExtent =['AsiaExtent']
		
		self.SnowExtent_anom = ['SnowExtent Anomaly']
		self.IceExtent_anom = ['IceExtent Anomaly']
		
	def masksload(self):
	
		filename = 'Masks/Region_Mask.msk'
		with open(filename, 'rb') as fr:
			self.regionmask = np.fromfile(fr, dtype='uint8')
		filename = 'Masks/Pixel_area_crop.msk'
		with open(filename, 'rb') as fr:
			self.pixelarea = np.fromfile(fr, dtype='uint16')
		
		
		filename = 'Masks/Latitude_Mask.msk'
		with open(filename, 'rb') as fr:
			self.Latitude_Mask = np.fromfile(fr, dtype='float32')


#		self.maskview(self.pixelarea)
#		plt.show()
			


	def viewloop(self):
		for day_of_year in range (1,366): #366
#			filename = 'DataFiles/NOAA_{}{}_24km.bin'.format(self.year,str(day_of_year).zfill(3))
#			filename = 'DataFiles/Mean/NOAA_Mean_{}_24km.bin'.format(str(day_of_year).zfill(3))
			filename = 'DataFiles/Max/NOAA_Max_{}_24km.bin'.format(str(day_of_year).zfill(3))
			with open(filename, 'rb') as fr:
				snow = np.fromfile(fr, dtype='uint8')
			self.dailyview(snow,day_of_year)
		plt.show()
		
		
	def dayloop(self):
		filename_list = []
		filename_listmean = []
		for self.year in range(1998,2005):
			for day_of_year in range (1,366): #366
				stringday = str(day_of_year).zfill(3)
				filenameMean = 'DataFiles/Mean/NOAA_Mean_{}_24km.bin'.format(stringday)
				filename = 'DataFiles/Max/NOAA_Max_{}_24km.bin'.format(str(day_of_year).zfill(3))
#				filename = 'Datafiles/NOAA_{}{}_24km.bin'.format(self.year,stringday)
				filename_list.append(filename)
				filename_listmean.append(filenameMean)
				self.CSVDatum.append('{}_{}'.format(self.year,stringday))
			
			
			
#		print(filename_list)
		p = Pool(processes=self.threads)
		data = p.map(self.threaded, filename_list)
		p.close()
		
		for value in data:
			self.IceExtent.append (value[0]/1e6)
			self.NorthAmericaExtent.append (value[1]/1e6)
			self.GreenlandExtent.append (value[2]/1e6)
			self.EuropeExtent.append (value[3]/1e6)
			self.AsiaExtent.append (value[4]/1e6)

			
	def threaded(self,filename):
		
#		with open(filenameMean, 'rb') as fr:
#				snowMean = np.fromfile(fr, dtype=np.float16)
		with open(filename, 'rb') as fr:
			snow = np.fromfile(fr, dtype='uint8')
#		snowMean = np.array(snowMean,dtype=np.float)
#		snow = np.array(snow,dtype=np.float)
			
			
		aaa = np.vectorize(self.calculateExtent)
		iceextent,NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent = aaa(snow,self.regionmask,self.pixelarea)

		return np.sum(iceextent),np.sum(NorthAmericaExtent),np.sum(GreenlandExtent),np.sum(EuropeExtent),np.sum(AsiaExtent)
		

	def calculateExtent(self,icemap,regionmask,pixelarea):
		iceextent = 0
		NorthAmericaExtent = 0
		GreenlandExtent = 0
		EuropeExtent = 0
		AsiaExtent = 0
#		iceanomaly = icemap-icemean
		
		if icemap==3:
			iceextent = pixelarea
		if regionmask==3 and icemap==4:
			NorthAmericaExtent = pixelarea
		if regionmask==4 and icemap==4:
			GreenlandExtent = pixelarea
		if regionmask==5 and icemap==4:
			EuropeExtent = pixelarea
		if regionmask==6 and icemap==4:
			AsiaExtent = pixelarea
	
		return iceextent,NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent
		
		
	def dailyview(self,snowmap,day_of_year):
		snowmap = snowmap.reshape(610,450)
		
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		
		self.ax.clear()
		self.ax.set_title('Year '+str(self.year)+'   Day '+str(day_of_year).zfill(3),x=0.15)
		self.ax.set_xlabel('NOAA: Snow / Ice Extent')
#		self.cax = self.ax.imshow(snowmap, interpolation='nearest', vmin=-25, vmax=25, cmap=cmap)
		self.cax = self.ax.imshow(snowmap, interpolation='nearest', vmin=0, vmax=4, cmap=cmap)
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		plt.tight_layout(pad=1)
#		self.fig.savefig(self.mode)
		plt.pause(0.01)
		
		
	def maskview(self,snowmap):		
		snowmap = snowmap.reshape(610,450)
		fig = plt.figure(figsize=(4.5, 5.5))
		ax = fig.add_subplot(111)
		
		ax.imshow(snowmap, interpolation='nearest')
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.axis('off')
		ax.set_position([0, 0, 1, 1])
#		fig.savefig('Landmask.png',bbox_inches=0)
		
		
	def dailyorcumu(self):		
		self.icenull = np.zeros(247500, dtype=float)
		self.icenull = self.icenull.reshape(550, 450)
		
		if self.plottype == 'daily':
			self.fig, self.ax = plt.subplots(figsize=(8, 10))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=1,cmap = plt.cm.jet)
#			self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Ice concentration in %')
#			self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Ice concentration in %')
#			self.title = self.fig.suptitle('Concentration Map', fontsize=14, fontweight='bold',x=0.175)
			
		if self.plottype == 'mask':
			self.fig, self.ax = plt.subplots(figsize=(8, 10))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest')
			#self.cbar = self.fig.colorbar(self.cax).set_label('stuff')
#			self.title = self.fig.suptitle('Mask', fontsize=14, fontweight='bold')
			
	def writetofile(self):
		with open('_NOAA_snow_Cover_multithread2.csv', "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for x in range(0,len(self.IceExtent)):
				writer.writerow([self.CSVDatum[x],self.IceExtent[x],self.NorthAmericaExtent[x],self.GreenlandExtent[x],self.EuropeExtent[x],self.AsiaExtent[x]])

			
		
		
if __name__ == "__main__":
	action = NOAA_Snow_Cover()
#	action.viewloop()
#	action.masksload()
	action.dayloop()
	action.writetofile()
#	