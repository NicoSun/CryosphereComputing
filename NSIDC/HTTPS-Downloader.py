import multiprocessing
import requests
import numpy as np
import pandas
import datetime
from datetime import timedelta

import sys
sys.path.append('X:/NSIDC_south')

import Daily_NSIDC_Area
import Daily_NSIDC_Area_Graphs

import Daily_NSIDC_Area_south
import Daily_NSIDC_Area_south_Graphs

import Arctic_Daily_AWP
#import Daily_AWP_anomaly_south_MJ



class Downloader:

	def __init__  (self):
		self.year = 2017
		self.month = 1
		self.day = 30
		self.daycount = 4
			
		self.start = datetime.date.today()
		self.today = self.start
		self.year = self.today.year
		self.stringmonth = str(self.today.month).zfill(2)
		self.stringday = str(self.today.day).zfill(2)
		
		Columns = ['hole']
		csvdata = pandas.read_csv('Tools/2008_polehole.csv', names=Columns,dtype=int)
		self.icepole = csvdata.hole.tolist()
		 		
		Columns = ['edge']
		csvdata = pandas.read_csv('Tools/2008_poleholeedge.csv', names=Columns,dtype=int)
		self.icepoleedge = csvdata.edge.tolist()
		


	def dayloop(self):
		self.mysession=requests.Session()
		self.getday(self.daycount)
		for count in range (0,self.daycount,1): #372
			newfilename =  'X:/NSIDC/DataFiles/NSIDC_{}{}{}.bin'.format(self.year,self.stringmonth,self.stringday)
			newfilename_south =  'X:/NSIDC_south/DataFiles/NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
			#newfilenametrue = 'X:/NSIDC/DataFiles/NSIDC_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.bin'

			print(newfilename)
			self.download(newfilename,newfilename_south)
			self.format(newfilename,newfilename_south)
			
			self.today = self.today+timedelta(days=1)
			self.year = self.today.year
			self.stringmonth = str(self.today.month).zfill(2)
			self.stringday = str(self.today.day).zfill(2)


	def download(self,newfilename,newfilename_south):
		
		url = 'https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0081_nrt_nasateam_seaice/north/nt_{}{}{}_f18_nrt_n.bin'.format(self.year,self.stringmonth,self.stringday)
		url_south = 'https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0081_nrt_nasateam_seaice/south/nt_{}{}{}_f18_nrt_s.bin'.format(self.year,self.stringmonth,self.stringday)
		
		# get the requested data, note that the auth. Login credentials have to be in .netrc file
		res = self.mysession.get(url)
		res_south = self.mysession.get(url_south)

		# save the results
		with open(newfilename,"wb") as fd:
			fd.write(res.content)
			
		with open(newfilename_south,"wb") as fd:
			fd.write(res_south.content)
		print(self.stringday,self.stringmonth)
		
			
	def format(self, newfilename,newfilename_south):
	
		try:
			with open(newfilename, 'rb') as fr:
				hdr = fr.read(300)
				ice = np.fromfile(fr, dtype=np.uint8)
		
			
			icepolecon = []
			for val in self.icepoleedge:
				icepolecon.append (ice[val])
				
			icepolecon = np.mean(icepolecon)
			
			for val2 in self.icepole:
				ice[val2] = icepolecon
			
		
			with open(newfilename, 'wb') as frr:
				icewr = frr.write(ice)
		except:
			print('no data')
			
		#southern hemisphere	
		try:
			with open(newfilename_south, 'rb') as fr:
				hdr = fr.read(300)
				ice2 = np.fromfile(fr, dtype=np.uint8)
	
			with open(newfilename_south, 'wb') as fff:
				icewr = fff.write(ice2)
		except:
			print('no data')
		
		
		
	def getday(self, daycount):
	
		self.today = self.start-timedelta(days=daycount)
		self.year = self.today.year
		self.stringmonth = str(self.today.month).zfill(2)
		self.stringday = str(self.today.day).zfill(2)
		print('getday','{}{}{}'.format(self.year ,self.stringmonth,self.stringday))
		
	def Areacalc(self):
		self.getday(self.daycount)
		Daily_NSIDC_Area.action.automated(self.today.day,self.today.month,self.year,self.daycount)
		self.getday(1)
		Daily_NSIDC_Area_Graphs.action.automated(self.stringday,self.stringmonth,self.year)
		
	def Areacalc_south(self):
		self.getday(self.daycount)
		Daily_NSIDC_Area_south.action.automated(self.today.day,self.today.month,self.year,self.daycount)
		self.getday(1)
		Daily_NSIDC_Area_south_Graphs.action.automated(self.stringday,self.stringmonth,self.year)
		
		
	def AWPcalc_north(self):
		self.getday(1)
		Arctic_Daily_AWP.action.automated(self.year,self.stringmonth,self.stringday)
		
# =============================================================================
# 	def AWPcalc_south(self):
# 		self.getday(1)
# 		Daily_AWP_anomaly_south_MJ.action.automated(self.year,self.stringmonth,self.stringday)
# =============================================================================
		
		
		

action = Downloader()
#action.AWPcalc_north()

if __name__ == '__main__':		
#	print('fff')
	action.dayloop()
	p = multiprocessing.Process(target=action.Areacalc())
	q = multiprocessing.Process(target=action.Areacalc_south())
	r = multiprocessing.Process(target=action.AWPcalc_north())
#	s = multiprocessing.Process(target=action.AWPcalc_south())
	p.start()
	q.start()
	r.start()
#	s.start()
