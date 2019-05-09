import numpy as np
import numpy.ma as ma
import csv
import matplotlib.pyplot as plt
#import multiprocessing
import time
import os


class Warming:

	def __init__  (self):
		self.year = 1978
		self.month = 10 # begin 22 september
		self.day = 26
		self.daycount = 147 #366year, 181 austral summer
		
		self.datum = ['Date']
		self.dailyenergy = ['Daily MJ/m2']
		self.cumuenergy = ['Cumulative MJ/m2']
		
		self.labelfont = {'fontname':'Arial'}
		self.plottype = 'both' #daily, cumu, both
		self.end = 'false'
		self.masksload()
		self.dailyorcumu()
		
		self.Wed = ['Weddel Sea']
		self.Wedcoa = ['Weddel Sea Coast']
		self.Ind = ['Indian Ocean']
		self.Indcoa = ['Indian Ocean Coast']
		self.Pac = ['Pacific Ocean']
		self.Paccoa = ['Pacific Ocean Coast']
		self.Ross = ['Ross Sea']
		self.Rosscoa = ['Ross Sea Coast']
		self.Bell = ['Bell-Amun Sea']
		self.Bellcoa = ['Bell-Amun Sea Coast']
		
		
		self.Wed_daily = ['Weddel Sea Daily']
		self.Wedcoa_daily = ['Weddel Sea Coast']
		self.Ind_daily = ['Indian Ocean']
		self.Indcoa_daily = ['Indian Ocean Coast']
		self.Pac_daily = ['Pacific Ocean']
		self.Paccoa_daily = ['Pacific Ocean Coast']
		self.Ross_daily = ['Ross Sea']
		self.Rosscoa_daily = ['Ross Sea Coast']
		self.Bell_daily = ['Bell-Amun Sea']
		self.Bellcoa_daily = ['Bell-Amun Sea Coast']
		
		self.start = time.time()

	def masksload(self):
		'''Loads regionmask, pixel area mask, latitudemask and
		AWP values for southern latitudes
		'''
		regionmaskfile = 'Masks/region_s_coast.msk'
		with open(regionmaskfile, 'rb') as frmsk:
			mask = np.fromfile(frmsk, dtype=np.uint8)
		self.regmaskf = np.array(mask, dtype=float)
		
		areamaskfile = 'Masks/pss25area_v3.dat'
		with open(areamaskfile, 'rb') as famsk:
			mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(mask2, dtype=float)/1000
		
		latmaskfile = 'Masks/pss25lats_v3.dat'
		with open(latmaskfile, 'rb') as flmsk:
			mask3 = np.fromfile(flmsk, dtype=np.int32)
		self.latmaskf = np.array(mask3, dtype=float)/100000
	
		
		#latitudes [-50,-50.2,-50.4,-50.6,-50.8,-51,-51.2,-51.4,-51.6,-51.8,-52,-52.2,-52.4,-52.6,-52.8,-53,-53.2,-53.4,-53.6,-53.8,-54,-54.2,-54.4,-54.6,-54.8,-55,-55.2,-55.4,-55.6,-55.8,-56,-56.2,-56.4,-56.6,-56.8,-57,-57.2,-57.4,-57.6,-57.8,-58,-58.2,-58.4,-58.6,-58.8,-59,-59.2,-59.4,-59.6,-59.8,-60,-60.2,-60.4,-60.6,-60.8,-61,-61.2,-61.4,-61.6,-61.8,-62,-62.2,-62.4,-62.6,-62.8,-63,-63.2,-63.4,-63.6,-63.8,-64,-64.2,-64.4,-64.6,-64.8,-65,-65.2,-65.4,-65.6,-65.8,-66,-66.2,-66.4,-66.6,-66.8,-67,-67.2,-67.4,-67.6,-67.8,-68,-68.2,-68.4,-68.6,-68.8,-69,-69.2,-69.4,-69.6,-69.8,-70,-70.2,-70.4,-70.6,-70.8,-71,-71.2,-71.4,-71.6,-71.8,-72,-72.2,-72.4,-72.6,-72.8,-73,-73.2,-73.4,-73.6,-73.8,-74,-74.2,-74.4,-74.6,-74.8,-75,-75.2,-75.4,-75.6,-75.8,-76,-76.2,-76.4,-76.6,-76.8,-77,-77.2,-77.4,-77.6,-77.8,-78,-78.2,-78.4,-78.6,-78.8,-79,-79.2,-79.4,-79.6,-79.8,-80]
		self.latitudelist = np.loadtxt('Masks/Lattable_south_MJ.csv', delimiter=',')
		
	def dayloop(self):
		'''for loop to load binary data files and pass them to the calculation function
		'''
		AWPdaily = np.zeros(104912, dtype=float)
		AWPcumulative = np.zeros(104912, dtype=float)
		
		filepath = 'X:/NSIDC_south/DataFiles/'
		for count in range (0,self.daycount,1):
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			filename = 'NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
			filenameMean = 'Daily_Mean/NSIDC_Mean_{}{}_south.bin'.format(self.stringmonth,self.stringday)
