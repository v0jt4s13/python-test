from operator import truediv
import requests
import urllib.request
import time
import json

# ?? funkcja/procedura ??
# wyszukiwanie fragmentu adresu url w dostarczonej tablicy stringow
# if 'http://' in str
#################################
def wyszukajWStringu(str):
  if 'http://' in str:
    return True
  elif 'https://' in str:
    return True
  else:
    return False

# ?? funkcja/procedura ??
# odpytanie za pomoca biblioteki requests domeny - oczekiwana odpowiedz 200
# import requests czy import urllib.request - czy nie wystarczy 1  z tych linii ??
#################################
def webRequest(url):
  try:
    r = requests.get(url, verify=False, timeout=10)
    #r.raise_for_status()
    return [r.status_code, r.headers]
  except requests.exceptions.HTTPError as e: 
    return [0, "Error"]

# ?? funkcja/procedura ??
# tablica blednych domen, uzupelniana recnie z uwagi na blad nad ktorym nie jestem w stanie zapanowac
# uruchomienie aplikacji aktywuje blad, chyba ze tablica zostanie uzupelniona do konca
#################################
def bledneDomeny(str):
  bledne_domeny_list = ["http://www.marcyg.pl", "http://martaitwaw.pl", "http://elara-zp.pl", "http://cheswawprograms.pl", "http://www.agentdkkabelek.pl"]
  bledne_domeny_list.append("http://pythonprogramowanie.pl")
  bledne_domeny_list.append("http://www.python-nanotechnologia")
  bledne_domeny_list.append("http://www.python-chemia-nanotechnologia")
  bledne_domeny_list.append("http://zajecia-programowania-xd.pl")
  bledne_domeny_list.append("http://emocrec.pl")
  bledne_domeny_list.append("http://rafal-gala.pl")
  bledne_domeny_list.append("http://takietamprogramowanie.pl")
  if str in bledne_domeny_list:
    print('***********************************************************\n!!!!!==',str,' in ',bledne_domeny_list,'==!!!!!\n********************************************')
    return True
  else:
    return False

# ?? funkcja/procedura ??
# pobranie listy domen, obrobienie stringow zawierajacych adresy stron (URI) i dodanie ich do tablic oraz wywołań (request) domen 
# linia 99 -> status_code = webRequest(url) - miejsce wysypki domeny która odpowiedziała -> DNS_PROBE_FINISHED_NXDOMAIN
# *****     **********       *****
# ***** jakies propozycje ?? *****
# *****     **********       *****
#################################
def flagsList():
  link = 'http://zajecia-programowania-xd.pl/flagi'
  flagi_response = requests.get(link)
  flagi_tekst = flagi_response.text
  #print(flagi_tekst) 
                                  #==> Zawisło 762 Flag.<p>http://awojcieszek.pl</p><p>http://neftays.pl</p><p>http://www.cyberprzemo.pl</p><p>http://www.agentdkkabelek.pl</p><p>http://pythonprogramowanie.pl</p><p>http://www.joanna-portfolio.pl</p><p>http://czysteuprawy.pl</p><p>http://jjtest.pl</p><p>http://macijawo.pl</p>
  
  
  flagi_lista = flagi_tekst.split('</p>')
  status_code_list = []
  status_code2_list = []
  clearUrlList = ['website url', 'status']
  clearUrlList.clear()
  licz = 0
  status_ok_count = 0
  #try:
  #  flagi_lista.remove("http://www.marcyg.pl")
  #  flagi_lista.remove("http://martaitwaw.pl")
  #  flagi_lista.remove("http://elara-zp.pl")
  #  flagi_lista.remove("http://cheswawprograms.pl")
  #  flagi_lista.remove("http://www.agentdkkabelek.pl")
  #except ValueError:
  #  print("Cos sie tu wykrzaczylo ....")
  
  for url in flagi_lista:
    #print(type(url), url)                         # <class 'str'> <p>http://judy-website.pl
    if licz == 0:
      pierwszy_url = url.split('<p>')
      url = pierwszy_url[1]
    elif wyszukajWStringu(url):
      url = url[3:]

    if bledneDomeny(url):
      print(licz, ' AWARIA ', url)
      continue
    
    licz += 1
    try:
      print(licz, url)
      url_tmp_list = url.split(' ')
      if len(url_tmp_list) > 1:
        url = url_tmp_list[0]                     # obsluga wyjatkow gdzie sa dodane 2 domeny w jednym ciagu
        print(licz, url, sep=' <== ')
      
      try:
        status_code = webRequest(url)
        print(licz, ' Sprawdzam status code dla domeny:', url, '==>', status_code[0])
      except ValueError:
        print(licz, ' Problem z domeną: ', url)
        
      #time.sleep(2)
      if status_code[0] == 200:
        status_ok_count += 1

      status_code_list.append(status_code[0])
      status_code_str = status_code_list[licz-1]
      sc_str = " " + str(status_code[0]) + " "
      sc_str = sc_str + " ==> " + url
      status_code2_list.append(sc_str)
      clearUrlList.append([url, status_code[0]])

    except ValueError:
      print(url)
      print("*****************************************\n*****************************************\n  Oops! ", ValueError)

    
    #time.sleep(2)                               # Pause 5.5 seconds
    #if ( licz == 3 ):
    #  break
  
  return [clearUrlList, licz, status_ok_count]


# ?? funkcja/procedura ??
# uruchomienie procedur main()
#################################
def main():
    val_list = flagsList()
    res = ' '.join([str(item) for item in val_list[0]])
    print(len(res))
    print(len(val_list[0]))
    flags_list = val_list[0]
    for val in flags_list:
      print(val)
    
    str_out = "Ilość wszystkich stron: " + str(val_list[1])
    print(str_out, val_list[2], sep='\n Stron ze statusem 200: ')

if __name__ == '__main__':
    main()
