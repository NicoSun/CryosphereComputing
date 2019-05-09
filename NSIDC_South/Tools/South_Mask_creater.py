import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from matplotlib import cm

class Simpleviewer:


	def __init__  (self):
		self.year = 2016
		self.month = 10
		self.day = 21
		self.daycount = 1 #366 year 183 austral summer
		
		self.dailyorcumu()
	
	
	

	def masksload(self):
	
		self.regionmask = 'Masks/region_s.msk'
		with open(self.regionmask, 'rb') as frmsk:
			hdr = frmsk.read(300)
			self.mask = np.fromfile(frmsk, dtype=np.uint8)
		self.regmaskf = np.array(self.mask, dtype=float)
		
		self.mask = self.mask.reshape(332, 316)
		for y in range (60,280):
			for x in range (40,288):
				for yoff in range(1,6):
					for xoff in range(1,6):
						for region in range (2,7):
							if self.mask[y,x]== 12 and self.mask[y-yoff,x] == region:
								self.mask[y-yoff,x] = 20+region
							if self.mask[y,x]== 12 and  self.mask[y+yoff,x] == region:
								self.mask[y+yoff,x] = 20+region
				
							if self.mask[y,x]== 12 and self.mask[y,x-xoff] == region:
								self.mask[y,x-xoff] = 20+region
							if self.mask[y,x]== 12 and  self.mask[y,x+xoff] == region:
								self.mask[y,x+xoff] = 20+region
								
							if self.mask[y,x]== 12 and self.mask[y-yoff,x-xoff] == region:
								self.mask[y-yoff,x-xoff] = 20+region
							if self.mask[y,x]== 12 and  self.mask[y+yoff,x+xoff] == region:
								self.mask[y+yoff,x+xoff] = 20+region
							if self.mask[y,x]== 12 and self.mask[y-yoff,x+xoff] == region:
								self.mask[y-yoff,x+xoff] = 20+region
							if self.mask[y,x]== 12 and  self.mask[y+yoff,x-xoff] == region:
								self.mask[y+yoff,x-xoff] = 20+region
				
				
		
		
		with open('Masks/region_s_coast.msk', 'wb') as msk:
			icewr = msk.write(self.mask)

		
		self.maskview(self.mask)
		plt.show()
		
		
		
	def maskview(self,icemap):		
		#icemap = icemap.reshape(332, 316)
		self.ax.clear()
		#self.ax.set_title('Date: '+str(self.year)+'/'+str(self.month).zfill(2)+'/'+str(self.day).zfill(2))
		#self.ax.set_xlabel(': '+str(icesum)+' Wh/m2')
		self.cax = self.ax.imshow(icemap, interpolation='nearest')
		#self.fig.savefig('Animation/Daily_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'.png')
		plt.pause(0.01)
		
		
	def dailyorcumu(self):		
		self.icenull = np.zeros(104912, dtype=float)
		self.icenull = self.icenull.reshape(332, 316)
		
		self.fig, self.ax = plt.subplots(figsize=(8, 8))
		self.cax = self.ax.imshow(self.icenull, interpolation='nearest')
		#self.cbar = self.fig.colorbar(self.cax).set_label('stuff')
		self.title = self.fig.suptitle('Mask', fontsize=14, fontweight='bold')
			
		
		
		
action = Simpleviewer()
#action.viewloop()
action.masksload()


#Values are coded as follows:

#0-250  concentration
#251 pole hole
#252 unused
#253 coastline
#254 landmask
#255 NA
