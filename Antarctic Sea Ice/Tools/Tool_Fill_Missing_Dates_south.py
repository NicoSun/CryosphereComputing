import numpy as np
import os
from datetime import date
from datetime import timedelta

class NSIDC_Filler:

	def __init__  (self):
		self.start = date(1987, 12, 3)
		self.year = self.start.year
		self.month = self.start.month
		self.day = self.start.day
		
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
		
		self.daycount = 42 #366year, 186summer
		###Missing:1987-12-03 to 1988-01-12
		
	def dayloop(self):
		self.loopday	= self.start
		
		self.regionmask = 'X:/NSIDC_south/Masks/region_s_pure.msk'
		with open(self.regionmask, 'rb') as frmsk:
			self.regionmask = np.fromfile(frmsk, dtype=np.uint8)
		self.regionmask = np.array(self.regionmask, dtype=float)
			
		for count in range (0,self.daycount,1): 
			filepath = 'DataFiles/'	
			filename = 'NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
		
# =============================================================================
# 			#longgap_code
# 			ice = self.longgap(filepath,count)
# 			with open(os.path.join('DataFiles/',filename), 'wb') as write:
# 				write.write(ice)
# =============================================================================
		
			try:
				with open(os.path.join(filepath,filename), 'rb') as fr:
					ice = np.fromfile(fr, dtype=np.uint8)
			except FileNotFoundError:
			
				filenamePlus1 = 'NSIDC_{}_south.bin'.format(self.calcday(1))
				filenameMinus1 = 'NSIDC_{}_south.bin'.format(self.calcday(-1))
				
				with open(os.path.join(filepath,filenamePlus1), 'rb') as fr:
					iceP1 = np.fromfile(fr, dtype=np.uint8)
				
				with open(os.path.join(filepath,filenameMinus1), 'rb') as fr:
					iceM1 = np.fromfile(fr, dtype=np.uint8)
					
				iceP1 = np.array(iceP1, dtype=float)
				iceM1 = np.array(iceM1, dtype=float)
				
				ice = np.add(iceP1 , iceM1) *0.5
				ice = np.array(ice, dtype=np.uint8)
	
				with open(os.path.join('DataFiles/',filename), 'wb') as write:
					write.write(ice)

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
		
		filenamePlus1 = 'NSIDC_19880114_south.bin'
		filenameMinus1 = 'NSIDC_19871202_south.bin'
				
				
		with open(os.path.join(filepath,filenamePlus1), 'rb') as fr:
			iceP1 = np.fromfile(fr, dtype=np.uint8)
			iceP1 = np.array(iceP1,dtype=float)
				
		with open(os.path.join(filepath,filenameMinus1), 'rb') as fr:
			iceM1 = np.fromfile(fr, dtype=np.uint8)
			iceM1 = np.array(iceM1,dtype=float)
		
		ice = np.zeros(len(iceP1),dtype=float)
		for x in range (0,len(iceP1)):
			if self.regionmask[x] < 10:
				ice[x] = iceM1[x]+(iceP1[x]-iceM1[x])*((count)/(self.daycount))
			elif self.regionmask[x] > 9:
				ice[x] = 255

		ice = np.array(ice,dtype=np.uint8)
		return ice

	def gapyear(self):
		self.year = 1991
		self.month = 2
		self.day = 29
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
			
		filepath = 'DataFiles/'	
		filename = 'NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
		
		filenamePlus1 = 'NSIDC_{}0301_south.bin'.format(self.year)
		filenameMinus1 = 'NSIDC_{}0228_south.bin'.format(self.year)
		with open(os.path.join(filepath,filenamePlus1), 'rb') as fr:
			iceP1 = np.fromfile(fr, dtype=np.uint8)
				
		with open(os.path.join(filepath,filenameMinus1), 'rb') as fr:
			iceM1 = np.fromfile(fr, dtype=np.uint8)
					
		iceP1 = np.array(iceP1, dtype=float)
		iceM1 = np.array(iceM1, dtype=float)
				
		ice = np.add(iceP1 , iceM1) *0.5
		ice = np.array(ice, dtype=np.uint8) 
			
		with open(os.path.join(filepath,filename), 'wb') as write:
			write.write(ice)
			
				
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