import numpy as np
import numpy.ma as ma
import csv
import matplotlib.pyplot as plt
#import multiprocessing


class Warming:

	def __init__  (self):
		self.year = 2017
		self.month = 9 # begin 20 september
		self.day = 22
		self.daycount = 181 #366year, 181 austral summer
		
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
		
		
		self.Wed_daily = ['Weddel Sea']
		self.Wedcoa_daily = ['Weddel Sea Coast']
		self.Ind_daily = ['Indian Ocean']
		self.Indcoa_daily = ['Indian Ocean Coast']
		self.Pac_daily = ['Pacific Ocean']
		self.Paccoa_daily = ['Pacific Ocean Coast']
		self.Ross_daily = ['Ross Sea']
		self.Rosscoa_daily = ['Ross Sea Coast']
		self.Bell_daily = ['Bell-Amun Sea']
		self.Bellcoa_daily = ['Bell-Amun Sea Coast']

	def masksload(self):
	
		self.regionmask = 'Masks/region_s_coast.msk'
		with open(self.regionmask, 'rb') as frmsk:
				self.mask = np.fromfile(frmsk, dtype=np.uint8)
		self.regmaskf = np.array(self.mask, dtype=float)
		
		self.areamask = 'Masks/pss25area_v3.dat'
		with open(self.areamask, 'rb') as famsk:
				self.mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(self.mask2, dtype=float)
		self.areamaskf = self.areamaskf /1000
		
		self.latmask = 'Masks/pss25lats_v3.dat'
		with open(self.latmask, 'rb') as flmsk:
				self.mask3 = np.fromfile(flmsk, dtype=np.int32)
		self.latmaskf = np.array(self.mask3, dtype=float)
		self.latmaskf = self.latmaskf /100000		
		
		self.latitudelist = [-50,-50.2,-50.4,-50.6,-50.8,-51,-51.2,-51.4,-51.6,-51.8,-52,-52.2,-52.4,-52.6,-52.8,-53,-53.2,-53.4,-53.6,-53.8,-54,-54.2,-54.4,-54.6,-54.8,-55,-55.2,-55.4,-55.6,-55.8,-56,-56.2,-56.4,-56.6,-56.8,-57,-57.2,-57.4,-57.6,-57.8,-58,-58.2,-58.4,-58.6,-58.8,-59,-59.2,-59.4,-59.6,-59.8,-60,-60.2,-60.4,-60.6,-60.8,-61,-61.2,-61.4,-61.6,-61.8,-62,-62.2,-62.4,-62.6,-62.8,-63,-63.2,-63.4,-63.6,-63.8,-64,-64.2,-64.4,-64.6,-64.8,-65,-65.2,-65.4,-65.6,-65.8,-66,-66.2,-66.4,-66.6,-66.8,-67,-67.2,-67.4,-67.6,-67.8,-68,-68.2,-68.4,-68.6,-68.8,-69,-69.2,-69.4,-69.6,-69.8,-70,-70.2,-70.4,-70.6,-70.8,-71,-71.2,-71.4,-71.6,-71.8,-72,-72.2,-72.4,-72.6,-72.8,-73,-73.2,-73.4,-73.6,-73.8,-74,-74.2,-74.4,-74.6,-74.8,-75,-75.2,-75.4,-75.6,-75.8,-76,-76.2,-76.4,-76.6,-76.8,-77,-77.2,-77.4,-77.6,-77.8,-78,-78.2,-78.4,-78.6,-78.8,-79,-79.2,-79.4,-79.6,-79.8,-80]
		self.latitudelist = np.loadtxt('Masks/Lattable_south_MJ.csv', delimiter=',')
		
	def dayloop(self):		
		self.icecumf = np.zeros(104912, dtype=float)
				
		for count in range (0,self.daycount,1):
			filename = 'DataFiles/NSIDC_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'_south.bin'
			filenamedav = 'DataFiles/Daily_Mean/NSIDC_Mean_'+str(self.month).zfill(2)+str(self.day).zfill(2)+'_south.bin'
			#filenamemax = 'Maximum/NSIDC_Max_'+str(self.month).zfill(2)+str(self.day).zfill(2)+'_south.bin'
			#filenamemin = 'Minimum/NSIDC_Min_'+str(self.month).zfill(2)+str(self.day).zfill(2)+'_south.bin'
			
			
			self.datum.append(str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
						
			with open(filenamedav, 'rb') as fr:
				iceav = np.fromfile(fr, dtype=np.uint8)
			try:	
				with open(filename, 'rb') as frr:
					ice2 = np.fromfile(frr, dtype=np.uint8)
			except:
				pass
			self.icedf = np.zeros(104912, dtype=float)
			self.iceavf = np.array(iceav, dtype=float)
			self.ice2f = np.array(ice2, dtype=float)
			
			
			self.albedosumdaily = np.zeros(104912, dtype=float)
			self.oceanpixareadaily = np.zeros(104912, dtype=float)
			self.albedosumcumu = np.zeros(104912, dtype=float)
			self.oceanpixareacumu = np.zeros(104912, dtype=float)
			
			self.ice2f = self.ice2f / 250
			self.iceavf = self.iceavf / 250
			
			self.regioncalc(count)
			
			if self.month == 3:
				if self.plottype == 'daily' or self.plottype == 'both':
					self.dailyloop(self.icedf,self.dailyenergy[count+1])
				if self.plottype == 'cumu' or self.plottype == 'both':
					self.cumulativeloop(self.icecumf,self.cumuenergy[count+1])
			
			

			#print('Progress: ',100*count/self.daycount)
			print(self.month, self.day)
			self.day = self.day+1
			count = count+1
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
		self.writetofile()	
		self.end = 'true'
		with open('AWP_anomaly_'+str(self.year)+'_s.bin', 'wb') as writecumu:
				icewr = writecumu.write(self.icecumf)
		self.cumulativeloop(self.icecumf,self.cumuenergy[count])
		self.fig2.savefig('Final_'+str(self.year)+'.png')
		plt.show()
			
	
	def regioncalc(self,count):
		
		Wed = []
		Wedcoa = []
		Ind = []
		Indcoa = []
		Pac = []
		Paccoa = []
		Ross = []
		Rosscoa = []
		Bel = []
		Belcoa = []
		
		
		Wed_daily = []
		Wedcoa_daily = []
		Ind_daily = []
		Indcoa_daily = []
		Pac_daily = []
		Paccoa_daily = []
		Ross_daily = []
		Rosscoa_daily = []
		Bel_daily = []
		Belcoa_daily = []
		
		
		Wed_area = []
		Wedcoa_area = []
		Ind_area = []
		Indcoa_area = []
		Pac_area = []
		Paccoa_area = []
		Ross_area = []
		Rosscoa_area = []
		Bel_area = []
		Belcoa_area = []
		
		
		for x in range (0,104912):
			if  1 < self.regmaskf[x] < 7 or 20 < self.regmaskf[x] < 27:	
				self.energycalc(x,count)
				

				if self.icedf[x] < 0 or self.icedf[x] >0:
					self.albedosumdaily[x] = self.icedf[x]*self.areamaskf[x]
					self.oceanpixareadaily[x] = self.areamaskf[x]
				
				if self.icecumf[x] < 0 or self.icecumf[x] >0:
					self.albedosumcumu[x] = self.icecumf[x]*self.areamaskf[x]
					self.oceanpixareacumu[x] = self.areamaskf[x]
						
					if self.regmaskf[x] == 2:
						Wed_daily.append  (self.albedosumdaily[x])
						Wed.append  (self.albedosumcumu[x])
						Wed_area.append (self.areamaskf[x])
					elif self.regmaskf[x] == 22:
						Wedcoa_daily.append  (self.albedosumdaily[x])
						Wedcoa.append  (self.albedosumcumu[x])
						Wedcoa_area.append (self.areamaskf[x])
					elif self.regmaskf[x] == 3:
						Ind_daily.append  (self.albedosumdaily[x])
						Ind.append  (self.albedosumcumu[x])
						Ind_area.append (self.areamaskf[x])
					elif self.regmaskf[x] == 23:
						Indcoa_daily.append  (self.albedosumdaily[x])
						Indcoa.append  (self.albedosumcumu[x])
						Indcoa_area.append (self.areamaskf[x])
					elif self.regmaskf[x] == 4:
						Pac_daily.append  (self.albedosumdaily[x])
						Pac.append  (self.albedosumcumu[x])
						Pac_area.append (self.areamaskf[x])
					elif self.regmaskf[x] == 24:
						Paccoa_daily.append  (self.albedosumdaily[x])
						Paccoa.append  (self.albedosumcumu[x])
						Paccoa_area.append (self.areamaskf[x])
					elif self.regmaskf[x] == 5:
						Ross_daily.append  (self.albedosumdaily[x])
						Ross.append  (self.albedosumcumu[x])
						Ross_area.append (self.areamaskf[x])
					elif self.regmaskf[x] == 25:
						Rosscoa_daily.append  (self.albedosumdaily[x])
						Rosscoa.append  (self.albedosumcumu[x])
						Rosscoa_area.append (self.areamaskf[x])
					elif self.regmaskf[x] == 6:
						Bel_daily.append  (self.albedosumdaily[x])
						Bel.append  (self.albedosumcumu[x])
						Bel_area.append (self.areamaskf[x])
					elif self.regmaskf[x] == 26:
						Belcoa_daily.append  (self.albedosumdaily[x])
						Belcoa.append  (self.albedosumcumu[x])
						Belcoa_area.append (self.areamaskf[x])		
						
			else:
				self.icedf[x] = 9999
				self.icecumf[x] =9999
			
			
		self.icedf = ma.masked_greater(self.icedf, 9998)
		self.icecumf = ma.masked_greater(self.icecumf, 9998)
		
			
		self.Wed.append  (round((sum(Wed)/sum(Wed_area)),3))
		self.Wedcoa.append  (round((sum(Wedcoa)/sum(Wedcoa_area)),3))
		self.Ind.append  (round((sum(Ind)/sum(Ind_area)),3))
		self.Indcoa.append  (round((sum(Indcoa)/sum(Indcoa_area)),3))
		self.Pac.append  (round((sum(Pac)/sum(Pac_area)),3))
		self.Paccoa.append  (round((sum(Paccoa)/sum(Paccoa_area)),3))
		self.Ross.append  (round((sum(Ross)/sum(Ross_area)),3))
		self.Rosscoa.append  (round((sum(Rosscoa)/sum(Rosscoa_area)),3))
		self.Bell.append  (round((sum(Bel)/sum(Bel_area)),3))
		self.Bellcoa.append  (round((sum(Belcoa)/sum(Belcoa_area)),3))
		
		self.Wed_daily.append  (round((sum(Wed_daily)/sum(Wed_area)),3))
		self.Wedcoa_daily.append  (round((sum(Wedcoa_daily)/sum(Wedcoa_area)),3))
		self.Ind_daily.append  (round((sum(Ind_daily)/sum(Ind_area)),3))
		self.Indcoa_daily.append  (round((sum(Indcoa_daily)/sum(Indcoa_area)),3))
		self.Pac_daily.append  (round((sum(Pac_daily)/sum(Pac_area)),3))
		self.Paccoa_daily.append  (round((sum(Paccoa_daily)/sum(Paccoa_area)),3))
		self.Ross_daily.append  (round((sum(Ross_daily)/sum(Ross_area)),3))
		self.Rosscoa_daily.append  (round((sum(Rosscoa_daily)/sum(Rosscoa_area)),3))
		self.Bell_daily.append  (round((sum(Bel_daily)/sum(Bel_area)),3))
		self.Bellcoa_daily.append  (round((sum(Belcoa_daily)/sum(Belcoa_area)),3))
		
		
		self.dailyenergy.append  (round(sum(self.albedosumdaily) / sum(self.oceanpixareadaily),3))
		self.cumuenergy.append  (round(sum(self.albedosumcumu) / sum(self.oceanpixareacumu),3))
		
	
		
	def energycalc(self,x,count):
		self.icedf[x] = self.iceavf[x]-self.ice2f[x]
				
		pixlat = min(-50,self.latmaskf[x])
		indexx = int(round((pixlat+50)*(-5)))
		kwh = self.latitudelist[indexx][count+1]
		self.icedf[x] = self.icedf[x]*kwh*0.8
		self.icecumf[x] = self.icecumf[x]+self.icedf[x]


	

	def dailyloop(self,icemap,icesum):		
		icemap = icemap.reshape(332, 316)
		icemap = icemap[10:300,30:310]
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
		self.fig.savefig('Daily_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		plt.pause(0.01)
		
	def cumulativeloop(self,icemap,icesum):		
		icemap = icemap.reshape(332, 316)
		icemap = icemap[10:300,30:310]
		cmap2 = plt.cm.coolwarm
		cmap2.set_bad('black',0.6)
		
		self.ax2.clear()
		self.ax2.set_title('Date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2))
		if self.end == 'true':
			self.ax2.set_title('Astronomical Summer '+str(self.year-1)+'/'+str(self.year-2000)) # -2000
		self.ax2.set_xlabel('Average: '+str(round(icesum,2))+' [MJ / 'r'$m^2$]')
		self.cax = self.ax2.imshow(icemap, interpolation='nearest', vmin=-1000, vmax=1000, cmap=cmap2)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 8, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 18, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.fig2.tight_layout(pad=2)
		self.fig2.savefig('Cumulative_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		plt.pause(0.01)
		
	def dailyorcumu(self):		
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

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA

# available years
# 1986-1993
# 2005-2017

'''
Pixel Value	Antarctic Region
2	Weddell Sea
3	Indian Ocean
4	Pacific Ocean
5	Ross Sea
6	Bellingshausen Amundsen Sea
11	Land
12	Coast

'''