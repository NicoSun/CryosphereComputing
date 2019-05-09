import pandas as pd
import matplotlib.pyplot as plt
import csv



class NSIDC_area:

	def __init__  (self):
		
		self.SoO = ['Sea of Okhotsk']
		self.Bers = ['Bering Sea']
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
		
		self.datum = []
		self.AWP_Daily_mean = []
		self.AWP_Accu_mean = []
		self.AWP_Daily_mean_centre = []
		self.AWP_Accu_mean_centre = []

			
	def makeSuperRegionList(self,df,sheet):
#		self.SoO.append(sheet)
		SuperList = [df.values.tolist()]
		
#		superlist[year][row][column]
		for x in range(0,len(df)):
			self.SoO.append(SuperList[0][x][0])
			self.Bers.append(SuperList[0][x][1])
			self.HB.append(SuperList[0][x][2])
			self.BB.append(SuperList[0][x][3])
			self.EG.append(SuperList[0][x][4])
			self.BaS.append(SuperList[0][x][5])
			self.KS.append(SuperList[0][x][6])
			self.LS.append(SuperList[0][x][7])
			self.ES.append(SuperList[0][x][8])
			self.CS.append(SuperList[0][x][9])
			self.BeaS.append(SuperList[0][x][10])
			self.CA.append(SuperList[0][x][11])
			self.AB.append(SuperList[0][x][12])
		
#		print(SuperList[0][0])
#		print(self.SoO)
			
	def makeSuperList(self,data):
		
		for x,y in enumerate(data[0]):
			self.datum.append(data[0][x])
			self.AWP_Daily_mean.append(data[1][x])
			self.AWP_Accu_mean.append(data[2][x])
			self.AWP_Daily_mean_centre.append(data[3][x])
			self.AWP_Accu_mean_centre.append(data[4][x])
		
	def writeRegionfile(self):
		
		with open('Super_regional_List.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.SoO))):
				writer.writerow([self.SoO[x],self.Bers[x],self.HB[x],self.BB[x],self.EG[x],
					 self.BaS[x],self.KS[x],self.LS[x],self.ES[x],self.CS[x],self.BeaS[x],self.CA[x],self.AB[x]])
	
	def writetofile(self):
		with open('Super_regional_mutli_region.csv', "w") as output:
			writer = csv.writer(output, lineterminator='\n')
			for x in range(0,(len(self.datum))):
				writer.writerow([self.datum[x],self.AWP_Daily_mean[x],self.AWP_Accu_mean[x],self.AWP_Daily_mean_centre[x],
					 self.AWP_Accu_mean_centre[x]])
	
	def loadyearcsvdata (self):
		for yearload in range(1979,2019):
			AWP_mean = ['A', 'B', 'C', 'D', 'E']
			Climatedata = pd.read_csv('raw/_AWP_{}.csv'.format(yearload), names=AWP_mean)
			column1 = Climatedata.A.tolist()
			column2 = Climatedata.B.tolist()
			column3 = Climatedata.C.tolist()
			column4 = Climatedata.D.tolist()
			column5 = Climatedata.E.tolist()
			data = [column1,column2,column3,column4,column5]
			self.makeSuperList(data)
			
		self.writetofile()
		
	def loadYeardata (self):
		
		excelfile = 'AWP_regional_by_year.xlsx'
		for x in range(0,42):	#41 years
			df = pd.read_excel(excelfile,sheet_name=x)
			df.drop(['Date'], 1, inplace=True)
			
			xls = pd.ExcelFile(excelfile, on_demand = True)
			sheets = xls.sheet_names[x]
			self.makeSuperRegionList(df,sheets)
		self.writeRegionfile()
		


action = NSIDC_area()
if __name__ == "__main__":
	print('main')
	action.loadYeardata()
#	action.loadyearcsvdata()