# =============================================================================
# 			filenameMax = 'Max/NSIDC_Max_{}{}.bin'.format(self.stringmonth,self.stringday)
# 			filenameMin = 'Min/NSIDC_Min_{}{}.bin'.format(self.stringmonth,self.stringday)
# =============================================================================
			
			# loads the mean data file
			with open(os.path.join(filepath,filenameMean), 'rb') as fr:
				iceav = np.fromfile(fr, dtype=np.uint8)
			try:
				#loads data file
				with open(os.path.join(filepath,filename), 'rb') as frr:
					ice = np.fromfile(frr, dtype=np.uint8)
			except:
				print('Unavailable:',self.year ,self.stringmonth, self.stringday)
			iceavf = np.array(iceav, dtype=float) / 250
			icef = np.array(ice, dtype=float) / 250
			
			
			#define lists for regional area calculation
			self.Wed_calc = []
			self.Wedcoa_calc = []
			self.Ind_calc = []
			self.Indcoa_calc = []
			self.Pac_calc = []
			self.Paccoa_calc = []
			self.Ross_calc = []
			self.Rosscoa_calc = []
			self.Bel_calc = []
			self.Belcoa_calc = []
		
			self.Wed_daily_calc = []
			self.Wedcoa_daily_calc = []
			self.Ind_daily_calc = []
			self.Indcoa_daily_calc = []
			self.Pac_daily_calc = []
			self.Paccoa_daily_calc = []
			self.Ross_daily_calc = []
			self.Rosscoa_daily_calc = []
			self.Bel_daily_calc = []
			self.Belcoa_daily_calc = []
		
			self.Wed_area = []
			self.Wedcoa_area = []
			self.Ind_area = []
			self.Indcoa_area = []
			self.Pac_area = []
			self.Paccoa_area = []
			self.Ross_area = []
			self.Rosscoa_area = []
			self.Bel_area = []
			self.Belcoa_area = []
			
			#calculate the map
			aaa = np.vectorize(self.energycalc)
			AWPdaily,AWPcumulative,AWPdaily_areaweighted,AWPcumulative_areaweighted,AWPdaily_oceanarea,AWPcumulative_oceanarea = aaa(count,icef,iceavf,AWPcumulative,self.regmaskf,self.areamaskf,self.latmaskf)
			
			#append pan Antarctic lists
			self.datum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			self.dailyenergy.append (round(np.nansum(AWPdaily_areaweighted) / np.nansum(AWPdaily_oceanarea),3))
			self.cumuenergy.append (np.nansum(AWPcumulative_areaweighted) / np.nansum(AWPcumulative_oceanarea))
			
			
			#append regional lists
			self.Wed.append  (round((np.nansum(self.Wed_calc)/np.nansum(self.Wed_area)),3))
			self.Wedcoa.append  (round((np.nansum(self.Wedcoa_calc)/np.nansum(self.Wedcoa_area)),3))
			self.Ind.append  (round((np.nansum(self.Ind_calc)/np.nansum(self.Ind_area)),3))
			self.Indcoa.append  (round((np.nansum(self.Indcoa_calc)/np.nansum(self.Indcoa_area)),3))
			self.Pac.append  (round((np.nansum(self.Pac_calc)/np.nansum(self.Pac_area)),3))
			self.Paccoa.append  (round((np.nansum(self.Paccoa_calc)/np.nansum(self.Paccoa_area)),3))
			self.Ross.append  (round((np.nansum(self.Ross_calc)/np.nansum(self.Ross_area)),3))
			self.Rosscoa.append  (round((np.nansum(self.Rosscoa_calc)/np.nansum(self.Rosscoa_area)),3))
			self.Bell.append  (round((np.nansum(self.Bel_calc)/np.nansum(self.Bel_area)),3))
			self.Bellcoa.append  (round((np.nansum(self.Belcoa_calc)/np.nansum(self.Belcoa_area)),3))
		
			#append daily regional lists
			self.Wed_daily.append  (round((np.nansum(self.Wed_daily_calc)/np.nansum(self.Wed_area)),3))
			self.Wedcoa_daily.append  (round((np.nansum(self.Wedcoa_daily_calc)/np.nansum(self.Wedcoa_area)),3))
			self.Ind_daily.append  (round((np.nansum(self.Ind_daily_calc)/np.nansum(self.Ind_area)),3))
			self.Indcoa_daily.append  (round((np.nansum(self.Indcoa_daily_calc)/np.nansum(self.Indcoa_area)),3))
			self.Pac_daily.append  (round((np.nansum(self.Pac_daily_calc)/np.nansum(self.Pac_area)),3))
			self.Paccoa_daily.append  (round((np.nansum(self.Paccoa_daily_calc)/np.nansum(self.Paccoa_area)),3))
			self.Ross_daily.append  (round((np.nansum(self.Ross_daily_calc)/np.nansum(self.Ross_area)),3))
			self.Rosscoa_daily.append  (round((np.nansum(self.Rosscoa_daily_calc)/np.nansum(self.Rosscoa_area)),3))
			self.Bell_daily.append  (round((np.nansum(self.Bel_daily_calc)/np.nansum(self.Bel_area)),3))
			self.Bellcoa_daily.append  (round((np.nansum(self.Belcoa_daily_calc)/np.nansum(self.Belcoa_area)),3))
			
