import os
from rich import print
from rich.console import Console
# creating the console object
console = Console(width=120)
import shutil
import time

def current_milli_time():
	return round(time.time() * 1000)

def main():
	console.clear()
	############## kilka linijek konfiguracyjnych ###########
	USER = "ubuntu"
	GROUP = "www-data"
	SERWER_TEMPLATES_PATH = "/var/www/flaga"
	HOME_TEMPLATES_PATH = "/home/ubuntu/python-test/templates"
	#########################################################
	
	print('\n\n')
	file_name = console.input("\t\t\t\t*** Podaj nazwe pliku html lub wykonaj synchronizacje (rsync) - ENTER\n\t\t\t\t*** ")

	tmp_serwer_templates_path = console.input("\t\t\t\t*** Wpisz scieżke do katalogu templates na serwerze lub wciśnij ENTER\n\t\t\t\t\t (default: "+SERWER_TEMPLATES_PATH+")\n\t\t\t\t*** ")
	if tmp_serwer_templates_path != "":
		SERWER_TEMPLATES_PATH = tmp_serwer_templates_path

	tmp_home_templates_path = console.input("\t\t\t\t*** Wpisz scieżke do katalogu templates z repozytorium lub wciśnij ENTER\n\t\t\t\t\t (default: "+HOME_TEMPLATES_PATH+")\n\t\t\t\t*** ")
	if tmp_home_templates_path != "":
		HOME_TEMPLATES_PATH = tmp_home_templates_path

	if file_name in ("rsync",""):
		os.system('rsync -avzh '+HOME_TEMPLATES_PATH+' '+SERWER_TEMPLATES_PATH)
		print('Synchronizacja:\n sudo rsync -avzh '+HOME_TEMPLATES_PATH+' '+SERWER_TEMPLATES_PATH+' \n wykonana, trwa reboot serwera .... ')
	else:	
		file_path = SERWER_TEMPLATES_PATH+"/templates/"+file_name+".html"

		html_str = "<html>\n\t<head>\n\t\t<style>\n\n\t\t</style>\n\t</head>\n\t<body>"+file_name+".html {{text}}\n\n\t</body>\n</html>"

		pomin_dodawanie = 0
		tmp_file_exist = ""
		if os.path.exists(file_path):
			tmp_file_exist = console.input("\t\t\t\t\t\t*** !!! UWAGA !!! ***\n\t\t\t\t*** Plik "+file_name+" już istnieje, czy nadpisać plik? \n\t\t\t\t\t (default: Y)\n\t\t\t\t*** ")
			pomin_dodawanie = 1
			#os.remove("demofile.txt")

		if tmp_file_exist in ("t","T","Y","y",""):

			with open(file_path, 'w') as file:
				file.write(html_str)
			file.close()
			print('Zapisane, trwa reboot serwera .... ')
			
			flask_app_path = "/var/www/flaga/app.py"
			# file backup
			milli_time = str(current_milli_time())
			shutil.copy(flask_app_path, flask_app_path+'.backup.'+milli_time)
			with open(flask_app_path, 'r+') as file:
				line_list = file.readlines()
			file.close()
			count = 0
			new_list = []
			max_row = len(line_list)
			start_new_line = max_row-1
			#print('************ '+str(max_row)+' ******')
			# Strips the newline character
			for line in line_list:
				count += 1
				if pomin_dodawanie == 0:
					if count == start_new_line:
						new_list.append('@app.route(\'/'+file_name+'\')')
						new_list.append('def '+file_name+'():')
						new_list.append('    return render_template("'+file_name+'.html")')
						new_list.append('')
				#new_list.append(line.strip())
				new_list.append(line)
				#print("line=%s >> line.strip=%s" %(line,line.strip()))
				#print("Line{}: {}".format(count, line.strip()))
			
			count = 0
			max_row = len(new_list)
			start_last_line = max_row-1
			#print('************ '+str(max_row)+' ****** '+new_list)
			file1 = open(flask_app_path, 'w')
			for new_line in new_list:
				count += 1
				if count >= start_new_line and count < start_last_line:
					#print(new_line)
					file1.write(new_line)
					file1.write('\n')
				else:
					#print(new_line)
					file1.write(new_line)
		
			file1.close()

	os.system('sudo systemctl daemon-reload')
	os.system('sudo systemctl restart nginx')
	os.system('sudo systemctl restart flaga.service')

	if file_name not in ("rsync",""):
		os.system('sudo chown '+USER+'.'+GROUP+' '+file_path)
		print(os.system('ls -l '+SERWER_TEMPLATES_PATH+'/templates'))
		#print(os.system('nano '+file_path))

if __name__ == '__main__':
	if os.getuid() == 0:
		main()
	else:
		print('\n\n\t\t\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**')
		print('\t\t\t\t**-** Program ułatwiający życie ;) \t\t\t\t\t\t\t**-**')
		print('\t\t\t\t**-**\t 1. dodaje nową stronę do /var/www/flaga/templates/ oraz uaktualnia plik app.py **-**')
		print('\t\t\t\t**-**\t 2. synchronizuje katalog roboczy z /var/www/flaga/templates/ \t\t\t**-**')
		print('\t\t\t\t**-** Po wykonaniu wybranej operacji następuje restart usług.\t\t\t\t**-**')
		print('\t\t\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**')
		print('\n\n\t\t\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**')
		print('\n\t\t\t\t**-**\t\t Uruchom program ponownie z uprawnieniami root\'a lub sudo.\t\t**-**\n')
		print('\t\t\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\n\n')
