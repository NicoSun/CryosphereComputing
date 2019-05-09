import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib import style
#style.use('ggplot')


class NSIDC_area:

	def __init__  (self):
		self.year = 2016
		self.month = 1
		self.day = 1
		
		self.daycount = 366 #366year, 186summer
		
		self.CSVDatum = ['Date']
		self.CSVArea =['Area']
		self.CSVExtent = ['Extent']
		self.CSVCompaction = ['Compaction']
		
		self.tarea_anom = ['Area Anomaly']
		self.textent_anom = ['Extent Anomaly']
		
		self.mode = 'man' #man, on
		
		
			
	def makegraph(self,df,sheet):
		fig = plt.figure(figsize=(14, 8))
		fig.suptitle(str(sheet)+' Cumulative Albedo-Warming Values (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel(''r'$ \Delta$ clear sky energy absorption in  [MJ / 'r'$m^2$]')
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		ax.text(0.55, -0.06, 'https://sites.google.com/site/cryospherecomputing/warming-potential',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		colourlist = [[0.1,0.7,0.1],[0.2,0.8,0.8],[0.65,0.1,0.4],[0.2,0.8,0.2],[0.5,0.5,0.5],[0.9,0.9,0],
		[0.9,0.1,0.1],[0.4,0,0.4],[0,0,0.6],[0.55,0.27,0.08],[1,0.6,0.2],[1,0.26,1],[0,0,0]]
		
		min = 0
		max = 0
		for col in df:
			for row in df[col]:
				if row < min:
					min = row
				if row > max:
					max = row
		
		ax.grid(True)
		#[plt.plot (df[x]) for x in df]
		#plt.plot(df,color=colourlist)
		j =0
		for i in df:
			plt.plot(df[i],color=colourlist[j])
			j=j+1
		
		
		plt.axis([0,186,min*1.1,max*1.1])
		ax.legend(loc='center left',bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
		fig.tight_layout(pad=2)
		fig.subplots_adjust(right=0.85)
		fig.subplots_adjust(top=0.95)
		fig.savefig('AWP_MJ_anomaly_sheet_'+str(sheet)+'.png')
		#plt.show()
		
		return
		
	
	
	def loadRegionaldata (self):
		
		excelfile = 'AWP_MJ_anomaly_regional_by_region.xlsx'
		for x in range(0,13):	#13 regional
			df = pd.read_excel(excelfile,sheetname=x)
			df.drop(['Date'], 1, inplace=True)
			df.drop([1988,1992,2017,2018,2019,2020], 1, inplace=True)
			
			xls = pd.ExcelFile(excelfile, on_demand = True)
			sheets = xls.sheet_names[x]
			self.makegraph(df,sheets)
		#[[plt.scatter(ii[0],ii[1],s=100,color=i) for ii in df[i]] for i in df]
		
	def loadYeardata (self):
		
		excelfile = 'AWP_MJ_anomaly_regional_by_year..xlsx'
		for x in range(0,14):	#14 years
			df = pd.read_excel(excelfile,sheetname=x)
			df.drop(['Date'], 1, inplace=True)
			
			xls = pd.ExcelFile(excelfile, on_demand = True)
			sheets = xls.sheet_names[x]
			self.makegraph(df,sheets)
		#[[plt.scatter(ii[0],ii[1],s=100,color=i) for ii in df[i]] for i in df]
	
	
	def automated (self,day,month,year):
	
		self.mode = 'auto'
	
		self.loadYeardata()
		self.dayloop()
		#self.makegraph()
		#self.makegraph_full()
		#self.makegraph_compaction()

action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	action.loadRegionaldata()
	#action.automated(1,2,2017)
	#action.makegraph()
	#action.makegraph_compaction()

#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA