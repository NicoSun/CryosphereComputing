'''
NOAA Daily Snow Extent / Ice Extent Data


array size: 247500 (550:450)
'''
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import csv
import pandas


class NOAA_Snow_Cover:


	def __init__  (self):
		self.year = 2018
		self.daycount = 1 #366 year,39 years
		self.day_of_year = 50
		
		self.threads = 1
		
		self.masksload()
		
		self.CSVDatum = ['Date']
		self.IceExtent = ['IceExtent']
		self.NorthAmericaExtent =['NorthAmericaExtent']
		self.GreenlandExtent =['GreenlandExtent']
		self.EuropeExtent =['EuropeExtent']
		self.AsiaExtent =['AsiaExtent']
		
		self.SnowExtent_anom = ['SnowExtent Anomaly']
		self.IceExtent_anom = ['IceExtent Anomaly']
		
	def masksload(self):
	
		filename = 'X:/SnowCover/Masks/Region_Mask.msk'
		with open(filename, 'rb') as fr:
			self.regionmask = np.fromfile(fr, dtype='uint8')
		filename = 'X:/SnowCover/Masks/Pixel_area_crop.msk'
		with open(filename, 'rb') as fr:
			self.pixelarea = np.fromfile(fr, dtype='uint16')
		filename = 'X:/SnowCover/Masks/Coastmask.msk'
		with open(filename, 'rb') as fr:
			self.coastmask = np.fromfile(fr, dtype='uint8')
		
		
		filename = 'X:/SnowCover/Masks/Latitude_Mask.msk'
		with open(filename, 'rb') as fr:
			self.Latitude_Mask = np.fromfile(fr, dtype='float32')
		

			

		
	def load_days(self):
		self.stringday = str(self.day_of_year).zfill(3)
		self.stringday2 = str(self.day_of_year-1).zfill(3)
		filenameMean = 'X:/SnowCover/DataFiles/Mean/NOAA_Mean_{}_24km.bin'.format(self.stringday)
		filename = 'X:/SnowCover/Datafiles/NOAA_{}{}_24km.bin'.format(self.year,self.stringday)
		filenameyesterday = 'X:/SnowCover/Datafiles/NOAA_{}{}_24km.bin'.format(self.year,self.stringday2)
		
		self.CSVDatum.append('{}_{}'.format(self.year,self.stringday))
			
		with open(filenameMean, 'rb') as fr:
				snowMean = np.fromfile(fr, dtype='uint8')
		with open(filename, 'rb') as fr:
			snow = np.fromfile(fr, dtype='uint8')
		with open(filenameyesterday, 'rb') as fr:
			snowy = np.fromfile(fr, dtype='uint8')
		snowMean = np.array(snowMean,dtype=np.float)
		snowy = np.array(snowy,dtype=np.float)
			
		aaa = np.vectorize(self.calculateExtent)
		iceextent,NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent,snowanomaly,snowchange = aaa(snow,self.regionmask,self.pixelarea,snowMean,snowy)

		data = [np.sum(iceextent),np.sum(NorthAmericaExtent),np.sum(GreenlandExtent),np.sum(EuropeExtent),np.sum(AsiaExtent)]
		snowextent= np.sum(data[1:])
		iceextent= np.sum(data[0])
		
		
		self.IceExtent.append (data[0]/1e6)
		self.NorthAmericaExtent.append (data[1]/1e6)
		self.GreenlandExtent.append (data[2]/1e6)
		self.EuropeExtent.append (data[3]/1e6)
		self.AsiaExtent.append (data[4]/1e6)
		
		for x,y in enumerate(snowanomaly):
			if self.coastmask[x]==3:
				snowanomaly[x]=3
			if snowchange[x]==-2:
				snow[x]=6
			if snowchange[x]==2:
				snow[x]=7
		
		self.createmap(snow,snowextent,iceextent)
		self.create_anolamy_map(snowanomaly)
