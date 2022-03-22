
import subprocess


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


def search_syslog_for_error():
  
	syslog_list = subprocess.getoutput('cat /var/log/syslog').split('\n')
	syslog_list.reverse()
	err_msg_list = prepareSyslogOutput(syslog_list)
 
	#print(err_msg_list)
	if len(err_msg_list) > 0:
		print('\n\n\n Ostatnie błędy w pliku syslog:\n')
		for err_date, info, place in err_msg_list:
			print(' - - -',err_date,'- '*40)
			print('Komunikat błędu:', info) #,'place===>',place)
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
		print('\n\n\n Nie ma błędów w pliku syslog.')
  
  
def main():
  search_syslog_for_error()
    
if __name__ == '__main__':
	main()
