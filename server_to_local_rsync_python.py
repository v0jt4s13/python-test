import json
import subprocess
import os
import sys
import configparser
from os.path import exists

path_to_config_file = "server_to_local_rsync_python.ini"

try:
	config = configparser.ConfigParser()
	config.read(path_to_config_file)
	conf_user = config['rsync_conf']['conf_user']
	conf_user_id = config['rsync_conf']['conf_user_id']
	conf_group = config['rsync_conf']['conf_group']
	conf_flaga_path = config['rsync_conf']['conf_flaga_path']
	conf_domain = config['rsync_conf']['conf_domain']
	
	conf_local_python_dir = config['rsync_conf']['conf_local_python_dir']
	conf_templ_path = config['rsync_conf']['conf_templ_path']
	conf_ssh_key_file_name = config['rsync_conf']['conf_ssh_key_file_name']
	conf_local_user_name = config['rsync_conf']['conf_local_user_name']
	conf_local_rsync_path = config['rsync_conf']['conf_local_rsync_path']
except:
    print('...')

def findDuplicateInList(str,lista):
	if type(lista) == list:
		try:
			rowElCount = len(lista)
			zz = 0
			while zz < rowElCount:
				xx = 0
				while xx < len(lista[0]):
					if lista[zz][xx] == str:
						return 1
					xx+= 1
				zz+= 1		
			return 0
		except ValueError as e:
			print('%s ==> Err %s' %(lista,e))

def rsyncDataBetweenLocalAndRemote():

	config = configparser.ConfigParser()
	config.read(path_to_config_file)
	conf_user = config['rsync_conf']['conf_user']
	conf_domain = config['rsync_conf']['conf_domain']
	conf_ssh_key_file_name = config['rsync_conf']['conf_ssh_key_file_name']
	conf_local_user_name = config['rsync_conf']['conf_local_user_name']
	conf_local_rsync_path = config['rsync_conf']['conf_local_rsync_path']
 
	rsync_str = "rsync -Pavp --rsh=\"ssh -i /home/"+conf_local_user_name+"/.ssh/"+conf_ssh_key_file_name+"\" "
	rsync_str+= conf_user+"@"+conf_domain+":/home/"+conf_user+"/ ./"+conf_local_rsync_path
	rsync_executed_line_list = []
	rsync_executed_line_list.append(rsync_str)
	#rsync_executed_line_list.append('rsync -Pavp --rsh="ssh -i /home/'+conf_local_user_name+'/.ssh/'+key_file_name+'" '+conf_user+'@'+conf_domain+':/var/www/ ./'+conf_local_rsync_path+'/')

	print('\n\n\t\t====================================================\n\t\t\t %s'  %rsync_str)
	print('\t\t\tZaczynamy synchronizację .... \n\t\t\t\n')
	rsync_wynik_list = []
	for rsync_executed_line in rsync_executed_line_list:
		try:
			tmp_str = subprocess.check_output(rsync_executed_line, shell=True)
			rsync_wynik_list.append(tmp_str.decode().split('\n'))
		except ValueError as e:
			print('\t\t\tNie ma nic do synchronizacji: '+conf_user+'@'+conf_domain+':/home/'+conf_user+'/ ./'+conf_local_rsync_path+'/')

	print('\n\n\t\t====================================================')
	xx = 0
	while xx < len(rsync_wynik_list):
		tmp_list = list(filter(None, rsync_wynik_list[xx]))
		tmp_str = '\n\t\t'.join(tmp_list)
		#print(len(tmp_list),tmp_list)
		print('\t\t%s' %tmp_str)
		xx+= 1
	print('\t\t====================================================')
    
