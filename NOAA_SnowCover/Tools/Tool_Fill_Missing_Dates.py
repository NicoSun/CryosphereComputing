import numpy as np
import os


class NOAA_Filler:

	def __init__  (self):
		self.year = 2017
		self.daycount = 366
		
	def dayloop(self):
			
		for day_of_year in range (1,self.daycount): 
			filename = 'DataFiles/NOAA_{}{}_24km.bin'.format(self.year,str(day_of_year).zfill(3))
#			print(filename)
		
			try:
				with open(filename, 'rb') as fr:
					ice = np.fromfile(fr, dtype=np.uint8)
			except FileNotFoundError:
			
				filenameMinus1 = 'DataFiles/NOAA_{}{}_24km.bin'.format(self.year,str(day_of_year-1).zfill(3))
				
				with open(filenameMinus1,'rb') as fr:
					iceM1 = np.fromfile(fr, dtype=np.uint8)
						
				with open(os.path.join(filename), 'wb') as writer:
					writer.write(iceM1)
			
			except Exception as e:
				print(e)
				
			print('{}-{}'.format(self.year,str(day_of_year).zfill(3)))


action = NOAA_Filler()
if __name__ == "__main__":
	print('main')
	action.dayloop()
	#action.gapyear()