#		plt.show()
		

	def calculateExtent(self,snowmap,regionmask,pixelarea,snowMean,snowy):
		iceextent = 0
		NorthAmericaExtent = 0
		GreenlandExtent = 0
		EuropeExtent = 0
		AsiaExtent = 0
		snowanomaly = snowmap-snowMean/10
		snowchange = snowmap - snowy
		
		if snowmap==3:
			iceextent = pixelarea
			snowanomaly = (snowmap-1)-snowMean/10
		if snowmap==2:
			snowanomaly = (snowmap+1)-snowMean/10
		if regionmask==3 and snowmap==4:
			NorthAmericaExtent = pixelarea
		if regionmask==4 and snowmap==4:
			GreenlandExtent = pixelarea
		if regionmask==5 and snowmap==4:
			EuropeExtent = pixelarea
		if regionmask==6 and snowmap==4:
			AsiaExtent = pixelarea
	
		return iceextent,NorthAmericaExtent,GreenlandExtent,EuropeExtent,AsiaExtent,snowanomaly,snowchange
		
		
	def createmap(self,snowmap,snowextent,iceextent):
		snowmap = snowmap.reshape(610,450)
		map1 = ma.masked_outside(snowmap,-0.5,2.5) # Land -> Water
		map2 = ma.masked_outside(snowmap,2.5,4.5) # Ice -> Snow
		map3 = ma.masked_outside(snowmap,6,7) # Snow extent gain/loss
		
		fig, ax = plt.subplots(figsize=(8, 10))
		cmap = plt.cm.ocean_r
		cmap2 = plt.cm.Greys
		cmap3 = plt.cm.RdBu
		
		ax.clear()
		ax.text(0.82, 0.98, 'Map: Nico Sun', fontsize=10,color='white',transform=ax.transAxes)
		ax.text(0.66, 0.03, 'Ice extent: '+'{:,}'.format(iceextent)+' 'r'$km^2$', fontsize=10,color='white',transform=ax.transAxes)
		ax.text(0.66, 0.01, 'Snow extent: '+'{:,}'.format(snowextent)+' 'r'$km^2$', fontsize=10,color='white',transform=ax.transAxes)
		
		ax.text(0.62, -0.02, 'Snow cover gain', fontsize=10,color='blue',transform=ax.transAxes)
		ax.text(0.82, -0.02, 'Snow cover loss', fontsize=10,color='red',transform=ax.transAxes)
		
		ax.set_title('NOAA / NSIDC IMS Snow & Ice Extent      {}-{}-{}'.format(self.year,self.month,self.day),x=0.5)
		ax.set_xlabel('Data source: https://nsidc.org/data/g02156',x=0.22)
		ax.set_ylabel('https://sites.google.com/site/cryospherecomputing/snow-cover',y=0.25)
		
		ax.imshow(map1, interpolation='nearest', vmin=0, vmax=2, cmap=cmap) # Water & Land
		ax.imshow(map2, interpolation='nearest', vmin=3, vmax=5.5, cmap=cmap2) #Snow & Ice
		ax.imshow(map3, interpolation='nearest', vmin=5.6, vmax=7.4, cmap=cmap3) # Snow gain/loss
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		plt.tight_layout(pad=1)
		fig.savefig('X:/Upload/Snow_Cover_Data/NOAA_Snowmap.png')
		fig.savefig('X:/SnowCover/Images/NOAA_Snowmap_normal_{}.png'.format(str(self.day_of_year).zfill(3)))
		plt.pause(0.01)
#		plt.show()
		
	def create_anolamy_map(self,snowmap):
		snowmap = ma.masked_greater(snowmap, 2)
		snowmap = snowmap.reshape(610,450)
		
		fig, ax = plt.subplots(figsize=(8, 10))
		cmap_anom = plt.cm.RdBu
		cmap_anom.set_bad('black',0.8)
		ax.clear()
		
		ax.text(0.82, 0.98, 'Map: Nico Sun', fontsize=10,color='black',transform=ax.transAxes)
		ax.text(0.65, 0.05, 'red: below climatology (-100%)', fontsize=10,color='darkred',transform=ax.transAxes)
		ax.text(0.65, 0.03, 'white: at climatology (+0%)', fontsize=10,color='grey',transform=ax.transAxes)
		ax.text(0.65, 0.01, 'blue: above climatology (+100%)', fontsize=10,color='darkblue',transform=ax.transAxes)
