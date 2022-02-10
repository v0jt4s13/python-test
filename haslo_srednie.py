import random
import string
import logging
import logging.handlers
import time

def log_setup():
  log_file_name = "haslo_srednie_output.log"
  log_handler = logging.handlers.WatchedFileHandler('haslo_srednie_output.log')
  formatter = logging.Formatter(
      '%(asctime)s program [%(process)d]: %(message)s',
      '%b %d %H:%M:%S')
  formatter.converter = time.gmtime  # if you want UTC time
  log_handler.setFormatter(formatter)
  logger = logging.getLogger()
  logger.addHandler(log_handler)
  logger.setLevel(logging.DEBUG)
log_setup()
logging.info('=====>START<====')

def listRandomSort(lista):
	new_list = []
	list_len = len(lista)
	xx = 0
	while list_len > 1:
		rand_number = random.randrange(0,int(list_len-1))
		val = lista[rand_number]
		val_count = lista.count(val)
		#print('list_len:',list_len,' val:',val,' val_count:',val_count)

		lista.pop(rand_number)
		new_list.append(val)
		list_len = int(list_len-1)

		xx+= 1
		if xx > 25:
			break
	
	new_list.append(lista[0])
	new_list_str = ''.join(new_list)
	return new_list_str

def main():
	#console.clear()
	print("\n\n")
	print("\t\t\t####### Generator haseł #######")
	print("\t\t\tWstępne założenia: min 8 znakow, a w tym: 2 duże litery, 2 małe litery, 2 cyfry oraz 2 znaki specjalne")
	print()
	ilosc_znakow = int(input("\t\t\tPodaj dlugość hasła, pomiędzy 8 a 20 znaków: "))
	punctuation = "!#$%&*+,.:;=?@" #string.punctuation

	haslo_znaki_lista = []
	xx = 0
	while xx < 2:
		haslo_znaki_lista.append(str(random.sample(punctuation, 1)[0]))
		haslo_znaki_lista.append(str(random.randrange(0,9)))
		haslo_znaki_lista.append(str(random.choice(string.ascii_lowercase)))
		haslo_znaki_lista.append(str(random.choice(string.ascii_uppercase)))
		xx+= 1
	first8char = ''.join(haslo_znaki_lista)	

	xx = 8
	while xx < ilosc_znakow:
		num = random.random()*1000
		first = int(str(num)[0])
		last = int(str(num)[-1])
		rand_number = random.randrange(0,9)
		logging.info('# rand_number='+str(rand_number)+' -> first:'+str(first)+' -> last:'+str(last)+'')
		if first <= 3:
			haslo_znaki_lista.append(str(first))
			xx+= 1
			continue
		elif last <= 6:
			if int(first+last) % 2 != 0:
				char = random.choice(string.ascii_lowercase)
			else:
				char = random.choice(string.ascii_uppercase)
			haslo_znaki_lista.append(char)
			xx+= 1
			continue
		else:
			char = str(random.sample(punctuation, 1)[0])
			haslo_znaki_lista.append(char)
			xx+= 1
			continue


	haslo = [''.join(haslo_znaki_lista)]
	haslo.append(listRandomSort(haslo_znaki_lista))
	print('\t\t\tPierwsze wylosowane znaki hasła, aby uzyskać min. 8 znaków\n\t\t\t(DUZE-2;małe-2;cyfry-2;znaki specj-2):\n\t\t\t\t\t %s' %str(first8char))
	print()
	print('\t\t\tWygenerowane hasło, %s znaków: %s' %(ilosc_znakow,str(haslo[0])))
	print('\t\t\tDodatkowo przesortowane randomowo: %s' %str(haslo[1]))
	print()
	print('************************************************************************************')
	print()

if __name__ == '__main__':
  main()

# Zadanie domowe:

# Wypracowaliśmy generator haseł średnich :D Teraz Twoja kolej, korzystajac z kodu wyżej
# zamień hasło średnie na hasło mocne.

# Udoskonal generator haseł tak aby:
# 1. brał po 2 losowe cyfry/znaki i duze/male litery
# 2. losowa kolejnosc cyfr, znakow, duzych i malych liter
# 3. Pogłówkujcie co robic aby to dzialalo dobrze dla zadanej
#    liczby znakow od 8 do 20 

# Zadanie domowe trzymamy u siebie na serwerze i
# W poniedzialek bedzie omowione jak bedziemy
# gromadzic zadania, domowe, projekty,
# tez pare slow o GIT i VSC