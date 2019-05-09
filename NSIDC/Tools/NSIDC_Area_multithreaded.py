from multiprocessing import Pool
import numpy as np
import csv
import os
import time



class NSIDC_area:

	def __init__  (self):
		self.year = 1979
		self.month = 1
		self.day = 1
		
		self.daycount = 366#366*39 #366year
		self.threads = 15
		
		self.CSVDatum = ['Date']
		self.CSVArea =['Area']
		self.CSVExtent = ['Extent']
		
		self.tarea_anom = ['Area Anomaly']
		self.textent_anom = ['Extent Anomaly']
		
		self.masksload()


	def masksload(self):
	
		self.regionfile = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		with open(self.regionfile, 'rb') as frmsk:
			self.regionmask = np.fromfile(frmsk, dtype=np.uint32)
		
		self.areamask = 'X:/NSIDC/Masks/psn25area_v3.dat'
		with open(self.areamask, 'rb') as famsk:
				self.mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(self.mask2, dtype=float)
		self.areamaskf = self.areamaskf /1000
		
		
	def calculateAreaExtent(self,icemap,areamask,regionmask):
		area = 0
		extent = 0
#		areaanomaly = 0
		
		if  regionmask < 1:
			icemap = 0
#		iceanomaly = icemap	
		if  1 < regionmask < 16:
#			iceanomaly = icemap-icemean
			if 0.15 <= icemap <=1:
				area = icemap*areamask
				extent = areamask
#			if  iceanomaly <=1 and icemap <=1:
#				areaanomaly = iceanomaly*areamask
	
		return icemap,area,extent
		
	def dayloop(self):
		self.start = time.time()
		self.filepath = 'X:/NSIDC/DataFiles/'	
		filename_list = []
		for count in range (0,self.daycount,1): 
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			
#			filename = 'NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
#			filenamedav = 'Daily_Mean/NSIDC_Mean_{}{}.bin'.format(self.stringmonth,self.stringday)
			filenamedav = 'S:/Temp/Mean_80_{}{}.bin'.format(self.stringmonth,self.stringday)
			
			filename_list.append(filenamedav)

			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			print(self.year,self.month,self.day)
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
					
		p = Pool(processes=self.threads)
		data = p.map(self.threaded, filename_list)
		p.close()
#		print(data)
		
		for x in range(0,len(data)):
			self.CSVArea.append(data[x][0]/1e6)
			self.CSVExtent.append (data[x][1]/1e6)
		
		self.end = time.time()
		self.CSVDatum.append (round(self.end-self.start,3))
		self.CSVArea.append (' seconds ')
		self.CSVExtent.append (str(round((self.end-self.start)/self.daycount,3))+' seconds/day')
		
	def threaded(self,filename):
		
		with open(os.path.join(self.filepath,filename), 'rb') as fr:
			ice = np.fromfile(fr, dtype=np.uint8)
			
#		with open(os.path.join(self.filepath,filenamedav), 'rb') as frr:
#			iceaverage = np.fromfile(frr, dtype=np.uint8)
			
		if len(ice) > 5000:
			icef = np.array(ice, dtype=float)/250
#			iceaveragef = np.array(iceaverage, dtype=float)/250
#			iceanomaly = np.zeros(136192, dtype=float)
		
			area=[]
			extent = []
#			area_anom=[]
			
			aaa = np.vectorize(self.calculateAreaExtent)
			icemap,area,extent = aaa(icef,self.areamaskf,self.regionmask)

		return np.sum(area),np.sum(extent)
		
			
	def writetofile(self):

		with open('_NSIDC_Area_optimized_multithread.csv', "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for x in range(0,len(self.CSVArea)):
				writer.writerow([self.CSVDatum[x],self.CSVArea[x],self.CSVExtent[x]])

action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	action.dayloop()
	action.writetofile()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA

'''
#regionmask
0; Lakes
1: open ocean
2-15: Arctic regions
20: Land
21: coast
'''