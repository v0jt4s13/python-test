import random
import string

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

def password_generator(char_count):

	if type(char_count) == int:
		punctuation = "!#$%&*+,.:;=?@" #string.punctuation
		haslo_znaki_lista = []
		xx = 0
		while xx < 2:
			haslo_znaki_lista.append(str(random.sample(punctuation, 1)[0]))
			haslo_znaki_lista.append(str(random.randrange(0,9)))
			haslo_znaki_lista.append(str(random.choice(string.ascii_lowercase)))
			haslo_znaki_lista.append(str(random.choice(string.ascii_uppercase)))
			xx+= 1

		xx = 8
		while xx < char_count:
			num = random.random()*1000
			first = int(str(num)[0])
			last = int(str(num)[-1])
			rand_number = random.randrange(0,9)
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
	else:
		haslo_znaki_lista = "Cyfry miały być!"
  
	haslo = [''.join(haslo_znaki_lista)]
	haslo.append(listRandomSort(haslo_znaki_lista))
	return haslo[1]
