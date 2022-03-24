import sys
import subprocess
from rich.console import Console
# creating the console object
console = Console(width=100)

def readFile(file_name):
	# wczytaj plik do tablicy
	with open(file_name,'r+') as file:
		file_data_list = file.read().split('\n')

	return file_data_list

def saveDataListToFile(lprof_file_name, file_data_list):
	# zapisz dane w pliku
	with open(lprof_file_name, 'w') as f:
		for item in file_data_list:
			f.write("%s\n" % item)
  
	return True

def rebuildToLineProfile(file_data_list):
	# dodaj brakujace linie @profile
	new_file_data_list = []
	for line in file_data_list:
		if "def " == line[:4]:
			new_file_data_list.append("@profile")
			new_file_data_list.append(line)
		elif line.strip()[:1] != "#":
			new_file_data_list.append(line)

	return new_file_data_list


def main(argv):
	console.clear()
	
	if len(argv) > 1:
		file_name = argv[1]
	else:
		file_name = 'licz_domeny.py'

	lprof_file_name = file_name+".lprof" #.replace(".py", ".lprof.py")

	file_data_list = rebuildToLineProfile(readFile(file_name))

	try:
		if not saveDataListToFile(lprof_file_name, file_data_list):
			print('Wystąpił problem podczas zapisu pliku.')
			raise SystemExit
 
		try:
			kernprof_executed_line = "kernprof -l "+lprof_file_name
			i = input("\n\n\t\tPlik utworzony: "+lprof_file_name+"\n\n\t\tWykonac komende "+kernprof_executed_line+" (T/N)? ")
			if i in ("t","T","y","Y",""):
				out_str = subprocess.check_output(kernprof_executed_line, shell=True)
				#print(out_str.decode())
    
		except:
			print('cos poszko nie tak ;/')
   
		print("\n\t\tPlik gotowy do pracy z profilerem. \n\n\t\tAby zobaczyć statystyki uruchom: \n\t\tpython3 -m line_profiler",lprof_file_name+".lprof\n\n")
		ii = input('\t\tOdpalić go za Ciebie? ')
		if ii in ("t","T","y","Y",""):
			lprof_file_name_output = lprof_file_name+".output"
			lp_executed_line = "python3 -m line_profiler "+lprof_file_name+".lprof > "+lprof_file_name_output
			#try:
			print('\n\t\tOdpalam:',lp_executed_line)
			out_str = subprocess.check_output(lp_executed_line, shell=True)
			read_file_lines_list = readFile(lprof_file_name_output)

			header_list = []
			tmp_header_list = []
			for nr, line in enumerate(read_file_lines_list):
				# complete header info
				if "Total time: " in line:
					tmp_header_list.append(line)
				elif "File: " in line:
					tmp_header_list.append(line)
				elif "Function: " in line:
					tmp_header_list.append(line)
					tmp_list = tmp_header_list[0].split(' ')
					time = tmp_list[2]
					header_list.append([time,list(tmp_header_list)])
					tmp_header_list.clear()
				
			#print('===========',len(header_list),'=================')
			header_list2 = sorted(header_list, key=lambda x: x)
			#print(header_list2)

			output_list = []
			br = '='*40
			br+= '\n'
			output_list.append(br)
			licz_line = 0
			for time,lista in header_list2:
				licz_line+= 1
				if licz_line == 4:
					br = '\n'
					br+= '='*45
					br+= '\n'
				else:
					br = '='*45
				output_list.append(br)	
				lista_str = '\n'.join(lista).center(20)
				output_list.append(lista_str)


			br = '\n'
			br+= '='*88
			br+= '\n'
			output_list.append(br)
   
			for linia in read_file_lines_list:
				#lista_str = '\n'.join(lista)
				output_list.append(linia)

			#print('\n'.join(output_list))
			if saveDataListToFile(lprof_file_name_output, output_list):
				print('\t\tPlik wynikowy utworzony ==>',lprof_file_name_output,'\n\n\n')
				print('\n'.join(output_list[1:7]))
				
	except ValueError as e:
		print('\t\tBłąd: ',e)

	raise SystemExit

if __name__ == '__main__':
		main(sys.argv)

