import numpy as np
import pandas
import matplotlib.pyplot as plt



class AWP_graphs:

	def __init__  (self):
		self.labelfont = {'fontname':'Arial'}
		
	def minus(self,a,b):
		'''calculates the FDD anomaly'''
		a = float(a)
		b = float(b)
		c = a-b
		return c
		

	def dailygraph(self):
		
		Climatecolnames = ['Date', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Climatology/Arctic_AWP_pan_Daily.csv', names=Climatecolnames,header=0)
		Date = Climatedata.Date.tolist()
		
		C2000s = Climatedata.A.tolist()
		C2010s = Climatedata.B.tolist()
		C2012 = Climatedata.C.tolist()
		C2013 = Climatedata.D.tolist()
		C2016 = Climatedata.E.tolist()
		C2017 = Climatedata.F.tolist()
		C2018 = Climatedata.G.tolist()
		
		C2000s_anom = list(map(self.minus,C2000s,self.AWP_Daily_mean))
		C2010s_anom = list(map(self.minus,C2010s,self.AWP_Daily_mean))
		C2012_anom = list(map(self.minus,C2012,self.AWP_Daily_mean))
		C2013_anom = list(map(self.minus,C2013,self.AWP_Daily_mean))
		C2016_anom = list(map(self.minus,C2016,self.AWP_Daily_mean))
		C2017_anom = list(map(self.minus,C2017,self.AWP_Daily_mean))
		C2018_anom = list(map(self.minus,C2018,self.AWP_Daily_mean))
		current_anom = list(map(self.minus,self.CSVDaily,self.AWP_Daily_mean))
	
		
		fig = plt.figure(figsize=(10,6.5))
		fig.suptitle('Daily Pan Arctic Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-10,10,0.5)
		ax.set_yticks(major_ticks)
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,color='grey', fontsize=10)
		ax.text(0.75, -0.06, 'cryospherecomputing.tk/awp',transform=ax.transAxes,color='grey', fontsize=10)
		ax.text(0.75, 0.02, 'Anomaly Base: 2000-2018', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
		
		ax.grid(True)
		plt.plot( C2000s_anom, color=(0.7,0.7,0.7),label='2000s',lw=2,ls='--')
		plt.plot( C2010s_anom, color=(0.25,0.25,0.25),label='2010s',lw=2,ls='--')
		plt.plot( C2012_anom, color='orange',label='2012',lw=1)
		plt.plot( C2013_anom, color='purple',label='2013',lw=1)
		plt.plot( C2016_anom, color='green',label='2016',lw=1)
		plt.plot( C2017_anom, color='brown',label='2017',lw=1)
		plt.plot( C2018_anom, color='red',label='2018',lw=1)
		plt.plot( current_anom, color='black',label='2019',lw=2)
		
		ymin = -1
		ymax = 1.6
		plt.axis([0,186,ymin,ymax])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		lgd = ax.legend(loc='upper right')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(top=0.95)
		fig.savefig('X:/Upload/AWP/North_AWP_Graph1.png',bbox_extra_artists=(lgd,))

	
	def cumugraph(self):
		
		Climatecolnames = ['Date', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Climatology/Arctic_AWP_pan_Acumulated.csv', names=Climatecolnames,header=0)
		Date = Climatedata.Date.tolist()
		
		C2000s = Climatedata.A.tolist()
		C2010s = Climatedata.B.tolist()
		C2012 = Climatedata.C.tolist()
		C2013 = Climatedata.D.tolist()
		C2016 = Climatedata.E.tolist()
		C2017 = Climatedata.F.tolist()
		C2018 = Climatedata.G.tolist()
		
		C2000s_anom = list(map(self.minus,C2000s,self.AWP_Accu_mean))
		C2010s_anom = list(map(self.minus,C2010s,self.AWP_Accu_mean))
		C2012_anom = list(map(self.minus,C2012,self.AWP_Accu_mean))
		C2013_anom = list(map(self.minus,C2013,self.AWP_Accu_mean))
		C2016_anom = list(map(self.minus,C2016,self.AWP_Accu_mean))
		C2017_anom = list(map(self.minus,C2017,self.AWP_Accu_mean))
		C2018_anom = list(map(self.minus,C2018,self.AWP_Accu_mean))
		current_anom = list(map(self.minus,self.CSVCumu,self.AWP_Accu_mean))
	
		
		fig = plt.figure(figsize=(10,6.5))
		fig.suptitle('Acumulated Pan Arctic Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-500,500,10)
		ax.set_yticks(major_ticks)
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,color='grey', fontsize=10)
		ax.text(0.75, -0.06, 'cryospherecomputing.tk/awp', transform=ax.transAxes, color='grey', fontsize=10)
		ax.text(0.75, 0.02, 'Anomaly Base: 2000-2018', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
		
		ax.grid(True)
		plt.plot( C2000s_anom, color=(0.7,0.7,0.7),label='2000s',lw=2,ls='--')
		plt.plot( C2010s_anom, color=(0.25,0.25,0.25),label='2010s',lw=2,ls='--')
		plt.plot( C2012_anom, color='orange',label='2012',lw=1)
		plt.plot( C2013_anom, color='purple',label='2013',lw=1)
		plt.plot( C2016_anom, color='green',label='2016',lw=1)
		plt.plot( C2017_anom, color='brown',label='2017',lw=1)
		plt.plot( C2018_anom, color='red',label='2018',lw=1)
		plt.plot( current_anom, color='black',label='2019',lw=2)
		
		ymin = -60
		ymax = 120
		plt.axis([0,186,ymin,ymax])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		lgd = ax.legend(loc='upper left')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(top=0.95)
		fig.savefig('X:/Upload/AWP/North_AWP_Graph2.png',bbox_extra_artists=(lgd,))
		
	def centredailygraph(self):
		
		Climatecolnames = ['Date', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Climatology/Arctic_AWP_centre_Daily.csv', names=Climatecolnames,header=0)
		Date = Climatedata.Date.tolist()
		
		C2000s = Climatedata.A.tolist()
		C2010s = Climatedata.B.tolist()
		C2012 = Climatedata.C.tolist()
		C2013 = Climatedata.D.tolist()
		C2016 = Climatedata.E.tolist()
		C2017 = Climatedata.F.tolist()
		C2018 = Climatedata.G.tolist()
		
		C2000s_anom = list(map(self.minus,C2000s,self.AWP_centre_Daily_mean))
		C2010s_anom = list(map(self.minus,C2010s,self.AWP_centre_Daily_mean))
		C2012_anom = list(map(self.minus,C2012,self.AWP_centre_Daily_mean))
		C2013_anom = list(map(self.minus,C2013,self.AWP_centre_Daily_mean))
		C2016_anom = list(map(self.minus,C2016,self.AWP_centre_Daily_mean))
		C2017_anom = list(map(self.minus,C2017,self.AWP_centre_Daily_mean))
		C2018_anom = list(map(self.minus,C2018,self.AWP_centre_Daily_mean))
		current_anom = list(map(self.minus,self.CSVDaily_central,self.AWP_centre_Daily_mean))
	
		
		fig = plt.figure(figsize=(10,6.5))
		fig.suptitle('Daily High Arctic Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-10,10,0.5)
		ax.set_yticks(major_ticks)
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,color='grey', fontsize=10)
		ax.text(0.75, -0.06, 'cryospherecomputing.tk/awp',transform=ax.transAxes,color='grey', fontsize=10)
		ax.text(0.75, 0.02, 'Anomaly Base: 2000-2018', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
		
		ax.grid(True)
		plt.plot( C2000s_anom, color=(0.7,0.7,0.7),label='2000s',lw=2,ls='--')
		plt.plot( C2010s_anom, color=(0.25,0.25,0.25),label='2010s',lw=2,ls='--')
		plt.plot( C2012_anom, color='orange',label='2012',lw=1)
		plt.plot( C2013_anom, color='purple',label='2013',lw=1)
		plt.plot( C2016_anom, color='green',label='2016',lw=1)
		plt.plot( C2017_anom, color='brown',label='2017',lw=1)
		plt.plot( C2018_anom, color='red',label='2018',lw=1)
		plt.plot( current_anom, color='black',label='2019',lw=2)
		
		ymin = -1.1
		ymax = 2.6
		plt.axis([0,186,ymin,ymax])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		lgd = ax.legend(loc='upper right')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(top=0.95)
		fig.savefig('X:/Upload/AWP/North_AWP_Graph3.png',bbox_extra_artists=(lgd,))

	
	def centreaccumulatedgraph(self):
		
		Climatecolnames = ['Date', 'A', 'B', 'C', 'D', 'E', 'F', 'G']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Climatology/Arctic_AWP_centre_Acumulated.csv', names=Climatecolnames,header=0)
		Date = Climatedata.Date.tolist()
		
		C2000s = Climatedata.A.tolist()
		C2010s = Climatedata.B.tolist()
		C2012 = Climatedata.C.tolist()
		C2013 = Climatedata.D.tolist()
		C2016 = Climatedata.E.tolist()
		C2017 = Climatedata.F.tolist()
		C2018 = Climatedata.G.tolist()
		
		C2000s_anom = list(map(self.minus,C2000s,self.AWP_centre_Accu_mean))
		C2010s_anom = list(map(self.minus,C2010s,self.AWP_centre_Accu_mean))
		C2012_anom = list(map(self.minus,C2012,self.AWP_centre_Accu_mean))
		C2013_anom = list(map(self.minus,C2013,self.AWP_centre_Accu_mean))
		C2016_anom = list(map(self.minus,C2016,self.AWP_centre_Accu_mean))
		C2017_anom = list(map(self.minus,C2017,self.AWP_centre_Accu_mean))
		C2018_anom = list(map(self.minus,C2018,self.AWP_centre_Accu_mean))
		current_anom = list(map(self.minus,self.CSVAccu_central,self.AWP_centre_Accu_mean))
	
		
		fig = plt.figure(figsize=(10,6.5))
		fig.suptitle('Acumulated High Arctic Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-500,500,20)
		ax.set_yticks(major_ticks)
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,color='grey', fontsize=10)
		ax.text(0.75, -0.06, 'cryospherecomputing.tk/awp', transform=ax.transAxes, color='grey', fontsize=10)
		ax.text(0.75, 0.02, 'Anomaly Base: 2000-2018', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
		
		ax.grid(True)
		plt.plot( C2000s_anom, color=(0.7,0.7,0.7),label='2000s',lw=2,ls='--')
		plt.plot( C2010s_anom, color=(0.25,0.25,0.25),label='2010s',lw=2,ls='--')
		plt.plot( C2012_anom, color='orange',label='2012',lw=1)
		plt.plot( C2013_anom, color='purple',label='2013',lw=1)
		plt.plot( C2016_anom, color='green',label='2016',lw=1)
		plt.plot( C2017_anom, color='brown',label='2017',lw=1)
		plt.plot( C2018_anom, color='red',label='2018',lw=1)
		plt.plot( current_anom, color='black',label='2019',lw=2)
		
		ymin = -80
		ymax = 180
		plt.axis([0,186,ymin,ymax])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		lgd = ax.legend(loc='upper left')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(top=0.95)
		fig.savefig('X:/Upload/AWP/North_AWP_Graph4.png',bbox_extra_artists=(lgd,))

			
	def regiongraph(self):
		
		Climatecolnames = ['Date','B','C','D','E','F','G','H','I','J','K','L','M','N']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Climatology/Arctic_AWP_mean_regional.csv', names=Climatecolnames,header=0)
		Date = Climatedata.Date.tolist()
		
		SoO_mean = Climatedata.B.tolist()
		Bers_mean = Climatedata.C.tolist()
		HB_mean = Climatedata.D.tolist()
		BB_mean = Climatedata.E.tolist()
		EG_mean = Climatedata.F.tolist()
		BaS_mean = Climatedata.G.tolist()
		KS_mean = Climatedata.H.tolist()
		LS_mean = Climatedata.I.tolist()
		ES_mean = Climatedata.J.tolist()
		CS_mean = Climatedata.K.tolist()
		BeaS_mean = Climatedata.L.tolist()
		CA_mean = Climatedata.M.tolist()
		AB_mean = Climatedata.N.tolist()
				
		Region1 = list(map(self.minus,self.SoO,SoO_mean))
		Region2 = list(map(self.minus,self.Bers,Bers_mean))
		Region3 = list(map(self.minus,self.HB,HB_mean))
		Region4 = list(map(self.minus,self.BB,BB_mean))
		Region5 = list(map(self.minus,self.EG,EG_mean))
		Region6 = list(map(self.minus,self.BaS,BaS_mean))
		Region7 = list(map(self.minus,self.KS,KS_mean))
		Region8 = list(map(self.minus,self.LS,LS_mean))
		Region9 = list(map(self.minus,self.ES,ES_mean))
		Region10 = list(map(self.minus,self.CS,CS_mean))
		Region11 = list(map(self.minus,self.BeaS,BeaS_mean))
		Region12 = list(map(self.minus,self.CA,CA_mean))
		Region13 = list(map(self.minus,self.AB,AB_mean))
		
		data = [Region1,Region2,Region3,Region4,Region5,Region6,Region7,Region8,Region9,Region10,Region11,Region12,Region13]

		fig = plt.figure(figsize=(10,6.5))
		fig.suptitle(str(self.year)+' Acumulated Regional Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-800,800,25)
		ax.set_yticks(major_ticks)
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.75, -0.06, 'cryospherecomputing.tk/awp', transform=ax.transAxes, color='grey', fontsize=10)
		ax.text(0.75, 0.02, 'Anomaly Base: 2000-2018', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
		
		ax.grid(True)
		
		plt.plot( Region1, color=(0.1,0.7,0.1),label='Sea of Okhotsk',lw=2)
		plt.plot( Region2, color=(0.2,0.8,0.8),label='Bering Sea',lw=2)
		plt.plot( Region3, color=(0.65,0.1,0.4),label='Hudson Bay',lw=2)
		plt.plot( Region4, color=(0.2,0.8,0.2),label='Baffin Bay',lw=2)
		plt.plot( Region5, color=(0.5,0.5,0.5),label='East Greenland',lw=2)
		plt.plot( Region6, color=(0.9,0.9,0),label='Barents Sea',lw=2)
		plt.plot( Region7, color=(0.9,0.1,0.1),label='Kara Sea',lw=2)
		plt.plot( Region8, color=(0.4,0,0.4),label='Laptev Sea',lw=2)
		plt.plot( Region9, color=(0,0,0.6),label='East. Siberian',lw=2)
		plt.plot( Region10, color=(0.55,0.27,0.08),label='Chukchi',lw=2)
		plt.plot( Region11, color=(1,0.6,0.2),label='Beaufort Sea',lw=2)
		plt.plot( Region12, color=(1,0.26,1),label='Can. Archipelago',lw=2)
		plt.plot( Region13, color='black',label='Central Arctic',lw=2)
		
		ymin = 0
		ymax = 0
		
		for x in data:
			value = x[-1]
			if value > ymax:
				ymax = value
			if value < ymin:
				ymin = value
			
		plt.axis([0,len(Region1),min(-15,ymin*1.1),ymax*1.1])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		lgd = ax.legend(loc='upper left')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(top=0.95)
		#fig.subplots_adjust(bottom=0.1)
		fig.savefig('X:/Upload/AWP/North_AWP_Graph_Region1.png')

			
	def regiongraph_daily(self):
		
		Climatecolnames = ['Date','B','C','D','E','F','G','H','I','J','K','L','M','N']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Climatology/Arctic_AWP_mean_regional_daily.csv', names=Climatecolnames,header=0)
		Date = Climatedata.Date.tolist()
		
		SoO_mean = Climatedata.B.tolist()
		Bers_mean = Climatedata.C.tolist()
		HB_mean = Climatedata.D.tolist()
		BB_mean = Climatedata.E.tolist()
		EG_mean = Climatedata.F.tolist()
		BaS_mean = Climatedata.G.tolist()
		KS_mean = Climatedata.H.tolist()
		LS_mean = Climatedata.I.tolist()
		ES_mean = Climatedata.J.tolist()
		CS_mean = Climatedata.K.tolist()
		BeaS_mean = Climatedata.L.tolist()
		CA_mean = Climatedata.M.tolist()
		AB_mean = Climatedata.N.tolist()
				
		Region1 = list(map(self.minus,self.SoO_daily,SoO_mean))
		Region2 = list(map(self.minus,self.Bers_daily,Bers_mean))
		Region3 = list(map(self.minus,self.HB_daily,HB_mean))
		Region4 = list(map(self.minus,self.BB_daily,BB_mean))
		Region5 = list(map(self.minus,self.EG_daily,EG_mean))
		Region6 = list(map(self.minus,self.BaS_daily,BaS_mean))
		Region7 = list(map(self.minus,self.KS_daily,KS_mean))
		Region8 = list(map(self.minus,self.LS_daily,LS_mean))
		Region9 = list(map(self.minus,self.ES_daily,ES_mean))
		Region10 = list(map(self.minus,self.CS_daily,CS_mean))
		Region11 = list(map(self.minus,self.BeaS_daily,BeaS_mean))
		Region12 = list(map(self.minus,self.CA_daily,CA_mean))
		Region13 = list(map(self.minus,self.AB_daily,AB_mean))
		
		data = [Region1,Region2,Region3,Region4,Region5,Region6,Region7,Region8,Region9,Region10,Region11,Region12,Region13]

		fig = plt.figure(figsize=(10,6.5))
		fig.suptitle(str(self.year)+' Daily Regional Albedo-Warming Potential (Anomaly)', fontsize=14, fontweight='bold')
		ax = fig.add_subplot(111)
		labels = ['Mar','Apr','May','Jun','Jul', 'Aug', 'Sep']
		x = [-20,11,42,72,103,134,163]
		plt.xticks(x,labels)

		ax.set_ylabel('clear sky energy absorption anomaly in [MJ / 'r'$m^2$]',**self.labelfont)
		major_ticks = np.arange(-20,20,0.5)
		ax.set_yticks(major_ticks)
		
		ax.text(0.01, -0.06, 'Last date: {}-{}-{}'.format(self.year,self.stringmonth,self.stringday),
        transform=ax.transAxes,
        color='grey', fontsize=10)
		ax.text(0.75, -0.06, 'cryospherecomputing.tk/awp', transform=ax.transAxes, color='grey', fontsize=10)
		ax.text(0.75, 0.02, 'Anomaly Base: 2000-2018', color='black',fontweight='bold',transform=ax.transAxes, fontsize=10)
		
		ax.grid(True)
		
		plt.plot( Region1, color=(0.1,0.7,0.1),label='Sea of Okhotsk',lw=2)
		plt.plot( Region2, color=(0.2,0.8,0.8),label='Bering Sea',lw=2)
		plt.plot( Region3, color=(0.65,0.1,0.4),label='Hudson Bay',lw=2)
		plt.plot( Region4, color=(0.2,0.8,0.2),label='Baffin Bay',lw=2)
		plt.plot( Region5, color=(0.5,0.5,0.5),label='East Greenland',lw=2)
		plt.plot( Region6, color=(0.9,0.9,0),label='Barents Sea',lw=2)
		plt.plot( Region7, color=(0.9,0.1,0.1),label='Kara Sea',lw=2)
		plt.plot( Region8, color=(0.4,0,0.4),label='Laptev Sea',lw=2)
		plt.plot( Region9, color=(0,0,0.6),label='East. Siberian',lw=2)
		plt.plot( Region10, color=(0.55,0.27,0.08),label='Chukchi',lw=2)
		plt.plot( Region11, color=(1,0.6,0.2),label='Beaufort Sea',lw=2)
		plt.plot( Region12, color=(1,0.26,1),label='Can. Archipelago',lw=2)
		plt.plot( Region13, color='black',label='Central Arctic',lw=2)
		
		ymin = -3
		ymax = 6
					
		plt.axis([0,len(Region1),ymin,ymax])
		
		ax.text(0.02, 0.05, r'Concentration Data: NSIDC', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		ax.text(0.02, 0.03, r'Calculations: Nico Sun', fontsize=10,color='black',fontweight='bold',transform=ax.transAxes)
		
		lgd = ax.legend(loc='upper left')
		fig.tight_layout(pad=1)
		fig.subplots_adjust(top=0.95)
		fig.savefig('X:/Upload/AWP/North_AWP_Graph_Region2.png')

	
	def loadCSVdata (self):
		Yearcolnames = ['Date','B','C','D','E']
		Yeardata = pandas.read_csv('X:/Upload/AWP_data/Arctic_AWP_NRT.csv', names=Yearcolnames,header=0)
		self.CSVDatum = Yeardata.Date.tolist()
		self.CSVDaily = Yeardata.B.tolist()
		self.CSVCumu = Yeardata.C.tolist()
		self.CSVDaily_central = Yeardata.D.tolist()
		self.CSVAccu_central = Yeardata.E.tolist()
		
		AWP_mean = ['A','B','C','D']
		Climatedata = pandas.read_csv('X:/Upload/AWP_data/Climatology/Arctic_AWP_mean.csv', names=AWP_mean,header=0)
		self.AWP_Daily_mean = Climatedata.A.tolist()
		self.AWP_Accu_mean = Climatedata.B.tolist()
		self.AWP_centre_Daily_mean = Climatedata.C.tolist()
		self.AWP_centre_Accu_mean = Climatedata.D.tolist()
	
	
	def loadCSVRegiondata (self):
		Yearcolnames = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
		Yeardata = pandas.read_csv('X:/Upload/AWP_data/Arctic_AWP_NRT_regional.csv', names=Yearcolnames,header=0)
		self.SoO = Yeardata.Sea_of_Okhotsk.tolist()
		self.Bers = Yeardata.Bering_Sea.tolist()
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
		
		Yearcolnames_daily = ['Sea_of_Okhotsk', 'Bering_Sea', 'Hudson_Bay', 'Baffin_Bay', 'East_Greenland_Sea', 'Barents_Sea', 'Kara_Sea', 'Laptev_Sea', 'East_Siberian_Sea', 'Chukchi_Sea', 'Beaufort_Sea', 'Canadian_Archipelago', 'Central_Arctic']
		Yeardata_daily = pandas.read_csv('X:/Upload/AWP_data/Arctic_AWP_NRT_regional_daily.csv', names=Yearcolnames_daily,header=0)
		self.SoO_daily = Yeardata_daily.Sea_of_Okhotsk.tolist()
		self.Bers_daily = Yeardata_daily.Bering_Sea.tolist()
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
	
	
	
	def automated (self,year,month,day):
		
		self.year = year
		self.stringmonth = month
		self.stringday = day
		
		self.loadCSVdata()
		self.loadCSVRegiondata()

		self.dailygraph()
		self.cumugraph()
		self.centredailygraph()
		self.centreaccumulatedgraph()
		self.regiongraph()
		self.regiongraph_daily()
#		plt.show()
		

action = AWP_graphs()
if __name__ == "__main__":
	print('main')
	action.automated(2019,'04','33') 

