import numpy as np
import numpy.ma as ma
import csv
import pandas
import matplotlib.pyplot as plt
import os


class Warming:

	def __init__  (self):
		self.year = 2018
		self.month = 9 # begin 22 september
		self.day = 22
		self.daycount = 62 #366year, 181 austral summer
		self.index = 0
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
		
		
		self.labelfont = {'fontname':'Arial'}
		self.masksload()


	def masksload(self):
		'''Loads regionmask, pixel area mask, latitudemask and
		AWP values for southern latitudes
		'''
		regionmaskfile = 'X:/NSIDC_south/Masks/region_s_coast.msk'
		with open(regionmaskfile, 'rb') as frmsk:
			mask = np.fromfile(frmsk, dtype=np.uint8)
		self.regmaskf = np.array(mask, dtype=float)
		
		areamaskfile = 'X:/NSIDC_south/Masks/pss25area_v3.dat'
		with open(areamaskfile, 'rb') as famsk:
			mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(mask2, dtype=float)/1000
		
		latmaskfile = 'X:/NSIDC_south/Masks/pss25lats_v3.dat'
		with open(latmaskfile, 'rb') as flmsk:
			mask3 = np.fromfile(flmsk, dtype=np.int32)
		self.latmaskf = np.array(mask3, dtype=float)/100000
	
		
		#latitudes [-50 to -80, step = 0.2]
		self.latitudelist = np.loadtxt('X:/NSIDC_south/Masks/Lattable_south_MJ.csv', delimiter=',')
		
	def dayloop(self):
		'''for loop to load binary data files and pass them to the calculation function
		'''
		self.AWPcumulative = np.zeros(104912, dtype=float)
		countmax = self.index+self.daycount
		filepath = 'X:/NSIDC_south/DataFiles/'
		
		with open('X:/Upload/AWP_data/South_AWP_NRT_cumudata.bin', 'rb') as readcumu:
			self.AWPcumulative = np.fromfile(readcumu, dtype=float)
				
		for count in range (self.index,countmax,1):
			print(count)
			self.stringmonth = str(self.month).zfill(2)
			self.stringday = str(self.day).zfill(2)
			
			filename = 'NSIDC_{}{}{}_south.bin'.format(self.year,self.stringmonth,self.stringday)
			filenameMean = 'Daily_Mean/NSIDC_Mean_{}{}_south.bin'.format(self.stringmonth,self.stringday)	
			
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
			AWPdaily,self.AWPcumulative,AWPdaily_areaweighted,AWPcumulative_areaweighted,AWPdaily_oceanarea,AWPcumulative_oceanarea = aaa(count,icef,iceavf,self.AWPcumulative,self.regmaskf,self.areamaskf,self.latmaskf)
			
			#append pan Antarctic lists
			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.stringmonth,self.stringday))
			self.CSVDaily.append (round(np.nansum(AWPdaily_areaweighted) / np.nansum(AWPdaily_oceanarea),3))
			self.CSVCumu.append (np.nansum(AWPcumulative_areaweighted) / np.nansum(AWPcumulative_oceanarea))
			
			
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
			
			print(self.year ,self.stringmonth, self.stringday)
