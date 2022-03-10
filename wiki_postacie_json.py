import random 
import json
import sys

file_name = "postacie_lista.json"

def postac_wiki(postac:str):
    
	import wikipedia as wiki

	wiki.set_lang("pl")
	strona = wiki.search(postac)
	postać = wiki.page(strona[0])
	content = postać.content
	content = content.split("\n\n\n")
	opis = []
	opis.append(content[0])

	for n in content:
		if "== Życ" in n or "== Twór" in n:
			opis.append(n)

	img = ""
	try:
		imgs = wiki.page(strona[0]).images

		for img in imgs:
			if img and img.endswith("svg"):
				imgs.remove(img)
		if len(imgs) > 0:
			img  = imgs[0]
	except:
		img = ""

	opis = "\n".join(opis)
	ludz = postac

	return [ludz, opis ,img]
    

def postacieListToFile_fileCheck_dead():
	#########################################
 	# sprawdzenie czy plik json istnieje i
	#########################################
	from os.path import exists
	f_mode = "a"
	file_exists = exists(file_name)
	if file_exists is False:
		print("Brak pliku %s, wiec zostanie utworzony " %file_name)
		f_mode = "w"
	else:
		stworz_nowy_plik = input("Czy chcesz nadpisywac plik czy dopisywac zawartosc (T/N) ? ")
		if stworz_nowy_plik in ("T", "t", ""):
			f_mode = "w"
		else:
			f_mode = "a"
	return f_mode
	
def preparePostacieListToFile_dead(lista):

	line = 0
	wiersz_list = []
	wiersz_str = ""
	for items in lista:
		if line == 0:
			wiersz_list.append(["Nazwisko",lista[line]])
			wiersz_str = "'Nazwisko':'"+lista[line]+"'"
			#print(wiersz)		
		if line == len(lista)-1:
			wiersz_list.append(["Img",lista[line]])
			wiersz_str+= ", 'Img':'"+lista[line]+"'"
		else:
			wiersz_list.append(["Opis",lista[line][:10]])
			wiersz_str+= ", 'Opis':'"+lista[line][:10]+"'"
		line+= 1

	return json.dumps(wiersz_list)
	#return [{wiersz_str}]

def postacieListToFile(file_name,json_str,f_mode):
	try:
		with open(file_name, mode=f_mode) as f:
			f.writelines(json_str.decode())
	
		f.close()
  
		return "Zapisane"	
	except ValueError as e:	
		return "Błąd podczas zapisu:"+e	

def postacieListToSaveInFile(lista_postaci,extra_para=""):
    #############################################
    # Wykorzystanie funkcji postac_wiki() do pobrania opisu postaci 
    # a nastepnie przetworzenie jej do postaci json
    #############################################
	postac_list = []
	for postac in lista_postaci:
		postac_opis = postac_wiki(postac)
		if extra_para == "test":
			postac_list.append({'Ilosc':len(postac_opis),'Name':postac_opis[0],'url':postac_opis[-1]})
		else:
			postac_list.append({'Name':postac_opis[0],'Opis':postac_opis[1],'url':postac_opis[-1]})
	
	wszytkie_postacie_list = {'Postacie':postac_list}
	wszytkie_postacie_json = json.dumps(wszytkie_postacie_list, ensure_ascii=False).encode('utf8')
	f_mode = "w"
	zapis = postacieListToFile(file_name,wszytkie_postacie_json,f_mode)
	return zapis

def postacieWikiToFile(lista_postaci,extra_para=""):
	if len(lista_postaci) == "":
		lista_postaci = ["Kubuś puchatek", "Kopernik", "Małysz"]
  
	postacieListToSaveInFile(lista_postaci)
	lista_postaci_out = json.dumps(lista_postaci, ensure_ascii=False, sort_keys=True, indent=4).encode('utf8')
	
	if extra_para == "print":
		print('\n\nPrint json file:',file_name,'')
		postacieWikiFromFile()
  		#print(lista_postaci_out.decode())

 

def postacieWikiFromFile():
    
	try:
		print('\n\nPrint json file:')
		f = open(file_name)
		data = json.load(f)
		for line in data['Name']:
			print(line)
			f.close()
	except:
		print("\n\n\n\t\t\t\t Funkcja trakcie tworzenia \n\n")	

def main(argv):
	####### testowanie ######
	if len(sys.argv) == 1:
		print("\n\n\t Zapis postaci do pliku",file_name)
		print("\n\t\t 1. Tworzenie pliku .json => postacieWikiToFile(lista_postaci)")
		#print("\n\t\t\t wywolanie: postacieWikiToFile('test','test') \n\t\t\t generuje przykladowa liste")
		#print("\n\t\t\t wywolanie: postacieWikiToFile('test','print') \n\t\t\t generuje przykladowa liste i wyswietla wynik na ekran")
		print("\n\t\t 2. Lista z pliku .json  => postacieWikiFromFile() ")
		print("\n\t\t 3. Test z terminala: \n\t\t\tpython3 wiki_postacie_json.py test\n\t\t\tpython3 wiki_postacie_json.py test print")
		print("\n\n")
	else:
		argv_str = argv[1]
		if len(argv) == 3:
			if argv[1] == "test":
				lista_postaci = ["Kubuś puchatek", "Kopernik", "Małysz"]
				if argv[2] == "print":
					#print("1. postacieListToSaveInFile(",lista_postaci,",print)")
					postacieWikiToFile(lista_postaci,'print')
				else:
					postacieWikiToFile(lista_postaci,'')
		elif len(argv) == 2:
			lista_postaci = ["Kubuś puchatek", "Kopernik", "Małysz"]
			#print('2. postacieListToSaveInFile(',lista_postaci,',extra_para='')')
			postacieWikiToFile(lista_postaci,'')
		else:
			print('\n\n\nCos nie tak z wywolaniem ....')
#	else:
#		postacieWikiToFile(argv[1])

if __name__ == '__main__':
  main(sys.argv)