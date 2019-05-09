import numpy as np
import os
from datetime import date
from datetime import timedelta

class ADS_Filler:

	def __init__  (self):
		self.start = date(2018, 5, 31)
		self.year = self.start.year
		self.month = self.start.month
		self.day = self.start.day
		
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
		
		self.daycount = 5 #366year, 186summer
		
	def dayloop(self):
		self.loopday	= self.start
			
		for count in range (0,self.daycount,1): 
			filepath = 'DataFiles/'	
			filename = 'ADS_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday)
		
			try:
				with open(os.path.join(filepath,filename), 'rb') as fr:
					ice = np.fromfile(fr, dtype=np.uint8)
			except FileNotFoundError:
			
			
				filenamePlus1 = 'ADS_SIT_{}.dat'.format(self.calcday(1))
				
				
				filenameMinus1 = 'ADS_SIT_{}.dat'.format(self.calcday(-1))
				
				
				with open(os.path.join(filepath,filenamePlus1), 'rb') as fr:
					iceP1 = np.fromfile(fr, dtype=np.uint8)
				
				with open(os.path.join(filepath,filenameMinus1), 'rb') as fr:
					iceM1 = np.fromfile(fr, dtype=np.uint8)
					
				iceP1 = np.array(iceP1, dtype=float)
				iceM1 = np.array(iceM1, dtype=float)
				
				ice = np.add(iceP1 , iceM1) *0.5
				ice = np.array(ice, dtype=np.uint8) 
			
				with open(os.path.join('DataFiles/',filename), 'wb') as write:
						icewr = write.write(ice)
			
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

	def gapyear(self):
		self.year = 2018
		self.month = 2
		self.day = 29
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
			
		filepath = 'DataFiles/'	
		filename = 'ADS_SIT_{}{}{}.dat'.format(self.year,self.stringmonth,self.stringday)
		
		filenamePlus1 = 'ADS_SIT_{}0301.dat'.format(self.year)
		filenameMinus1 = 'ADS_SIT_{}0228.dat'.format(self.year)
		with open(os.path.join(filepath,filenamePlus1), 'rb') as fr:
			iceP1 = np.fromfile(fr, dtype=np.uint8)
				
		with open(os.path.join(filepath,filenameMinus1), 'rb') as fr:
			iceM1 = np.fromfile(fr, dtype=np.uint8)
					
		iceP1 = np.array(iceP1, dtype=float)
		iceM1 = np.array(iceM1, dtype=float)
				
		ice = np.add(iceP1 , iceM1) *0.5
		ice = np.array(ice, dtype=np.uint8) 
			
		with open(os.path.join(filepath,filename), 'wb') as write:
			icewr = write.write(ice)
			
				
		print('{}-{}-{}'.format(self.year,self.stringmonth,self.stringday))	

action = ADS_Filler()
if __name__ == "__main__":
	print('main')
	action.dayloop()
	#action.gapyear()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA