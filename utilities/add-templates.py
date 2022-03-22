import sys
from asyncio.format_helpers import _get_function_source
from asyncore import ExitNow
import enum
from genericpath import isfile
import os
import subprocess
from flask import redirect
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


def app_py_file_to_list(flaga_path):
	app_py_code_list = []
	with open(flaga_path+'/app.py', 'r') as file:
		file_line_list = file.readlines()

	for line_nr, line in enumerate(file_line_list):
		if " import " in line or line[:6] == "import":
			app_py_code_list.append([line_nr,"import",line])
		elif "def " in line:
			app_py_code_list.append([line_nr,"def",line])
		elif "@app.route" in line:
			app_py_code_list.append([line_nr,"route",line])
		elif "render_template" in line:
			app_py_code_list.append([line_nr,"render_template",line])
		elif ".jinja" in line:
			app_py_code_list.append([line_nr,"html.jinja",line])
		elif ".html" in line:
			app_py_code_list.append([line_nr,"html",line])
		elif ".txt" in line:
			app_py_code_list.append([line_nr,"txt",line])
		elif line.replace('\t','') == "\n":
			app_py_code_list.append([line_nr,"brakeline",line])
		else:
			app_py_code_list.append([line_nr,"others",line])

	return app_py_code_list

def build_files_list():
	files_list = []
	files_list1 = []
	files_list2 = []
	pozostale_pliki_list = []
	root_folder_searched = True
	excluded_files_list = ["requirements.txt"]
	############################################################################
	# ogolne przegladniecie katalogow oraz plikow i zapisanie ich do tablicy
 	############################################################################
	for (root_folder, dirs_list, dir_files_list) in os.walk(const_var('SERWER_TEMPLATES_PATH')):
		
		for dir in dirs_list:
			
			if dir in (".git","flagaenv"):
				continue
			else:
				if root_folder == "/var/www/flaga" and root_folder_searched:
					#print('aaaa',root_folder,dir,dir_files_list)
					#print(dir_files_list)
					for file in dir_files_list:
						file_split_tup = os.path.splitext(file)
						extension = file_split_tup[-1].lstrip('.')
						if file not in excluded_files_list:
							home_dir = ""
							files_list1.append([root_folder,extension,file,home_dir])

					root_folder_searched = False

				for (root_folder2, dir2s_list, dir2_list) in os.walk(const_var('SERWER_TEMPLATES_PATH')+'/'+dir):
					
					#print('bbbb',root_folder2, dir2s_list, dir2_list)
					#files_list.append([root_folder,dir2s_list,dir2_list])
					for file in dir2_list:
						file_split_tup = os.path.splitext(file)
						extension = file_split_tup[-1].lstrip('.')
						if file not in excluded_files_list:
							home_dir = root_folder2.replace(root_folder,'').lstrip('/')
							files_list2.append([root_folder2,extension,file,home_dir])
  
	files_list = files_list1+files_list2
	#print('================= files list1 ===================')
	#print(files_list1)
	#print('================= files list2 ===================')
	#print(files_list2)
	return files_list
 
def build_extensions_files_list(flaga_path,files_list):
	import magic
	############################################################
	# pliki .txt, .py, .pyc, .html, .jinja, .css, .js
	############################################################
	txt_files_list = []
	py_files_list = []
	pyc_files_list = []
	html_files_list = []
	web_static_files_list = []
	image_files_list = []
	others_files_list = []
	#print(files_list)
	for file in files_list:
		try:
			#print(file)
			if "txt" in file[1]: txt_files_list.append(file)
			elif "pyc" in file[1]: pyc_files_list.append(file)
			elif "py" in file[1]: py_files_list.append(file)
			elif "html" in file[1] or "jinja" in file[1]: html_files_list.append(file)
			elif "css" in file[1] or "js" in file[1]: web_static_files_list.append(file)
			else:
				pass
				# try:
				# 	detected = magic.detect_from_filename(file[0]+"/"+file[-1])
				# 	if "image" in detected.mime_type:
				# 		image_files_list.append(file)
				# 	else:
				# 		others_files_list.append(file)
				# 	#print('mime: %s ==> %s' %(detected.mime_type,file[-1]))
				# except:
				# 	print('Nierozpoznany format pliku: %s' %file[-1])
		except:
			continue
	
	return [txt_files_list, py_files_list,	pyc_files_list, html_files_list, web_static_files_list, image_files_list, others_files_list]

def find_in_app_py(file_type,search_files_list,app_py_file_code_list):
	founded_list = []
	#print(len(app_py_file_code_list),search_files_list)
	#print('-----------')
	for line_nr,app_line in enumerate(app_py_file_code_list):
		#print(line_nr, file_type, '+++',app_line,'***')
		if file_type == app_line[1] or file_type in app_line[2]:
			#print(line_nr, file_type, '+++',app_line,'***')
			#print(line_nr, app_line[2])
			pos = 0
			for path, ext, file, home_dir in search_files_list:
				#print(path, ext, file)
				if file in app_line[2]:
					#print(pos,line_nr,app_line[2])
					if home_dir != '': home_dir+= "/"
					founded_list.append([home_dir+file,app_line[2]])
					search_files_list.pop(pos)
				pos+= 1
    
	return [search_files_list, founded_list]


def logsReport():

	return subprocess.console('lastlog |head -1000')

def lostLibInstallRequest(lib_name):
	
	if lib_name == "termcolor":
		extra_text = " do kolorowania textu w terminalu. "
	if lib_name == "file-magic":
		extra_text = " do rozpoznawania typów plików. \n\n\tWięcej informacji na temat biblioteki dostępne jest na stronie:\n\t\thttps://github.com/file/file/tree/master/python"

	input_text = "\n\n\tBrakuje biblioteki "+lib_name+extra_text+" \n\n\t Czy chcesz teraz zainstalować bibliotekę 'pip3 install termcolor' (Tak/Nie)? "
  
	if input(input_text) in ("Tak","tak"):
		resp = subprocess.getoutput('pip3 install '+lib_name)
		print(resp)
		print('\n\n\tUruchom program ponownie.')
	
		return False
	
	else:
		#print('\n\n\tOK, Wróć jak będziesz miał zainstalowaną bibliotekę '+lib_name+'. \n\n\n')
		return 'NoColors'
		
def cleanLogListFromBadInsert(gunicorn_error_proc_id_list):
	#print(gunicorn_error_proc_id_list)
	pid_list = []
	for date,pid,short,message in gunicorn_error_proc_id_list:
		pid_list.append(pid)

	new_gunicorn_error_proc_id_list = []
	#print(len(gunicorn_error_proc_id_list),len(new_gunicorn_error_proc_id_list))
	for l in gunicorn_error_proc_id_list:
		#print(nr,pid_list.count(l[1]),l)
		if pid_list.count(l[1]) == 1:
			continue
		else:
			new_gunicorn_error_proc_id_list.append(l)

	#print('-----------------------------------------')
	#print(len(gunicorn_error_proc_id_list),len(new_gunicorn_error_proc_id_list))
	#print(new_gunicorn_error_proc_id_list)
	return new_gunicorn_error_proc_id_list
 
def cleanLogLineAndPutInToList(line):
	line_list = line.split(']: [')
	#print('\n\naaaaa ===>',line_list)
	new_list = line_list[1].split(']')
	tmp_list = []
	for nr,l in enumerate(new_list):
		tmp_list.append(l.replace(' [','').lstrip())
  
	return tmp_list

