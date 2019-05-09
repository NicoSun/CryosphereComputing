import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import date
from datetime import timedelta
import statistics




class NSIDC_area:

	def __init__  (self):
		self.start = date(2012, 9, 15)
		self.month = self.start.month
		self.day = self.start.day
		self.daycount = 200 #155 (Oct-Feb)
		#01/04 day 92
		#31/08 day 244
		self.masksload()
		
		
	def masksload(self):
	
		regionmaskfile = 'Masks/region_s_pure.msk'
		with open(regionmaskfile, 'rb') as frmsk:
			self.regmask = np.fromfile(frmsk, dtype=np.uint8)

	def dayloop(self):
		filepath = 'X:/NSIDC_south/DataFiles/'
		loopday	= self.start
		day_of_year	= self.start.timetuple().tm_yday
		
		with open(os.path.join(filepath,'Minimum/NSIDC_Min_0915_south.bin'), 'rb') as fr:
			iceminyear = np.fromfile(fr, dtype=np.uint8)
			iceminyear = np.array(iceminyear, dtype=float)
		with open(os.path.join(filepath,'Daily_Mean/NSIDC_Mean_0915_south.bin'), 'rb') as fr:
			icemeanyear = np.fromfile(fr, dtype=np.uint8)
			icemeanyear = np.array(icemeanyear, dtype=float)
		with open(os.path.join(filepath,'Maximum/NSIDC_Max_0915_south.bin'), 'rb') as fr:
			icemaxyear = np.fromfile(fr, dtype=np.uint8)
			icemaxyear = np.array(icemaxyear, dtype=float)
				
				
		#assigns day 500 for ice covered sea and day 0 for ice free sea
		for y in range (0,len(iceminyear)):
			if  iceminyear[y] > 37:
				iceminyear[y] = 500
			else:
				iceminyear[y] = 0
				
			if  icemeanyear[y] > 37:
				icemeanyear[y] = 500
			else:
				icemeanyear[y] = 0
				
			if  icemaxyear[y] > 37:
				icemaxyear[y] = 500
			else:
				icemaxyear[y] = 0

		
		for count in range (0,self.daycount):
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			
			filename6 = 'NSIDC_2006{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename7 = 'NSIDC_2007{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename8 = 'NSIDC_2008{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename9 = 'NSIDC_2009{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename10 = 'NSIDC_2010{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename11 = 'NSIDC_2011{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename12 = 'NSIDC_2012{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename13 = 'NSIDC_2013{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename14 = 'NSIDC_2014{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename15 = 'NSIDC_2015{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename16 = 'NSIDC_2016{}{}_south.bin'.format(self.stringmonth,self.stringday)
			filename17 = 'NSIDC_2017{}{}_south.bin'.format(self.stringmonth,self.stringday)
			
			with open(os.path.join(filepath,filename6), 'rb') as fr6:
				ice6 = np.fromfile(fr6, dtype=np.uint8)
			with open(os.path.join(filepath,filename7), 'rb') as fr7:
				ice7 = np.fromfile(fr7, dtype=np.uint8)
			with open(os.path.join(filepath,filename8), 'rb') as fr8:
				ice8 = np.fromfile(fr8, dtype=np.uint8)
			with open(os.path.join(filepath,filename9), 'rb') as fr9:
				ice9 = np.fromfile(fr9, dtype=np.uint8)
			with open(os.path.join(filepath,filename10), 'rb') as fr:
				ice10 = np.fromfile(fr, dtype=np.uint8)
			with open(os.path.join(filepath,filename11), 'rb') as fr:
				ice11 = np.fromfile(fr, dtype=np.uint8)	
			with open(os.path.join(filepath,filename12), 'rb') as fr:
				ice12 = np.fromfile(fr, dtype=np.uint8)
			with open(os.path.join(filepath,filename13), 'rb') as fr:
				ice13 = np.fromfile(fr, dtype=np.uint8)
			with open(os.path.join(filepath,filename14), 'rb') as fr:
				ice14 = np.fromfile(fr, dtype=np.uint8)	
			with open(os.path.join(filepath,filename15), 'rb') as fr:
				ice15 = np.fromfile(fr, dtype=np.uint8)
			with open(os.path.join(filepath,filename16), 'rb') as fr:
				ice16 = np.fromfile(fr, dtype=np.uint8)
			with open(os.path.join(filepath,filename17), 'rb') as fr:
				ice17 = np.fromfile(fr, dtype=np.uint8)
				
			aaa = np.vectorize(self.daycalc)
			iceminyear,icemeanyear,icemaxyear = aaa(iceminyear,icemeanyear,icemaxyear,day_of_year,ice6,ice7,ice8,ice9,ice10,ice11,ice12,ice13,ice14,ice15,ice16,ice17)
			
			print('Date: {} , DayofYear: {}'.format(loopday,day_of_year))
			if count < self.daycount:
				loopday = loopday+timedelta(days=-1)
				self.month = loopday.month
				self.day = loopday.day
				day_of_year = loopday.timetuple().tm_yday
			
			
		#mask out land cover
		for x in range (0,len(iceminyear)):
			if self.regmask[x] > 10:
				iceminyear[x] = 999
				icemeanyear[x] = 999
				icemaxyear[x] = 999
			else:
				if iceminyear[x] == 60:
					iceminyear[x] == -2
				if icemeanyear[x] == 60:
					icemeanyear[x] = -2
				elif icemeanyear[x] == 500:
					icemeanyear[x] = 0
				if icemaxyear[x] == 60:
					icemaxyear[x] = -2
				elif icemaxyear[x] == 500:
					icemaxyear[x] = 0
				
#		with open('tempgif/South_Melt_Date.bin', 'wb') as writecumu:
#				icewr = writecumu.write(iceminyear)	
		self.normalshow(iceminyear,'min')
		self.normalshow(icemeanyear,'mean')
		self.normalshow(icemaxyear,'max')
		self.combograph(iceminyear,icemeanyear,icemaxyear)
		plt.show()
						
			
	def daycalc(self,iceminyear,icemeanyear,icemaxyear,day_of_year,ice6,ice7,ice8,ice9,ice10,ice11,ice12,ice13,ice14,ice15,ice16,ice17):
		'''calculates if cell is icefree'''
		icelist = [ice6,ice7,ice8,ice9,ice10,ice11,ice12,ice13,ice14,ice15,ice16,ice17]
		icemin = min(icelist)
		icemax = max(icelist)
		icemean = statistics.median(icelist)
		
		if icemin > 37 and day_of_year < iceminyear:
			iceminyear = day_of_year
		if icemean > 37 and day_of_year < icemeanyear:
			icemeanyear = day_of_year
		if icemax > 37 and day_of_year < icemaxyear:
			icemaxyear = day_of_year
		

		return iceminyear,icemeanyear,icemaxyear
			
			
		

	def normalshow(self,icemap,code):
		icemap = icemap.reshape(332, 316)
				
		cmap = plt.cm.gist_rainbow # plt.cm.jet
		cmap.set_bad('black',0.8)
		
		map1 = np.ma.masked_outside(icemap,55,300) 
		map2 = np.ma.masked_outside(icemap,-3,+2) 
		
		fig = plt.figure(figsize=(8, 8))
		ax = fig.add_subplot(111)

		cax = ax.imshow(map1, interpolation='nearest', vmin=59, vmax=248, cmap=cmap)
		cbar = fig.colorbar(cax, ticks=[60,91,121,152,182,213,244])
		cbar.ax.set_yticklabels(['Mar', 'Apr','May','Jun','Jul','Aug','Sep'])
		
		ax.imshow(map2, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		if code == 'max':
			ax.set_title('Earliest Freeze Date') 
			ax.set_xlabel('white = never icefree', fontsize=14)
		elif code == 'mean':
			ax.set_title('Median Freeze Date') 
			ax.set_xlabel('white = not always icefree', fontsize=14)
		elif code == 'min':
			ax.set_title('Latest Freeze Date')
			ax.set_xlabel('white = usually not icefree', fontsize=14)
		
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		ax.text(2, 8, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		ax.text(2, 18, r'Map: Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.text(-0.04, 0.48, 'https://sites.google.com/site/cryospherecomputing/analysis',
        transform=ax.transAxes,rotation='vertical',color='grey', fontsize=10)
		fig.tight_layout(pad=1)
		fig.subplots_adjust(left=0.05)
		
# =============================================================================
# 		if code == 'min':
# 			fig.savefig('csvexport/South_Earliest_Freeze_Date.png')
# 		elif code == 'mean':
# 			fig.savefig('csvexport/South_Mean_Freeze_Date.png')
# 		elif code == 'max':
# 			fig.savefig('csvexport/South_Latest_Freeze_Date.png')
# =============================================================================
#		plt.pause(0.01)
	
	
	def combograph (self,early,median,late):
		
		early = early.reshape(332, 316)
		median = median.reshape(332, 316)
		late = late.reshape(332, 316)
		
		cmap = plt.cm.gist_rainbow # plt.cm.jet
		cmap.set_bad('black',0.8)
		
		map1 = np.ma.masked_outside(late,55,300) 
		map11 = np.ma.masked_outside(late,-3,+2)
		map2 = np.ma.masked_outside(median,55,300) 
		map21 = np.ma.masked_outside(median,-3,+2)
		map3 = np.ma.masked_outside(early,55,300) 
		map31 = np.ma.masked_outside(early,-3,+2)
		
		
		fig = plt.figure(figsize=(18, 7))
		ax1 = fig.add_subplot(131)
		ax2 = fig.add_subplot(132)
		ax3 = fig.add_subplot(133)
		
		fig.subplots_adjust(left=0.03, right=0.97, wspace=0.05)
		fig.suptitle('Antarctic Freeze Days',fontweight='bold',fontsize=14)

		ax1.set_title('Earliest Freeze Date')
		ax1.imshow(map1, interpolation='nearest', vmin=59, vmax=248, cmap=cmap)
		ax1.imshow(map11, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax2.set_title('Median Freeze Date')
		ax2.imshow(map2, interpolation='nearest', vmin=59, vmax=248, cmap=cmap)
		ax2.imshow(map21, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax3.set_title('Latest Freeze Date')
		cax = ax3.imshow(map3, interpolation='nearest', vmin=59, vmax=248, cmap=cmap)
		ax3.imshow(map31, interpolation='nearest', vmin=-1, vmax=1, cmap=plt.cm.Greys)
		
		ax1.set_xlabel('white: never ice free', fontsize=14)
		ax2.set_xlabel('white: usually not ice free', fontsize=14)
		ax3.set_xlabel('white: not always ice free', fontsize=14)

		ax1.axes.get_yaxis().set_ticks([])
		ax1.axes.get_xaxis().set_ticks([])
		ax2.axes.get_yaxis().set_ticks([])
		ax2.axes.get_xaxis().set_ticks([])
		ax3.axes.get_yaxis().set_ticks([])
		ax3.axes.get_xaxis().set_ticks([])
		
		ax1.text(0.02, 0.96, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax1.transAxes)
		ax1.text(0.02, 0.93, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax1.transAxes)
		ax3.text(0.02, 0.02, 'https://sites.google.com/site/cryospherecomputing/analysis',transform=ax1.transAxes)
		
		
		fig.tight_layout(pad=-3)
		
		cbar = fig.colorbar(cax, ticks=[60,91,121,152,182,213,244])
		cbar.ax.set_yticklabels(['Mar', 'Apr','May','Jun','Jul','Aug','Sep'])
		
		fig.subplots_adjust(top=0.85)
		fig.subplots_adjust(bottom=0.1)
		fig.subplots_adjust(right=0.98)
		
#		fig.savefig('csvexport/Combo_South_Freeze_Date.png')
		
		

action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	#action.loadCSVdata()
	action.dayloop()
#	action.combograph()
	
'''
Values are coded as follows:

0-250  concentration
251 pole hole
252 unused
253 coastline
254 landmask
255 NA

'''