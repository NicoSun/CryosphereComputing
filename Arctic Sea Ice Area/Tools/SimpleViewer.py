import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt



class Simpleviewer:


	def __init__  (self):
		self.year = 1979
		self.month = 8
		self.day = 16
		self.daycount = 1 #366 year,39 years
		
		self.plottype = 'daily' # daily ,  mask
#		self.dailyorcumu()
		self.mode = 'Mean'
		
	
	
	def viewloop(self):
	
		for count in range (0,self.daycount,1): 
#			filename = 'DataFiles/NSIDC_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.bin'
#			filenamemax = 'DataFiles/Maximum/NSIDC_Max_'+str(self.month).zfill(2)+str(self.day).zfill(2)+'.bin'
#			filenamemean = 'DataFiles/Daily_Mean/NSIDC_Mean_'+str(self.month).zfill(2)+str(self.day).zfill(2)+'.bin'
#			filenamemin = 'DataFiles/Minimum/NSIDC_Min_'+str(self.month).zfill(2)+str(self.day).zfill(2)+'.bin'
#			filenameChange = 'DataFiles/Daily_change/NSIDC_SIC_Change_{}{}.bin'.format(str(self.month).zfill(2),str(self.day).zfill(2))
#			filenameStdv = 'DataFiles/Stdv/NSIDC_Stdv_{}{}.bin'.format(str(self.month).zfill(2),str(self.day).zfill(2))
			forecast = 'test/SIPN2_SIC_{}_2018{}{}.bin'.format(self.mode ,str(self.month).zfill(2),str(self.day).zfill(2))
#			forecast = 'test/SIPN2_Thickness_{}_20180918.bin'.format(self.mode)
			
			try:
				with open(forecast, 'rb') as fr:
					ice = np.fromfile(fr, dtype=np.uint8) # int8,unit8,float
#					ice = ice / 250.
#				with open(forecast, 'rb') as fr:
#					ice = np.fromfile(fr, dtype=np.uint16) # int8,unit8,float
#					ice = np.array(ice,dtype=float) /1000
#				with open(filenameStdv, 'rb') as frr:
#					iceStdv = np.fromfile(frr, dtype=np.float16)
#				iceStdv = np.array(iceStdv, dtype=float)
			except:
				print('N/A:',self.year,self.month,self.day)

#			plt.plot(ice)


			plt.hist(ice, bins = [38,90,150,200,220,250]) 
			plt.title("histogram")
			plt.tight_layout(pad=1)
#			plt.axis([0,10,0,60000])
			
			
			water = 0
			land = 0
			icec = 0
			icef = 0
			for x in range (0,len(ice)):
				if ice[x] == 255:
					land = land+1
				if ice[x] == 0:
					water = water+1
				if 37 <ice[x] < 250:
					icec = icec+1
				if ice[x] == 250:
					icef = icef+1
			print('land',land)
			print('water',water)
			print('icec',icec)
			print('icefull',icef)
			
#			self.dailyloop(ice)

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
			
		plt.show()
		

	def masksload(self):
	
		self.regionfile = 'Masks/Arctic_region_mask.bin'
		with open(self.regionfile, 'rb') as frmsk:
			#header = frmsk.read(300)
			self.regionmask = np.fromfile(frmsk, dtype=np.uint32)
		
		self.areamask = 'Masks/psn25area_v3.dat'
		with open(self.areamask, 'rb') as famsk:
			self.mask2 = np.fromfile(famsk, dtype=np.int32)
		self.areamaskf = np.array(self.mask2, dtype=float)
		self.areamaskf = self.areamaskf /(1000)
		
		self.latmask = 'Masks/psn25lats_v3.dat'
		with open(self.latmask, 'rb') as flmsk:
			self.mask3 = np.fromfile(flmsk, dtype=np.int32)
		self.latmaskf = np.array(self.mask3, dtype=float)
		self.latmaskf = self.latmaskf /100000

		'''
		self.icemask = 'Masks/SEAICEMASKS/NIC_valid_ice_mask.N25km.01.1972-2007.nc'
		print(len(self.icemask))
		with open(self.icemask, 'rb') as flmsk:
			self.mask4 = np.fromfile(flmsk, dtype=np.int32)
		
		self.icemaskf = np.array(self.mask4, dtype=float)
		#self.icemaskf = self.icemaskf /100000
		'''
		self.maskview(self.regionmask)
		plt.show()
		
		
	def dailyloop(self,icemap):
#		icemap = ma.masked_greater(icemap, 1)
		icemap = icemap.reshape(448, 304)
		icemap = icemap[60:410,30:260]
		
		cmap = plt.cm.jet
		cmap.set_bad('black',0.6)
		
		self.ax.clear()
		self.ax.set_title('Date: '+str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2),x=0.15)
		self.ax.set_xlabel('NSIDC Area: Ice concentration'+self.mode)
#		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=-25, vmax=25, cmap=cmap)
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=1, cmap=cmap)
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		plt.tight_layout(pad=1)
#		self.fig.savefig(self.mode)
		plt.pause(0.01)
		
		
	def maskview(self,icemap):		
		icemap = icemap.reshape(448, 304)
		self.ax.clear()
		#self.ax.set_title('Date: '+str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
		#self.ax.set_xlabel(': '+str(icesum)+' Wh/m2')
		self.cax = self.ax.imshow(icemap, interpolation='nearest')
		#self.fig.savefig('Animation/Daily_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		plt.pause(0.1)
		
		
	def dailyorcumu(self):		
		self.icenull = np.zeros(136192, dtype=float)
		self.icenull = self.icenull.reshape(448, 304)
		
		if self.plottype == 'daily':
			self.fig, self.ax = plt.subplots(figsize=(8, 10))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest', vmin=0, vmax=1,cmap = plt.cm.jet)
#			self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Ice concentration in %')
			self.cbar = self.fig.colorbar(self.cax, ticks=[0,25,50,75,100]).set_label('Ice concentration in %')
#			self.title = self.fig.suptitle('Concentration Map', fontsize=14, fontweight='bold',x=0.175)
			
		if self.plottype == 'mask':
			self.fig, self.ax = plt.subplots(figsize=(8, 10))
			self.cax = self.ax.imshow(self.icenull, interpolation='nearest')
			#self.cbar = self.fig.colorbar(self.cax).set_label('stuff')
#			self.title = self.fig.suptitle('Mask', fontsize=14, fontweight='bold')
			
		
		
		
action = Simpleviewer()
action.viewloop()
#action.masksload()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
