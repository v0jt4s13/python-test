from logging import LogRecord
import subprocess

def	header_print(text):
	print()
	print('='*60)
	print(text.center(60))
	print('='*60)
	print()


def prepare_syslog_output(syslog_list):
  ################################################
  #+#   Prepare syslog output to better view   #+#
  ################################################
  # Mar 22 00:15:55 ip-172-31-29-165 gunicorn[792103]: [2022-03-22 00:15:55 +0000] [792103] [INFO] Worker exiting (pid: 792103)
	# ['2022-03-22 00:15:55 +0000', '792103', 'INFO', 'Worker exiting (pid: 792103)']
  ################################################
	gunicorn_error_proc_id_list = []
	error_line_list = []
	pids_done_list = []
	for nr, line in enumerate(syslog_list):

		tmp_line_list = line.split(':')
		pid = 0
		#################################################
		# Search for specific string in syslog line
		#################################################
		if "[INFO]" in line and "Worker exiting" in line:

			tmp_list = clean_log_line_and_put_in_to_list2(syslog_list,line,pids_done_list)
			pids_done_list.append(str(tmp_list[0]))
			gunicorn_error_proc_id_list.append([tmp_list[1],tmp_list[2],tmp_list[3],tmp_list[4]])

		elif "[ERROR]" in line and "Exception in worker process" in line:
			
			tmp_list = clean_log_line_and_put_in_to_list2(syslog_list,line,pids_done_list)
			pids_done_list.append(str(tmp_list[0]))
			gunicorn_error_proc_id_list.append([tmp_list[1],tmp_list[2],tmp_list[3],tmp_list[4]])

		elif "ERROR in app:" in line:
			
			tmp_list = clean_log_line_and_put_in_to_list2(syslog_list,line,pids_done_list)
			pids_done_list.append(str(tmp_list[0]))
			
			if len(tmp_list) >= 4:
				gunicorn_error_proc_id_list.append([tmp_list[1],tmp_list[2],tmp_list[3],tmp_list[4]])
			else:
				gunicorn_error_proc_id_list.append([tmp_list[1],tmp_list[2],tmp_list[3],''])
	
	new_gunicorn_error_proc_id_list = clean_log_list_from_bad_insert(gunicorn_error_proc_id_list)

	#for line in gunicorn_error_proc_id_list:
	#	print(line)
  
	#print('*'*50) 
	#for line in new_gunicorn_error_proc_id_list:
	#	print('new_gunicorn_error_proc_id_list line: ',line)

	for data,pid,short,message in new_gunicorn_error_proc_id_list:
		for line in syslog_list:
			if str(pid) in line:
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
				worker_info_err_message = error_line_list[id+1][1][5].rstrip(':')
				tmp_line_err_msg2 = ''
				#print('worker_info_err_message==>',worker_info_err_message)
				if worker_info_err_message in ("ModuleNotFoundError","IndentationError","AttributeError"):
					tmp_line_err_msg2 = ' '.join(error_line_list[id+2][1][5:])
     
				pid = error_list[0]
				data = str(error_list[1][5]+' '+error_list[1][6]).replace('[','')
				tmp_line_err_msg1 = ' '.join(error_line_list[id+1][1][5:])
				tmp_line_err_msg3 = ' '.join(error_line_list[id+3][1][5:])
				strstr = tmp_line_err_msg1+' '+tmp_line_err_msg2
				
				if tmp_err_list.count(strstr) == 0:
					tmp_err_list.append(strstr)
					#print(id,pid,data,tmp_line_err_mg,tmp_line_err_msg2)
					err_msg_list.append([data,tmp_line_err_msg1,tmp_line_err_msg2,tmp_line_err_msg3])
			else:
				pid = error_list[1][4].replace('gunicorn[','').replace(']:','')
				if pid.isnumeric:
					if "TemplateNotFound" in ' '.join(error_list[1][5:]):
						#print('error_list==',pid,' '.join(error_list[1][5:]))
						#print(error_list)

						tmp_line_err_msg1 = ' '.join(error_list[1][5:])
						tmp_line_err_msg2 = 'Błąd zwiazany z template strony www.'
						tmp_line_err_msg3 = error_list
      
						err_msg_list.append([data,tmp_line_err_msg1,tmp_line_err_msg2,tmp_line_err_msg3])

	return err_msg_list


