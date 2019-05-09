import numpy as np
import numpy.ma as ma
import csv
import matplotlib.pyplot as plt


class Warming:

	def __init__  (self):
		self.year = 2018
		self.month = 3
		self.day = 20
		self.daycount = 109 #366year, 186summer
		
		self.datum = ['Date']
		self.dailyenergy = ['Daily KJ/m2']
		self.cumuenergy = ['Cumulative MJ/m2']
		
		self.SoO = ['Sea of Okhotsk']
		self.Bers = ['Berling Sea']
		self.HB = ['Hudson Bay']
		self.BB = ['Baffin Bay']
		self.EG = ['East Greenland Sea']
		self.BaS = ['Barents Sea']
		self.KS = ['Kara Sea']
		self.LS = ['Laptev Sea']
		self.ES = ['East Siberian Sea']
		self.CS = ['Chukchi Sea']
		self.BeaS = ['Beaufort Sea']
		self.CA = ['Canadian Archipelago']
		self.AB = ['Central Arctic']
		
		self.SoO_daily = ['Sea of Okhotsk']
		self.Bers_daily = ['Berling Sea']
		self.HB_daily = ['Hudson Bay']
		self.BB_daily = ['Baffin Bay']
		self.EG_daily = ['East Greenland Sea']
		self.BaS_daily = ['Barents Sea']
		self.KS_daily = ['Kara Sea']
		self.LS_daily = ['Laptev Sea']
		self.ES_daily = ['East Siberian Sea']
		self.CS_daily = ['Chukchi Sea']
		self.BeaS_daily = ['Beaufort Sea']
		self.CA_daily = ['Canadian Archipelago']
		self.AB_daily = ['Central Arctic']
		
		self.labelfont = {'fontname':'Arial'}
		self.plottype = 'both' #daily, cumu, both
		self.end = 'false'
		self.masksload()
		self.dailyorcumu()

	def masksload(self):
	
		self.regionmask = 'Masks/Arctic_region_mask.bin'
		with open(self.regionmask, 'rb') as frmsk:
				self.mask = np.fromfile(frmsk, dtype=np.uint32)
		self.regmaskf = np.array(self.mask, dtype=float)
		
		self.areamask = 'Masks/psn25area_v3.dat'
		with open(self.areamask, 'rb') as famsk:
				self.mask2 = np.fromfile(famsk, dtype=np.uint32)
		self.areamaskf = np.array(self.mask2, dtype=float)
		self.areamaskf = self.areamaskf /1000
		
		self.latmask = 'Masks/psn25lats_v3.dat'
		with open(self.latmask, 'rb') as flmsk:
				self.mask3 = np.fromfile(flmsk, dtype=np.uint32)
		self.latmaskf = np.array(self.mask3, dtype=float)
		self.latmaskf = self.latmaskf /100000		
		
		self.latitudelist = np.loadtxt('Masks/Lattable_MJ.csv', delimiter=',')
		
		self.maskview(self.latmaskf)
		plt.show()
		
	def maskview(self,icemap):
		'''displays loaded masks'''
		icemap = icemap.reshape(448, 304)
		plt.imshow(icemap, interpolation='nearest', vmin=30, vmax=90, cmap=plt.cm.jet)
		
		
		
	def dayloop(self):		
		self.icecumf = np.zeros(136192, dtype=float)
				
		for count in range (0,self.daycount,1):
			filename = 'DataFiles/NSIDC_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.bin'
			filenamedav = 'DataFiles/Daily_Mean/NSIDC_Mean_'+str(self.month).zfill(2)+str(self.day).zfill(2)+'.bin'
			
			self.datum.append(str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
						
			with open(filenamedav, 'rb') as fr:
				iceav = np.fromfile(fr, dtype=np.uint8)
			with open(filename, 'rb') as frr:
				ice2 = np.fromfile(frr, dtype=np.uint8)
		
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
				self.dailyloop(self.icedf,self.dailyenergy[count+1])
			if self.plottype == 'cumu' or self.plottype == 'both':
				self.cumulativeloop(self.icecumf,self.cumuenergy[count+1])
			
			print('Progress: ',100*count/self.daycount)
			self.day = self.day+1
			count = count+1
			if self.day==32 and (self.month==1 or 3 or 5 or 7 or 8 or 10 or 12):
				self.day=1
				self.month = self.month+1
			elif self.day==31 and (self.month==4 or self.month==6 or self.month==9 or self.month==11):
				self.day=1
				self.month = self.month+1
			elif self.day==30 and self.month==2:
				self.day=1
				self.month = self.month+1
		
		self.end = 'true'
		with open('AWP_anomaly_'+str(self.year)+'.bin', 'wb') as writecumu:
				icewr = writecumu.write(self.icecumf)
		
		self.cumulativeloop(self.icecumf,self.cumuenergy[count])
		#self.fig2.savefig('Exports/Final_'+str(self.year)+'.png')
		self.writetofile()		
		plt.show()
		
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
			if  1 < self.regmaskf[x] < 5 or 5 < self.regmaskf[x] < 16:	
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
		
		self.dailyenergy.append  (int(1000*(sum(self.albedosumdaily) / sum(self.oceanpixareadaily))))
		self.cumuenergy.append  (round((sum(self.albedosumcumu) / sum(self.oceanpixareacumu)),2))
		
	
		
	def energycalc(self,x,count):
		self.icedf[x] = self.iceavf[x]-self.ice2f[x]
				
		pixlat = max(40,self.latmaskf[x])
		indexx = int(round((pixlat-40)*5))
		MJ = self.latitudelist[indexx][count+1]
		self.icedf[x] = self.icedf[x]*MJ*0.8
		self.icecumf[x] = self.icecumf[x]+self.icedf[x]
		
	

	def dailyloop(self,icemap,icesum):		
		icemap = icemap.reshape(448, 304)
		icemap = icemap[70:410,30:260]
		cmap = plt.cm.coolwarm
		cmap.set_bad('black',0.6)
		
		self.ax.clear()
		self.ax.set_title('Date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2))
		#self.ax.set_title('Maximum of Maxima: '+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
		
		
		self.ax.set_xlabel('Average: '+str(icesum)+' [KJ / 'r'$m^2$]',**self.labelfont)
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=-18, vmax=18, cmap=cmap)
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 8, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax.text(2, 18, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.fig.tight_layout(pad=2)
		#self.fig.savefig('Animation/Daily_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		plt.pause(0.01)
		
	def cumulativeloop(self,icemap,icesum):		
		icemap = icemap.reshape(448, 304)
		icemap = icemap[70:410,30:260]
		cmap2 = plt.cm.coolwarm
		cmap2.set_bad('black',0.6)
		
		self.ax2.clear()
		self.ax2.set_title('Date: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2))
		if self.end == 'true':
			self.ax2.set_title('Astronomical Summer '+str(self.year))
		#self.ax2.set_title('Maximum of Maxima: '+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
		
		self.ax2.set_xlabel('Average: '+str(icesum)+' [MJ / 'r'$m^2$]',**self.labelfont)
		self.cax = self.ax2.imshow(icemap, interpolation='nearest', vmin=-800, vmax=800, cmap=cmap2)
		
		self.ax2.axes.get_yaxis().set_ticks([])
		self.ax2.axes.get_xaxis().set_ticks([])
		self.ax2.text(2, 8, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		self.ax2.text(2, 18, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold')
		self.fig2.tight_layout(pad=2)
		#self.fig2.savefig('Animation/Cumulative_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		plt.pause(0.01)
		
	def dailyorcumu(self):		
		self.icenull = np.zeros(136192, dtype=float)
		self.icenull = self.icenull.reshape(448, 304)
		
		if self.plottype == 'daily' or  self.plottype == 'both':
			self.fig, self.ax = plt.subplots(figsize=(8, 10))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=-18, vmax=18, cmap=plt.cm.coolwarm)
			self.cbar = self.fig.colorbar(self.cax, ticks=[-18,-9, 0,9, 18]).set_label(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
			self.title = self.fig.suptitle('Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold', position=(0.4,0.99) )
		if self.plottype == 'cumu' or self.plottype == 'both':
			self.fig2, self.ax2 = plt.subplots(figsize=(8, 10))
			self.cax = self.ax2.imshow(self.icenull, interpolation='nearest', vmin=-800, vmax=800, cmap=plt.cm.coolwarm)
			self.cbar = self.fig2.colorbar(self.cax, ticks=[-800,-400, 0,400, 800]).set_label(''r'$ \Delta$ clear sky energy absorption in [MJ / 'r'$m^2$]',**self.labelfont)
			self.title = self.fig2.suptitle('Cumulative Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold',position=(0.4,0.99))
			#print('true')
			
		
	def writetofile(self):
		
		with open('CSVexport/_AWP_'+str(self.year)+'.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for writeing in range(0,(len(self.dailyenergy))):
				writer.writerow([self.datum[writeing],self.dailyenergy[writeing],self.cumuenergy[writeing]])
				 
		
		with open('CSVexport/_AWP_regional_'+str(self.year)+'.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for writeing in range(0,(len(self.datum))):
				writer.writerow([self.datum[writeing],self.SoO[writeing],self.Bers[writeing],
				self.HB[writeing],self.BB[writeing],self.EG[writeing],self.BaS[writeing],
				self.KS[writeing],self.LS[writeing],self.ES[writeing],self.CS[writeing],
				self.BeaS[writeing],self.CA[writeing],self.AB[writeing]])
				
		with open('CSVexport/_AWP_regional_daily_'+str(self.year)+'.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for writeing in range(0,(len(self.datum))):
				writer.writerow([self.datum[writeing],self.SoO_daily[writeing],self.Bers_daily[writeing],
				self.HB_daily[writeing],self.BB_daily[writeing],self.EG_daily[writeing],self.BaS_daily[writeing],
				self.KS_daily[writeing],self.LS_daily[writeing],self.ES_daily[writeing],self.CS_daily[writeing],
				self.BeaS_daily[writeing],self.CA_daily[writeing],self.AB_daily[writeing]])


action = Warming()
#action.dayloop()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