def findStringInPythonFiles():
	search_word = "import"
	"""print('findStringInPythonFiles')
	print(conf_local_rsync_path)
	print(conf_local_python_dir)"""

	tmp_pwd = subprocess.check_output('pwd').decode().replace('\n','')
	#main_dir_list = subprocess.check_output('ls -d */', shell=True).decode().split('\n')
	search_main_dir_path = 'find . -maxdepth 3 -type d -not -path "*/.*" -exec ls -d "{}" \;'
	main_dir_list = subprocess.check_output(search_main_dir_path, shell=True).decode().split('\n')
 
	#print(main_dir_list) # ['.', '', './python-test', './templates', './rsync-home-directory', './rsync-home-directory/python-test', './rsync-home-directory/python-test/templates', './rsync-home-directory/python-test/rsync-home-directory', './rsync-home-directory/python-test/github-clone', './rsync-home-directory/ipython-in-depth', './rsync-home-directory/ipython-in-depth/tools', './rsync-home-directory/ipython-in-depth/examples', './rsync-home-directory/ipython-in-depth/binder', './rsync-home-directory/ipython-in-depth/exercises']
	search_dir_list = []
	tmp_founded_str_list = []
	import_modules_list = []
	for dir in main_dir_list:
		if dir in ('.',''):
			continue
		#print('dir: '+dir)
		tmp_find_py_file_line = "find "+dir+" -name \"*.py\" -type f |wc -l"
		tmp_find_py_file_count = int(subprocess.check_output(tmp_find_py_file_line, shell=True).decode().lstrip().replace('\n',''))
		#print(type(tmp_find_py_file_count),tmp_find_py_file_count) #+' ===> 0')
		if tmp_find_py_file_count == 0:
			continue
		try:
			search_line = 'less '+dir+'/*.py |grep '+search_word
			#print('AAAAAAAAAAAAA==>%s' %search_line)
			#print(str(tmp_find_py_file_count)) #+' ===> '+search_line)
			tmp_founded_str_list = subprocess.check_output(search_line, shell=True).decode().lstrip().split('\n')
			#print('BBBBBBBBBBBBBB==>%s' %search_line)
			for line in tmp_founded_str_list:
				import_modules_list.append(line)
		except ValueError as e:
			print('1. Error in: %s' %search_line)
		except:
			print('2. Error in: %s' %search_line)
			continue
		
		#print(len(tmp_founded_str_list),len(import_modules_list))
  
	xx = 0
	tmp_lib_name_list = []
	
	tmp_find_py_file_line = 'find . -maxdepth 4 -type f -name "*.py" -not -path "*/.*" -exec grep import {} \;'
	#tmp_find_py_file_line = "find "+dir+" -name \"*.py\" -type f |wc -l"
	#tmp_find_py_file_count = int(subprocess.check_output(tmp_find_py_file_line, shell=True).decode().lstrip().replace('\n',''))
	#print(len(subprocess.check_output(tmp_find_py_file_line, shell=True).decode().lstrip().split('\n')))
	tmp_find_py_file_list = subprocess.check_output(tmp_find_py_file_line, shell=True).decode().lstrip().split('\n')

	#print(len(import_modules_list),len(tmp_find_py_file_list))
	lib_name_extracted_metod1_list = []
	lib_name_extracted_metod1_list.append(pullOutLibNameFromMessList(import_modules_list))
	lib_name_extracted_metod1_list.append(pullOutLibNameFromMessList(tmp_find_py_file_list))
	#print(len(lib_name_extracted_metod1_list[0]),len(lib_name_extracted_metod1_list[1]))

	return lib_name_extracted_metod1_list

