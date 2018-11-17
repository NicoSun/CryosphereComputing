"""
Created on Sun Oct 21 13:36:16 2018
@author: Nico Sun

The script decompresses and renames the sea ice thickness ADS files from
https://ads.nipr.ac.jp/portal/kiwa/Summary.action?owner_site=ADS&selectFile=A20170123-003&version=1.00&scr=list_home

"""

import os
import sys
import shutil
import re
import gzip
import ADS_SIT


def deletion(year,month,pattern):
	'''this function deletes ascencion node files and SIT files with 00 version numbers'''
	filepath = 'DataFiles/{}{}'.format(str(year),str(month).zfill(2))
	for file in os.listdir(filepath):
		if re.search(pattern,file):
			print(os.path.join(filepath,file))
			os.remove(os.path.join(filepath,file))

	
def rename(year,month):
	'''this function renames all files to the format ADS_SIT_YYYYMMDD'''
	filepath = 'DataFiles/{}{}'.format(str(year),str(month).zfill(2))
	for file in os.listdir(filepath):		
		pattern = r'{}{}..D'.format(str(year),str(month).zfill(2))
		match = re.search(pattern,file)
		if match:
			#print(match.group(0)[0:8])
			#print(os.path.join(filepath,file))
			os.rename(os.path.join(filepath,file),os.path.join(filepath,'ADS_SIT_'+match.group(0)[0:8]+'.dat.gz'))
			#print(os.path.join(filepath,'ADS_SIT_'+match.group(0)[0:8]))
		
def decompress(year,month):
	'''this function decompresses all renamed files'''
	filepath = 'DataFiles/{}{}'.format(str(year),str(month).zfill(2))
	for file in os.listdir(filepath):		
		pattern = r'ADS' 
		match = re.search(pattern,file)
		if match:
			#print(os.path.join(filepath,file))
			print(os.path.join('DataFiles',file[0:16]+'.dat'))
			with gzip.open(os.path.join(filepath,file), mode='rb') as fr:
				file_content = fr.read()
				
			with open(os.path.join('DataFiles',file[0:16]+'.dat'), 'wb') as fw:
				fw.write(file_content)


year = 2018
month = 10
day = 1
daycount = 31


#patterns: r'A_' Ascending nodes ; r'D_00' old versions;
deletion(year,month,r'A_')
deletion(year,month,r'D_00')
rename(year,month)
decompress(year,month)

ADS_SIT.action.automated(day,month,year,daycount)