def clean_log_line_and_put_in_to_list2(syslog_list,line,pids_done_list):
	#line: Mar 24 13:59:38 ip-172-31-29-165 gunicorn[126855]: [2022-03-24 13:59:38 +0000] [126855] [INFO] Worker exiting (pid: 126855)
	tmp_line_list = line.split(']: [')
	pid = int(tmp_line_list[0].split('[')[-1])
	if pid not in pids_done_list:
		tmp_str = ''
		tmp_count = 0
		tmp_list = []
		for tmp_line in syslog_list:
			if str(pid) in tmp_line:
				tmp_tmp_line_list = tmp_line.split(']: [')
				if len(tmp_tmp_line_list) == 2:
					#print(tmp_count,tmp_tmp_line_list[-1])
					pass
				else:
					tmp_tmp_line_list = tmp_line.split(']:')
					#print(tmp_count,tmp_tmp_line_list[-1])
     
				if tmp_count == 0:
					data = ' '.join(tmp_tmp_line_list[-1].split(' ')[:2])
					msg1 = ' '.join(tmp_tmp_line_list[-1].split(' ')[3:])
					tmp_list.append([data,pid,msg1])
				elif tmp_count < 5:
					tmp_list.append([data,pid,tmp_line])
				else:
					break
				
				tmp_count+= 1

		# '\n'.join(tmp_list)
	
		#print('*'*50)
		#print('\n\n',tmp_list)
		#print('='*50)

		return [pid, tmp_list[0][0], tmp_list[0][1], tmp_list[0][2], tmp_list[0][3:]]

	else:
   
		return pid

def clean_log_list_from_bad_insert(gunicorn_error_proc_id_list):
  ##################################################
  #+#  Remove duplicates and not necessary data  #+#
  ##################################################
	pid_list = []
	for date,pid,short,message in gunicorn_error_proc_id_list:
		if short != 'ERROR':
			pid_list.append(pid)

	new_gunicorn_error_proc_id_list = []
	#print(len(gunicorn_error_proc_id_list),len(new_gunicorn_error_proc_id_list))
	for l in gunicorn_error_proc_id_list:
		#print('qqaa==',pid_list.count(l[1]),l)
		if pid_list.count(l[1]) == 1 and gunicorn_error_proc_id_list[2] != "ERROR":
			#print(pid_list[2], len(pid_list),pid_list)
			continue
		else:
			#print('aaaa',l)
			new_gunicorn_error_proc_id_list.append(l)

	return new_gunicorn_error_proc_id_list


def search_syslog_for_error():

	header_print('Przeglądam plik syslog')
  
	syslog_list = subprocess.getoutput('cat /var/log/syslog').split('\n')
	syslog_list.reverse()
	err_msg_list = prepare_syslog_output(syslog_list[:500])
 
	#print(err_msg_list)
	if len(err_msg_list) > 0:
		print('\n\n\t Ostatnie błędy w pliku syslog:\n')
		for err_date, msgl1, msgl2, msgl3 in err_msg_list:
			print(' - - -',err_date,'- '*40)
			print('Komunikat błędu:', msgl1) #,'msgl2===>',msgl2)
			if "IndentationError" in msgl1:
				print('Sprawdź wcięcia w pliku app.py w linii:')
				print(msgl2)
				#tmp_place = msgl2.split(':')[3:]
				#print(' '.join(tmp_place))
			elif "AssertionError" in msgl1:
				tmp_info_list = msgl1.split(':')
				if "function" in tmp_info_list[1] and "overwriting" in tmp_info_list[1] and "an existing" in tmp_info_list[1]:
					print('Sprawdź nazwę funkcji, prawdopodobnie w pliku app.py masz 2 funkcje nazywające się:',tmp_info_list[-1])
					print('\n',msgl2)
			elif "ERROR in app:" in msgl1:
				tmp_info_list = msgl1.split(':')
				if "Exception" in tmp_info_list[-1] and "[GET]" in tmp_info_list[-1]:
					print('Sprawdź nazwę wywoływanego pliku html.')
					print('\n',msgl2)
    
			else:
				print(msgl2)
			print(msgl3)
			print('\n')
		#print(err_msg_list[0])
	else:
		print('\n\n\t Nie ma błędów w pliku syslog.')
  