def pullOutLibNameFromMessList(import_modules_list):

	waste_list = []
	lib_name_list = []
	xx = 0
	#print(import_modules_list) #[0].strip(),import_modules_list[1].strip(),import_modules_list[2].strip())
	for lib_name in import_modules_list:
		lib_name = lib_name.strip().replace('\t','')
		if lib_name != "":
			#print(lib_name)
			if lib_name[:1] != "#" and lib_name[:7] == "import ":
				tmp_lib_name = lib_name[7:]
				if len(tmp_lib_name.split('.')) == 2:
					tmp_lib_name = ['dot',tmp_lib_name.split('.')[1],lib_name]
				elif len(tmp_lib_name.split(' ')) > 1:
					tmp_lib_name = ['space',tmp_lib_name.split(' '),lib_name]

				if type(tmp_lib_name) == str:
					if len(lib_name_list) > 0:
						if findDuplicateInList(tmp_lib_name,lib_name_list) == 0:
							#print('>>> 1 <<< '+tmp_lib_name)
							#print('findDuplicateInList(%s,%s)' %(tmp_lib_name,lib_name_list))
							lib_name_list.append(['1.',type(tmp_lib_name),tmp_lib_name,lib_name])
					else:
						if findDuplicateInList(tmp_lib_name,lib_name_list) == 0:
							#print('>>> 2 <<< '+tmp_lib_name)
							lib_name_list.append(['2.',type(tmp_lib_name),tmp_lib_name,lib_name])

				elif type(tmp_lib_name) == list:
					if type(tmp_lib_name[1]) == list:
						licz = 0
						for tmp_tmp_lib_name in tmp_lib_name[1]:
							if tmp_lib_name[1][licz] == "as":
								break
							new_text = ""
							for character in tmp_tmp_lib_name:
								if character.isalnum():
									new_text += character
							tmp_tmp_lib_name = new_text
		
							if findDuplicateInList(tmp_tmp_lib_name,lib_name_list) == 0:
								#print('>>> 3 <<< '+tmp_tmp_lib_name)
								#print(tmp_lib_name[1])
								lib_name_list.append(['3.',type(tmp_tmp_lib_name),tmp_tmp_lib_name,lib_name])
							#else:
							#	print('>>> 4 <<< '+tmp_tmp_lib_name)
							licz+= 1

					else:
						tmp_lib_name_list = tmp_lib_name[1].split('.')
						tmp_lib_name_list_len = len(tmp_lib_name_list)
						#print('4-5. ',tmp_lib_name_list_len,tmp_lib_name)
						if tmp_lib_name_list_len == 2:
							if findDuplicateInList(tmp_lib_name_list[1],lib_name_list) == 0:
								#print('>>> 4 <<< '+tmp_lib_name_list[1])
								lib_name_list.append(['4.',type(tmp_lib_name),tmp_lib_name_list[1],lib_name])
						else:
							if findDuplicateInList(tmp_lib_name[1],lib_name_list) == 0:
								#print('>>> 5 <<< '+tmp_lib_name_list[0])
								lib_name_list.append(['5.',type(tmp_lib_name[1]),tmp_lib_name[1],lib_name])
						#if len(lib_name_list) > 0:
				else:
					waste_list.append(['RESZTA=>'+lib_name[:6],type(tmp_lib_name),lib_name])

			elif lib_name[:1] != "#" and lib_name[:4] == "from":
				tmp_lib_name_list = lib_name.split(' ')
				tmp_lib_name_list_len = len(tmp_lib_name_list)
				tmp_lib_name_len = len(tmp_lib_name_list[1].split('.'))
				if tmp_lib_name_len == 2:
					tmp_lib_name = tmp_lib_name_list[1].split('.')[0]
					if findDuplicateInList(tmp_lib_name,lib_name_list) == 0:
						#print('==================> kropka '+tmp_lib_name)
						lib_name_list.append(['6.',type(tmp_lib_name),tmp_lib_name,lib_name])
				else:
					tmp_lib_name = tmp_lib_name_list[1]
					if findDuplicateInList(tmp_lib_name,lib_name_list) == 0:
						#print('==================> bez kropki =>'+tmp_lib_name)
						lib_name_list.append(['7.',type(tmp_lib_name),tmp_lib_name,lib_name])
			else:
				waste_list.append(['5.',type(lib_name),lib_name])
		xx+= 1
	return lib_name_list
 