def prepareSyslogOutput(syslog_list):
	gunicorn_error_proc_id_list = []
	error_line_list = []
	for nr, line in enumerate(syslog_list):
		tmp_line_list = line.split(':')
		pid = 0
		if "[INFO]" in line and "Worker exiting" in line:
			#print('\n\tZZZ=',cleanLogLineAndPutInToList(line),'\n')
			tmp_list = cleanLogLineAndPutInToList(line)
			gunicorn_error_proc_id_list.append([tmp_list[0],tmp_list[1],tmp_list[2],tmp_list[3]])
		elif "[ERROR]" in line and "Exception in worker process" in line:
			#print('\n\tYYY=',cleanLogLineAndPutInToList(line),'\n')
			tmp_list = cleanLogLineAndPutInToList(line)
			gunicorn_error_proc_id_list.append([tmp_list[0],tmp_list[1],tmp_list[2],tmp_list[3]])
	
	new_gunicorn_error_proc_id_list = cleanLogListFromBadInsert(gunicorn_error_proc_id_list)
	for data,pid,short,message in new_gunicorn_error_proc_id_list:
		for line in syslog_list:
			if pid in line:
				#print(pid,line)
				tmp_error_list = line.split(' ')
				if len(tmp_error_list) > 4:
					#print(pid,tmp_error_list)
					error_line_list.append([pid,tmp_error_list])
				#else:
				#	print(error_line_list)
	
	err_msg_list = []
	tmp_err_msg = ""
	tmp_err_list = []
	for id, error_list in enumerate(error_line_list):
			if error_list[1][-4] == "Worker" and error_list[1][-5] == "[INFO]":
				pid = error_list[0]
				data = str(error_list[1][5]+' '+error_list[1][6]).replace('[','')
				tmp_line_err_mg = ' '.join(error_line_list[id+3][1][5:])
				tmp_line_err_msg2 = ' '.join(error_line_list[id+1][1][5:])
				strstr = tmp_line_err_mg+' '+tmp_line_err_msg2
				
				if tmp_err_list.count(strstr) == 0:
					tmp_err_list.append(strstr)
					#print(id,pid,data,tmp_line_err_mg,tmp_line_err_msg2)
					err_msg_list.append([data,tmp_line_err_msg2,tmp_line_err_mg])

	return err_msg_list

