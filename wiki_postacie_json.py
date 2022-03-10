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
    
def postacieListToFile(file_name,json_str):
	try:

		# Serializing json 
		json_obj = json.dumps(json_str, indent = 4)
		with open(file_name, "w") as outfile:
			outfile.write(json_obj)

		outfile.close()
  
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
	zapis = postacieListToFile(file_name,wszytkie_postacie_list)
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
	#if 1 == 1:
		print('\n\nPrint json file:')
		#f = open(file_name)
		# Opening JSON file
		with open(file_name) as json_file:
			data = json.load(json_file)

			# Print the type of data variable
			print("Type:", type(data))

			# Print the data of dictionary
			print("\nPeople1:", data['people1'])
			print("\nPeople2:", data['people2'])
	except:
	#else:
		print("\n\n\n\t\t\t\t Funkcja w trakcie tworzenia \n\n")	

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
			if argv[1] == "read":
				postacieWikiFromFile()
			else:
				lista_postaci = ["Kubuś puchatek", "Kopernik", "Małysz"]
				#print('2. postacieListToSaveInFile(',lista_postaci,',extra_para='')')
				postacieWikiToFile(lista_postaci,'')
		else:
			print('\n\n\nCos nie tak z wywolaniem ....')
#	else:
#		postacieWikiToFile(argv[1])

if __name__ == '__main__':
  main(sys.argv)