#			self.datecalc()
			
		self.dailyorcumu()
		self.normalshow(AWPdaily,self.CSVDaily[-1])
		self.cumulativeshow(self.AWPcumulative,self.CSVCumu[-1])
		with open('X:/Upload/AWP_data/South_AWP_NRT_cumudata.bin', 'wb') as writecumu:
			writecumu.write(self.AWPcumulative)
		self.fig2.savefig('X:/Upload/AWP/South_AWP_map_cumu.png')
		self.fig.savefig('X:/Upload/AWP/South_AWP_map_day.png')
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
			if icef == 1.02:
				icef = iceavf
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
		cmap1 = plt.cm.coolwarm
		cmap1.set_bad('black',0.6)
		
		self.ax.clear()
		self.ax.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
		self.ax.set_xlabel('Average: '+str(icesum)+' [MJ / 'r'$m^2$]')
		self.ax.imshow(icemap, interpolation='nearest', vmin=-20, vmax=20, cmap=cmap1)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 8, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax.text(2, 18, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.fig.tight_layout(pad=2)
		self.fig.canvas.draw()
		plt.pause(0.01)

		
		
	def cumulativeshow(self,icemap,icesum):
		'''displays cumulative AWP data'''
		icemap = icemap.reshape(332, 316)
		icemap = icemap[10:300,30:310]
		icemap = ma.masked_greater(icemap, 9000)
		cmap2 = plt.cm.coolwarm
		cmap2.set_bad('black',0.6)
		
		self.ax2.clear()
		self.ax2.set_title('Date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday))
		self.ax2.set_xlabel('Average: '+str(round(icesum,2))+' [MJ / 'r'$m^2$]')
		self.ax2.imshow(icemap, interpolation='nearest', vmin=-1000, vmax=1000, cmap=cmap2)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 8, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 18, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.fig2.tight_layout(pad=2)
		self.fig2.canvas.draw()
		plt.pause(0.01)

		
		
	def dailyorcumu(self):
		'''creates separate figures for sea ice data'''
		self.icenull = np.zeros(104912, dtype=float)
		self.icenull = self.icenull.reshape(332, 316)
		

		self.fig, self.ax = plt.subplots(figsize=(8, 8))
		self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=-20, vmax=20, cmap=plt.cm.coolwarm)
		self.fig.colorbar(self.cax, ticks=[-20,-10, 0,10, 20]).set_label(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		self.fig.suptitle('Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold',x=0.42)
		self.normalshow(self.icenull,0)

		self.fig2, self.ax2 = plt.subplots(figsize=(8, 8))
		self.cax2 = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=-1000, vmax=1000, cmap=plt.cm.coolwarm)
		self.fig2.colorbar(self.cax2, ticks=[-1000,-500, 0,500, 1000]).set_label(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		self.fig2.suptitle('Cumulative Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold',x=0.42)
		self.cumulativeshow(self.icenull,0)
	

	def makedailygraph(self):
		
		Climatecolnames = ['Date','C1993','C2007', 'C2008','C2012', 'C2013', 'C2014', 'C2015','C2016','C2017','C2018']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/South_AWP_daily.csv', names=Climatecolnames,header=0)
		Date = Climatedata.Date.tolist()
		
		C1993 = Climatedata.C1993.tolist()
		C2007 = Climatedata.C2007.tolist()
		C2008 = Climatedata.C2008.tolist()
		C2012 = Climatedata.C2012.tolist()
		C2013 = Climatedata.C2013.tolist()
		C2014 = Climatedata.C2014.tolist()
		C2015 = Climatedata.C2015.tolist()
		C2016 = Climatedata.C2016.tolist()
		C2017 = Climatedata.C2017.tolist()
		C2018 = Climatedata.C2018.tolist()
		
		fig = plt.figure(figsize=(14, 8))
		fig.suptitle('Daily Pan Antarctic Albedo-Warming Values (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Sep','Oct','Nov','Dec','Jan', 'Feb', 'Mar']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-5,5,0.5)
		ax.set_yticks(major_ticks)
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.66, -0.06, 'https://sites.google.com/site/cryospherecomputing/awp',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		ax.grid(True)		
		plt.plot( C1993, color=(0.2,0.8,0.8),label='1992/93',lw=2)
		plt.plot( C2007, color=(0.6,0,0.3),label='2006/07',lw=2)
		plt.plot( C2008, color=(0.2,0.8,0.2),label='2007/08',lw=2)
		plt.plot( C2012, color=(0.5,0.5,0.5),label='2011/12',lw=2)
		plt.plot( C2013, color=(0.9,0.9,0),label='2012/13',lw=2)
		plt.plot( C2014, color=(0.9,0.1,0.1),label='2013/14',lw=2)
		plt.plot( C2015, color=(0.4,0,0.4),label='2014/15',lw=2)
		plt.plot( C2016, color=(0,0,0.6),label='2015/16',lw=2)
		plt.plot( C2017, color=(0.6,0,0),label='2016/17',lw=2)
		plt.plot( C2018, color=(1,0.6,0.2),label='2017/18',lw=2)
		plt.plot( self.CSVDaily, color='black',label='2018/19',lw=2)
		
		ymin = -3.1
		ymax = 3.6
		plt.axis([0,181,ymin,ymax])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		lgd = ax.legend(loc='center left',bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
		fig.tight_layout(pad=2)
		fig.subplots_adjust(right=0.9)
		fig.subplots_adjust(top=0.95)
		
		fig.savefig('X:/Upload/AWP/South_AWP_daily.png',bbox_extra_artists=(lgd,))
		
	
	def makecumugraph(self):
		
		Climatecolnames = ['Date','C1993','C2007', 'C2008','C2012', 'C2013', 'C2014', 'C2015','C2016','C2017','C2018']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/South_AWP_cumu.csv', names=Climatecolnames,header=0)
		C1993 = Climatedata.C1993.tolist()
		C2007 = Climatedata.C2007.tolist()
		C2008 = Climatedata.C2008.tolist()
		C2012 = Climatedata.C2012.tolist()
		C2013 = Climatedata.C2013.tolist()
		C2014 = Climatedata.C2014.tolist()
		C2015 = Climatedata.C2015.tolist()
		C2016 = Climatedata.C2016.tolist()
		C2017 = Climatedata.C2017.tolist()
		C2018 = Climatedata.C2018.tolist()
		
		fig = plt.figure(figsize=(14, 8))
		fig.suptitle('Cumulative Pan Antarctic Albedo-Warming Values (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Sep','Oct','Nov','Dec','Jan', 'Feb', 'Mar']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)
		major_ticks = np.arange(-500,500,25)
		ax.set_yticks(major_ticks)

		ax.set_ylabel(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.66, -0.06, 'https://sites.google.com/site/cryospherecomputing/awp',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		ax.grid(True)
		plt.plot( C1993, color=(0.2,0.8,0.8),label='1992/93',lw=2)
		plt.plot( C2007, color=(0.6,0,0.3),label='2006/07',lw=2)
		plt.plot( C2008, color=(0.2,0.8,0.2),label='2007/08',lw=2)
		plt.plot( C2012, color=(0.5,0.5,0.5),label='2011/12',lw=2)
		plt.plot( C2013, color=(0.9,0.9,0),label='2012/13',lw=2)
		plt.plot( C2014, color=(0.9,0.1,0.1),label='2013/14',lw=2)
		plt.plot( C2015, color=(0.4,0,0.4),label='2014/15',lw=2)
		plt.plot( C2016, color=(0,0,0.6),label='2015/16',lw=2)
		plt.plot( C2017, color=(0.6,0,0),label='2016/17',lw=2)
		plt.plot( C2018, color=(1,0.6,0.2),label='2017/18',lw=2)
		plt.plot( self.CSVCumu, color='black',label='2018/19',lw=2)
		
		ymin = -90
		ymax = 180
		plt.axis([0,181,ymin,ymax])
		
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.legend(loc='center left',bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
		ax.legend(loc='center left',bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
		fig.tight_layout(pad=2)
		fig.subplots_adjust(right=0.9)
		fig.subplots_adjust(top=0.95)
		
		fig.savefig('X:/Upload/AWP/South_AWP_cumu.png')
		
	def makeregiongraph(self):
				
	
		fig = plt.figure(figsize=(14, 8))
		fig.suptitle('Cumulative Regional Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Sep','Oct','Nov','Dec','Jan', 'Feb', 'Mar']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.66, -0.06, 'https://sites.google.com/site/cryospherecomputing/awp',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		ax.grid(True)
		
		plt.plot( self.Wed, color=(0.1,0.7,0.1),label='Weddel Sea',lw=2)
		plt.plot( self.Wedcoa, color=(0.2,0.8,0.8),label='Weddel Sea Coast',lw=2)
		plt.plot( self.Ind, color=(0.65,0.1,0.4),label='Indian Ocean',lw=2)
		plt.plot( self.Indcoa, color=(0.5,0.5,0.5),label='Indian Ocean Coast',lw=2)
		plt.plot( self.Pac, color=(0.9,0.9,0),label='Pacific Ocean',lw=2)
		plt.plot( self.Paccoa, color=(0.9,0.1,0.1),label='Pacific Ocean Coast',lw=2)
		plt.plot( self.Ross, color=(0,0,0.6),label='Ross Sea',lw=2)
		plt.plot( self.Rosscoa, color=(1,0.6,0.2),label='Ross Sea Coast',lw=2)
		plt.plot( self.Bell, color=(1,0.26,1),label='Bell-Amun Sea',lw=2)
		plt.plot( self.Bellcoa, color=(0,0,0),label='Bell-Amun Sea Coast',lw=2)
		
		ymin = min(float(self.Wed[-1]),float(self.Wedcoa[-1]),float(self.Ind[-1]),
			float(self.Indcoa[-1]),float(self.Pac[-1]),float(self.Paccoa[-1]),
			float(self.Ross[-1]),float(self.Rosscoa[-1]),float(self.Bell[-1]),float(self.Bellcoa[-1]))*1.1
		
		ymax = max(float(self.Wed[-1]),float(self.Wedcoa[-1]),float(self.Ind[-1]),
			 float(self.Indcoa[-1]),float(self.Pac[-1]),float(self.Paccoa[-1]),
			 float(self.Ross[-1]),float(self.Rosscoa[-1]),float(self.Bell[-1]),float(self.Bellcoa[-1]))*1.1
		
		if max(ymax,abs(ymin)) < 210:
			step = 25
		else:
			step = 50
		major_ticks = np.arange(-1000,1000,step)
		ax.set_yticks(major_ticks)
		plt.axis([0,len(self.Wed)-1,ymin,ymax])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		ax.legend(loc='center left',bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
		fig.tight_layout(pad=2)
		fig.subplots_adjust(right=0.85)
		fig.subplots_adjust(top=0.95)
		fig.subplots_adjust(bottom=0.08)
		
		fig.savefig('X:/Upload/AWP/South_AWP_region.png')
#		plt.show()
			
	def makeregiongraph_daily(self):
				
		fig = plt.figure(figsize=(14, 8))
		fig.suptitle('Daily Regional Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Sep','Oct','Nov','Dec','Jan', 'Feb', 'Mar']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-10,10,0.5)
		ax.set_yticks(major_ticks)
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.66, -0.06, 'https://sites.google.com/site/cryospherecomputing/awp',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		ax.grid(True)
		
		plt.plot( self.Wed_daily, color=(0.1,0.7,0.1),label='Weddel Sea',lw=2)
		plt.plot( self.Wedcoa_daily, color=(0.2,0.8,0.8),label='Weddel Sea Coast',lw=2)
		plt.plot( self.Ind_daily, color=(0.65,0.1,0.4),label='Indian Ocean',lw=2)
		plt.plot( self.Indcoa_daily, color=(0.5,0.5,0.5),label='Indian Ocean Coast',lw=2)
		plt.plot( self.Pac_daily, color=(0.9,0.9,0),label='Pacific Ocean',lw=2)
		plt.plot( self.Paccoa_daily, color=(0.9,0.1,0.1),label='Pacific Ocean Coast',lw=2)
		plt.plot( self.Ross_daily, color=(0,0,0.6),label='Ross Sea',lw=2)
		plt.plot( self.Rosscoa_daily, color=(1,0.6,0.2),label='Ross Sea Coast',lw=2)
		plt.plot( self.Bell_daily, color=(1,0.26,1),label='Bell-Amun Sea',lw=2)
		plt.plot( self.Bellcoa_daily, color=(0,0,0),label='Bell-Amun Sea Coast',lw=2)
		
		ymin = -3
		ymax = 4
		plt.axis([0,len(self.Wed_daily)-1,ymin,ymax])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		ax.legend(loc='center left',bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
		fig.tight_layout(pad=2)
		fig.subplots_adjust(right=0.85)
		fig.subplots_adjust(top=0.95)
		fig.subplots_adjust(bottom=0.08)
		
		fig.savefig('X:/Upload/AWP/South_AWP_region_day.png')
#		plt.show()
		
		
	def writetofile(self):
		'''writes data to a csv files'''
		with open('X:/Upload/AWP_data/South_AWP_NRT.csv', 'w') as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.CSVDaily))):
				writer.writerow([self.CSVDatum[x],self.CSVDaily[x],self.CSVCumu[x]])
				 
		with open('X:/Upload/AWP_data/South_AWP_NRT_regional.csv','w') as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.Wed))):
				writer.writerow([self.CSVDatum[x],self.Wed[x],self.Wedcoa[x],
				self.Ind[x],self.Indcoa[x],self.Pac[x],self.Paccoa[x],
				self.Ross[x],self.Rosscoa[x],self.Bell[x],self.Bellcoa[x]])
				
		with open('X:/Upload/AWP_data/South_AWP_NRT_regional_daily.csv', 'w') as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.Wed_daily))):
				writer.writerow([self.CSVDatum[x],self.Wed_daily[x],self.Wedcoa_daily[x],
				self.Ind_daily[x],self.Indcoa_daily[x],self.Pac_daily[x],self.Paccoa_daily[x],
				self.Ross_daily[x],self.Rosscoa_daily[x],self.Bell_daily[x],self.Bellcoa_daily[x]])
	
	def loadCSVdata (self):
		Yearcolnames = ['Date', 'Daily_MJ', 'Cumulative_kMJ']
		Yeardata = pandas.read_csv('X:/Upload/AWP_data/South_AWP_NRT.csv', names=Yearcolnames)
		self.CSVDatum = Yeardata.Date.tolist()
		self.CSVDaily = Yeardata.Daily_MJ.tolist()
		self.CSVCumu = Yeardata.Cumulative_kMJ.tolist()
		
	def loadCSVRegiondata (self):
		Yearcolnames = ['A','B','C','D','E','F','G','H','I','J','K']
		Yeardata = pandas.read_csv('X:/Upload/AWP_data/South_AWP_NRT_regional.csv', names=Yearcolnames)
		self.Wed = Yeardata.B.tolist()
		self.Wedcoa = Yeardata.C.tolist()
		self.Ind = Yeardata.D.tolist()
		self.Indcoa = Yeardata.E.tolist()
		self.Pac = Yeardata.F.tolist()
		self.Paccoa = Yeardata.G.tolist()
		self.Ross = Yeardata.H.tolist()
		self.Rosscoa = Yeardata.I.tolist()
		self.Bell = Yeardata.J.tolist()
		self.Bellcoa = Yeardata.K.tolist()

		Yearcolnames_daily = ['A','B','C','D','E','F','G','H','I','J','K']
		Yeardata_daily = pandas.read_csv('X:/Upload/AWP_data/South_AWP_NRT_regional_daily.csv', names=Yearcolnames_daily)
		self.Wed_daily = Yeardata_daily.B.tolist()
		self.Wedcoa_daily = Yeardata_daily.C.tolist()
		self.Ind_daily = Yeardata_daily.D.tolist()
		self.Indcoa_daily = Yeardata_daily.E.tolist()
		self.Pac_daily = Yeardata_daily.F.tolist()
		self.Paccoa_daily = Yeardata_daily.G.tolist()
		self.Ross_daily = Yeardata_daily.H.tolist()
		self.Rosscoa_daily = Yeardata_daily.I.tolist()
		self.Bell_daily = Yeardata_daily.J.tolist()
		self.Bellcoa_daily = Yeardata_daily.K.tolist()
			
	
	def automated (self,day,month,year):
		
		self.year = year
		self.month = month
		self.day = day
		
		if (month>8):
			self.index = int((month-1)*30.5)+day-264
		else:
			self.index = 102+int((month-1)*30.5)+day
		
		self.daycount = 1
		self.loadCSVdata()
		self.loadCSVRegiondata()
		self.dayloop()
		self.writetofile()
		self.makedailygraph()
		self.makecumugraph()
		self.makeregiongraph()
		self.makeregiongraph_daily()
		

action = Warming()
if __name__ == "__main__":
	print('main')
# =============================================================================
# 	action.loadCSVdata()
# 	action.loadCSVRegiondata()
# 	action.dayloop()
# 	action.writetofile()
# 	action.makeregiongraph()
# 	action.makeregiongraph_daily()
# =============================================================================

	action.automated(23,11,2018)

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