import json
import subprocess

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
		return "/home/ubuntu/python-test/templates"
	if str_p == "DOMAIN":
		return "pp.marzec.eu"
	#########################################################


git_out = "" #subprocess.check_output('git clone https://github.com/v0jt4s13/python-test ./github-clone/', shell=True)

rsync_executed_line = 'rsync -Pavp --rsh="ssh -i ~/.ssh/aws-python-xd.pem" '+const_var('USER')+'@'+const_var('DOMAIN')+':~/ ./rsync-home-directory/'
#print('rsync -Pavp --rsh="ssh -i ~/.ssh/aws-python-xd.pem" ubuntu@pp.marzec.eu:~/python-test/ ./rsync-files/')

rsync_wynik = subprocess.check_output(rsync_executed_line, shell=True)
import_lines_list = subprocess.check_output('less github-clone/*.py |grep import', shell=True)

print(rsync_wynik)


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