#		gs = gridspec.GridSpec(1, 2)
		
		ax.set_title('NOAA / NSIDC IMS Snow & Ice Extent Anomaly      {}-{}-{}'.format(self.year,self.month,self.day),x=0.5)
		ax.set_xlabel('Data source: https://nsidc.org/data/g02156',x=0.22)
		ax.set_ylabel('https://sites.google.com/site/cryospherecomputing/snow-cover',y=0.25)
		cax = ax.imshow(snowmap, interpolation='nearest', vmin=-1, vmax=1, cmap=cmap_anom)
#		cbaxes = inset_axes(ax, width="5%", height="25%", loc=4)
#		fig.colorbar(cax,ax=cbaxes, orientation='vertical',shrink=0.25,panchor=(0.0, 0.5))
		ax.axes.get_yaxis().set_ticks([])
		ax.axes.get_xaxis().set_ticks([])
		plt.tight_layout(pad=1)
		
		fig.savefig('X:/Upload/Snow_Cover_Data/NOAA_Snowmap_anomaly.png')
		fig.savefig('X:/SnowCover/Images/NOAA_Snowmap_anomaly_{}.png'.format(str(self.day_of_year).zfill(3)))
		

# =============================================================================
# 		NAchange = int(float(self.NorthAmericaExtent[-2])-float(self.NorthAmericaExtent[-1])*1e6)
# 		GRchange = int(float(self.GreenlandExtent[-2])-float(self.GreenlandExtent[-1])*1e6)
# 		EUchange = int(float(self.EuropeExtent[-2])-float(self.EuropeExtent[-1])*1e6)
# 		ASchange = int(float(self.AsiaExtent[-2])-float(self.AsiaExtent[-1])*1e6)
# 		ax2.text(0.77, 0.07, 'America: {}'.format(NAchange), fontsize=10,color='darkred',transform=ax.transAxes)
# 		ax2.text(0.77, 0.05, 'Greenland: {}'.format(GRchange), fontsize=10,color='grey',transform=ax.transAxes)
# 		ax2.text(0.77, 0.03, 'Europe: {}'.format(EUchange), fontsize=10,color='darkblue',transform=ax.transAxes)
# 		ax2.text(0.77, 0.01, 'Asia: {}'.format(ASchange), fontsize=10,color='darkblue',transform=ax.transAxes)
# =============================================================================
#		
		plt.pause(0.01)
#		plt.show()
		

			
	def writetofile(self):
		with open('X:/Upload/Snow_Cover_Data/NRT_extent_data_'+str(self.year)+'.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n') #str(self.year)
			for x in range(0,len(self.IceExtent)):
				writer.writerow([self.CSVDatum[x],self.IceExtent[x],self.NorthAmericaExtent[x],self.GreenlandExtent[x],self.EuropeExtent[x],self.AsiaExtent[x]])

	def loadCSVdata(self):
		
		#NRT Data
		Yearcolnames = ['Date', 'IceExtent', 'NorthAmericaExtent','GreenlandExtent','EuropeExtent','AsiaExtent']
		Yeardata = pandas.read_csv('X:/Upload/Snow_Cover_Data/NRT_extent_data_'+str(self.year)+'.csv', names=Yearcolnames)
		self.CSVDatum = Yeardata.Date.tolist()
		self.IceExtent = Yeardata.IceExtent.tolist()
		self.NorthAmericaExtent = Yeardata.NorthAmericaExtent.tolist()
		self.GreenlandExtent = Yeardata.GreenlandExtent.tolist()
		self.EuropeExtent = Yeardata.EuropeExtent.tolist()
		self.AsiaExtent = Yeardata.AsiaExtent.tolist()
		
	def automated(self,day,month,year,dayofyear):
		'''function to automate parts of the monthly update procedure'''
		self.year = year
		self.month =str(month).zfill(2)
		self.day = str(day).zfill(2)
		self.day_of_year = dayofyear


		self.loadCSVdata()
		self.load_days()
		self.writetofile()



action = NOAA_Snow_Cover()
if __name__ == "__main__":
	
	action.automated(13,11,2018,317)
#	action.extentdata()
#	action.writetofile()
#	