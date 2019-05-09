import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from datetime import timedelta




class NSIDC_area:

	def __init__  (self):
		self.start = date(1979, 1, 1)
		self.year = self.start.year
		self.stringmonth = str(self.start.month).zfill(2)
		self.stringday = str(self.start.day).zfill(2)
		self.daycount = 368# 366*40
		self.masksload()
		
		
	def masksload(self):
	
		regionmaskfile = 'Masks/region_s_pure.msk'
		with open(regionmaskfile, 'rb') as frmsk:
			self.regmask = np.fromfile(frmsk, dtype=np.uint8)

	def dayloop(self):
		loopday	= self.start
		
		icefreecount = np.zeros(len(self.regmask))
		for count in range (0,self.daycount):
			
#			filename = 'DataFiles/Forecast_Mean/NSIDC_Mean_{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename = 'DataFiles/NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
			with open(filename, 'rb') as fr:
				ice = np.fromfile(fr, dtype=np.uint8)

			aaa = np.vectorize(self.daycalc)
			icefreecount= aaa(icefreecount,ice)
				
			loopday = loopday+timedelta(days=1)
			self.year = loopday.year
			self.stringmonth = str(loopday.month).zfill(2)
			self.stringday = str(loopday.day).zfill(2)
			
			if loopday.month==1 and loopday.day==1:
				self.normalshow(icefreecount)
				
				with open('netcdf/Icefreedays_{}.bin'.format(self.year-1), 'wb') as fwr:
					fwr.write(icefreecount)

				icefreecount = np.zeros(len(self.regmask))
	
			print('Date: {}'.format(loopday))

		plt.show()
			
	def daycalc(self,icefreecount,ice):
		'''calculates icefree days'''
	
		if ice < 37:
			icefreecount = icefreecount +1
		elif ice > 250:
			icefreecount = 400
		return icefreecount
			
		
	def normalshow(self,icemap):
		icemap = icemap.reshape(332, 316)
				
		cmap = plt.cm.magma_r # plt.cm.jet
		cmap.set_bad('black',0.8)
		
		map1 = np.ma.masked_outside(icemap,0,370) 
		
		fig = plt.figure(figsize=(8, 7))
		ax = fig.add_subplot(111)

		cax = ax.imshow(map1, interpolation='nearest', vmin=0, vmax=300, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[0,50,100,150,200,250,300]).set_label('Ice Free Days')
		
		ax.imshow(map1, interpolation='nearest', vmin=0, vmax=300, cmap=cmap)
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.set_title('Antarctic Ice Free Days: {}'.format(self.year-1),x=0.5)
		ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_xlabel('cryospherecomputing.tk/IceFreeDays',x=0.50)
		ax.set_ylabel('nsidc.org/data/NSIDC-0051',y=0.15)
		fig.tight_layout()

		fig.savefig('csvexport/Icefreedays_{}.png'.format(self.year-1))

	def anomalyshow(self,icemap,year):
		cmap = plt.cm.RdBu # plt.cm.jet
		cmap.set_bad('black',0.8)
		
		for x,y in enumerate(self.regmask):
			if y > 6:
				icemap[x] = 400
		
		icemap = np.ma.masked_outside(icemap,-300,370) 
		icemap = icemap.reshape(332, 316)
		fig = plt.figure(figsize=(8, 7))
		ax = fig.add_subplot(111)

		cax = ax.imshow(icemap, interpolation='nearest', vmin=-100, vmax=100, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[-100,-50,0,50,100]).set_label('Ice Free Days Anomaly')
		
		ax.imshow(icemap, interpolation='nearest', vmin=-100, vmax=100, cmap=cmap)
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.set_title('Antarctic Ice Free Days Anomaly: {}'.format(year),x=0.5)
		ax.text(2, 8, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_xlabel('cryospherecomputing.tk/IceFreeDays',x=0.50)
		ax.set_ylabel('nsidc.org/data/NSIDC-0051',y=0.15)
		fig.tight_layout()

		fig.savefig('csvexport/Icefreedays_anom_{}.png'.format(year))
		
	def calcanomaly(self):
		
		icemean = np.zeros(len(self.regmask))
		icelist = []

		for year in range(1979,2019):
			with open('netcdf/Icefreedays_{}.bin'.format(year), 'rb') as fr:
				icelist.append(np.fromfile(fr, dtype=np.float))
		
		for x in icelist:
			icemean = icemean + x/len(icelist)
		
		year = 1979
		for x in icelist:
			iceanomaly = icemean - x
			self.anomalyshow(iceanomaly,year)
			year +=1
		plt.show()
		

action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	#action.loadCSVdata()
#	action.dayloop()
	action.calcanomaly()

'''
Values are coded as follows:

0-250  concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

'''