def findLostModules(lib_name_list):
    
	biblioteki_do_importu_list = []
	biblioteki_zainstalowane_list = []
	#print(lib_name_list)

	import importlib
 
	for val in lib_name_list:
		try:
			toolbox_specs = importlib.util.find_spec(val[2])
			toolbox = importlib.util.module_from_spec(toolbox_specs)
			toolbox_specs.loader.exec_module(toolbox)

			module_found = True
			biblioteki_zainstalowane_list.append(val[2])
		except ImportError:
			module_found = False
			biblioteki_do_importu_list.append(val[2])
			print('\t\t\t* \t Biblioteka %s nieznaleziona.' %val[2])
		except:
			biblioteki_do_importu_list.append(val[2])
			print('\t\t\t* \t Biblioteka %s nieznaleziona.' %val[2])
		
	print('\n\t\t\t* \tZainstalowane biblioteki(moduły): \n\t\t\t*\t\t%s' %str(', '.join(biblioteki_zainstalowane_list)))
	if len(biblioteki_do_importu_list) > 0:
		print('\n\t\t\t* \tBrakujące biblioteki(moduły): \n\t\t\t*\t\t%s' %str(', '.join(biblioteki_do_importu_list)))
	
	return biblioteki_do_importu_list

def installLostModules(biblioteki_do_importu_list):
	lib_install = input("\n\n\t\t\t* \t Czy zainstalować brakujące biblioteki? ")
	if lib_install in ("t","T","y","Y"):
		for val in biblioteki_do_importu_list:
			try:
				install_str = 'pip3 install '+val
				installed_lib_resp = subprocess.check_output(install_str, shell=True)
				print('\t\t'+installed_lib_resp)
			except ValueError as e:
				print(e)
				print('\t\t\t ******* Nie udało się zainstalować biblioteki %s. *******' %val)
				print('\t\t'+install_str)
			except:
				print('\t\t\t ******* Nie udało się zainstalować biblioteki %s. *******' %val)
				print('\t\t'+install_str)

def makeNewConfigFile():
	############## kilka linijek konfiguracyjnych ###########
	print("\n\t\t\t* Najpierw podaj potrzebne informacje dotyczące serwera. ")
	conf_user = input("\n\t\t\t* Wpisz nazwę użytkownika na serwerze (ubuntu, jas, malgosia): ")
	if conf_user == "": conf_user = "ubuntu"
	print('\t\t\t* Podaj unikatowy numer użytkownika (UID) na serwerze \n\t\t\t* \tMożesz wpisać: less /etc/passwd |grep ubuntu')
	conf_user_id = input('\t\t\t* \tW odpowiedzi powinieneś otrzymać (cyfry to UID): ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/usr/bin/zsh: ')
	if conf_user_id == "": conf_user_id = "1000"
	conf_group = input("\t\t\t* Wpisz nazwę grupy lub wciśnij ENTER (default: www-data): ")
	if conf_group == "": conf_group = "www-data"
	conf_flaga_path = input("\t\t\t* Wpisz ścieżkę do plików flagi na serwerze lub wciśnij ENTER (default: /var/www/flaga): ")
	if conf_flaga_path == "": conf_flaga_path = "/var/www/flaga"
	conf_local_user_str = str(subprocess.check_output('whoami', shell=True).decode().replace('\n',''))
	conf_domain = input("\t\t\t* Wpisz nazwę swojej domeny lub IP do połączeń z serwerem: ")
	conf_local_python_dir_tmp = subprocess.check_output('pwd').decode().replace('\n','')
 
	print("\n\n\t\t\t* Teraz kolej na informacje dotyczące twojej lokalnej maszyny.\n")
	conf_local_python_dir = input("\t\t\t* Wpisz nazwę lokalnego katalogu gdzie trzymasz pliki swoich projektów w pythonie: (default: "+conf_local_python_dir_tmp+"/): ")
	if conf_local_python_dir == "": conf_local_python_dir = conf_local_python_dir_tmp
	conf_templ_path = input("\t\t\t* Wpisz ścieżkę do lokalnych plików html (default: "+conf_local_python_dir+"/templates): ")
	if conf_templ_path == "": conf_templ_path = conf_local_python_dir+"/templates"
	conf_ssh_key_file_name = input("\t\t\t* Wpisz nazwę klucza ssh lub pełną ścieżkę do lokalnego pliku (default: /home/"+conf_local_user_str+"/.ssh/moj_klucz.pem): ")
	if conf_ssh_key_file_name == "": conf_ssh_key_file_name = "aws-python-xd.pem"
	conf_local_user_name = input("\t\t\t* Wpisz nazwę lokalnego użytkownika jeżeli inny: (default: "+conf_local_user_str+"): ")
	if conf_local_user_name == "": conf_local_user_name = conf_local_user_str
	conf_local_rsync_path = input("\t\t\t* Wpisz nazwę lub pełną ścieżkę katalogu lokalnego do synchronizacji plików lub wciśnij ENTER: (default: "+conf_local_python_dir+"/rsync-home-directory): ")
	if conf_local_rsync_path == "": conf_local_rsync_path = "rsync-home-directory"

	with open(path_to_config_file, "w") as file:
		file.write("[rsync_conf]")
		file.write("\nconf_user = "+conf_user)
		file.write("\nconf_user_id = "+conf_user_id)
		file.write("\nconf_group = "+conf_group)
		file.write("\nconf_flaga_path = "+conf_flaga_path)
		file.write("\nconf_domain = "+conf_domain)
		file.write("\nconf_local_python_dir = "+conf_local_python_dir)
		file.write("\nconf_templ_path = "+conf_templ_path)
		file.write("\nconf_ssh_key_file_name = "+conf_ssh_key_file_name)
		file.write("\nconf_local_user_name = "+conf_local_user_name)
		file.write("\nconf_local_rsync_path = "+conf_local_rsync_path)

	print('\n\n\t\t\t* Plik konfiguracyjny stworzony. Potwierdź poprawność poniższych danych.')
	print('\n\t\t\t* Ustawienia dla serwera: \n\t\t\t* \t użytkownik(%i): %s / groupa: %s' %(int(conf_user_id),conf_user,conf_group))
	print('\t\t\t* \t domena: %s / katalog flagi: %s' %(conf_domain,conf_flaga_path))

	print('\n\t\t\t* Ustawienia lokalne: \n\t\t\t* \t user: %s / klucz: %s' %(conf_local_user_str,conf_ssh_key_file_name))
	print('\t\t\t* \t katalog projektu: %s \n\t\t\t* \t katalog do synchronizacji: %s' %(conf_local_python_dir,conf_local_rsync_path))


