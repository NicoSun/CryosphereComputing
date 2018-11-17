import numpy as np
import os
from datetime import date
from datetime import timedelta

class NSIDC_Filler:

	def __init__  (self):
		self.start = date(1987,12, 2)
		self.year = self.start.year
		self.month = self.start.month
		self.day = self.start.day
		
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
		
		self.daycount = 42 #366year, 186summer
		###Missing:1987-12-03 to 1988-01-12
		
		
	def dayloop(self):
		self.loopday	= self.start
			
		for count in range (0,self.daycount,1): 
			filepath = 'DataFiles/'	
			filename = 'NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
		
			try:
				with open(os.path.join(filepath,filename), 'rb') as fr:
					ice = np.fromfile(fr, dtype=np.uint8)
			except FileNotFoundError:
			
			
				filenamePlus1 = 'NSIDC_{}.bin'.format(self.calcday(1))
				filenameMinus1 = 'NSIDC_{}.bin'.format(self.calcday(-1))
				
				
				with open(os.path.join(filepath,filenamePlus1), 'rb') as fr:
					iceP1 = np.fromfile(fr, dtype=np.uint8)
				
				with open(os.path.join(filepath,filenameMinus1), 'rb') as fr:
					iceM1 = np.fromfile(fr, dtype=np.uint8)
					
				iceP1 = np.array(iceP1, dtype=float)
				iceM1 = np.array(iceM1, dtype=float)
				
				ice = np.add(iceP1 , iceM1) *0.5
				
				with open(os.path.join('DataFiles/',filename), 'wb') as wr:
					wr.write(ice)
			
			except Exception as e:
				print(e)
				
			print('{}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
			self.advanceday(1)
			
	def advanceday(self,delta):	
		self.loopday = self.loopday+timedelta(days=delta)
		self.year = self.loopday.year
		self.month = self.loopday.month
		self.day = self.loopday.day
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
		return '{}{}{}'.format(self.year,self.stringmonth,self.stringday)
		
	def calcday(self,delta):	
		loopday = self.loopday+timedelta(days=delta)
		year = loopday.year
		month = loopday.month
		day = loopday.day
		stringmonth = str(month).zfill(2)
		stringday = str(day).zfill(2)
		return '{}{}{}'.format(year,stringmonth,stringday)
	
	def longgap(self,filepath,count):
		
		filenamePlus1 = 'NSIDC_19880113.bin'
		filenameMinus1 = 'NSIDC_19871202.bin'
				
				
		with open(os.path.join(filepath,filenamePlus1), 'rb') as fr:
			iceP1 = np.fromfile(fr, dtype=np.uint8)
				
		with open(os.path.join(filepath,filenameMinus1), 'rb') as fr:
			iceM1 = np.fromfile(fr, dtype=np.uint8)
		
		ice = np.zeros(136192)
		for x in range (0,136192):
			ice[x] = iceM1[x]+(iceP1[x]-iceM1[x])/(self.daycount/(count+1))

		ice = np.array(ice,dtype=np.uint8)
		return ice
		

	def gapyear(self):
		self.year = 2001
		self.month = 2
		self.day = 29
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
			
		filepath = 'DataFiles/'	
		filename = 'NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
		
		filenamePlus1 = 'NSIDC_{}0301.bin'.format(self.year)
		filenameMinus1 = 'NSIDC_{}0228.bin'.format(self.year)
		with open(os.path.join(filepath,filenamePlus1), 'rb') as fr:
			iceP1 = np.fromfile(fr, dtype=np.uint8)
				
		with open(os.path.join(filepath,filenameMinus1), 'rb') as fr:
			iceM1 = np.fromfile(fr, dtype=np.uint8)
					
		iceP1 = np.array(iceP1, dtype=float)
		iceM1 = np.array(iceM1, dtype=float)
				
		ice = np.add(iceP1 , iceM1) *0.5
		ice = np.array(ice, dtype=np.uint8) 
			
		with open(os.path.join(filepath,filename), 'wb') as wr:
			wr.write(ice)
			
				
		print('{}-{}-{}'.format(self.year,self.stringmonth,self.stringday))	

action = NSIDC_Filler()
if __name__ == "__main__":
	print('main')
#	action.dayloop()
	action.gapyear()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA