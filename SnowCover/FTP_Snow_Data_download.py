from ftplib import FTP
import datetime
import File_Manager


class Downloader:

	def __init__  (self):
		self.today = datetime.date.today()
		self.day_of_year = self.today.timetuple().tm_yday-1
		self.year = self.today.year
		self.month = self.today.month
		self.day = self.today.day



	def mass_download(self):
		'''download multiple days, the version number has to be changed for earlier dates, see ftp server for exact info'''
		ftp = FTP('sidads.colorado.edu')     # connect to host, default port
		ftp.login()                     # user anonymous, passwd anonymous@
		start = 297
		for count in range (start,310): #366
			try:
				filename = 'ims'+str(self.year)+str(count).zfill(3)+'_24km_v1.3.asc.gz' # final data
				filenameformatted = 'DataFiles/gzip_files/NOAA_'+str(self.year)+str(count).zfill(3)+'_24km_v1.1.asc.gz'
				print(filename)
				ftp.cwd('/pub/DATASETS/NOAA/G02156/24km//'+str(self.year))  # final gsfc
				ftp.retrbinary('RETR '+filename, open(filenameformatted, 'wb').write)
				self.extract(filenameformatted[21:])
			except:
				print('Error: '+str(self.year)+str(count).zfill(3))
			
		print('Done')
		ftp.quit()
		
	def daily_download(self):
		
		ftp = FTP('sidads.colorado.edu')     # connect to host, default port
		ftp.login()                     # user anonymous, passwd anonymous@
		
		try:
			filename = 'ims'+str(self.year)+str(self.day_of_year).zfill(3)+'_24km_v1.3.asc.gz' # final data
			filenameformatted = 'DataFiles/gzip_files/NOAA_'+str(self.year)+str(self.day_of_year).zfill(3)+'_24km_v1.1.asc.gz'
			print(filename)
			ftp.cwd('/pub/DATASETS/NOAA/G02156/24km//'+str(self.year))  # final gsfc
			ftp.retrbinary('RETR '+filename, open(filenameformatted, 'wb').write)
			ftp.quit()
		except:
			print('Error: '+str(self.year)+str(self.day_of_year).zfill(3))

		self.process_data(filenameformatted[21:])
		print('Done')


			
	def process_data(self, filenameformatted):
		File_Manager.dailyupdate(filenameformatted)

		

action = Downloader()
#action.mass_download()
action.daily_download()
#action.process_data('NOAA_2018311_24km_v1.1.asc.gz')

'''National Ice Center. 2008, updated daily. IMS Daily Northern Hemisphere Snow and Ice Analysis at 1 km, 4 km, and 24 km Resolutions, Version 1. [Indicate subset used]. Boulder, Colorado USA. NSIDC: National Snow and Ice Data Center. doi: https://doi.org/10.7265/N52R3PMC. [Date Accessed].'''