def main():
    
	print('\n\n')
	print('\t\t\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * *')
	print('\t\t\t* Program do synchronizacji plików local-server ąść (tworzy kopie plikow na serwerze, lokalnie na komputerze) ')
	print('\t\t\t*')
	print('\t\t\t* Do działania wymagana wstępna konfiguracja, która zapisana zostanie w pliku: server_to_local_rsync_python.ini ')
	print('\t\t\t*')
	
	file_exists = exists(path_to_config_file)
	#print(file_exists)
	update_conf_file = ""
	make_new_conf_file = ""
	if file_exists:
		update_conf_file = input('\t\t\t* Plik konfiguracyjny istnieje, czy chcesz nadpisać ten plik nowymi danymi (T/N)? ')
	else:
		make_new_conf_file = input('\t\t\t* Brak pliku konfiguracyjnego, a bez niego nigdzie nie zajedziemy. \n\t\t\t* \t\t Czy chcesz teraz utworzyć ten plik (T/N)? ')

	if make_new_conf_file in ("t","T","y","Y") or update_conf_file in ("t","T","y","Y"):
		makeNewConfigFile()

	try:
		conf_test = conf_local_user_name
	except:
		config = configparser.ConfigParser()
		config.read(path_to_config_file)
		conf_user = config['rsync_conf']['conf_user']
		conf_user_id = config['rsync_conf']['conf_user_id']
		conf_group = config['rsync_conf']['conf_group']
		conf_flaga_path = config['rsync_conf']['conf_flaga_path']
		conf_domain = config['rsync_conf']['conf_domain']
		
		conf_local_python_dir = config['rsync_conf']['conf_local_python_dir']
		conf_templ_path = config['rsync_conf']['conf_templ_path']
		conf_ssh_key_file_name = config['rsync_conf']['conf_ssh_key_file_name']
		conf_local_user_name = config['rsync_conf']['conf_local_user_name']
		conf_local_rsync_path = config['rsync_conf']['conf_local_rsync_path']

	sync_start = input("\n\n\t\t\t* Czas na synchronizację katalogów, może to trochę potrwać. Go (T/N)? ")
	if sync_start in ("t","T","y","Y"):
		rsyncDataBetweenLocalAndRemote()

	xx = 0
	for lib_name_list in findStringInPythonFiles():
		xx+= 1
		biblioteki_do_importu_list = findLostModules(lib_name_list)
		lib_count = len(biblioteki_do_importu_list)
		print('Metoda %i - %i bibliotek' %(xx,lib_count))
		if lib_count > 0:
			installLostModules(biblioteki_do_importu_list)

	print('\n\n\t\t\t* \t I to na tyle, Twoje projekty mają teraz lokalną kopię zapasową.')
	print('\t\t\t* * * * * * * * * * * * * * * * * * * * * * * * * * * * *')

