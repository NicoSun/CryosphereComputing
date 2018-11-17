import numpy as np
import numpy.ma as ma
import pandas
import csv
import matplotlib.pyplot as plt
import os
from datetime import date
from datetime import timedelta
import statistics




class NSIDC_area:

	def __init__  (self):
		self.start = date(2000, 9, 6)
		self.month = self.start.month
		self.day = self.start.day
		self.daycount = 161 #161 (April-August)
		#01/04 day 92
		#31/08 day 244
		self.melttype = 'Latest' #Earliest,Latest,Median
				
		self.mode = 'man' #man, on
		self.masksload()
		
		
	def masksload(self):
	
		self.regionmask = 'D:/CryoComputing/NSIDC/Masks/Arctic_region_mask.bin'
		with open(self.regionmask, 'rb') as frmsk:
				self.mask = np.fromfile(frmsk, dtype=np.uint32)
		self.regmaskf = np.array(self.mask, dtype=float)
				
		
	def dayloop(self):		
		filepath = 'D:/CryoComputing/NSIDC/DataFiles/'
		loopday	= self.start	
		day_of_year	= self.start.timetuple().tm_yday	
		
		with open(os.path.join(filepath,'Daily_average/NSIDC_Mean_0331.bin'), 'rb') as fr6:
				iceminyear = np.fromfile(fr6, dtype=np.uint8)
				iceminyear = np.array(iceminyear, dtype=float)
		for y in range (0,136192):
			if  iceminyear[y] > 37:
				iceminyear[y] = 300
			elif  iceminyear[y] < 37:
				iceminyear[y] = 0
		
		for count in range (0,self.daycount,1):
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			
			#filename5 = 'NSIDC_2005{}{}.bin'.format(self.stringmonth,self.stringday)
			filename6 = 'NSIDC_2006{}{}.bin'.format(self.stringmonth,self.stringday)
			filename7 = 'NSIDC_2007{}{}.bin'.format(self.stringmonth,self.stringday)
			filename8 = 'NSIDC_2008{}{}.bin'.format(self.stringmonth,self.stringday)
			filename9 = 'NSIDC_2009{}{}.bin'.format(self.stringmonth,self.stringday)
			filename10 = 'NSIDC_2010{}{}.bin'.format(self.stringmonth,self.stringday)
			filename11 = 'NSIDC_2011{}{}.bin'.format(self.stringmonth,self.stringday)
			filename12 = 'NSIDC_2012{}{}.bin'.format(self.stringmonth,self.stringday)
			filename13 = 'NSIDC_2013{}{}.bin'.format(self.stringmonth,self.stringday)
			filename14 = 'NSIDC_2014{}{}.bin'.format(self.stringmonth,self.stringday)
			filename15 = 'NSIDC_2015{}{}.bin'.format(self.stringmonth,self.stringday)
			filename16 = 'NSIDC_2016{}{}.bin'.format(self.stringmonth,self.stringday)
			filename17 = 'NSIDC_2017{}{}.bin'.format(self.stringmonth,self.stringday)
			
			with open(os.path.join(filepath,filename6), 'rb') as fr6:
				ice6 = np.fromfile(fr6, dtype=np.uint8)
			with open(os.path.join(filepath,filename7), 'rb') as fr7:
				ice7 = np.fromfile(fr7, dtype=np.uint8)
			with open(os.path.join(filepath,filename8), 'rb') as fr8:
				ice8 = np.fromfile(fr8, dtype=np.uint8)
			with open(os.path.join(filepath,filename9), 'rb') as fr9:
				ice9 = np.fromfile(fr9, dtype=np.uint8)
			with open(os.path.join(filepath,filename10), 'rb') as fr10:
				ice10 = np.fromfile(fr10, dtype=np.uint8)
			with open(os.path.join(filepath,filename11), 'rb') as fr11:
				ice11 = np.fromfile(fr11, dtype=np.uint8)	
			with open(os.path.join(filepath,filename12), 'rb') as fr12:
				ice12 = np.fromfile(fr12, dtype=np.uint8)
			with open(os.path.join(filepath,filename13), 'rb') as fr13:
				ice13 = np.fromfile(fr13, dtype=np.uint8)
			with open(os.path.join(filepath,filename14), 'rb') as fr14:
				ice14 = np.fromfile(fr14, dtype=np.uint8)	
			with open(os.path.join(filepath,filename15), 'rb') as fr15:
				ice15 = np.fromfile(fr15, dtype=np.uint8)
			with open(os.path.join(filepath,filename16), 'rb') as fr16:
				ice16 = np.fromfile(fr16, dtype=np.uint8)
				
			
			#iceminyear = np.zeros(136192, dtype=float)
			
			
			for x in range (0,136192):
				if  1 < self.regmaskf[x] < 16:
					list = [ice6[x],ice7[x],ice8[x],ice9[x],ice10[x],ice11[x],ice12[x],ice13[x],ice14[x],ice15[x],ice16[x]]
					#icemin = min(list)
					icemin = max(list)
					#icemin = statistics.median(list)
					if icemin < 37 and day_of_year < iceminyear[x]:
						iceminyear[x] = day_of_year
					
						
				elif  self.regmaskf[x] > 16:
					iceminyear[x] = 3333
				else:
					iceminyear[x] = 0
					
			
			iceminyear = ma.masked_greater(iceminyear, 3000)
			#self.normalshow(iceminyear)
				

			count = count+1
			if count < self.daycount:
				loopday = loopday+timedelta(days=-1)
				self.month = loopday.month
				self.day = loopday.day
				day_of_year = loopday.timetuple().tm_yday
			print('Date: {} , DayofYear: {}'.format(loopday,day_of_year))
			
		for x in range (0,136192):
			if  iceminyear[x] == 300:
				iceminyear[x] = -2
		with open('Special_Animation/'+self.melttype+'_Melt_Date.bin', 'wb') as writecumu:
				icewr = writecumu.write(iceminyear)
			
		self.normalshow(iceminyear)
		plt.show()
		

	def normalshow(self,icemap):		
		icemap = icemap.reshape(448, 304)
				
		cmap = plt.cm.gist_rainbow # plt.cm.jet
		cmap.set_bad('black',0.8)
		
		map1 = ma.masked_outside(icemap,80,320) 
		map2 = ma.masked_outside(icemap,-3,+2) 
		
		fig = plt.figure(figsize=(8, 10))
		ax = fig.add_subplot(111)

		
		ax.set_title(self.melttype+' Melt Date') #Earliest,Latest,Median Melt
		cax = ax.imshow(map1, interpolation='nearest', vmin=90, vmax=250, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[91,121,152,182,213,244])
		cbar.ax.set_yticklabels(['Apr','May','Jun','Jul','Aug','Sep'])
		
		ax.imshow(map2, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax.set_xlabel('white = not always icefree', fontsize=14) # never,"usually not","not always" icefree
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.text(2, 8, r'Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.text(-0.04, 0.48, 'https://sites.google.com/site/cryospherecomputing',
        transform=ax.transAxes,rotation='vertical',color='grey', fontsize=10)
		fig.tight_layout(pad=1)
		fig.subplots_adjust(left=0.05)
		fig.savefig('Special_Animation/'+self.melttype+'_Melt_Date.png')
		plt.pause(0.01)		
	
	
	def combograph (self):
		
		with open('Special_Animation/Earliest_Melt_Date.bin', 'rb') as aaa:
			early = np.fromfile(aaa, dtype=np.float)
				
		with open('Special_Animation/Median_Melt_Date.bin', 'rb') as bbb:
			median = np.fromfile(bbb, dtype=np.float)
				
		with open('Special_Animation/Latest_Melt_Date.bin', 'rb') as ccc:
			late = np.fromfile(ccc, dtype=np.float)
		
		early = early.reshape(448, 304)
		median = median.reshape(448, 304)
		late = late.reshape(448, 304)
		
		cmap = plt.cm.gist_rainbow # plt.cm.jet
		cmap.set_bad('black',0.8)
		
		map1 = ma.masked_outside(early,90,250) 
		map11 = ma.masked_outside(early,-3,+2)
		map2 = ma.masked_outside(median,90,250) 
		map21 = ma.masked_outside(median,-3,+2)
		map3 = ma.masked_outside(late,90,250) 
		map31 = ma.masked_outside(late,-3,+2)
		
		
		fig = plt.figure(figsize=(17, 8))
		fig.suptitle('Arctic Melt Dates', fontsize=14, fontweight='bold')
		ax1 = fig.add_subplot(131)
		ax2 = fig.add_subplot(132)
		ax3 = fig.add_subplot(133)
		
		
		
		ax1.set_title('Earliest Melt Date')
		ax1.imshow(map1, interpolation='nearest', vmin=90, vmax=250, cmap=cmap)
		ax1.imshow(map11, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax2.set_title('Median Melt Date')
		ax2.imshow(map2, interpolation='nearest', vmin=90, vmax=250, cmap=cmap)
		ax2.imshow(map21, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax3.set_title('Latest Melt Date')
		cax = ax3.imshow(map3, interpolation='nearest', vmin=90, vmax=250, cmap=cmap)
		ax3.imshow(map31, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		cbar = fig.colorbar(cax, ticks=[91,121,152,182,213,244])
		cbar.ax.set_yticklabels(['Apr','May','Jun','Jul','Aug','Sep'])
		
		
		ax1.set_xlabel('white: never ice free', fontsize=14)
		ax2.set_xlabel('white: usually not ice free', fontsize=14)
		ax3.set_xlabel('white: not always ice free', fontsize=14)
		
		ax1.axes.get_yaxis().set_ticks([])
		ax2.axes.get_yaxis().set_ticks([])
		ax3.axes.get_yaxis().set_ticks([])
		ax1.axes.get_xaxis().set_ticks([])
		ax2.axes.get_xaxis().set_ticks([])
		ax3.axes.get_xaxis().set_ticks([])

		fig.text(0.02, 0.95, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax1.transAxes)
		fig.text(0.02, 0.92, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax1.transAxes)
		fig.text(0.66, 0.03, 'https://sites.google.com/site/cryospherecomputing/analysis',)
		
		fig.tight_layout(pad=1)
		fig.subplots_adjust(top=0.88)
		fig.subplots_adjust(bottom=0.1)
		fig.savefig('Special_Animation/Combo_Melt_Date.png')
		plt.show()
		
		

action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	#action.loadCSVdata()
	#action.dayloop()
	action.combograph()
	
	
	
	#action.writetofile()
	#action.automated(1,2,2017) #note substract 3 days from last available day
	#action.makegraph()
	#action.makegraph_compaction()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA