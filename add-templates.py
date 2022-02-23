import sys
import os
from rich import print
from rich.console import Console
# creating the console object
console = Console(width=120)
import shutil
import time

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
	#########################################################

def current_milli_time():
	return round(time.time() * 1000)

def main(argv):
	import subprocess
	console.clear()
	
	if len(argv) > 1 and argv[1] == "3":
		commit_text = console.input("\t\t\t\t*** Wpisz opis dla 'git commit': \n\t\t\t\t*** ")
		init_user = subprocess.check_output('whoami', shell=True)
		init_dir = subprocess.check_output('pwd', shell=True)
		init_user = init_user.decode().replace('\n','') #, os.system('pwd'))
		init_dir = init_dir.decode().replace('\n','')
		uid = const_var('UID')
		print('==>'+init_user+'<==='+init_dir+'===>'+str(uid))
		print()
		if init_user == "root":
			print("Real user ID of the current process:", os.getuid())
			change_user_resp = os.setuid(uid)
			print("Real user ID after changes:", os.getuid())
			#change_user_resp = subprocess.check_output(change_user_resp, shell=True)
			#print(change_user_resp)
			#new_user = subprocess.check_output('whoami', shell=True)
			os.system('cd '+init_dir+' && pwd')

		print(os.system('git add -A .; git commit -m "'+commit_text+'"; git push'))
		print('Wypchanie kodu na GitHub:\n git add -A .; git commit -m "'+commit_text+'"; git push')
	else:
		print('\n\n')
		option_nr = console.input("\t\t\t\t*** Wybierz jedną z poniższych opcji: \n\t\t\t\t*** 1. nazwe pliku html \n\t\t\t\t*** 2. wykonaj synchronizacje (rsync) \n\t\t\t\t*** 3. wypchnij kod na GitHub\n\t\t\t\t*** ")
		file_name = ""
		if option_nr == "1":
			file_name = console.input("\t\t\t\t*** Podaj nazwę pliku html (bez rozszerzenia): \n\t\t\t\t*** ")
		elif option_nr == "3":
			commit_text = console.input("\t\t\t\t*** Wpisz opis dla 'git commit': \n\t\t\t\t*** ")
			print(os.system('whoami'))
			print(os.system('git add -A .; git commit -m "'+commit_text+'"; git push'))
			print('Wypchanie kodu na GitHub:\n git add -A .; git commit -m "'+commit_text+'"; git push')
		
		if option_nr != "3":
			tmp_serwer_templates_path = console.input("\t\t\t\t*** Wpisz scieżke do katalogu templates na serwerze lub wciśnij ENTER\n\t\t\t\t\t (default: "+const_var('SERWER_TEMPLATES_PATH')+")\n\t\t\t\t*** ")
			if tmp_serwer_templates_path != "":
				SERWER_TEMPLATES_PATH = tmp_serwer_templates_path

			tmp_home_templates_path = console.input("\t\t\t\t*** Wpisz scieżke do katalogu templates z repozytorium lub wciśnij ENTER\n\t\t\t\t\t (default: "+const_var('HOME_TEMPLATES_PATH')+")\n\t\t\t\t*** ")
			if tmp_home_templates_path != "":
				HOME_TEMPLATES_PATH = tmp_home_templates_path

			print()
			if option_nr == "2":
				#wynik = os.system('rsync -avzh '+const_var('HOME_TEMPLATES_PATH')+' '+const_var('SERWER_TEMPLATES_PATH'))
				wynik = subprocess.check_output('rsync -avzh '+const_var('HOME_TEMPLATES_PATH')+' '+const_var('SERWER_TEMPLATES_PATH'), shell=True)
				str_wynik = str(wynik.decode())
				str_wynik_list = str_wynik.rsplit('\n') #replace('\n', '\n\t\t\t\t*** ')

				#print(str_wynik)
				print()
				for line in str_wynik_list:
					print('\t\t\t\t*** %s' %line)
				print('\n\t\t\t\t*** Synchronizacja:\n\t\t\t\t*** sudo rsync -avzh '+const_var('HOME_TEMPLATES_PATH')+' '+const_var('SERWER_TEMPLATES_PATH')+' \n\t\t\t\t*** wykonana, trwa reboot serwera .... \n\n')
			else:	
				file_path = const_var('SERWER_TEMPLATES_PATH')+"/templates/"+file_name+".html"
				html_str = "<html>\n\t<head>\n\t\t<style>\n\n\t\t</style>\n\t</head>\n\t<body>"+file_name+".html {{text}}\n\n\t</body>\n</html>"

				pomin_dodawanie = 0
				tmp_file_exist = ""
				if os.path.exists(file_path):
					tmp_file_exist = console.input("\t\t\t\t\t\t*** !!! UWAGA !!! ***\n\t\t\t\t*** Plik "+file_name+" już istnieje, czy nadpisać plik? \n\t\t\t\t\t (default: Y)\n\t\t\t\t*** ")
					pomin_dodawanie = 1
					#os.remove("demofile.txt")

				if tmp_file_exist in ("t","T","Y","y",""):
					tmp_extra_txt_file = console.input("\t\t\t\t*** Wpisz nazwe pliku textowego jezeli takowy ma byc dolaczony lub wciśnij ENTER\n\t\t\t\t*** ")
					if tmp_extra_txt_file != "":
						tmp_extra_txt_str = console.input("\t\t\t\t*** Wpisz zawartość pliku textowego \n\t\t\t\t*** ")	
						tmp_extra_txt_file = const_var('SERWER_TEMPLATES_PATH')+"/"+tmp_extra_txt_file+".txt"
						with open(tmp_extra_txt_file, 'w') as file:
							file.write(tmp_extra_txt_str)
						file.close()
						os.system('sudo chown '+const_var('USER')+'.'+const_var('GROUP')+' '+tmp_extra_txt_file)
						print('Plik utworzony .... ')

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
								if tmp_extra_txt_file != "":
									new_list.append('    jakis_text = open("'+tmp_extra_txt_file+'",encoding=\'utf8\').read()')
									new_list.append('    return render_template("'+file_name+'.html", text=jakis_text)')
								else:
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

		if option_nr == "1":
			os.system('sudo chown '+const_var('USER')+'.'+const_var('GROUP')+' '+file_path)
			print(os.system('ls -l '+const_var('SERWER_TEMPLATES_PATH')+'/templates'))
			#print(os.system('nano '+file_path))

if __name__ == '__main__':
	if os.getuid() == 0 or len(sys.argv) > 1:
		main(sys.argv)
	else:
		console.clear()
		print('\n\n\t\t\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**')
		print()
		print('\t\t\t\t**-**\t\t Uruchom nowy projekt / Synchronizuj dane / Wypchnij na GitHub ;) \t**-**')
		print()
		print('\t\t\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**')
		print()
		print('\t\t\t\t**-**\t 1. dodaje nową stronę do '+const_var('SERWER_TEMPLATES_PATH')+'/templates/ oraz uaktualnia plik app.py **-**')
		print('\t\t\t\t**-**\t 2. synchronizuje katalog roboczy z '+const_var('SERWER_TEMPLATES_PATH')+'/templates/ \t\t\t**-**')
		print('\t\t\t\t**-**\t 3. wypycha repozytorium na GitHub \t\t\t\t\t\t**-**')
		print()
		print('\t\t\t\t**-**\t\t Po wykonaniu wybranej operacji następuje restart usług.\t\t**-**')
		print()
		print('\t\t\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**')
		print('\n\n\t\t\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**')
		print('\n\t\t\t\t**-**\t\t Uruchom program ponownie z uprawnieniami root\'a (sudo) \t\t**-**\n')
		print('\t\t\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\n\n')