def maine():
	from pathlib import Path

	# https://www.pythontutorial.net/python-basics/python-filter-list/
	"""
 	carts = [['SmartPhone', 400],['Tablet', 450],['Laptop', 700]]
	TAX = 0.1
	carts = map(lambda item: [item[0], item[1], item[1] * TAX], carts)
	print(list(carts))
	high_value = filter(lambda v: v[1] > 500, carts)
	print(list(high_value))
	"""


	def searchFoldersAndFiles(du_data_list):
		files_py_list = []
		files_others_list = []
		dir_list = []
		folders_size_list = []
		for val in du_data_list:
			line_list = val.split('\t')
			if len(line_list) == 2: 
				folders_size_list.append([int(line_list[0]),line_list[1]])
				path_to_file = line_list[1]
				path = Path(path_to_file)

				if path.is_file() and path_to_file.split('.')[-1] == "py":
					#print('The file %s exists' %path_to_file)
					files_py_list.append(path_to_file)
				elif path.is_file():
					files_others_list.append(path_to_file)
				else:
					#print(f'The file {path_to_file} does not exist')
					dir_list.append(path_to_file)
		return files_py_list,files_others_list,dir_list


	get_cwd = os.getcwd()
	print('\n\n\t\t\t\tStart - aktualny folder: %s \n\n' %get_cwd)
	du_data_list = subprocess.check_output('du -s *', shell=True).decode().lstrip().split('\n')
	files_py_list = []
	files_others_list = []
	dir_list = []
	new_dir_list = []

	xx = 0
	while True:
		if len(dir_list) == 0:
			list_py,list_other,list_dir = searchFoldersAndFiles(du_data_list)
			print('\t\t\t\t1. folders: ',list_dir)
			for val in list_py: files_py_list.append(val)
			for val in list_other: files_others_list.append(val)
			for val in list_dir: new_dir_list.append(val)
		else:
			print('\n\n\n\t\t\t\tdir_list ==> %s' %dir_list)
			for dir in dir_list:
				tmp_get_cwd = get_cwd+"/"+dir
				print('\t\t\t\tKrok %i - bieżący folder: %s' %(xx,tmp_get_cwd))
				du_data_str = 'du -s '+tmp_get_cwd+'/*'
				du_data_list = subprocess.check_output(du_data_str, shell=True).decode().lstrip().split('\n')

				list_py,list_other,list_dir = searchFoldersAndFiles(du_data_list)
				print('\t\t\t\t2. folders: ','\n\t\t\t\t\t     '.join(list_dir).replace('/home/voj/projects/',''),'\n\t\t\t\t\t\t****************\n\n\n')
				for val in list_py: files_py_list.append(val)
				for val in list_other: files_others_list.append(val)
				for val in list_dir: new_dir_list.append(val)
				xx+= 1
		
		if len(list_dir) > 0:
			for val in list_dir:
				dir_list.append(val)
		else:
			False
		#print('\n\t\t\t\t*************\n\t\t\t\t<* * * * * * * * * * * all list.clear() * * * * * * * * * * * *>\n\t\t\t\tdir_list => ',dir_list,'\n\t\t\t\t*************')
		list_py.clear()
		list_other.clear()
		list_dir.clear()

		xx+= 1
		if xx > 5: 
			False
			break

	print('\n\n')
	#print(folders_size_list)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		maine()
	else:
		main()
