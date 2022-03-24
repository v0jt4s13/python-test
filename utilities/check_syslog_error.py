
import subprocess


def clean_log_list_from_bad_insert(gunicorn_error_proc_id_list):
  ##################################################
  #+#  Remove duplicates and not necessary data  #+#
  ##################################################
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

	return new_gunicorn_error_proc_id_list
 
def clean_log_line_and_put_in_to_list(line):
  ################################################
  #+#  Change syslog line from string to list  #+#
  ################################################
  # Mar 22 00:15:55 ip-172-31-29-165 gunicorn[792103]: [2022-03-22 00:15:55 +0000] [792103] [INFO] Worker exiting (pid: 792103)
	# ['2022-03-22 00:15:55 +0000', '792103', 'INFO', 'Worker exiting (pid: 792103)']
  ################################################
	line_list = line.split(']: [')
	#print('\n\naaaaa ===>',line_list)
	new_list = line_list[1].split(']')
	tmp_list = []
	for nr,l in enumerate(new_list):
		tmp_list.append(l.replace(' [','').lstrip())
  
	return tmp_list

def prepare_syslog_output(syslog_list):
  ################################################
  #+#   Prepare syslog output to better view   #+#
  ################################################
  # Mar 22 00:15:55 ip-172-31-29-165 gunicorn[792103]: [2022-03-22 00:15:55 +0000] [792103] [INFO] Worker exiting (pid: 792103)
	# ['2022-03-22 00:15:55 +0000', '792103', 'INFO', 'Worker exiting (pid: 792103)']
  ################################################
	gunicorn_error_proc_id_list = []
	error_line_list = []
	for nr, line in enumerate(syslog_list):
		tmp_line_list = line.split(':')
		pid = 0
		#################################################
		# Search for specific string in syslog line
		#################################################
		if "[INFO]" in line and "Worker exiting" in line:
			#print('\n\tZZZ=',clean_log_line_and_put_in_to_list(line),'\n')
			tmp_list = clean_log_line_and_put_in_to_list(line)
			gunicorn_error_proc_id_list.append([tmp_list[0],tmp_list[1],tmp_list[2],tmp_list[3]])
		elif "[ERROR]" in line and "Exception in worker process" in line:
			#print('\n\tYYY=',clean_log_line_and_put_in_to_list(line),'\n')
			tmp_list = clean_log_line_and_put_in_to_list(line)
			gunicorn_error_proc_id_list.append([tmp_list[0],tmp_list[1],tmp_list[2],tmp_list[3]])
	
	new_gunicorn_error_proc_id_list = clean_log_list_from_bad_insert(gunicorn_error_proc_id_list)
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
				worker_info_err_message = error_line_list[id+1][1][5].rstrip(':')
				tmp_line_err_msg2 = ''
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

	return err_msg_list


def search_syslog_for_error():
  
	syslog_list = subprocess.getoutput('cat /var/log/syslog').split('\n')
	syslog_list.reverse()
	err_msg_list = prepare_syslog_output(syslog_list)
 
	#print(err_msg_list)
	if len(err_msg_list) > 0:
		print('\n\n\n Ostatnie błędy w pliku syslog:\n')
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
			else:
				print(msgl2)
			print(msgl3)
			print('\n')
		#print(err_msg_list[0])
	else:
		print('\n\n\n Nie ma błędów w pliku syslog.')
  
def show_hdd_free_space():
	print()
	print('='*30)
	print('Miejsce na dysku'.center(20))
	print()
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
  
  
 
def main():
  search_syslog_for_error()
  
  show_hdd_free_space()
  
  
    
if __name__ == '__main__':
	main()



def python():
  """
  operatory aytmetyczne: +-*/ %
  mozliwy zapis: 
  a = 5
  a+=3 ===> a = a + 3
  a == 8
  
  stringi:
  funkcje:
		len(str)
  
  metody:
		str = 'jakis string'
		str.capitalize()
		str.upper() str.lower()
		str[0] = j
		str[0:2] = ja
		str[-3:] = ing
		str.split(' ') => lista_slow
		' '.join(lista_slow)
		str.startswith('j')
		str.endswith('g')
		str.rstrip('g') / str.lstrip('g') / str.strip()
		str.join(str1, str2)
		str(325).zfill(5) => 00325 / str(5).zfill(5) ==> 00005
  
	instrukcje warunkowe:
		print("Jedz") if light == 'green' else print("Czekaj")
  
  petle:
		while 
		for int in range(1,10):	-> for int in range(0,30, 3):
			1 - 9												0,3,6,9 ... 27


	struktury danych -> list, set, tuple(krotka), dictionary:
	list.reverse()
 	list.sort()
  list.append()
  list.count(el)
  list.pop()
  list.remove()
  list.clear()
  
	s = set()
	s.add('one')
	s.add('two')
	s.add('five')
	s.remove('five')
	s.discard('five') -> nie wystapi blad jezeli nie ma wartosci
   
  """