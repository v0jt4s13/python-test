Telewizja = [{'nazwa': 'film1', 'start': 9, 'end': 12, 'czas': 3},
             {'nazwa': 'film2', 'start': 15, 'end': 17, 'czas': 2},
             {'nazwa': 'film3', 'start': 11, 'end': 16, 'czas': 5},
             {'nazwa': 'film4', 'start': 12, 'end': 14, 'czas': 2},
             {'nazwa': 'film5', 'start': 11.5, 'end': 12.5, 'czas': 1}]

def in_rangeA(film,min,tv_list):
	if int(film['start'])*10 not in range(int(min['start'])*10,int(min['end'])*10) and int(film['end'])*10 not in range(int(min['start'])*10,int(min['end'])*10):
		tv_list.append(film)
		print(tv_list)
	return tv_list

def in_rangeB(film,min,tv_list): #Funkcja która usuwa z tv_list nakładające sie programy na najkrotszy z nich(a - film który sprawdzamy, najkrotszy program, lista z której usuwamy)
	print(len(tv_list),' ===> ',film)
	#W funkcji sprawdzam czy poczatek lub koniec sprawdzanego programu zawiera sie w przedziale (poczatek najkrotszego programu i koniec najkrotszego programu)
	#Oraz czy poczatek lub koniec najkrotszego programu zawiera sie w przedziale (poczatek sprawdzanego programu,koniec sprawdzanego programu)
	#Pomnozone *10 żeby uniknąć floatów.
	#print('if ',film['start']*10,' in range(',int(min['start']*10),',',int(min['end']*10),')')
	if film['start']*10 in range(int(min['start']*10),int(min['end']*10)) \
		or film['end']*10 in range(int(min['start']*10),int(min['end']*10)) \
		or int(min['start']*10) in range(int(film['start']*10),int(film['end']*10)) \
		or int(min['end']*10) in range(int(film['start']*10),int(film['end']*10)):
		print(f'\tusuwanie {film}')
		tv_list.remove(film)
		print('\t\tpo usuwaniu',tv_list)
	return tv_list

def in_rangeC(film,min,tv_list): #Funkcja która usuwa z tv_list nakładające sie programy na najkrotszy z nich(a - film który sprawdzamy, najkrotszy program, lista z której usuwamy)
	#print(len(tv_list),' ===> ',film)
	remove_film = ""
	if film['start']*10 in range(int(min['start']*10),int(min['end']*10)):
		remove_film = str(film['start']*10)+' in '+str(range(int(min['start']*10),int(min['end']*10)))
	elif film['end']*10 in range(int(min['start']*10),int(min['end']*10)):
		remove_film = str(film['end']*10)+' in '+str(range(int(min['start']*10),int(min['end']*10)))
	elif int(min['start']*10) in range(int(film['start']*10),int(film['end']*10)):
		remove_film = str(int(min['start']*10))+' in '+str(range(int(film['start']*10),int(film['end']*10)))
	elif int(min['end']*10) in range(int(film['start']*10),int(film['end']*10)):
		remove_film = str(int(min['end']*10))+' in '+str(range(int(film['start']*10),int(film['end']*10)))
  
	if remove_film != "":
		print(f'\t\t\t\tin_rangeC ==> {remove_film} ==> do usuniecia {film}')
		return False

	return True

def in_rangeRemove(film,min,tv_list): #Funkcja która usuwa z tv_list nakładające sie programy na najkrotszy z nich(a - film który sprawdzamy, najkrotszy program, lista z której usuwamy)
	#print(len(tv_list),' ===> ',film)
	remove_film = ""
	if film['start']*10 in range(int(min['start']*10),int(min['end']*10)):
		remove_film = str(film['start']*10)+' in '+str(range(int(min['start']*10),int(min['end']*10)))
	elif film['end']*10 in range(int(min['start']*10),int(min['end']*10)):
		remove_film = str(film['end']*10)+' in '+str(range(int(min['start']*10),int(min['end']*10)))
	elif int(min['start']*10) in range(int(film['start']*10),int(film['end']*10)):
		remove_film = str(int(min['start']*10))+' in '+str(range(int(film['start']*10),int(film['end']*10)))
	elif int(min['end']*10) in range(int(film['start']*10),int(film['end']*10)):
		remove_film = str(int(min['end']*10))+' in '+str(range(int(film['start']*10),int(film['end']*10)))
  
	if remove_film != "":
		print(f'\t\t\t\tin_rangeRemove ==> {remove_film} ==> do usuniecia {film}')
		tv_list.remove(film)

	return tv_list
    
def alg_B(tv_list):
	#print('1. tv_list: ',tv_list)
	min = tv_list[0]
	watch = []
	for film in tv_list: #Tutaj jest wybór najkrótszego programu, jest wszystko git
		if film['end'] - film['start'] == min['end'] - min['start']:
			if film['end'] < min['end']:
				min = film
			if (film['end'] - film['start'])*10 < (min['end'] - min['start'])*10:
				min = film
	tv_list.remove(min)
	#print('2. tv_list: ',tv_list)
 
	for film in tv_list: #Iteruje po liście programów bez najkrótszego
		print(f'\t\t=TV len={len(tv_list)}===> {film} <=====')
		#watch = in_rangeB(film,min,tv_list) #Film z listy programów bez najkrotszego programu,najkrotszy program, Program telewizyjny bez najkrotszego programu
		if in_rangeC(film,min,tv_list):
			watch.append(film)		
  
	#watch.append(min) #Dodaje min do listy programów
	
	return watch #Zwraca liste programów które mozna obejrzec.

def alg_B2(tv_list):
	min = tv_list[0]
	watch = []
	for film in tv_list: #Tutaj jest wybór najkrótszego programu, jest wszystko git
		if film['end'] - film['start'] == min['end'] - min['start']:
			if film['end'] < min['end']:
				min = film
			if (film['end'] - film['start'])*10 < (min['end'] - min['start'])*10:
				min = film
	tv_list.remove(min)
 
	for film in tv_list: #Iteruje po liście programów bez najkrótszego
		print(f'\t\t=TV len={len(tv_list)}===> {film} <=====')
		#watch = in_rangeB(film,min,tv_list) #Film z listy programów bez najkrotszego programu,najkrotszy program, Program telewizyjny bez najkrotszego programu
		watch = in_rangeRemove(film,min,tv_list)
			
	watch.append(min) # ?? co ta linia ma robic ? dodac to co zostalo usuniete kilka linii wyzej -->> tv_list.remove(min)
  
	#watch.append(min) #Dodaje min do listy programów
	
	return watch #Zwraca liste programów które mozna obejrzec.

print('\n\n')
txt = '\t\tDane wejsciowe: '+str(type(Telewizja))+' '+str(len(Telewizja))
print(txt.center(75),'\n','-'*100)
print(Telewizja,'\n')
print('\n\n','*-* '*25)
print('\t\t>>>> Telewizja alg_B <<<<'.center(75))
print('','*-* '*25,'\n')
print('\n\tKoniec ==> ',alg_B(Telewizja))

print('\n\n','*-* '*25)
print('\t\t>>>> Telewizja alg_B2 <<<<'.center(75))
print('','*-* '*25,'\n')
print('\n\tKoniec ==> ',alg_B2(Telewizja))
print('\n\n\n')