def flaskCleaner():
	
	lib_ok = True
	try:
		from termcolor import colored, cprint
		text_colored = 1
	except:
		lib_ok = lostLibInstallRequest('termcolor')
		if lib_ok == "NoColors":
			text_colored = 0
  
  # For MIME types
	try:
		import magic
	except:
		lib_ok = lostLibInstallRequest('file-magic')

	if not lib_ok:
		raise SystemExit

	console.clear()
 	
	tmp_serwer_templates_path = console.input("\t\t*** Wpisz scieżke do katalogu flask (flaga) lub jeżeli podana jest właściwa, wciśnij ENTER\n\t\t\t (default: "+const_var('SERWER_TEMPLATES_PATH')+")\n\t\t*** ")
	if tmp_serwer_templates_path == "q":
		raise SystemExit

	if tmp_serwer_templates_path != "":
		flaga_path = tmp_serwer_templates_path
	else:
		flaga_path = const_var('SERWER_TEMPLATES_PATH')

	# zapisz w tablicy linie z pliku app.py
	app_py_file_code_list = app_py_file_to_list(flaga_path)
	#print(app_py_file_code_list)
	
	# lista znalezionych plikow
	files_list = build_files_list()
	#print(files_list)
 
	# lista znalezionych plikow w podziale na rozszerzenia
	#txt_files_list, py_files_list,	pyc_files_list, html_files_list, web_static_files_list, image_files_list, others_files_list = build_extensions_files_list(files_list)
	extension_files_list = build_extensions_files_list(flaga_path,files_list)
	#print(extension_files_list)

	
	output_list = []
	#for nr, item in enumerate(extension_files_list):
	file_types_list = [[0,"txt"],[3,"html"],[1,"py"]]
	licz = 0
	for nr, ext in file_types_list:
		search_files_list = extension_files_list[nr]
		#print('Szukamy plików .%s' %ext)
		#if ext == "html": print('HTML',len(app_py_file_code_list))
		output_list.append([ext, find_in_app_py(ext,search_files_list,app_py_file_code_list)])
		#print('used',ext,'file output_list:',output_list[licz][1][1])
		#print('non used',ext,'file output_list:',output_list[licz][1][0])
		licz+= 1


	
	# pliki .txt
	output_unused_list = output_list[0][1][0]
	safe_to_remove_files_list = []
	necessary_files_list = []
	necessary_files_ok_list = []
	for path, ext, file, home_dir in output_unused_list: safe_to_remove_files_list.append(file)
	output_used_list = output_list[0][1][1]
	tmp_str = ""
	for file, line in output_used_list: necessary_files_list.append(file)
	if len(output_used_list) == len(necessary_files_list): necessary_files_ok_list.append(['txt',True,'pass'])
	elif len(necessary_files_list) < len(output_used_list): necessary_files_ok_list.append(['txt',False,'Brakuje wywołanego pliku .txt.'])

	# pliki .html
	output_unused_list = output_list[1][1][0]
	for path, ext, file, home_dir in output_unused_list: safe_to_remove_files_list.append(file)
	output_used_list = output_list[1][1][1]
	for file, line in output_used_list: necessary_files_list.append(file)
	if len(output_used_list) == len(necessary_files_list): necessary_files_ok_list.append(['html',True,'pass'])
	elif len(necessary_files_list) < len(output_used_list): necessary_files_ok_list.append(['html',False,'Brakuje wywołanego pliku .html.'])


	list_nr = 1
	print('\n'+str(list_nr)+'. Znaleziono plik app.py który wymaga do poprawnego działania w systemie pliki:\n\t\t\t',', '.join(necessary_files_list))
	for ext, return_bool, message in necessary_files_ok_list: 
		if not return_bool: txt_color = "red"
		else: txt_color = "green"
		if text_colored == 1: text = colored(message, txt_color, attrs=['reverse', 'blink']).center(40)
		else: text = message.center(40)
		print('\n\t\t','*'*20,'\n\t\t',text,'\n\t\t','*-'*20)
  
  #################################################################
	list_nr+= 1
	safe_to_remove_files_list = list(set(safe_to_remove_files_list))
	possibility_file_to_remove = '\n\n'+str(list_nr)+'. Pliki możliwe do usunięcia - '+str(len(safe_to_remove_files_list))+' (nie będą miały wpływu na działanie flagi):\n\t'
	print(possibility_file_to_remove, '\n\t '.join(safe_to_remove_files_list))

	#################################################################
	# pliki .py
	#################################################################
	# list_nr+= 1
	# safe_to_remove_files_list.clear()
	# necessary_files_list.clear()
	# output_unused_list = output_list[2][1][0]
	# for path, ext, file, home_dir in output_unused_list: safe_to_remove_files_list.append(file)
	# output_used_list = output_list[2][1][1]
	# for file, line in output_used_list: necessary_files_list.append(file)
	# if len(output_used_list) == len(necessary_files_list): necessary_files_ok_list.append(['py',True,'pass'])
	# elif len(necessary_files_list) < len(output_used_list): necessary_files_ok_list.append(['py',False,'Brakuje wywołanego pliku .py.'])

	# python_files_in_flaga_folder = output_used_list
	# print('\n\n'+str(list_nr)+'. py files: ',python_files_in_flaga_folder)

	#################################################################
	# lastlog on server
	#################################################################
	list_nr+= 1
	syslog_list = subprocess.getoutput('lastlog').split('\n')
	for nr,line in enumerate(syslog_list):
		line_list = line.split(' ')
		new_list = []
		for pos in line_list:
			if pos != '':
				new_list.append(pos)
      
		syslog_list[nr] = new_list
    #print(nr,line_list[0],line_list[-1])
	print('\n'+str(list_nr)+'. Ostatnie logowanie użytkownika:\n')
	zz = 0
	while zz < len(syslog_list):
		if len(syslog_list[zz]) > 4:
			#print(syslog_list[zz])
			log_str = '\t'+syslog_list[zz][0]+' z dnia: '+syslog_list[zz][-4]+' '+syslog_list[zz][-5]+' z godz.: '+syslog_list[zz][-3]+' z IP: '+syslog_list[zz][2]
			print(log_str)
		zz+= 1

	#################################################################
	# find error in syslog -> cat /var/log/syslog
	#################################################################
	list_nr+= 1
	syslog_list = subprocess.getoutput('cat /var/log/syslog').split('\n')
	syslog_list.reverse()
	err_msg_list = prepareSyslogOutput(syslog_list)
 
	#print(err_msg_list)
	if len(err_msg_list) > 0:
		print('\n'+str(list_nr)+'. Ostatnie błędy w pliku syslog:\n')
		for err_date, info, place in err_msg_list:
			print(err_date,'Komunikat błędu:', info) #,'place===>',place)
			if "IndentationError" in info:
				print('Sprawdź wcięcia w pliku app.py w linii:')
				print(place)
				#tmp_place = place.split(':')[3:]
				#print(' '.join(tmp_place))
			elif "AssertionError" in info:
				tmp_info_list = info.split(':')
				if "function" in tmp_info_list[1] and "overwriting" in tmp_info_list[1] and "an existing" in tmp_info_list[1]:
					print('Sprawdź nazwę funkcji, prawdopodobnie w pliku app.py masz 2 funkcje nazywające się:',tmp_info_list[-1])
					print('\n',place)
			else:
				print(place)
			print('\n')
		#print(err_msg_list[0])
	else:
		print('\n'+str(list_nr)+'. Nie ma błędów w pliku syslog.')

