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
		with open(lprof_file_name, 'w') as f:
			for item in file_data_list:
				f.write("%s\n" % item)

		try:
			kernprof_executed_line = "kernprof -l "+lprof_file_name
			i = input("\n\n\t\tPlik utworzony: "+lprof_file_name+"\n\n\t\tWykonac komende "+kernprof_executed_line+" (T/N)? ")
			if i in ("t","T","y","Y"):
				out_str = subprocess.check_output(kernprof_executed_line, shell=True)
				#print(out_str.decode())
    
		except:
			i = input("Tworzenie pliku")
   
		print("\n\tPlik gotowy do pracy z profilerem. \n\n\tAby zobaczyć statystyki uruchom: \n\t\tpython3 -m line_profiler",lprof_file_name+".lprof\n\n")

	except ValueError as e:
		print('\t\tBłąd: ',e)

	raise SystemExit

if __name__ == '__main__':
		main(sys.argv)

