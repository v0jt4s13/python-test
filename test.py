import requests

# Pobranie tekstu ze strony (jako tafla tesktu).
orangutan = 'https://zajecia-programowania-xd.pl/flagi'
surowe_info = requests.get( orangutan)
text = surowe_info.text

# Przygotowanie listy linków ze strony 🙂
lista_linii = text.split('</p>')
linki = []
for linia in lista_linii:

    link = linia.replace('<p>', '')
    link = link.replace('- ', '')
    link = link.strip()
    link = link.rstrip('.')

    if ' ' in link or '<' in link:
        continue
    linki.append(link)

lista_domen = linki 
#lista_domen = ["poz.jeden", "poz.pl", "poz.jedenascie", "pozkolejna.pl", "pozycjabezkropki"]

def ilosc_domen(lista_domen):
    bad_list = []
    nowa_lista = []
    nowa_lista_all = []
    for domena in lista_domen:
        try:
            tmp_list = domena.split('.')
            if len(tmp_list) > 1:
                d_ext = tmp_list[-1]
            else:
                d_ext = "error"
        except:
            d_ext = "error"
        #print('1. %s' %qq)
        nowa_lista_all.append(d_ext)
        if ":" in d_ext or "/" in d_ext:
            bad_list.append(domena)
        elif d_ext not in nowa_lista and d_ext != "error":
            nowa_lista.append(d_ext)
            #print('2. %s' %qq)
        #else:
            #res1 = d_ext in (item for sublist in nowa_lista for item in sublist)
            #print(d_ext+' ==> jest poz:'+str(nowa_lista.count(d_ext)))

    print('\n\n\tIlosc unikatowych rozszerzeń domen: '+str(len(nowa_lista)))
    print('\tBłędne domeny: %s \n\n' %str(bad_list))
    licz = 0
    nowa_lista2 = []
    for poz in nowa_lista:
        nowa_lista2.append([poz, nowa_lista_all.count(poz)])
        licz+= 1
        #print(str(licz)+'. '+poz)
    #print(nowa_lista2)
    return nowa_lista2

uni_ext_list = ilosc_domen(lista_domen)

# function to return the second element of the
# two elements passed as the parameter
def sortSecond(val):
    return val[1] 

uni_ext_list.sort(key = sortSecond, reverse = True) 
#print(uni_ext_list)

print("\tRozszerzenie\t  Ilość szt.")
print("      =============================== ")
for value in uni_ext_list:
    key = value[0]
    val = value[1]
    if len(key) > 6:
        print("\t."+key+"\t| "+str(val)+" szt.")
    else:
        print("\t."+key+"\t\t| "+str(val)+" szt.")

#for domena in lista_domen:
#    pozycja = lista[lista.index('.'):]
#ValueError: substring not found