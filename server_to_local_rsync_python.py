import json
import subprocess
import os

def const_var(str_p):
	############## kilka linijek konfiguracyjnych ###########
	if str_p == "USER":
		return "ubuntu"
	if str_p == "UID":
		return 1000 # uid uzytkownika -> :$ id ubuntu
	if str_p == "GROUP":
		return "www-data"
	if str_p == "SERWER_TEMPLATES_PATH":
		return "/var/www/flaga"
	if str_p == "HOME_TEMPLATES_PATH":
		return "/home/"+const_var('USER')+"/python-test/templates"
	if str_p == "DOMAIN":
		return "pp.marzec.eu"
	if str_p == "LOCAL_USER":
		return "voj"
	#########################################################


local_path = "rsync-home-directory"
local_python_folder = "python-test"
key_file_name = "aws-python-xd.pem"

rsync_executed_line_list = []
rsync_executed_line_list.append('rsync -Pavp --rsh="ssh -i /home/'+const_var('LOCAL_USER')+'/.ssh/'+key_file_name+'" '+const_var('USER')+'@'+const_var('DOMAIN')+':/home/'+const_var('USER')+'/ ./'+local_path+'/')
#rsync_executed_line_list.append('rsync -Pavp --rsh="ssh -i /home/'+const_var('LOCAL_USER')+'/.ssh/'+key_file_name+'" '+const_var('USER')+'@'+const_var('DOMAIN')+':/var/www/ ./'+local_path+'/')

print('\n\n\t\t====================================================')
print('\t\t\tZaczynamy synchronizacje ....')
rsync_wynik_list = []
for rsync_executed_line in rsync_executed_line_list:
	try:
		tmp_str = subprocess.check_output(rsync_executed_line, shell=True)
		rsync_wynik_list.append(tmp_str.decode().split('\n'))
	except ValueError as e:
		print('\t\t\tNic do synchronizacji: '+const_var('USER')+'@'+const_var('DOMAIN')+':/home/'+USER+'/ ./'+local_path+'/')

print
print('\n\n\t\t====================================================')
xx = 0
while xx < len(rsync_wynik_list):
	tmp_list = list(filter(None, rsync_wynik_list[xx]))
	tmp_str = '\n\t\t'.join(tmp_list)
	#print(len(tmp_list),tmp_list)
	print('\t\t%s' %tmp_str)
	xx+= 1
print('\t\t====================================================')
print
search_word = "import"
print('\n\n\t\t\tWyszukiwanie ciągu:'+search_word)
search_lines_list = []
search_lines_list.append('less '+local_path+'/'+local_python_folder+'/*.py |grep '+search_word)
search_wynik_list = []
for search_line in search_lines_list:
	try:
		print(search_line)
		tmp_str = subprocess.check_output(search_line, shell=True)
		search_wynik_list.append(tmp_str.decode().split('\n'))
	except ValueError as e:
		print('Nie znalazlem szukanego slowa: '+search_word)

print(len(search_wynik_list))
for lib_name in search_wynik_list:
	print(lib_name[:1])




#print('rsync -Pavp --rsh="ssh -i ~/.ssh/aws-python-xd.pem" ubuntu@pp.marzec.eu:~/python-test/ ./rsync-files/')
#rsync_wynik = subprocess.check_output(rsync_executed_line, shell=True)
#import_lines_list = subprocess.check_output('less '+local_path+'/*.py |grep import', shell=True)
#print(git_out,rsync_wynik,import_lines_list)
#Usage: rsync [OPTION]... SRC [SRC]... DEST
#  or   rsync [OPTION]... SRC [SRC]... [USER@]HOST:DEST
#  or   rsync [OPTION]... SRC [SRC]... [USER@]HOST::DEST
#  or   rsync [OPTION]... SRC [SRC]... rsync://[USER@]HOST[:PORT]/DEST
#  or   rsync [OPTION]... [USER@]HOST:SRC [DEST]
#  or   rsync [OPTION]... [USER@]HOST::SRC [DEST]
#  or   rsync [OPTION]... rsync://[USER@]HOST[:PORT]/SRC [DEST]
#The ':' usages connect via remote shell, while '::' & 'rsync://' usages connect
#to an rsync daemon, and require SRC or DEST to start with a module name.
