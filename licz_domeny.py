from logging import exception
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
    unique_ext_list = []
    all_domain_ext_list = []
    full_domain_list = []
    
    list_lista = []
    d_ext_list = []
    for domena in lista_domen:
        try:
            tmp_list = domena.split('.')
            if len(tmp_list) > 1:
                d_ext = tmp_list[-1]
                if d_ext == "pl" and tmp_list[-2] == "com":
                    d_ext = tmp_list[-2]+"."+tmp_list[-1]
            else:
                d_ext = "error"
        except:
            d_ext = "error"
        
        tmp_list_name = d_ext+'_list'
        if tmp_list_name not in list_lista:
            list_lista.append(tmp_list_name)
        
        if 1 == 2:
            try:
                print('list_lista[%s]' %tmp_list_name)
                xx = 0
                while xx < len(list_lista):
                    print('list_lista[%i] %s ==> %s' %(xx,tmp_list_name,list_lista[xx]))
                    xx+= 1
            except ValueError as e1:
                print('1. Error: %s' %e1)
            
        
        try:
            d_ext_list.append([d_ext,domena])
        except ValueError as e2:
            print('2. Error: %s' %e2)
        
        if domena != "":
            full_domain_list.append(domena)
            all_domain_ext_list.append(d_ext)

        if ":" in d_ext or "/" in d_ext:
            bad_list.append(domena)
        elif d_ext not in unique_ext_list and d_ext != "error":
            unique_ext_list.append(d_ext)
            #print('2. %s' %qq)
        #else:
            #res1 = d_ext in (item for sublist in unique_ext_list for item in sublist)
            #print(d_ext+' ==> jest poz:'+str(unique_ext_list.count(d_ext)))

    ########################################################################################
    # z przygotowanych tablic wydobywamy potrzebne informacje:
    # 1. Ilość domen .pl
    # 2. Ilość unikatowych rozszerzeń domen
    # 3. Błędne domeny
    # 4. Liczba znaków 'a' w nazwach domen
    # 5. Najmniejsza i największa ilość znaków w domenie
    
    tmp_str = ""
    for val in unique_ext_list:
        tmp_str+= val+" "
    #print('\n\n\t1. %s' %tmp_str)
    
    tmp_str = ""
    min_len = 0
    max_len = 0
    domain_min_char = ""
    domain_min_char_list = []
    domain_max_char = ""
    domain_max_char_list = []
    licz = 0
    for val in full_domain_list:
        domain_len = len(val)
        #if 0 in (min_len, max_len):
        #    print('Nowa wartosc:'+str(domain_len))
        if domain_len <= min_len or licz == 0:
            domain_min_char = val
            min_len = domain_len
            if min_len == domain_len:
                if len(domain_min_char_list) == 0:
                    domain_min_char_list.append(domain_min_char)
                if len(domain_min_char_list[-1]) > min_len:
                    domain_min_char_list = []
                    if domain_min_char not in domain_min_char_list:
                        domain_min_char_list.append(domain_min_char)
                if domain_min_char not in domain_min_char_list:
                    domain_min_char_list.append(val)
            #print('Nowa wartosc min:'+str(min_len)+'  ===> '+val)
        if domain_len > max_len:
            domain_max_char = val
            max_len = domain_len
            if max_len == domain_len:
                if len(domain_max_char_list) == 0:
                    domain_max_char_list.append(domain_max_char)
                if len(domain_max_char_list[-1]) < max_len:
                    domain_max_char_list = []
                    if domain_max_char not in domain_max_char_list:
                        domain_max_char_list.append(domain_max_char)
                if domain_max_char not in domain_max_char_list:
                    domain_max_char_list.append(val)
            #print('Nowa wartosc max:'+str(max_len)+'  ===> '+val)
        tmp_str+= val+" "
        licz+= 1
    #print('\n\n\t2. %s' %tmp_str)
    pl_ext_count = tmp_str.count('.pl')
    a_char_count = tmp_str.count('a')

    tmp_str = ""
    for val in all_domain_ext_list:
        tmp_str+= val+" "
    #print('\n\n\t3. %s' %tmp_str)
    
    tmp_str = ""
    for val in list_lista:
        tmp_str+= val+";"
    #tmp_str = "mojapierwszadomena.pl wozyweselne.pl adavxcq.pl soczkowato.pl do-it-today.pl"
    #print('\n\n\t4. %s' %tmp_str)

    #########################################################################################
    # wyswietlamy na ekranie
    print('\n\n\t*****************************************************************************')
    print('\t* Ilość domen .pl: '+str(pl_ext_count))
    print('\t* Ilość unikatowych rozszerzeń domen: '+str(len(unique_ext_list)))
    print('\t* Błędne domeny %i z %i: \n\t*\t\t\t%s' %(len(bad_list),len(all_domain_ext_list),str('\n\t*\t\t\t'.join(bad_list))))
    print('\t* Liczba znaków \'a\' w nazwach domen: '+str(a_char_count))
    print('\t* Najmniejsza i największa ilość znaków w domenie \n\t*\t\t\tmin: %s -> %s \n\t*\t\t\tmax: %s -> %s' %(str(min_len),', '.join(domain_min_char_list),str(max_len),', '.join(domain_max_char_list)))
    #print(domain_min_char_list)
    #print(domain_max_char_list)
    print('\t******************************************************************************\n\n')

    #tmp_str = ""
    #for val in d_ext_list:
    #    print(val)
    #    print(val[0],val[1])
        #tmp_str+= val+"==>"+val[0]+"<>"+val[1]+"++++++++++++"
    #print('\n\n\t4. %i ===> %s' %(len(d_ext_list),tmp_str))
    
    licz = 0
    nowa_lista2 = []
    d_ext_list_count = len(d_ext_list)
    for poz in unique_ext_list:
        xx = 0
        tmp_lista_domen = ""
        while xx < d_ext_list_count:
            if poz == d_ext_list[xx][0]:
                if tmp_lista_domen != "":
                    tmp_lista_domen+= ", "
                tmp_lista_domen+= d_ext_list[xx][1]
            xx+= 1
        nowa_lista2.append([poz, all_domain_ext_list.count(poz), tmp_lista_domen])
        licz+= 1
        #if licz >= 3:
        #    break
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
csv_str = ""
print("\tRozszerzenie\t  Ilość szt.")
print("      =============================== ")
#print(uni_ext_list)
for value in uni_ext_list:
    key = value[0]
    val = value[1]
    domena = value[2]
    str_domen = ""
    if val < 300:
        str_domen = '\n'+value[2]
    str_domen = ""
    csv_str+= key+";"+str(val)+"\n"
    if len(key) > 6:
        print("\t."+key+"\t| "+str(val)+" szt. "+str_domen)
    else:
        print("\t."+key+"\t\t| "+str(val)+" szt. "+str_domen)

#print(csv_str)
#for domena in lista_domen:
#    pozycja = lista[lista.index('.'):]
#ValueError: substring not found