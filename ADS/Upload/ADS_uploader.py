from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import multiprocessing
import time

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

# Create GoogleDrive instance with authenticated GoogleAuth instance.
drive = GoogleDrive(gauth)

def upload():
	
	#AWP stuff
	
	file12= drive.CreateFile({ "parents": [{"id": '16HJIBLuW_9mk6RLmtF6b5SVxBk_LTlow'}]})
	file12.SetContentFile('ADS_AMSR2_SIT_Nov.nc')
	file12.Upload()

	

	
def AMSR2_SIT_Images():		
	file_list10 = drive.ListFile({'q': "'16HJIBLuW_9mk6RLmtF6b5SVxBk_LTlow' in parents and title='AMSR2_SIT_Last_Day.png' and trashed=false"}).GetList()
	if len(file_list10) == 1:
		file10 = file_list10[0]
	file_list11 = drive.ListFile({'q': "'16HJIBLuW_9mk6RLmtF6b5SVxBk_LTlow' in parents and title='AMSR2_Sea_Ice_Volume.png' and trashed=false"}).GetList()
	if len(file_list11) == 1:
		file11 = file_list11[0]
	file_list12 = drive.ListFile({'q': "'16HJIBLuW_9mk6RLmtF6b5SVxBk_LTlow' in parents and title='AMSR2_Sea_Ice_Thickness.png' and trashed=false"}).GetList()
	if len(file_list12) == 1:
		file12 = file_list12[0]
		
	file10.SetContentFile('AMSR2_SIT_Last_Day.png')
	file10.Upload()
	file11.SetContentFile('AMSR2_Sea_Ice_Volume.png')
	file11.Upload()
	file12.SetContentFile('AMSR2_Sea_Ice_Thickness.png')
	file12.Upload()

	print('Images done')

def AMSR2_SIT_csv():	
	file_list20 = drive.ListFile({'q': "'16HJIBLuW_9mk6RLmtF6b5SVxBk_LTlow' in parents and title='AMSR2_SIT_Volume.csv' and trashed=false"}).GetList()
	if len(file_list20) == 1:
		file20 = file_list20[0]
	file_list21 = drive.ListFile({'q': "'16HJIBLuW_9mk6RLmtF6b5SVxBk_LTlow' in parents and title='AMSR2_SIT_Thickness.csv' and trashed=false"}).GetList()
	if len(file_list21) == 1:
		file21 = file_list21[0]
		
	file20.SetContentFile('AMSR2_SIT_Volume.csv')
	file20.Upload()
	file21.SetContentFile('AMSR2_SIT_Thickness.csv')
	file21.Upload()
	print('csv done')
	
def AMSR2_SIT_gif():	
	file_list12 = drive.ListFile({'q': "'16HJIBLuW_9mk6RLmtF6b5SVxBk_LTlow' in parents and title='AMSR2_SIT_Last_month.gif' and trashed=false"}).GetList()
	if len(file_list12) == 1:
		file12 = file_list12[0]
		
	file12.SetContentFile('AMSR2_SIT_Last_month.gif')
	file12.Upload()

	print('gif done')
	
def AMSR2_SIT_NETCDF():	
	import datetime
	today = datetime.date.today()
	lastmonth = today.month
	
	monthlist = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
	
	file= drive.CreateFile({ "parents": [{"id": '16HJIBLuW_9mk6RLmtF6b5SVxBk_LTlow'}]})
	file.SetContentFile('ADS_AMSR2_SIT_{}.nc'.format(monthlist[lastmonth-2]))
	file.Upload()

	print('NETCDF done')


if __name__ == '__main__':
#	upload()

	a = multiprocessing.Process(target=AMSR2_SIT_Images) 
	b = multiprocessing.Process(target=AMSR2_SIT_csv) 
	c = multiprocessing.Process(target=AMSR2_SIT_NETCDF)
	d = multiprocessing.Process(target=AMSR2_SIT_gif) 
#
	a.start()
	b.start()
	time.sleep(1)
	c.start()
	d.start()

