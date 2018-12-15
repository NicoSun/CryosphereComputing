from ftplib import FTP
import numpy as np


class Downloader:

	def __init__  (self):
		self.year = 2018
		self.month = 1
		self.day = 1
		self.daycount = 1 #year
		#start:n07, 19870821: f08, 1991219: f11 ,19950930: f13, 2008: f17

		

	def dayloop(self):
		
		ftp = FTP('sidads.colorado.edu')     # connect to host, default port
		ftp.login()                     # user anonymous, passwd anonymous@
		
		for count in range (0,self.daycount+1,1): 
		
			filenameNRT = 'nt_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'_f18_nrt_s.bin' # near realtime
			filenamefinal = 'nt_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'_f13_v1.1_s.bin' # final data
			filename2 = 'X:/NSIDC_south/DataFiles/NSIDC_'+str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2)+'_south.bin'
			
			ftp.cwd('/pub/DATASETS/nsidc0081_nrt_nasateam_seaice/south/')  # near realtime
			#ftp.cwd('/pub/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/south/daily/'+str(self.year))  # final gsfc
			ftp.retrbinary('RETR '+filenameNRT, open(filename2, 'wb').write)
			self.format(filename2)
			
						
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
				
		print('Done')
		ftp.quit()
		
			
	def format(self, newfilename):
	
		try:
			with open(newfilename, 'rb') as fr:
				header = fr.read(300)
				ice = np.fromfile(fr, dtype=np.uint8)
		except:
			print('cant read')
					
		try:
			with open(newfilename, 'wb') as frr:
				frr.write(ice)
		except:
			print('cant write')
		print(self.year,self.month,self.day)

action = Downloader()
action.dayloop()