def main(argv):
	import subprocess
	console.clear()
	
	if len(argv) > 1 and argv[1] == "3":
		commit_text = console.input("\t\t*** Wpisz opis dla 'git commit': \n\t\t*** ")
		init_user = subprocess.check_output('whoami', shell=True)
		init_dir = subprocess.check_output('pwd', shell=True)
		init_user = init_user.decode().replace('\n','') #, os.system('pwd'))
		init_dir = init_dir.decode().replace('\n','')
		uid = const_var('UID')
		#print('==>'+init_user+'<==='+init_dir+'===>'+str(uid))
		#print()
		if init_user == "root":
			print("Real user ID of the current process:", os.getuid())
			change_user_resp = os.setuid(uid)
			print("Real user ID after changes:", os.getuid())
			#change_user_resp = subprocess.check_output(change_u
			print("Coś tu jednak nie działa jak powinno ;/")
			#new_user = subprocess.check_output('whoami', shell=True)
			os.system('cd '+init_dir+' && pwd')

		print('Wypchanie kodu na GitHub:\n git add -A .; git commit -m "'+commit_text+'"; git push\n\n')
		#git_out = subprocess.check_output('git add -A .; git commit -m "'+commit_text+'"; git push', shell=True)
		#print(git_out.decode())
	elif len(argv) > 1 and argv[1] == "4":
		flaskCleaner()
		raise SystemExit
	else:
		print('\n\n')
		opt_str = "\t\t*** Wybierz jedną z poniższych opcji: \n\t\t*** "
		opt_str+= "1. nazwe pliku html \n\t\t*** "
		opt_str+= "2. wykonaj synchronizacje (rsync) \n\t\t*** "
		opt_str+= "3. wypchnij kod na GitHub\n\t\t*** "
		opt_str+= "4. sprawdź serwer FLASK\n\n\t\t*** "
		opt_str+= "q - wyjście\n\n\t\t\t --|> "
		option_nr = console.input(opt_str)
		file_name = ""
		if option_nr == "q":
			raise SystemExit
		elif option_nr == "4":
			flaskCleaner()
			raise SystemExit
		elif option_nr == "1":
			file_name = console.input("\t\t*** Podaj nazwę pliku html (bez rozszerzenia): \n\t\t*** ")
		elif option_nr == "3":
			commit_text = console.input("\t\t*** Wpisz opis dla 'git commit': \n\t\t*** ")
			print(os.system('whoami'))
			print(os.system('git add -A .; git commit -m "'+commit_text+'"; git push'))
			print('Wypchanie kodu na GitHub:\n git add -A .; git commit -m "'+commit_text+'"; git push')
		else:
			raise SystemExit
 
		if option_nr != "3":
			tmp_serwer_templates_path = console.input("\t\t*** Wpisz scieżke do katalogu templates na serwerze lub wciśnij ENTER\n\t\t\t (default: "+const_var('SERWER_TEMPLATES_PATH')+")\n\t\t*** ")
			if tmp_serwer_templates_path != "":
				SERWER_TEMPLATES_PATH = tmp_serwer_templates_path

			tmp_home_templates_path = console.input("\t\t*** Wpisz scieżke do katalogu templates z repozytorium lub wciśnij ENTER\n\t\t\t (default: "+const_var('HOME_TEMPLATES_PATH')+")\n\t\t*** ")
			if tmp_home_templates_path != "":
				HOME_TEMPLATES_PATH = tmp_home_templates_path

			print()
			if option_nr == "2":
				#wynik = os.system('rsync -avzh '+const_var('HOME_TEMPLATES_PATH')+' '+const_var('SERWER_TEMPLATES_PATH'))
				wynik = subprocess.check_output('rsync -avzh '+const_var('HOME_TEMPLATES_PATH')+' '+const_var('SERWER_TEMPLATES_PATH'), shell=True)
				str_wynik = str(wynik.decode())
				str_wynik_list = str_wynik.rsplit('\n') #replace('\n', '\n\t\t*** ')

				#print(str_wynik)
				print()
				for line in str_wynik_list:
					print('\t\t*** %s' %line)
				print('\n\t\t*** Synchronizacja:\n\t\t*** sudo rsync -avzh '+const_var('HOME_TEMPLATES_PATH')+' '+const_var('SERWER_TEMPLATES_PATH')+' \n\t\t*** wykonana, trwa reboot serwera .... \n\n')
			else:	
				file_path = const_var('SERWER_TEMPLATES_PATH')+"/templates/"+file_name+".html"
				html_str = "<html>\n\t<head>\n\t\t<style>\n\n\t\t</style>\n\t</head>\n\t<body>"+file_name+".html {{text}}\n\n\t</body>\n</html>"

				pomin_dodawanie = 0
				tmp_file_exist = ""
				if os.path.exists(file_path):
					tmp_file_exist = console.input("\t\t\t\t*** !!! UWAGA !!! ***\n\t\t*** Plik "+file_name+" już istnieje, czy nadpisać plik? \n\t\t\t (default: Y)\n\t\t*** ")
					pomin_dodawanie = 1
					#os.remove("demofile.txt")

				if tmp_file_exist in ("t","T","Y","y",""):
					tmp_extra_txt_file = console.input("\t\t*** Wpisz nazwe pliku textowego jezeli takowy ma byc dolaczony lub wciśnij ENTER\n\t\t*** ")
					if tmp_extra_txt_file != "":
						tmp_extra_txt_str = console.input("\t\t*** Wpisz zawartość pliku textowego \n\t\t*** ")	
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

	console.clear()
	if len(sys.argv) > 1 and sys.argv[1] == "4":
		flaskCleaner()
		raise SystemExit

	elif os.getuid() == 0 or len(sys.argv) > 1:
		main(sys.argv)
  
	else:
		
		print('*'*40)
		txt = "text wycentrowany do wartosci 40"
		x = txt.center(40)
		print(x)
		print('\n\n\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**')
		print('\t\t**-**','\t     '*10,'  **-**')
		print('\t\t**-**','\t     '*10,'  **-**')
		print('\t\t**-**\t Takie tam różne narzędzia ...')
		print('\t\t**-**\t')
		print('\t\t**-**\t 1. Uruchom nowy projekt (wymaga sudo)')
		print('\t\t**-**\t\t - dodaje nową stronę do '+const_var('SERWER_TEMPLATES_PATH')+'/templates/')
		print('\t\t**-**\t\t - uaktualnia plik app.py')
		print('\t\t**-**\t\t - restartuje usługi')
		print('\t\t**-**\t 2. Synchronizacja rsync (wymaga sudo)')
		print('\t\t**-**\t\t - synchronizuj katalog roboczy z '+const_var('SERWER_TEMPLATES_PATH')+'/templates/')
		print('\t\t**-**\t 3. Git push (git add -A .; git commit -m "commit_text"; git push)')
		print('\t\t**-**\t\t - dodaj pliki do repo, zakomituj i wypchnij na GitHub')
		print('\t\t**-**\t\t - działa bez sudo - uruchom z parametrem 3')
		print('\t\t**-**\t 4. Wystąpił nieoczekiwany błąd serwera?')
		print('\t\t**-**\t\t - sprawdza app.py pod kątem powiązań z plikami')
		print('\t\t**-**\t\t - pokazuje możliwe błędy z pliku syslog')
		print('\t\t**-**\t\t - uruchom z parametrem 4')
		print('\t\t**-**','\t     '*10,'  **-**')
		print('\t\t**-**','\t     '*10,'  **-**')
		print('\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**')
#		print('\n\n\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**')
#		print('\n\t\t**-**\t\t Uruchom program ponownie z uprawnieniami root\'a (sudo) \t\t**-**\n')
#		print('\t\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\t**-**\n\n')
