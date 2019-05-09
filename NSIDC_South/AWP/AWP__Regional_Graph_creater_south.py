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
		labels = ['Sep','Oct','Nov','Dec','Jan', 'Feb', 'Mar']
		x = [-22,8,39,69,100,131,160]
		plt.xticks(x,labels)

		ax.set_ylabel(''r'$ \Delta$ clear sky energy absorption in  [MJ / 'r'$m^2$]')
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		ax.text(0.55, -0.06, 'https://sites.google.com/site/cryospherecomputing/awp',
        transform=ax.transAxes,
        color='grey', fontsize=10)
		
		colourlist = [[0.1,0.7,0.1],[0.2,0.8,0.8],[0.65,0.1,0.4],[0.2,0.8,0.2],[0.5,0.5,0.5],[0.9,0.9,0],
		[0.9,0.1,0.1],[0.4,0,0.4],[0,0,0.6],[0.55,0.27,0.08],[1,0.6,0.2],[1,0.26,1],[0,0,0]]
		
		ymin = 0
		ymax = 0
		for col in df:
			for row in df[col]:
				if row < ymin:
					ymin = row
				if row > ymax:
					ymax = row
		
		ax.grid(True)
		[plt.plot (df[x]) for x in df]
#		plt.plot(df,color=colourlist)
# =============================================================================
# 		for i,j in enumerate(df):
# 			plt.plot(j,color=colourlist[i])
# =============================================================================
		
		
		
		plt.axis([0,186,ymin*1.1,ymax*1.1])
		ax.legend(loc='center left',bbox_to_anchor=(1.01, 0.5), borderaxespad=0)
		fig.tight_layout(pad=2)
		fig.subplots_adjust(right=0.9)
		fig.subplots_adjust(top=0.95)
		fig.savefig('Graphs/AWP_MJ_anomaly_sheet_'+str(sheet)+'.png')
#		plt.show()
		
		return
		
	
	
	def loadRegionaldata (self):
		
		excelfile = 'South_AWP_region_by_region.xlsx'
		for x in range(0,10):	#10 regional
			df = pd.read_excel(excelfile,sheetname=x)
			df.drop(['Date'], 1, inplace=True)
			df.drop(['1978-79','1979-80','1980-81','1981-82','1982-83','1983-84','1984-85','1985-86','1987-88','1988-89','1989-90','1990-91','1991-92','1993-94','1994-95','1995-96','1996-97','1997-98','1998-99','1999-00','2000-01','2001-02','2002-03','2003-04','2004-05','2008-09','2009-10','2018-19','2019-20'], 1, inplace=True)
			
			xls = pd.ExcelFile(excelfile, on_demand = True)
			sheets = xls.sheet_names[x]
			self.makegraph(df,sheets)
		#[[plt.scatter(ii[0],ii[1],s=100,color=i) for ii in df[i]] for i in df]
		
	def loadYeardata (self):
		
		excelfile = 'South_AWP_region_by year.xlsx'
		for x in range(0,40):	#40 years
			df = pd.read_excel(excelfile,sheetname=x)
			df.drop(['Date'], 1, inplace=True)
			
			xls = pd.ExcelFile(excelfile, on_demand = True)
			sheets = xls.sheet_names[x]
			self.makegraph(df,sheets)
		#[[plt.scatter(ii[0],ii[1],s=100,color=i) for ii in df[i]] for i in df]
	

action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	action.loadRegionaldata()
#	action.loadYeardata()
