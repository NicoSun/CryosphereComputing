"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script creates the Volume and Thickness graphs
"""

import numpy as np
import numpy.ma as ma
import pandas
import csv
import matplotlib.pyplot as plt
from datetime import date
from datetime import timedelta
import time

import ADS_netcdf


class ADS_data:
	def __init__  (self):
		'''ADS object initializing'''
		self.start = date(2012, 7, 3)
		self.year = self.start.year
		
	
	def makeVolumegraph(self):
		'''create volume graph'''
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('AMSR2 Snow & Ice Volume', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,30,59,90,120,151,181,212,243,273,304,334] # 1st Jan is day zero
		plt.xticks(x,labels)

		ax.text(5, 1000, r'Raw Data: JAXA / Arctic Data archieve System (ADS)', fontsize=10,color='black',fontweight='bold')
		ax.text(5, 400, r'Graph & Melt-Algorithm: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_ylabel('Sea Ice Volume in 'r'$km^3$')
		major_ticks = np.arange(0, 30000, 2500)
		ax.set_yticks(major_ticks)   

		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.month,self.day),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.8, -0.06, 'cryospherecomputing.tk/SIT',
        transform=ax.transAxes,
        color='grey', fontsize=10)	
   		
		ax.grid(True)
		
		plt.plot( self.VMean, color=(0.5,0.5,0.5),label='Mean',lw=2,ls='--')
		plt.plot( self.V2012, color='orange',label='2012',lw=1)
		plt.plot( self.V2013, color='purple',label='2013',lw=1)
		plt.plot( self.V2014, color='blue',label='2014',lw=1)
		#plt.plot( self.V2015, color='green',label='2015',lw=1)
		plt.plot( self.V2016, color='grey',label='2016',lw=1)
		plt.plot( self.V2017, color='red',label='2017',lw=1)
		plt.plot( self.V2018, color='green',label='2018',lw=1)
		plt.plot( self.V2019, color='black',label='2019',lw=2)
		
		last_value =  int(self.V2019[-1])
		ax.text(0.75, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^3$', fontsize=10,color='black',transform=ax.transAxes)
		
		ymin = 0
		ymax = 25500
		plt.axis([0,365,ymin,ymax])
		plt.legend(loc=4, shadow=True, fontsize='medium')
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.savefig('Upload/AMSR2_Sea_Ice_Volume.png')
		#plt.show()

			
	def makeThicknessgraph(self):
		'''create thickness graph'''
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('AMSR2 Snow & Ice Thickness', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,30,59,90,120,151,181,212,243,273,304,334] # 1st Jan is day zero
		plt.xticks(x,labels)

		ax.text(36, 56, r'Raw Data: JAXA / Arctic Data archieve System (ADS)', fontsize=10,color='black',fontweight='bold')
		ax.text(36, 53, r'Graph & Melt-Algorithm: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_ylabel('Sea Ice Volume in 'r'$km^3$')
		major_ticks = np.arange(0, 30000, 2500)
		ax.set_yticks(major_ticks)   

		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.month,self.day),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.8, -0.06, 'cryospherecomputing.tk/SIT',
        transform=ax.transAxes,
        color='grey', fontsize=10)	
		
		ax.set_ylabel('Sea Ice Thickness in centimetres')
		major_ticks = np.arange(0, 220, 10)
		ax.set_yticks(major_ticks)      		
		ax.grid(True)
		
		plt.plot( self.TMean, color=(0.5,0.5,0.5),label='Mean',lw=2,ls='--')
		plt.plot( self.T2012, color='orange',label='2012',lw=1)
		plt.plot( self.T2013, color='purple',label='2013',lw=1)
		plt.plot( self.T2014, color='blue',label='2014',lw=1)
		#plt.plot( self.T2015, color='green',label='2015',lw=1)
		plt.plot( self.T2016, color='grey',label='2016',lw=1)
		plt.plot( self.T2017, color='red',label='2017',lw=1)
		plt.plot( self.T2018, color='green',label='2018',lw=1)
		plt.plot( self.T2019, color='black',label='2019',lw=2)
		
		last_value =  self.T2019[-1]
		ax.text(0.75, 0.01, 'Last value: {} cm'.format(last_value), fontsize=10,color='black',transform=ax.transAxes)
		
		ymin = 50
		ymax = 192
		plt.axis([0,365,ymin,ymax])
		plt.legend(loc=3, shadow=True, fontsize='medium')
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.savefig('Upload/AMSR2_Sea_Ice_Thickness.png')

	
	def loadCSVdata (self):
		'''loads the graph data from csv files'''
		#Volume Data
		Volumecolnames = ['Date','Mean','C2012', 'C2013', 'C2014', 'C2015', 'C2016', 'C2017', 'C2018', 'C2019']
		Volumedata = pandas.read_csv('Upload/AMSR2_SIT_Volume.csv', names=Volumecolnames,header=0)
		self.VMean = Volumedata.Mean.tolist()
		self.V2012 = Volumedata.C2012.tolist()
		self.V2013 = Volumedata.C2013.tolist()
		self.V2014 = Volumedata.C2014.tolist()
		self.V2015 = Volumedata.C2015.tolist()
		self.V2016 = Volumedata.C2016.tolist()
		self.V2017 = Volumedata.C2017.tolist()
		self.V2018 = Volumedata.C2018.tolist()
		self.V2019= Volumedata.C2019.dropna().tolist()
		
		#Thickness Data
		Thicknesscolnames = ['Date','Mean','C2012', 'C2013', 'C2014', 'C2015', 'C2016', 'C2017', 'C2018', 'C2019']
		Thicknessdata = pandas.read_csv('Upload/AMSR2_SIT_Thickness.csv', names=Thicknesscolnames,header=0)
		self.TMean = Thicknessdata.Mean.tolist()
		self.T2012 = Thicknessdata.C2012.tolist()
		self.T2013 = Thicknessdata.C2013.tolist()
		self.T2014 = Thicknessdata.C2014.tolist()
		self.T2015 = Thicknessdata.C2015.tolist()
		self.T2016 = Thicknessdata.C2016.tolist()
		self.T2017 = Thicknessdata.C2017.tolist()
		self.T2018 = Thicknessdata.C2018.tolist()
		self.T2019 = Thicknessdata.C2019.dropna().tolist()


	def automated (self,day,month,year):
		'''function to automate parts of the monthly update procedure'''
		self.year = year
		self.month =str(month).zfill(2)
		self.day = str(day).zfill(2)

		self.loadCSVdata()
		self.makeVolumegraph()
		self.makeThicknessgraph()


	def makegif(self):
		import imageio
		import os
		filepath = 'Images'
		image_list = []
		for filename in os.listdir(filepath):
			image_list.append(imageio.imread(os.path.join(filepath,filename)))
		imageio.mimsave('Upload/AMSR2_SIT_Last_month.gif', image_list,duration=0.2)

year = 2019
month = 4
day = 30

action = ADS_data()
if __name__ == "__main__":
	print('main')
	action.automated(day,month,year) 
	action.makegif()
	ADS_netcdf.action.automated(1,month,year,day)
	#action.makegraph_compaction()

'''
Citation:
Hori, M., H. Yabuki, T. Sugimura, T. Terui, 2012, AMSR2 Level 3 product of Daily Polar Brightness Temperatures and Product, 1.00, Arctic Data archive System (ADS), Japan, https://ads.nipr.ac.jp/dataset/A20170123-003

'''