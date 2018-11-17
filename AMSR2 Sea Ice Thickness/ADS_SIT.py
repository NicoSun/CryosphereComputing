"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script calculates the sea ice thickness from the formatted ADS SIT data ( with File_Mangaer)
"""

import numpy as np
import numpy.ma as ma
import pandas
import csv
import matplotlib.pyplot as plt
from datetime import date
from datetime import timedelta
import time


class ADS_data:

	def __init__  (self):
		'''initializes the melt algorithm'''
		self.start = date(2012, 7, 3)
		self.year = self.start.year
		self.month = self.start.month
		self.day = self.start.day
		self.daycount = 2#2128 #total length: 2158 
		
		self.CSVDatum = ['Date']
		self.CSVVolume =['Volume']
		self.CSVThickness =['Thickness']
		
		#melt melt algorithm hyperparameters
		self.meltrate = 5
		self.freezerate = 2.2
		self.first_freeze_thickness = 20 # centimeter*(1-melt percentage)
		self.min_melt_thickness = 25 #cm 
		self.thicknesschange = 6.6 #cm per day
		self.max_thickness = 400 #cm
		
		#Poleholelist
		Columns = ['hole']
		csvdata = pandas.read_csv('Tools/zzz_polehole.csv', names=Columns,dtype=int)
		self.icepole = csvdata.hole.tolist()
		
		Columns = ['edge']
		csvdata = pandas.read_csv('Tools/zzz_poleholeEdge.csv', names=Columns,dtype=int)
		self.icepoleedge = csvdata.edge.tolist()
		
		
		self.labelfont = {'fontname':'Arial'}
		self.masksload()
		self.createfigure()
		

		
	def masksload(self):
		'''loads the landmask and latitude-longitude mask'''
		landmaskfile = 'Masks/landmask_low.map'
		with open(landmaskfile, 'rb') as frmsk:
				self.landmask = np.fromfile(frmsk, dtype=np.uint8)
		
		latlonmaskfile = 'Masks/latlon_low.map'
		with open(latlonmaskfile, 'rb') as famsk:
				mask2 = np.fromfile(famsk, dtype=np.uint16)
		mask2 = np.array(mask2, dtype=float)
		self.latmaskf = 0.01*mask2[:810000] 
		self.lonmaskf = 0.01*mask2[810000:]	
		
		
		
	def createfigure(self):
		'''creates the plot figure (map)'''
		icemap = self.landmask.reshape(900, 900)
		icemap = np.rot90(icemap,k=2)
		icemap = icemap[80:750,:700]
		
		self.fig, self.ax = plt.subplots(figsize=(11, 9))
		#self.fig = plt.figure(figsize=(18, 8))
		#self.ax = self.fig.add_subplot(121)
		#self.ax2 = self.fig.add_subplot(122)
		
		self.cax = self.ax.imshow(icemap, interpolation='nearest', vmin=0, vmax=300,cmap = plt.cm.gist_ncar)
		self.cbar = plt.colorbar(self.cax,shrink=0.9)
		self.cbar.set_label('Thickness in cm')
		self.fig.tight_layout(pad=1)
		#self.normalshow(self.latmaskf,1,2)
		#plt.show()
		
	def polehole(self,ice):
		'''calculates the pole hole'''
		#polehole calc
		icepolecon = []
		
		for val in range(0,len(self.icepoleedge)):
			icepolecon.append(min(self.max_thickness,ice[self.icepoleedge[val]]))
		#print(icepolecon)
		for val2 in range(0,len(self.icepole)):
			ice[self.icepole[val2]] = np.mean(icepolecon)
		
		return ice
		
	def dayloop(self):
		'''main melt algorithm'''
		loopday	= self.start	
		day_of_year	= self.start.timetuple().tm_yday
		self.start = time.time()
		self.freezedays = np.zeros(810000, dtype=float) #number of days with 20% melt, 40% melt = 2 days
		self.meltcount = np.zeros(810000, dtype=float) #number of days with 20% melt, 40% melt = 2 days
		self.freezecount = np.zeros(810000, dtype=float) #number of days with 20% melt, 40% melt = 2 days
		
		#for 2012 start date
#		with open('Datafiles/ADS_SIT_20170303.dat', 'rb') as fr:
#			iceread = np.fromfile(fr, dtype=np.uint16)
#		self.icethickess = np.array(iceread, dtype=float)/10
				
		for count in range (0,self.daycount,1): 
			filename = 'Datafiles/ADS_SIT_{}{}{}.dat'.format(self.year,str(self.month).zfill(2),str(self.day).zfill(2))
			
			try:
				with open(filename, 'rb') as frr:
					iceread = np.fromfile(frr, dtype=np.uint16)
			except:
				print('Date: {} not available'.format(loopday))
				
			
			icevolume = []
			icethickness = []
			icenewdate 	=  np.array(iceread, dtype=float)/10
			
			for x in range (0,len(icenewdate)):
				#new day contains thickness data
				if icenewdate[x] < 501:
					#old day is ice free or melt was estimates
					if self.icethickess[x] > 5700:
						self.icethickess[x] = min(self.max_thickness,icenewdate[x])
						self.freezedays[x] = 0
						
					#old day is not ice free
					else:
						self.icethickess[x] = max(self.icethickess[x]-self.thicknesschange,min(self.max_thickness,self.icethickess[x]+self.thicknesschange,icenewdate[x]))
						self.freezedays[x] = 0

						
				#new day is ice free
				elif 5700 < icenewdate[x] < 5800:
					self.icethickess[x] = icenewdate[x]
					self.freezedays[x] = 0
					
				#new day shows melt and old day is ice-free (first refreeze)
				elif  1000 < icenewdate[x] < 1002 and self.icethickess[x] > 5700:
					self.icethickess[x] = self.first_freeze_thickness*(1-(icenewdate[x]-1000))
					self.freezedays[x] = 1
					#self.freezecount[x] = self.freezecount[x]+1
				
				# melt & freeze algorithm				
				elif  1000 < icenewdate[x] < 1002 and self.icethickess[x] < 501:	
					#calculates melting
					if self.freezedays[x] < 1:
						self.icethickess[x] = max(self.min_melt_thickness,self.icethickess[x]*(1-((icenewdate[x]-1000)/self.meltrate)))
						#self.meltcount[x] = self.meltcount[x]+5*(icenewdate[x]-1000) # 0.2 melt == one melt day (0.2*5=1), 0.4 melt == 2 melt days
						self.freezedays[x] = -1						
						
					#calculates freezing after first refreeze	
					elif self.freezedays[x] > 0 :
						self.icethickess[x] = min(50,self.icethickess[x]+self.icethickess[x]*((icenewdate[x]-1000)/(self.freezerate*self.freezedays[x]**0.5)))
						self.freezedays[x] = self.freezedays[x]+1 # refreeze days
						#self.freezecount[x] = self.freezecount[x]+1
			
			#calculate pole hole
			self.icethickess = self.polehole(self.icethickess)

			#restricts the final thickness and volume data to north of 50N
			for y in range (0,810000):
				if  0 < self.icethickess[y] < 501 and self.latmaskf[y] > 50:
					icevolume.append  ((self.icethickess[y]/1e5)*100)
					icethickness.append (self.icethickess[y])
					

			self.CSVVolume.append (np.sum(icevolume))
			self.CSVThickness.append (np.sum(icethickness)/len(icethickness))
			
			#export daily data as png & binary for NETCDF conversion
			self.normalshow(self.icethickess,self.CSVVolume[-1],self.CSVThickness[-1])
			NETCDF_export = np.array(self.icethickess, dtype=np.uint16)
			with open('Binary/AMSR2_SIT_{}{}{}.dat'.format(self.year,str(self.month).zfill(2),str(self.day).zfill(2)),'wb') as writecumu:
				icewr = writecumu.write(NETCDF_export)
									
			self.CSVDatum.append('{}/{}/{}'.format(self.year,self.month,self.day))
			count = count+1
			print(round((100*count/self.daycount),2),' % \r', end="")
			if count < self.daycount:
				loopday = loopday+timedelta(days=1)
				self.year = loopday.year
				self.month = loopday.month
				self.day = loopday.day
				day_of_year = loopday.timetuple().tm_yday
				
			#print('Date: {}'.format(loopday))
			
			
		
# =============================================================================
			#saves freezecount and meltcount data
# 		with open('Images/AMSR2_meltcount_{}.dat'.format(str(self.year)),'wb') as writecumu:
# 				icewr = writecumu.write(self.meltcount)
# 			
# 		with open('Images/AMSR2_freezecount_{}.dat'.format(str(self.year)),'wb') as writecumu:
# 				icewr = writecumu.write(self.freezecount)
# =============================================================================
		
		
		
		self.fig.savefig('Upload/AMSR2_SIT_Last_Day.png')
		with open('Upload/AMSR2_SIT_{}{}{}.dat'.format(str(self.year),str(self.month).zfill(2),str(self.day).zfill(2)),'wb') as writecumu:
			icewr = writecumu.write(self.icethickess)
		
		self.end = time.time()
		self.CSVDatum.append (self.end-self.start)
		self.CSVVolume.append ('seconds')
		self.CSVThickness.append (str((self.end-self.start)/self.daycount)+'seconds/day')	

		plt.show()


	def normalshow(self,icemap,icesum,icethickness):	
		'''used to display data on a map'''
		from matplotlib.colors import LinearSegmentedColormap
		icemap = icemap.reshape(900, 900)
		icemap = np.rot90(icemap,k=2)
		icemap = icemap[80:750,:700]
		#icemap = icemap[180:600,200:600]
		icesum = int(icesum)
		icethickness = int(icethickness)

		
		map1 = ma.masked_outside(icemap,0,600) # SIT
		map2 = ma.masked_outside(icemap,5000,6000) # NoData -> Land -> Water
				
		plainmap = icemap
				
		colors = [(0.1, 0., 0.1), (0.6, 0.1, 0.1), (0.4, 0.4, 0.4)]  # NoData -> Land -> Water
		cmap_name = 'my_list'
		
		cm4 = LinearSegmentedColormap.from_list(cmap_name, colors, N=3)
		cmapice = plt.cm.gist_ncar
		
		self.ax.clear()
		self.ax.set_title('AMSR2 Sea Ice Volume: '+str(self.year)+'-'+str(self.month).zfill(2)+'-'+str(self.day).zfill(2))
		self.ax.set_xlabel('Volume: '+str(icesum)+' 'r'$km^3$''  /  Thickness: '+str(icethickness)+' cm', fontsize=14,**self.labelfont)
		
		self.ax.imshow(map2, interpolation='nearest',vmin=5500, vmax=5800 ,cmap=cm4)
		self.ax.imshow(map1, interpolation='nearest',vmin=0, vmax=300, cmap=cmapice)
		#self.ax.imshow(plainmap, interpolation='nearest',cmap=cmapice)
		#self.ax.imshow(plainmap, interpolation='nearest',vmin=0, vmax=100,cmap=cmapice)		
		
		self.ax.axes.get_yaxis().set_ticks([])
		self.ax.axes.get_xaxis().set_ticks([])
		self.ax.text(2, 18, r'Data: JAXA / Arctic Data archieve System (ADS)', fontsize=10,color='white',fontweight='bold')
		self.ax.text(2, 38, r'Map & Melt-Algorithm: Nico Sun', fontsize=10,color='white',fontweight='bold')
		self.ax.text(-0.04, 0.60, 'https://sites.google.com/site/cryospherecomputing/amsr2-sea-ice-volume',
        transform=self.ax.transAxes,rotation='vertical',color='grey', fontsize=10)
		self.fig.subplots_adjust(right = 1.03)
		self.fig.savefig('Images/AMSR2_SIT_{}{}{}.png'.format(str(self.year),str(self.month).zfill(2),str(self.day).zfill(2)))
		#plt.pause(0.01)
		
	def viewloop(self):
		'''used to display raw & calculated data on a map'''
		loopday	= self.start
		for count in range (0,self.daycount,1): 
			#filename = 'Images/AMSR2_SIT_{}{}{}.dat'.format(str(self.year),str(self.month).zfill(2),str(self.day).zfill(2))
			#filename = 'Analysis/AMSR2_meltcount_2012.dat'.format(str(self.year),str(self.month).zfill(2),str(self.day).zfill(2))
			filename = 'Datafiles/ADS_SIT_{}{}{}.dat'.format(str(self.year),str(self.month).zfill(2),str(self.day).zfill(2))
			
			try:
				with open(filename, 'rb') as frr:
					iceread = np.fromfile(frr, dtype=np.uint16)
			except:
				print('Date: {} not available'.format(loopday))
				
			iceread = iceread/10	
			self.normalshow(iceread,1,1)
			
				
			#print(round((100*count/self.daycount),2),' % \r', end="")
			if count < self.daycount:
				loopday = loopday+timedelta(days=1)
				self.year = loopday.year
				self.month = loopday.month
				self.day = loopday.day
				
		plt.show()
		
	def writetofile(self):
		'''exports data as csv'''
		with open('_AMSR2_sea_ice_volume_V1.5.csv', "w") as output: 
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for writeing in range(0,len(self.CSVDatum)):
				writer.writerow([self.CSVDatum[writeing],self.CSVVolume[writeing],self.CSVThickness[writeing]])

	
	def automated (self,day,month,year,daycount):
		'''used only to automate monthly updates'''
		self.year = year
		self.month = month
		self.day = day
		self.daycount = daycount

		self.start = date(year, month, day)
		prevdate = self.start-timedelta(days=1)
		prevyear = prevdate.year
		prevmonth = prevdate.month
		prevday = prevdate.day
		
		lastmonthdata = 'Upload/AMSR2_SIT_{}{}{}.dat'.format(prevyear,str(prevmonth).zfill(2),str(prevday).zfill(2))
		with open(lastmonthdata, 'rb') as fr:
			self.icethickess = np.fromfile(fr, dtype=float)
		
		self.dayloop()
		self.writetofile()

action = ADS_data()
if __name__ == "__main__":
	print('main')
	action.dayloop()
	#action.writetofile()
	#action.viewloop()
#	action.automated(1,5,2018,31) #start-day,month,year,daycount

'''
Current melt algorithm hyperparameters used:
V1.5: max thickness: 400cm; melt-rate: 5,freezerate:2.2; new melt area: 20cm*(1-melt percentage), max change 6.6cm, min melt thickness = 25cm

ADS sit file default encodings
no Data: 555X
Land: 5664.8
water: 5775.9
unknown: 654X/655X

Citation:
Hori, M., H. Yabuki, T. Sugimura, T. Terui, 2012, AMSR2 Level 3 product of Daily Polar Brightness Temperatures and Product, 1.00, Arctic Data archive System (ADS), Japan, https://ads.nipr.ac.jp/dataset/A20170123-003

'''