def show_hdd_free_space():

	header_print('Dostępne miejsce na dysku')

	df_list = subprocess.getoutput('df -h').split('\n')
	for nr,line in enumerate(df_list):

		new_lline = []
		if nr < 2: print(line)
		#elif nr in range(2, 4): #nr >= 2 and nr : 
		else:
			lline = line.split(' ')
			for inr, item in enumerate(lline):
				if lline[inr] == "":	# and lline[inr-1] == "":
					continue
				else:
					if len(new_lline) > 0:
						new_lline.append('')
						new_lline.append(lline[inr])
					else:
						new_lline.append(lline[inr])
			if int(new_lline[-3].rstrip('%')) >= 85 and "dev/loop" not in new_lline[0]:
				print(new_lline)
	
	print('\n\n')
  

def show_server_hacking_attempts(user_name):

	header_print('Logowania na serwer')

	ll_list = subprocess.getoutput('lastlog').split('\n')
	log_line_list = []
	for nr,line in enumerate(ll_list):
		if "Never logged in" not in line:
			print(line)
			line_list = line.split(' ')
			log_line_list.append(line_list)
			if nr > 0 and user_name != line_list[0]:
				print('Wykryto logowanie innego uzytkownika niż obecnie zalogowany ',user_name,' != ',line_list[0])
  

def show_serwer_ip_and_domain_connection():
	import configparser
	import os

	config = configparser.ConfigParser()
	config.read('/var/www/flaga/settings.ini')

	domena = config['XD']['domena']

	plik_nginxa = ''
	plik_nginxa_template = open('/var/www/flaga/nginx_file').readlines()
	for l in plik_nginxa_template:
		if l.strip().startswith('server_name'):
			l=l.replace('NAZWA_STRONY', domena)
		plik_nginxa += l
  
	server_ip = subprocess.getoutput('curl -s http://checkip.amazonaws.com')
	header_print('IP twojego serwera: '+server_ip)
	
	print(' Podpięta domena: '+plik_nginxa)
  
def server_last_access(user_name):
  
	header_print('Dostęp do serwera - zestawienie')

	ll_list = subprocess.getoutput('last').split('\n')
	log_line_list = []
	for nr,line in enumerate(ll_list):
		if nr < 10:
			print(line)
		log_line_list.append(line.split(' '))
		#if nr > 0 and user_name != log_line_list[0]:
		#	print('Wykryto logowanie innego uzytkownika niż obecnie zalogowany')
  
  
  
 
def main():
  
	user_name = subprocess.getoutput('whoami')
 
	print('\n\n')
	print('\t1. Szukaj błędów serwera flask (flaga) w pliku /var/log/syslog')
	print('\t2. Pokaż dostępne miejsce na dysku')
	print('\t3. Pokaż konfiguracje domeny oraz IP')
	print('\t4. Informacja z lastaccess')
	print('\t5. Informacja o probach logowań')


	print('\n\tq. Wyjdź')
	option = input("\t\tCo robimy ? ")
	while True:
		if option == "1":
			search_syslog_for_error()
			break
   
		elif option == "2":
			show_hdd_free_space()
			break
   
		elif option == "3":
			show_serwer_ip_and_domain_connection()
			break
   
		elif option == "4":
			server_last_access(user_name)
			break
   
		elif option == "5":
			show_server_hacking_attempts(user_name)
			break

		elif option == "q":
			break
		else:
			search_syslog_for_error()
			show_hdd_free_space()
			show_serwer_ip_and_domain_connection()
			server_last_access(user_name)
			show_server_hacking_attempts(user_name)
   
			break
  
	print('\n\n\t Dzięki za skorzystanie z programu. \n\t Chętnie posłucham ewentualnych uwag. Może masz pomysł co można by tu jeszcze dodać albo zmodyfikować?')	
 
 
if __name__ == '__main__':
	main()


