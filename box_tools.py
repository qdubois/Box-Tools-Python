#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import os, sys, timeit, csv, io
from boxsdk import Client
from boxsdk.exception import BoxAPIException
from boxsdk.object.collaboration import CollaborationRole
from auth import authenticate

FOLDER_PATH = 'download/' #define where you need the files to be stored
files_list = []

#Download file
def download_the_file(client, file_name, file_id, separator='' ):
	d = os.getcwd()+'/'+FOLDER_PATH
	#test if the path exist if not create it
	if (not os.path.exists(d)):
		os.makedirs(d)
	fdata = client.file(file_id=file_id).content()
	with open(d+file_name,'w') as f:
		f.write(fdata)
	f.closed
	return separator + '   - File: ' + file_name + ' ' # + file_id

#file info
def get_file_info(client, file_name, file_id, separator='',folder='' ):
	files_list.append([folder,file_name])
	#return separator + ';' + file_name + ' ' # + file_id
	return separator + '   - File: ' + file_name + ' ' # + file_id

#Scan recursively  & Download or Get file info
def scan_folder_and_action(client, action, folder_id, separator='', folder=''):
	x_folder = client.folder(folder_id=folder_id).get()
	items = x_folder.get_items(limit=500, offset=0)
	for item in items:
		if (item.type == 'folder' ):
			print(separator + '  + Folder: ' + item.name + ' ')
			scan_folder_and_action(client, action, item.id,separator + ' ',folder + item.name + '/'  )
		elif ( item.type == 'file' ):
			if (action == 'download'):
				print(download_the_file(client, item.name, item.id, separator))
			elif (action == 'info'):
				print(get_file_info(client, item.name, item.id, separator,folder))

#main
def main(argv):

	print('Connection init')
	oauth, _, _ = authenticate()
	client = Client(oauth)
	print('Connection established')

	start = timeit.default_timer()
	if (len(argv) == 2):
		action_param = argv[0]
		search_param = argv[1]
	else:
		print('Parameter error : Number of Paramater must be equal to 2')

	searched_folder = client.search(search_param, limit=1, offset=0,result_type='folder')
	#print searched_folder
	if (len(searched_folder) == 1):
		print('Folder ' + search_param + ' found')
		print('Start scanning & downloading folder:')
		print('+ ' + searched_folder[0].name)
		if (action_param == 'download' or  action_param == 'info'):
			scan_folder_and_action(client, action_param, searched_folder[0].id,'',searched_folder[0].name+'/')
			if(action_param == 'info'):
				filename= os.getcwd()+'/out.csv'
				with io.open(filename,'w',encoding='utf8') as csv_out_file:
					csv_out_file.write(u'folder,file_name'+'\n')
					for file_item in files_list:
						csv_out_file.write(u''+file_item[0]+';'+file_item[1]+'\n')
					csv_out_file.close()
		else:
			print('Pameter error: action unrecognized (download or info)')
	else:
		print('Folder ' + search_param + ' not found')
	stop = timeit.default_timer()
	time_exec = '{:.2f}'.format(stop - start)
	print('It took ' + time_exec + 's to execute')
	print('This is the end')


if __name__ == '__main__':
   main(sys.argv[1:])



#END OF Program