# =============================================================================
# 			if self.month == 3:
# 				if self.plottype == 'daily' or self.plottype == 'both':
# 					self.normalshow(AWPdaily,self.dailyenergy[count+1])
# 				if self.plottype == 'cumu' or self.plottype == 'both':
# 					self.cumulativeshow(AWPcumulative,self.cumuenergy[count+1])
# =============================================================================
			
			

			#print('Progress: ',100*count/self.daycount)
			print(self.year ,self.stringmonth, self.stringday)
			self.datecalc()
		end = time.time()
		print(end-self.start)
		self.writetofile()
		self.end = 'true'
		with open('CSVexport/AWP_anomaly_'+str(self.year-1)+'-'+str(self.year)+'_s.bin', 'wb') as writecumu:
			icewr = writecumu.write(AWPcumulative)
		self.normalshow(AWPdaily,self.dailyenergy[count+1])
		self.cumulativeshow(AWPcumulative,self.cumuenergy[(self.year-1980)*181+count+1])
		self.fig2.savefig('CSVexport/Final_'+str(self.year-1)+'-'+str(self.year)+'.png')
#		plt.show()
		
	def datecalc(self):
		''' calculates the day-month for a 366 day year'''
		self.day = self.day+1
		if self.day==32 and (self.month==1 or self.month==3 or self.month==5 or self.month==7 or self.month==8 or self.month==10):
			self.day=1
			self.month = self.month+1
		elif self.day==31 and (self.month==4 or self.month==6 or self.month==9 or self.month==11):
			self.day=1
			self.month = self.month+1
		elif self.day==30 and self.month==2:
			self.day=1
			self.month = self.month+1
		elif  self.day==32 and self.month == 12:
			self.day = 1
			self.month = 1
			self.year = self.year+1
			
	
	def energycalc(self,count,icef,iceavf,AWPcumulative,regmaskf,areamaskf,latmaskf):
		'''AWP energy calculation & Regional breakdown'''
		AWPdaily_areaweighted = np.nan
		AWPdaily_oceanarea = np.nan
		AWPcumulative_areaweighted = np.nan
		AWPcumulative_oceanarea = np.nan
		
		
		if 1 < regmaskf < 7 or 20 < regmaskf < 27:
			pixlat = min(-50,latmaskf)
			indexx = int(round((pixlat+50)*(-5)))
			kwh = self.latitudelist[indexx][count+1]
			AWPdaily = (iceavf - icef) * kwh * 0.8
			AWPcumulative = AWPcumulative + AWPdaily
			if AWPdaily != 0:
				AWPdaily_areaweighted = AWPdaily * areamaskf
				AWPdaily_oceanarea = areamaskf
			if AWPcumulative != 0:
				AWPcumulative_areaweighted = AWPcumulative * areamaskf
				AWPcumulative_oceanarea = areamaskf
				if regmaskf == 2:
					self.Wed_daily_calc.append(AWPdaily_areaweighted)
					self.Wed_calc.append(AWPcumulative_areaweighted)
					self.Wed_area.append(areamaskf)
				elif regmaskf == 22:
					self.Wedcoa_daily_calc.append (AWPdaily_areaweighted)
					self.Wedcoa_calc.append (AWPcumulative_areaweighted)
					self.Wedcoa_area.append (areamaskf)
				elif regmaskf == 3:
					self.Ind_daily_calc.append (AWPdaily_areaweighted)
					self.Ind_calc.append (AWPcumulative_areaweighted)
					self.Ind_area.append (areamaskf)
				elif regmaskf == 23:
					self.Indcoa_daily_calc.append (AWPdaily_areaweighted)
					self.Indcoa_calc.append (AWPcumulative_areaweighted)
					self.Indcoa_area.append (areamaskf)
				elif regmaskf == 4:
					self.Pac_daily_calc.append (AWPdaily_areaweighted)
					self.Pac_calc.append (AWPcumulative_areaweighted)
					self.Pac_area.append (areamaskf)
				elif regmaskf == 24:
					self.Paccoa_daily_calc.append (AWPdaily_areaweighted)
					self.Paccoa_calc.append (AWPcumulative_areaweighted)
					self.Paccoa_area.append (areamaskf)
				elif regmaskf == 5:
					self.Ross_daily_calc.append (AWPdaily_areaweighted)
					self.Ross_calc.append (AWPcumulative_areaweighted)
					self.Ross_area.append (areamaskf)
				elif regmaskf == 25:
					self.Rosscoa_daily_calc.append (AWPdaily_areaweighted)
					self.Rosscoa_calc.append (AWPcumulative_areaweighted)
					self.Rosscoa_area.append (areamaskf)
				elif regmaskf == 6:
					self.Bel_daily_calc.append (AWPdaily_areaweighted)
					self.Bel_calc.append (AWPcumulative_areaweighted)
					self.Bel_area.append (areamaskf)
				elif regmaskf == 26:
					self.Belcoa_daily_calc.append (AWPdaily_areaweighted)
					self.Belcoa_calc.append (AWPcumulative_areaweighted)
					self.Belcoa_area.append (areamaskf)
				
		elif regmaskf==11 or regmaskf==12:
			AWPdaily = 9999.9
			AWPcumulative = 9999.9
			
		return AWPdaily,AWPcumulative,AWPdaily_areaweighted,AWPcumulative_areaweighted,AWPdaily_oceanarea,AWPcumulative_oceanarea
	
	
	

	

	def normalshow(self,icemap,icesum):
		'''displays daily AWP data'''
		icemap = icemap.reshape(332, 316)
		icemap = icemap[10:300,30:310]
		icemap = ma.masked_greater(icemap, 9000)
		cmap = plt.cm.coolwarm
		cmap.set_bad('black',0.6)
		
		self.ax.clear()
		self.ax.set_title('Date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2))
		self.ax.set_xlabel('Average: '+str(icesum)+' [MJ / 'r'$m^2$]')
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=-20, vmax=20, cmap=cmap)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 8, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax.text(2, 18, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.fig.tight_layout(pad=2)
#		self.fig.savefig('Daily_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		plt.pause(0.01)
		
	def cumulativeshow(self,icemap,icesum):
		'''displays cumulative AWP data'''
		icemap = icemap.reshape(332, 316)
		icemap = icemap[10:300,30:310]
		icemap = ma.masked_greater(icemap, 9000)
		cmap2 = plt.cm.coolwarm
		cmap2.set_bad('black',0.6)
		
		self.ax2.clear()
		self.ax2.set_title('Date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2))
		if self.end == 'true':
			self.ax2.set_title('Astronomical Summer '+str(self.year-1)+'/'+str(self.year-1900)) # -2000
		self.ax2.set_xlabel('Average: '+str(round(icesum,2))+' [MJ / 'r'$m^2$]')
		self.cax = self.ax2.imshow(icemap, interpolation='nearest', vmin=-1000, vmax=1000, cmap=cmap2)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 8, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 18, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.fig2.tight_layout(pad=2)
#		self.fig2.savefig('Cumulative_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		plt.pause(0.01)
		
	def dailyorcumu(self):
		'''creates separate figures for sea ice data'''
		self.icenull = np.zeros(104912, dtype=float)
		self.icenull = self.icenull.reshape(332, 316)
		
		if self.plottype == 'daily' or  self.plottype == 'both':
			self.fig, self.ax = plt.subplots(figsize=(8, 8))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=-20, vmax=20, cmap=plt.cm.coolwarm)
			self.cbar = self.fig.colorbar(self.cax, ticks=[-20,-10, 0,10, 20]).set_label(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
			self.title = self.fig.suptitle('Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold',x=0.42)
		if self.plottype == 'cumu' or self.plottype == 'both':
			self.fig2, self.ax2 = plt.subplots(figsize=(8, 8))
			self.cax = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=-1000, vmax=1000, cmap=plt.cm.coolwarm)
			self.cbar = self.fig2.colorbar(self.cax, ticks=[-1000,-500, 0,500, 1000]).set_label(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
			self.title = self.fig2.suptitle('Cumulative Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold',x=0.42)
			#print('true')
			
		
	def writetofile(self):
		'''writes data to a csv files'''
		with open('CSVexport/AWP_anomaly_south_'+str(self.year-1)+'-'+str(self.year)+'.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for writeing in range(0,(len(self.dailyenergy))):
				writer.writerow([self.datum[writeing],self.dailyenergy[writeing],self.cumuenergy[writeing]])
				 
		with open('CSVexport/_AWP_regional_south_'+str(self.year)+'.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for writeing in range(0,(len(self.datum))):
				writer.writerow([self.datum[writeing],self.Wed[writeing],self.Wedcoa[writeing],
				self.Ind[writeing],self.Indcoa[writeing],self.Pac[writeing],self.Paccoa[writeing],
				self.Ross[writeing],self.Rosscoa[writeing],self.Bell[writeing],self.Bellcoa[writeing]])
				
		with open('CSVexport/_AWP_regional_south_daily_'+str(self.year)+'.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for writeing in range(0,(len(self.datum))):
				writer.writerow([self.datum[writeing],self.Wed_daily[writeing],self.Wedcoa_daily[writeing],
				self.Ind_daily[writeing],self.Indcoa_daily[writeing],self.Pac_daily[writeing],self.Paccoa_daily[writeing],
				self.Ross_daily[writeing],self.Rosscoa_daily[writeing],self.Bell_daily[writeing],self.Bellcoa_daily[writeing]])


action = Warming()
action.dayloop()
# =============================================================================
# for year in range(1979,1999):
# 	action.dayloop(year,9,22)
# action.writetofile()
# =============================================================================

'''
#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA

arraylength: 104912 (332, 316)

Pixel Value	Antarctic Region
2	Weddell Sea
3	Indian Ocean
4	Pacific Ocean
5	Ross Sea
6	Bellingshausen Amundsen Sea
11	Land
12	Coast

'''