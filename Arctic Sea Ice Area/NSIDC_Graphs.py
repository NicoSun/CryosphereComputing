import pandas
import matplotlib.pyplot as plt
import numpy as np

class NSIDC_Graph:

	def __init__  (self):
		self.year = 2000
		self.month = 1
		self.day = 1
		
			
	def makegraph(self):
		'''creates a smaller seasonal sea ice area graph'''
		fig = plt.figure(figsize=(8, 6))
		fig.suptitle('Arctic Sea Ice Area', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,31,60,91,121,152,182,213,244,274,305,335]
		plt.xticks(x,labels)

		ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
		
		ax.text(0.01, -0.08, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.35, -0.08, 'https://sites.google.com/site/cryospherecomputing/daily-data',
        transform=ax.transAxes,color='grey', fontsize=10)
		
		ax.grid(True)
		
		plt.plot( self.C1980s, color=(0.75,0.75,0.75),label='1980s',lw=2,ls='--')
		plt.plot( self.C1990s, color=(0.44,0.44,0.44),label='1990s',lw=2,ls='--')
		plt.plot( self.C2000s, color=(0.1,0.1,0.1),label='2000s',lw=2,ls='--')
		plt.plot( self.C2007, color='red',label='2007',lw=1)
		plt.plot( self.C2012, color='orange',label='2012',lw=1)
		plt.plot( self.C2013, color='purple',label='2013',lw=1)
		#plt.plot( self.C2014, color='blue',label='2014',lw=1)
		#plt.plot( self.C2015, color='green',label='2015',lw=1)
		plt.plot( self.C2016, color='green',label='2016',lw=1)
		plt.plot( self.C2017, color='brown',label='2017',lw=1)
		plt.plot( self.CSVArea, color='black',label='2018',lw=2)
		
		last_value =  int(self.CSVArea[-1]*1e6)
		ax.text(0.01, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
		
		ymin = max(0,float(self.CSVArea[-1])-4)
		ymax = min(14.5,float(self.CSVArea[-1])+4)
		plt.axis([(self.month-2.5)*30.5+self.day,self.day+(self.month)*30.5,ymin,ymax])
		plt.legend(loc=4, shadow=True, fontsize='medium')
		
		ax.text(0.52, 0.07, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.52, 0.04, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.subplots_adjust(bottom=0.08)
		fig.savefig('X:/Upload/Arctic_Graph.png')

			
	def makegraph_full(self):
		'''creates the full year sea ice area graph'''
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('Arctic Sea Ice Area', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,31,60,91,121,152,182,213,244,274,305,335]
		plt.xticks(x,labels)

		ax.text(5, 0.5, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold')
		ax.text(5, 0.2, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold')
		ax.set_ylabel('Sea Ice Area in 'r'[$10^6$ $km^2$]')
		major_ticks = np.arange(0, 15, 1)
		ax.set_yticks(major_ticks)  

		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.6, -0.06, 'https://sites.google.com/site/cryospherecomputing/daily-data',
        transform=ax.transAxes,
        color='grey', fontsize=10)	
		
		ax.grid(True)
				
		plt.plot( self.C1980s, color=(0.75,0.75,0.75),label='1980s',lw=2,ls='--')
		plt.plot( self.C1990s, color=(0.44,0.44,0.44),label='1990s',lw=2,ls='--')
		plt.plot( self.C2000s, color=(0.1,0.1,0.1),label='2000s',lw=2,ls='--')
		plt.plot( self.C2007, color='red',label='2007',lw=1)
		plt.plot( self.C2012, color='orange',label='2012',lw=1)
		plt.plot( self.C2013, color='purple',label='2013',lw=1)
		#plt.plot( self.C2014, color='blue',label='2014',lw=1)
		#plt.plot( self.C2015, color='green',label='2015',lw=1)
		plt.plot( self.C2016, color='green',label='2016',lw=1)
		plt.plot( self.C2017, color='brown',label='2017',lw=1)
		plt.plot( self.CSVArea, color='black',label='2018',lw=2)
		
		last_value =  int(self.CSVArea[-1]*1e6)
		ax.text(0.72, 0.01, 'Last value: '+'{:,}'.format(last_value)+' 'r'$km^2$', fontsize=10,color='black',transform=ax.transAxes)
		
		ymin = 0
		ymax = 14.5
		plt.axis([0,365,ymin,ymax])
		plt.legend(loc=4, shadow=True, fontsize='medium')
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.subplots_adjust(bottom=0.06)
		fig.savefig('X:/Upload/Arctic_Graph_full.png')

			
	def makegraph_compaction(self):
		'''creates the sea ice compaction graph (area/extent)'''
		fig = plt.figure(figsize=(12, 8))
		fig.suptitle('Arctic Sea Ice Compaction (Area / Extent)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		x = [0,31,60,91,121,152,182,213,244,274,305,335]
		plt.xticks(x,labels)
		
		ax.text(0.01, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.01, 0.03, r'Graph by Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.set_ylabel('Compaction in %')
		major_ticks = np.arange(0, 100, 5)
		ax.set_yticks(major_ticks)     

		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.6, -0.06, 'https://sites.google.com/site/cryospherecomputing/daily-data',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		ax.grid(True)
		
		plt.plot( self.Compaction1980s, color=(0.8,0.8,0.8),label='1980s',lw=2,ls='--')
		plt.plot( self.Compaction1990s, color=(0.5,0.5,0.5),label='1990s',lw=2,ls='--')
		plt.plot( self.Compaction2000s, color=(0.25,0.25,0.25),label='2000s',lw=2,ls='--')
		plt.plot( self.Compaction2010s, color=(0.1,0.1,0.1),label='2010s',lw=2,ls='--')
		plt.plot( self.Compaction2007, color='red',label='2007',lw=1)
		plt.plot( self.Compaction2012, color='orange',label='2012',lw=1)
		plt.plot( self.Compaction2013, color='purple',label='2013',lw=1)
		#plt.plot( self.Compaction2014, color='blue',label='2014',lw=1)
		#plt.plot( self.Compaction2015, color='green',label='2015',lw=1)
		plt.plot( self.Compaction2016, color='green',label='2016',lw=1)
		plt.plot( self.Compaction2017, color='brown',label='2017',lw=1)
		plt.plot( self.CSVCompaction, color='black',label='2018',lw=2)
		
		last_value =  round(self.CSVCompaction[-1],2)
		ax.text(0.75, 0.01, 'Last value: '+str(last_value)+' %', fontsize=10,color='black',transform=ax.transAxes)
		
		yearday = int((self.month-1)*30.5+self.day)
		variance = [self.Compaction1980s[yearday],self.Compaction1990s[yearday],self.Compaction2000s[yearday],self.Compaction2010s[yearday]]
		variance_new = np.asarray(variance).astype(np.float32)
		deviation = np.std(variance_new)+1
		ymin = max(49,float(self.CSVCompaction[-1])-8*deviation)
		ymax = min(96,float(self.CSVCompaction[-1])+8*deviation)
		plt.axis([(self.month-2.5)*30.5+self.day,self.day+(self.month)*30.5,ymin,ymax])
		
		
		plt.legend(loc=4, shadow=True, fontsize='medium')
		fig.tight_layout(pad=2)
		fig.subplots_adjust(top=0.95)
		fig.subplots_adjust(bottom=0.06)
		fig.savefig('X:/Upload/Arctic_Graph_Compaction.png')

	def loadCSVdata (self):
		'''Loads NRT & Climate data'''
		#NRT Data
		Yearcolnames = ['Date', 'Area', 'Extent','Compaction']
		Yeardata = pandas.read_csv('X:/Upload/AreaData/Arctic_NSIDC_Area_NRT_'+str(self.year)+'.csv', names=Yearcolnames,header=0)
		self.CSVDatum = Yeardata.Date.tolist()
		self.CSVArea = Yeardata.Area.tolist()
		self.CSVExtent = Yeardata.Extent.tolist()
		self.CSVCompaction = Yeardata.Compaction.tolist()
		
		#Climate Data
		Climatecolnames = ['Date','Mean','C1980s','C1990s','C2000s','C2007', 'C2008', 'C2009', 'C2010', 'C2011', 'C2012', 'C2013', 'C2014', 'C2015', 'C2016', 'C2017']
		Climatedata = pandas.read_csv('X:/Upload/AreaData/Arctic_climate_full.csv', names=Climatecolnames,header=0)
		self.Mean = Climatedata.Mean.tolist()
		self.C1980s = Climatedata.C1980s.tolist()
		self.C1990s = Climatedata.C1990s.tolist()
		self.C2000s = Climatedata.C2000s.tolist()
		self.C2007 = Climatedata.C2007.tolist()
		self.C2008 = Climatedata.C2008.tolist()
		self.C2009 = Climatedata.C2009.tolist()
		self.C2010 = Climatedata.C2010.tolist()
		self.C2011 = Climatedata.C2011.tolist()
		self.C2012 = Climatedata.C2012.tolist()
		self.C2013 = Climatedata.C2013.tolist()
		self.C2014 = Climatedata.C2014.tolist()
		self.C2015 = Climatedata.C2015.tolist()
		self.C2016 = Climatedata.C2016.tolist()
		self.C2017 = Climatedata.C2017.tolist()
	
		#Compaction Data
		Compactioncolnames = ['Date','C1980s','C1990s','C2000s','C2010s','C2007', 'C2008', 'C2009', 'C2010', 'C2011', 'C2012', 'C2013', 'C2014', 'C2015', 'C2016', 'C2017']
		Compactiondata = pandas.read_csv('X:/Upload/AreaData/Arctic_climate_compaction.csv', names=Compactioncolnames,header=0)
		self.Compaction1980s = Compactiondata.C1980s.tolist()
		self.Compaction1990s = Compactiondata.C1990s.tolist()
		self.Compaction2000s = Compactiondata.C2000s.tolist()
		self.Compaction2010s = Compactiondata.C2010s.tolist()
		self.Compaction2007 = Compactiondata.C2007.tolist()
		self.Compaction2008 = Compactiondata.C2008.tolist()
		self.Compaction2009 = Compactiondata.C2009.tolist()
		self.Compaction2010 = Compactiondata.C2010.tolist()
		self.Compaction2011 = Compactiondata.C2011.tolist()
		self.Compaction2012 = Compactiondata.C2012.tolist()
		self.Compaction2013 = Compactiondata.C2013.tolist()
		self.Compaction2014 = Compactiondata.C2014.tolist()
		self.Compaction2015 = Compactiondata.C2015.tolist()
		self.Compaction2016 = Compactiondata.C2016.tolist()
		self.Compaction2017 = Compactiondata.C2017.tolist()
	
	
	
	def automated (self,day,month,year):
		
		self.year = year
		self.month = month
		self.day = day
		self.stringmonth = str(self.month).zfill(2)
		self.stringday = str(self.day).zfill(2)
		
		self.loadCSVdata()
		self.makegraph()
		self.makegraph_full()
		self.makegraph_compaction()
#		plt.show()

action = NSIDC_Graph()
if __name__ == "__main__":
	print('main')
	action.automated(17,11,2018)
	#action.loadCSVdata()
	#action.makegraph()
	#action.makegraph_compaction()
