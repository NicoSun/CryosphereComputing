import numpy as np
import numpy.ma as ma
import csv
import pandas
import matplotlib.pyplot as plt



class Warming:

	def __init__  (self):
		self.year = 2017
		self.month = 3 # begin 20 march
		self.day = 20
		self.daycount = 5 #186 summer
		self.index = 0
		
		'''
		self.SoO = ['Sea_of_Okhotsk']
		self.Bers = ['Bering_Sea']
		self.HB = ['Hudson_Bay']
		self.BB = ['Baffin_Bay']
		self.EG = ['East_Greenland_Sea']
		self.BaS = ['Barents_Sea']
		self.KS = ['Kara_Sea']
		self.LS = ['Laptev_Sea']
		self.ES = ['East_Siberian_Sea']
		self.CS = ['Chukchi_Sea']
		self.BeaS = ['Beaufort_Sea']
		self.CA = ['Canadian_Archipelago']
		self.AB = ['Central_Arctic']
		'''		
		self.plottype = 'both'
		self.labelfont = {'fontname':'Arial'}
		self.masksload()
		self.dailyorcumu()
		
		

	def masksload(self):
	
		self.regionmask = 'X:/NSIDC/Masks/Arctic_region_mask.bin'
		with open(self.regionmask, 'rb') as frmsk:
				mask = np.fromfile(frmsk, dtype=np.uint32)
		self.regmaskf = np.array(mask, dtype=float)
		
		self.areamask = 'X:/NSIDC/Masks/psn25area_v3.dat'
		with open(self.areamask, 'rb') as famsk:
				mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(mask2, dtype=float)
		self.areamaskf = self.areamaskf /1000
		
		self.latmask = 'X:/NSIDC/Masks/psn25lats_v3.dat'
		with open(self.latmask, 'rb') as flmsk:
				mask3 = np.fromfile(flmsk, dtype=np.uint32)
		self.latmaskf = np.array(mask3, dtype=float)
		self.latmaskf = self.latmaskf /100000		
		
		#latititudes loaded: [40,40.2,40.4,40.6,40.8,41,41.2,41.4,41.6,41.8,42,42.2,42.4,42.6,42.8,43,43.2,43.4,43.6,43.8,44,44.2,44.4,44.6,44.8,45,45.2,45.4,45.6,45.8,46,46.2,46.4,46.6,46.8,47,47.2,47.4,47.6,47.8,48,48.2,48.4,48.6,48.8,49,49.2,49.4,49.6,49.8,50,50.2,50.4,50.6,50.8,51,51.2,51.4,51.6,51.8,52,52.2,52.4,52.6,52.8,53,53.2,53.4,53.6,53.8,54,54.2,54.4,54.6,54.8,55,55.2,55.4,55.6,55.8,56,56.2,56.4,56.6,56.8,57,57.2,57.4,57.6,57.8,58,58.2,58.4,58.6,58.8,59,59.2,59.4,59.6,59.8,60,60.2,60.4,60.6,60.8,61,61.2,61.4,61.6,61.8,62,62.2,62.4,62.6,62.8,63,63.2,63.4,63.6,63.8,64,64.2,64.4,64.6,64.8,65,65.2,65.4,65.6,65.8,66,66.2,66.4,66.6,66.8,67,67.2,67.4,67.6,67.8,68,68.2,68.4,68.6,68.8,69,69.2,69.4,69.6,69.8,70,70.2,70.4,70.6,70.8,71,71.2,71.4,71.6,71.8,72,72.2,72.4,72.6,72.8,73,73.2,73.4,73.6,73.8,74,74.2,74.4,74.6,74.8,75,75.2,75.4,75.6,75.8,76,76.2,76.4,76.6,76.8,77,77.2,77.4,77.6,77.8,78,78.2,78.4,78.6,78.8,79,79.2,79.4,79.6,79.8,80,80.2,80.4,80.6,80.8,81,81.2,81.4,81.6,81.8,82,82.2,82.4,82.6,82.8,83,83.2,83.4,83.6,83.8,84,84.2,84.4,84.6,84.8,85,85.2,85.4,85.6,85.8,86,86.2,86.4,86.6,86.8,87,87.2,87.4,87.6,87.8,88,88.2,88.4,88.6,88.8,89,89.2,89.4,89.6,89.8,90]
		self.latitudelist = np.loadtxt('X:/NSIDC/Masks/Lattable_MJ.csv', delimiter=',')
		
	def dayloop(self):		
		self.icecumf = np.zeros(136192, dtype=float)
		countmax = self.index+self.daycount
		
		with open('X:/Upload/AWP_data/North_AWP_Cumulative.bin', 'rb') as readcumu:
			self.icecumf = np.fromfile(readcumu, dtype=float)
				
		for count in range (self.index,countmax,1):
			filename = 'X:/NSIDC/DataFiles/NSIDC_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.bin'
			filenamedav = 'X:/NSIDC/DataFiles/Daily_Mean/NSIDC_Mean_'+str(self.month).zfill(2)+str(self.day).zfill(2)+'.bin'
			#filenamemax = 'X:/NSIDC/DataFiles/Maximum/NSIDC_Max_'+str(self.month).zfill(2)+str(self.day).zfill(2)+'_south.bin'
			#filenamemin = 'X:/NSIDC/DataFiles/Minimum/NSIDC_Min_'+str(self.month).zfill(2)+str(self.day).zfill(2)+'_south.bin'
			
			
			with open(filenamedav, 'rb') as fr:
				iceav = np.fromfile(fr, dtype=np.uint8)
			with open(filename, 'rb') as frr:
				ice2 = np.fromfile(frr, dtype=np.uint8)
		
			self.waterdf = np.zeros(136192, dtype=float)
			self.icedf = np.zeros(136192, dtype=float)
			self.iceavf = np.array(iceav, dtype=float)
			self.ice2f = np.array(ice2, dtype=float)
			
			self.albedosumdaily = np.zeros(136192, dtype=float)
			self.oceanpixareadaily = np.zeros(136192, dtype=float)
			self.albedosumcumu = np.zeros(136192, dtype=float)
			self.oceanpixareacumu = np.zeros(136192, dtype=float)
			
			self.ice2f = self.ice2f / 250
			self.iceavf = self.iceavf / 250
			
			self.regioncalc(count)
			
			
			if self.plottype == 'daily' or self.plottype == 'both':
				self.dailyloop(self.icedf,self.CSVDaily[-1])
			if self.plottype == 'cumu' or self.plottype == 'both':
				self.cumulativeloop(self.icecumf,self.CSVCumu[-1])
			
			print(count)
			self.CSVDatum.append(str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
			count = count+1			
			if count < countmax:
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
				
		with open('X:/Upload/AWP_data/North_AWP_Cumulative.bin', 'wb') as writecumu:
				icewr = writecumu.write(self.icecumf)
		self.fig2.savefig('X:/Upload/AWP/North_AWP_map_cumu.png')
		self.fig.savefig('X:/Upload/AWP/North_AWP_map_daily.png')
		#plt.show()
	
	def regioncalc(self,count):
		
		SoO = []
		Bers = []
		HB = []
		BB = []
		EG = []
		BaS = []
		KS = []
		LS = []
		ES = []
		CS = []
		BeaS = []
		CA = []
		AB = []
		
		SoO_daily = []
		Bers_daily = []
		HB_daily = []
		BB_daily = []
		EG_daily = []
		BaS_daily = []
		KS_daily = []
		LS_daily = []
		ES_daily = []
		CS_daily = []
		BeaS_daily = []
		CA_daily = []
		AB_daily = []
		
		SoOarea = []
		Bersarea = []
		HBarea = []
		BBarea = []
		EGarea = []
		BaSarea = []
		KSarea = []
		LSarea = []
		ESarea = []
		CSarea = []
		BeaSarea = []
		CAarea = []
		ABarea = []
		
		for x in range (0,136192):
			if  1 < self.regmaskf[x] < 5  or 5 < self.regmaskf[x] < 16:	
				self.energycalc(x,count)
				

				if self.icedf[x] < 0 or self.icedf[x] >0:
					self.albedosumdaily[x] = self.icedf[x]*self.areamaskf[x]
					self.oceanpixareadaily[x] = self.areamaskf[x]
				
				if self.icecumf[x] < 0 or self.icecumf[x] >0:
					self.albedosumcumu[x] = self.icecumf[x]*self.areamaskf[x]
					self.oceanpixareacumu[x] = self.areamaskf[x]
						
					if self.regmaskf[x] == 2:
						SoO_daily.append  (self.albedosumdaily[x])
						SoO.append  (self.albedosumcumu[x])
						SoOarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 3:
						Bers_daily.append  (self.albedosumdaily[x])
						Bers.append  (self.albedosumcumu[x])
						Bersarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 4:
						HB_daily.append  (self.albedosumdaily[x])
						HB.append  (self.albedosumcumu[x])
						HBarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 6:
						BB_daily.append  (self.albedosumdaily[x])
						BB.append  (self.albedosumcumu[x])
						BBarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 7:
						EG_daily.append  (self.albedosumdaily[x])
						EG.append  (self.albedosumcumu[x])
						EGarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 8:
						BaS_daily.append  (self.albedosumdaily[x])
						BaS.append  (self.albedosumcumu[x])
						BaSarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 9:
						KS_daily.append  (self.albedosumdaily[x])
						KS.append  (self.albedosumcumu[x])
						KSarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 10:
						LS_daily.append  (self.albedosumdaily[x])
						LS.append  (self.albedosumcumu[x])
						LSarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 11:
						ES_daily.append  (self.albedosumdaily[x])
						ES.append  (self.albedosumcumu[x])
						ESarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 12:
						CS_daily.append  (self.albedosumdaily[x])
						CS.append  (self.albedosumcumu[x])
						CSarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 13:
						BeaS_daily.append  (self.albedosumdaily[x])
						BeaS.append  (self.albedosumcumu[x])
						BeaSarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 14:
						CA_daily.append  (self.albedosumdaily[x])
						CA.append  (self.albedosumcumu[x])
						CAarea.append (self.areamaskf[x])
					elif self.regmaskf[x] == 15:
						AB_daily.append  (self.albedosumdaily[x])
						AB.append  (self.albedosumcumu[x])	
						ABarea.append (self.areamaskf[x])		
						

			
			elif  0 <= self.regmaskf[x] < 2 or self.regmaskf[x] == 5:
				self.icedf[x] = 0
			else:
				self.icedf[x] = 9999
				self.icecumf[x] =9999
			
			
		self.icedf = ma.masked_greater(self.icedf, 9998)
		self.icecumf = ma.masked_greater(self.icecumf, 9998)
		
			
		self.SoO.append  (round((sum(SoO)/sum(SoOarea)),3))
		self.Bers.append  (round((sum(Bers)/sum(Bersarea)),3))
		self.HB.append  (round((sum(HB)/sum(HBarea)),3))
		self.BB.append  (round((sum(BB)/sum(BBarea)),3))
		self.EG.append  (round((sum(EG)/sum(EGarea)),3))
		self.BaS.append  (round((sum(BaS)/sum(BaSarea)),3))
		self.KS.append  (round((sum(KS)/sum(KSarea)),3))
		self.LS.append  (round((sum(LS)/sum(LSarea)),3))
		self.ES.append  (round((sum(ES)/sum(ESarea)),3))
		self.CS.append  (round((sum(CS)/sum(CSarea)),3))
		self.BeaS.append  (round((sum(BeaS)/sum(BeaSarea)),3))
		self.CA.append  (round((sum(CA)/sum(CAarea)),3))
		self.AB.append  (round((sum(AB)/sum(ABarea)),3))
		
		self.SoO_daily.append  (round((sum(SoO_daily)/sum(SoOarea)),3))
		self.Bers_daily.append  (round((sum(Bers_daily)/sum(Bersarea)),3))
		self.HB_daily.append  (round((sum(HB_daily)/sum(HBarea)),3))
		self.BB_daily.append  (round((sum(BB_daily)/sum(BBarea)),3))
		self.EG_daily.append  (round((sum(EG_daily)/sum(EGarea)),3))
		self.BaS_daily.append  (round((sum(BaS_daily)/sum(BaSarea)),3))
		self.KS_daily.append  (round((sum(KS_daily)/sum(KSarea)),3))
		self.LS_daily.append  (round((sum(LS_daily)/sum(LSarea)),3))
		self.ES_daily.append  (round((sum(ES_daily)/sum(ESarea)),3))
		self.CS_daily.append  (round((sum(CS_daily)/sum(CSarea)),3))
		self.BeaS_daily.append  (round((sum(BeaS_daily)/sum(BeaSarea)),3))
		self.CA_daily.append  (round((sum(CA_daily)/sum(CAarea)),3))
		self.AB_daily.append  (round((sum(AB_daily)/sum(ABarea)),3))
		
		self.CSVDaily.append  (int(round(1000*sum(self.albedosumdaily) / sum(self.oceanpixareadaily))))
		self.CSVCumu.append  (round((sum(self.albedosumcumu) / sum(self.oceanpixareacumu)),3))
		
	
		
	def energycalc(self,x,count):
		self.icedf[x] = self.iceavf[x]-self.ice2f[x]
				
		pixlat = max(40,self.latmaskf[x])
		indexx = int(round((pixlat-40)*5))
		MJ = self.latitudelist[indexx][count+1]
		if self.ice2f[x]<=1:
			self.icedf[x] = self.icedf[x]*MJ*0.8
			self.icecumf[x] = self.icecumf[x]+self.icedf[x]

	def dailyloop(self,icemap,icesum):		
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		cmapd = plt.cm.coolwarm
		cmapd.set_bad('black',0.6)
		#print('its called')
		
		self.ax.clear()
		self.ax.set_title('Date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2))
		self.ax.set_xlabel('Average: '+str(icesum)+' [KJ / 'r'$m^2$]',**self.labelfont)
		self.ax.imshow(icemap, interpolation='nearest', vmin=-18, vmax=18, cmap=cmapd)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 8, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax.text(2, 18, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.ax.text(-0.04, 0.44, 'https://sites.google.com/site/cryospherecomputing/awp',
        transform=self.ax.transAxes,rotation='vertical',
        color='grey', fontsize=10)
		
		self.fig.tight_layout(pad=2)
		self.fig.canvas.draw()
		#self.fig.savefig('Animation/Daily_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		
		
	def cumulativeloop(self,icemap,icesum):		
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		cmap2 = plt.cm.coolwarm
		cmap2.set_bad('black',0.6)
		
		self.ax2.clear()
		self.ax2.set_title('Date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2))
		self.ax2.set_xlabel('Average: '+str(icesum)+' [MJ / 'r'$m^2$]',**self.labelfont)
		self.ax2.imshow(icemap, interpolation='nearest', vmin=-800, vmax=800, cmap=cmap2)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 8, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 18, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(-0.04, 0.44, 'https://sites.google.com/site/cryospherecomputing/awp',
        transform=self.ax2.transAxes,rotation='vertical',
        color='grey', fontsize=10)
		self.fig2.tight_layout(pad=2)
		self.fig2.canvas.draw()
		#self.fig2.savefig('Animation/Cumulative_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		
		
	def dailyorcumu(self):		
		self.icenull = np.zeros(136192, dtype=float)
		self.icenull = self.icenull.reshape(448, 304)
		
		if self.plottype == 'daily' or  self.plottype == 'both':
			self.fig, self.ax = plt.subplots(figsize=(8, 10))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=-18, vmax=18, cmap=plt.cm.coolwarm)
			self.cbar = self.fig.colorbar(self.cax, ticks=[-18,-9, 0,9, 18]).set_label(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
			self.title = self.fig.suptitle('Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold',x=0.42)
			self.dailyloop(self.icenull,0)
		if self.plottype == 'cumu' or self.plottype == 'both':
			self.fig2, self.ax2 = plt.subplots(figsize=(8, 10))
			self.cax2 = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=-800, vmax=800, cmap=plt.cm.coolwarm)
			self.cbar2 = self.fig2.colorbar(self.cax2, ticks=[-800,-400, 0,400, 800]).set_label(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
			self.title2 = self.fig2.suptitle('Cumulative Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold',x=0.42)
			self.cumulativeloop(self.icenull,0)
	
	def writetofile(self):
		
		with open('X:/Upload/AWP_data/Arctic_AWP_NRT.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for writeing in range(0,(len(self.CSVDaily))):
				writer.writerow([self.CSVDatum[writeing],self.CSVDaily[writeing],self.CSVCumu[writeing]])
				 
		with open('X:/Upload/AWP_data/Arctic_AWP_NRT_regional.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for writeing in range(0,(len(self.SoO))):
				writer.writerow([self.CSVDatum[writeing],self.SoO[writeing],self.Bers[writeing],
				self.HB[writeing],self.BB[writeing],self.EG[writeing],self.BaS[writeing],
				self.KS[writeing],self.LS[writeing],self.ES[writeing],self.CS[writeing],
				self.BeaS[writeing],self.CA[writeing],self.AB[writeing]])
				
		with open('X:/Upload/AWP_data/Arctic_AWP_NRT_regional_daily.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for writeing in range(0,(len(self.SoO_daily))):
				writer.writerow([self.CSVDatum[writeing],self.SoO_daily[writeing],self.Bers_daily[writeing],
				self.HB_daily[writeing],self.BB_daily[writeing],self.EG_daily[writeing],self.BaS_daily[writeing],
				self.KS_daily[writeing],self.LS_daily[writeing],self.ES_daily[writeing],self.CS_daily[writeing],
				self.BeaS_daily[writeing],self.CA_daily[writeing],self.AB_daily[writeing]])
		
	def makedailygraph(self):
		
		Climatecolnames = ['Date', 'C2007', 'C2008', 'C2009', 'C2010', 'C2011', 'C2012', 'C2013', 'C2014', 'C2015','C2016','C2017']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Arctic_AWP_daily.csv', names=Climatecolnames,header=0)
		Date = Climatedata.Date.tolist()
		
		C2007 = Climatedata.C2007.tolist()
		C2008 = Climatedata.C2008.tolist()
		C2009 = Climatedata.C2009.tolist()
		C2010 = Climatedata.C2010.tolist()
		C2011 = Climatedata.C2011.tolist()
		C2012 = Climatedata.C2012.tolist()
		C2013 = Climatedata.C2013.tolist()
		C2014 = Climatedata.C2014.tolist()
		C2015 = Climatedata.C2015.tolist()
		C2016 = Climatedata.C2016.tolist()
		C2017 = Climatedata.C2017.tolist()		
		
		fig = plt.figure(figsize=(14, 8))
		fig.suptitle('Daily Pan Arctic Albedo-Warming Values (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel(''r'$ \Delta$ clear sky energy absorption in [KJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-2000,2000,500)
		ax.set_yticks(major_ticks)
		
		ax.text(0.01, -0.06, 'Last date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.66, -0.06, 'https://sites.google.com/site/cryospherecomputing/awp',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		ax.grid(True)
		plt.plot( C2008, color=(0.65,0.1,0.34),label='2008',lw=1)
		plt.plot( C2009, color=(0.2,0.8,0.2),label='2009',lw=1)
		plt.plot( C2010, color=(0.5,0.5,0.5),label='2010',lw=1)
		plt.plot( C2011, color=(0.9,0.9,0),label='2011',lw=1)
		plt.plot( C2012, color=(0.9,0.1,0.1),label='2012',lw=1)
		plt.plot( C2013, color=(0.4,0,0.4),label='2013',lw=1)
		plt.plot( C2014, color=(0,0,0.6),label='2014',lw=1)
		plt.plot( C2015, color=(0.55,0.27,0.08),label='2015',lw=1)
		plt.plot( C2016, color=(1,0.6,0.2),label='2016',lw=1)
		plt.plot( C2017, color=(0.2,0.8,0.8),label='2017',lw=1)
		plt.plot( self.CSVDaily, color='black',label='2018',lw=2)
		
		ymin = -1600
		ymax = 1600
		plt.axis([0,186,ymin,ymax])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		lgd = ax.legend(loc='center left',bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
		fig.tight_layout(pad=2)
		fig.subplots_adjust(right=0.9)
		fig.subplots_adjust(top=0.95)
		fig.savefig('X:/Upload/AWP/North_AWP_daily.png',bbox_extra_artists=(lgd,))

	
	def makecumugraph(self):
		
		Climatecolnames = ['Date','C2007', 'C2008', 'C2009', 'C2010', 'C2011', 'C2012', 'C2013', 'C2014', 'C2015','C2016','C2017']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Arctic_AWP_cumu.csv', names=Climatecolnames,header=0)
		C2007 = Climatedata.C2007.tolist()
		C2008 = Climatedata.C2008.tolist()
		C2009 = Climatedata.C2009.tolist()
		C2010 = Climatedata.C2010.tolist()
		C2011 = Climatedata.C2011.tolist()
		C2012 = Climatedata.C2012.tolist()
		C2013 = Climatedata.C2013.tolist()
		C2014 = Climatedata.C2014.tolist()
		C2015 = Climatedata.C2015.tolist()
		C2016 = Climatedata.C2016.tolist()
		C2017 = Climatedata.C2017.tolist()
				
		fig = plt.figure(figsize=(14, 8))
		fig.suptitle('Cumulative Pan Arctic Albedo-Warming Values (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-200,200,20)
		ax.set_yticks(major_ticks)
		
		ax.text(0.01, -0.06, 'Last date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.66, -0.06, 'https://sites.google.com/site/cryospherecomputing/awp',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		ax.grid(True)			
		plt.plot( C2008, color=(0.65,0.1,0.4),label='2008',lw=2)
		plt.plot( C2009, color=(0.2,0.8,0.2),label='2009',lw=2)
		plt.plot( C2010, color=(0.5,0.5,0.5),label='2010',lw=2)
		plt.plot( C2011, color=(0.9,0.9,0),label='2011',lw=2)
		plt.plot( C2012, color=(0.9,0.1,0.1),label='2012',lw=2)
		plt.plot( C2013, color=(0.4,0,0.4),label='2013',lw=2)
		plt.plot( C2014, color=(0,0,0.6),label='2014',lw=2)
		plt.plot( C2015, color=(0.55,0.27,0.08),label='2015',lw=2)
		plt.plot( C2016, color=(1,0.6,0.2),label='2016',lw=2)
		plt.plot( C2017, color=(0.2,0.8,0.8),label='2017',lw=2)
		plt.plot( self.CSVCumu, color='black',label='2018',lw=2)
		
		ymin = -80
		ymax = 65
		plt.axis([0,186,ymin,ymax])
		
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		lgd = ax.legend(loc='center left',bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
		fig.tight_layout(pad=2)
		fig.subplots_adjust(right=0.9)
		fig.subplots_adjust(top=0.95)
		#fig.subplots_adjust(bottom=0.1)
		fig.savefig('X:/Upload/AWP/North_AWP_cumu.png')

			
	def makeregiongraph(self):
				
		del self.SoO[0],self.Bers[0],self.HB[0],self.BB[0],self.EG[0],self.BaS[0],self.KS[0],self.LS[0],self.ES[0],self.CS[0],self.BeaS[0],self.CA[0], self.AB[0]
		
		
		fig = plt.figure(figsize=(14, 8))
		fig.suptitle(str(self.year)+' Cumulative Regional Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-800,800,25)
		ax.set_yticks(major_ticks)
		
		ax.text(0.01, -0.06, 'Last date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.66, -0.06, 'https://sites.google.com/site/cryospherecomputing/awp',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		ax.grid(True)
		
		plt.plot( self.SoO, color=(0.1,0.7,0.1),label='Sea of Okhotsk',lw=2)
		plt.plot( self.Bers, color=(0.2,0.8,0.8),label='Bering Sea',lw=2)
		plt.plot( self.HB, color=(0.65,0.1,0.4),label='Hudson Bay',lw=2)
		plt.plot( self.BB, color=(0.2,0.8,0.2),label='Baffin Bay',lw=2)
		plt.plot( self.EG, color=(0.5,0.5,0.5),label='East Greenland',lw=2)
		plt.plot( self.BaS, color=(0.9,0.9,0),label='Barents Sea',lw=2)
		plt.plot( self.KS, color=(0.9,0.1,0.1),label='Kara Sea',lw=2)
		plt.plot( self.LS, color=(0.4,0,0.4),label='Laptev Sea',lw=2)
		plt.plot( self.ES, color=(0,0,0.6),label='East. Siberian',lw=2)
		plt.plot( self.CS, color=(0.55,0.27,0.08),label='Chukchi',lw=2)
		plt.plot( self.BeaS, color=(1,0.6,0.2),label='Beaufort Sea',lw=2)
		plt.plot( self.CA, color=(1,0.26,1),label='Can. Archipelago',lw=2)
		plt.plot( self.AB, color='black',label='Central Arctic',lw=2)
		
		ymin = min(float(self.SoO[-1]),float(self.Bers[-1]),float(self.HB[-1]),float(self.BB[-1]),float(self.EG[-1]),float(self.BaS[-1]),
		float(self.KS[-1]),float(self.LS[-1]),float(self.ES[-1]),float(self.CS[-1]),float(self.BeaS[-1]),float(self.CA[-1]),float(self.AB[-1]),)*1.1
		
		ymax = max(float(self.SoO[-1]),float(self.Bers[-1]),float(self.HB[-1]),float(self.BB[-1]),float(self.EG[-1]),float(self.BaS[-1]),
		float(self.KS[-1]),float(self.LS[-1]),float(self.ES[-1]),float(self.CS[-1]),float(self.BeaS[-1]),float(self.CA[-1]),float(self.AB[-1]),)*1.1
		plt.axis([0,len(self.SoO),ymin,ymax])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		lgd = ax.legend(loc='center left',bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
		fig.tight_layout(pad=2)
		fig.subplots_adjust(right=0.85)
		fig.subplots_adjust(top=0.95)
		#fig.subplots_adjust(bottom=0.1)
		fig.savefig('X:/Upload/AWP/North_AWP_region.png')

			
	def makeregiongraph_daily(self):
				
		del self.SoO_daily[0],self.Bers_daily[0],self.HB_daily[0],self.BB_daily[0],self.EG_daily[0],self.BaS_daily[0],self.KS_daily[0],self.LS_daily[0],self.ES_daily[0],self.CS_daily[0],self.BeaS_daily[0],self.CA_daily[0], self.AB_daily[0]
		
		
		fig = plt.figure(figsize=(14, 8))
		fig.suptitle(str(self.year)+' Daily Regional Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-10,10,0.5)
		ax.set_yticks(major_ticks)
		
		ax.text(0.01, -0.06, 'Last date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.55, -0.06, 'https://sites.google.com/site/cryospherecomputing/warming-potential',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		ax.grid(True)
		
		plt.plot( self.SoO_daily, color=(0.1,0.7,0.1),label='Sea of Okhotsk',lw=2)
		plt.plot( self.Bers_daily, color=(0.2,0.8,0.8),label='Bering Sea',lw=2)
		plt.plot( self.HB_daily, color=(0.65,0.1,0.4),label='Hudson Bay',lw=2)
		plt.plot( self.BB_daily, color=(0.2,0.8,0.2),label='Baffin Bay',lw=2)
		plt.plot( self.EG_daily, color=(0.5,0.5,0.5),label='East Greenland',lw=2)
		plt.plot( self.BaS_daily, color=(0.9,0.9,0),label='Barents Sea',lw=2)
		plt.plot( self.KS_daily, color=(0.9,0.1,0.1),label='Kara Sea',lw=2)
		plt.plot( self.LS_daily, color=(0.4,0,0.4),label='Laptev Sea',lw=2)
		plt.plot( self.ES_daily, color=(0,0,0.6),label='East. Siberian',lw=2)
		plt.plot( self.CS_daily, color=(0.55,0.27,0.08),label='Chukchi',lw=2)
		plt.plot( self.BeaS_daily, color=(1,0.6,0.2),label='Beaufort Sea',lw=2)
		plt.plot( self.CA_daily, color=(1,0.26,1),label='Can. Archipelago',lw=2)
		plt.plot( self.AB_daily, color='black',label='Central Arctic',lw=2)
		
		ymin = -5.2
		ymax = 5.2
		plt.axis([0,len(self.SoO),ymin,ymax])
		plt.axis([0,len(self.SoO_daily),ymin,ymax])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		lgd = ax.legend(loc='center left',bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
		fig.tight_layout(pad=2)
		fig.subplots_adjust(right=0.85)
		fig.subplots_adjust(top=0.95)
		#fig.subplots_adjust(bottom=0.1)
		fig.savefig('X:/Upload/AWP/North_AWP_region_daily.png')

	
	def loadCSVdata (self):
		Yearcolnames = ['Date', 'Daily_Wh', 'Cumulative_kWh']
		Yeardata = pandas.read_csv('X:/Upload/AWP_data/Arctic_AWP_NRT.csv', names=Yearcolnames)
		self.CSVDatum = Yeardata.Date.tolist()
		self.CSVDaily = Yeardata.Daily_Wh.tolist()
		self.CSVCumu = Yeardata.Cumulative_kWh.tolist()
	
	
	def loadCSVRegiondata (self):
		Yearcolnames = ['Sea_of_Okhotsk', 'Berling_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
		Yeardata = pandas.read_csv('X:/Upload/AWP_data/Arctic_AWP_NRT_regional.csv', names=Yearcolnames)
		self.SoO = Yeardata.Sea_of_Okhotsk.tolist()
		self.Bers = Yeardata.Berling_Sea.tolist()
		self.HB = Yeardata.Hudson_Bay.tolist()
		self.BB = Yeardata.Baffin_Bay.tolist()
		self.EG = Yeardata.East_Greenland_Sea.tolist()
		self.BaS = Yeardata.Barents_Sea.tolist()
		self.KS = Yeardata.Kara_Sea.tolist()
		self.LS = Yeardata.Laptev_Sea.tolist()
		self.ES = Yeardata.East_Siberian_Sea.tolist()
		self.CS = Yeardata.Chukchi_Sea.tolist()
		self.BeaS = Yeardata.Beaufort_Sea.tolist()
		self.CA = Yeardata.Canadian_Archipelago.tolist()
		self.AB = Yeardata.Central_Arctic.tolist()
		
		Yearcolnames_daily = ['Sea_of_Okhotsk', 'Berling_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
		Yeardata_daily = pandas.read_csv('X:/Upload/AWP_data/Arctic_AWP_NRT_regional_daily.csv', names=Yearcolnames_daily)
		self.SoO_daily = Yeardata_daily.Sea_of_Okhotsk.tolist()
		self.Bers_daily = Yeardata_daily.Berling_Sea.tolist()
		self.HB_daily = Yeardata_daily.Hudson_Bay.tolist()
		self.BB_daily = Yeardata_daily.Baffin_Bay.tolist()
		self.EG_daily = Yeardata_daily.East_Greenland_Sea.tolist()
		self.BaS_daily = Yeardata_daily.Barents_Sea.tolist()
		self.KS_daily = Yeardata_daily.Kara_Sea.tolist()
		self.LS_daily = Yeardata_daily.Laptev_Sea.tolist()
		self.ES_daily = Yeardata_daily.East_Siberian_Sea.tolist()
		self.CS_daily = Yeardata_daily.Chukchi_Sea.tolist()
		self.BeaS_daily = Yeardata_daily.Beaufort_Sea.tolist()
		self.CA_daily = Yeardata_daily.Canadian_Archipelago.tolist()
		self.AB_daily = Yeardata_daily.Central_Arctic.tolist()
	
	
	
	def automated (self,day,month,year):
		
		self.year = year
		self.month = month
		self.day = day
		
		print(self.day,self.month,self.year)
		
		
		self.index = int((month-1)*30.5)+day-80
		
		
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
	#action.loadCSVdata()
	#action.loadCSVRegiondata()
	#action.dayloop()
	#action.makedailygraph()
	#action.makecumugraph()
	#action.makeregiongraph()
	#action.makeregiongraph_daily()
	
	action.automated(20,3,2018) #note substract xx days from last available day

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA