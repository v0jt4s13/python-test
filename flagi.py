from operator import truediv
import urllib.request
import time
import json
import re

def wyszukajWStringu(str):
  em = re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",str)
  if len(em) > 0:
    #print('==================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  em=',em[0])
    #return True
    return em[0]
  else:
    print('String nie jest poprawnym adresem URI: ',str)
    #return False
    return ""

def webRequest(url):
  import requests
  import urllib3
  urllib3.disable_warnings()
  try:
    resp = requests.get(url, verify=False, timeout=10)
    #r.raise_for_status()
    return [resp.status_code, resp.headers]
  except requests.exceptions.HTTPError as e: 
    return [e, "Error"]

def bledneDomeny(str):
  bledne_domeny_list = ["http://www.marcyg.pl", "http://martaitwaw.pl", "http://elara-zp.pl", "http://cheswawprograms.pl", "http://www.agentdkkabelek.pl"]
  bledne_domeny_list.append("http://pythonprogramowanie.pl")
  bledne_domeny_list.append("http://www.python-nanotechnologia")
  bledne_domeny_list.append("http://www.python-chemia-nanotechnologia")
  bledne_domeny_list.append("http://zajecia-programowania-xd.pl")
  bledne_domeny_list.append("http://emocrec.pl")
  bledne_domeny_list.append("http://rafal-gala.pl")
  bledne_domeny_list.append("http://takietamprogramowanie.pl")
  bledne_domeny_list.append("http://patrycja-kaluza.pl")
  bledne_domeny_list.append("http://fizykadlateoretyka.pl")
  bledne_domeny_list.append("http://www.martaprogramuje.pl")
  bledne_domeny_list.append("http://www.jj-s.pl")
  bledne_domeny_list.append("http://programowanie-zalno.pl")
  bledne_domeny_list.append("http://annre.pl")
  bledne_domeny_list.append("http://www.teszka.pl")
  bledne_domeny_list.append("http://poswojemu.online")
  bledne_domeny_list.append("http://www.anowidesign.pl")
  bledne_domeny_list.append("http://botul.tech")
  bledne_domeny_list.append("http://www.joannahurnowicz.pl")
  bledne_domeny_list.append("http://awojcieszek.pl")
  bledne_domeny_list.append("http://jkubex.pl")
  bledne_domeny_list.append("http://miniquee.pl")
  bledne_domeny_list.append("http://tm-pytcourse.pl")
  bledne_domeny_list.append("http://www.koks-strona.pl")
  bledne_domeny_list.append("http://www.pimpa.pl")
  bledne_domeny_list.append("http://panna-hakasse.plp")
  bledne_domeny_list.append("http://witchystuff.com.pl")
  bledne_domeny_list.append("http://www.kmleszczak.pl")
  bledne_domeny_list.append("http://www.programistapython0122.pl")
  bledne_domeny_list.append("http://portfolio-michal.pl")
  bledne_domeny_list.append("http://artispace.pl")
  bledne_domeny_list.append("http://biologicznyszop.pl")
  bledne_domeny_list.append("http://kody-jagody.pl")
  bledne_domeny_list.append("http://www.wechikulzkompa.pl")
  bledne_domeny_list.append("http://kaktus-pieniazek.pl")
  bledne_domeny_list.append("http://borzymowski.com.pl")
  bledne_domeny_list.append("http://jaspersmeadow.pl")
  bledne_domeny_list.append("http://www.meng.pl")
  bledne_domeny_list.append("http://www.pompus.pl")
  bledne_domeny_list.append("http://sylwar-python.pl")
  bledne_domeny_list.append("http://www.savent.pl")
  bledne_domeny_list.append("http://www.artcave.pl")
  bledne_domeny_list.append("http://www.optymistycznanazycie.pl")
  bledne_domeny_list.append("https://botul.tech")
  bledne_domeny_list.append("https://www.solidny-analityk.pl")
  bledne_domeny_list.append("http://techdomain.pl")
  bledne_domeny_list.append("http://dziedzic.me")
  bledne_domeny_list.append("http://www.ichimokumaster.pl")
  if str == "list_out":
    print(bledne_domeny_list)
  if str in bledne_domeny_list:
    #print('***********************************************************************************\n!!!!!==',str,' in ',bledne_domeny_list,'==!!!!!\n********************************************************************')
    return True
  else:
    return False

def flagsList(link):
  import requests
  wszystkieDomenyOut_list = []
  
  flagi_response = requests.get(link)
  flagi_tekst = flagi_response.text
  #print(flagi_tekst) 
                                  #==> Zawislo 762 Flag.<p>http://awojcieszek.pl</p><p>http://neftays.pl</p><p>http://www.cyberprzemo.pl</p><p>http://www.agentdkkabelek.pl</p><p>http://pythonprogramowanie.pl</p><p>http://www.joanna-portfolio.pl</p><p>http://czysteuprawy.pl</p><p>http://jjtest.pl</p><p>http://macijawo.pl</p>
  
  flagi_lista = flagi_tekst.split('</p>')
  all_status_code_list = []
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
    #if licz == 0:
    #  pierwszy_url = url.split('<p>')
    #  url = pierwszy_url[1]
    #elif wyszukajWStringu(url):
    #  url = url[3:]

    tmpUrl = wyszukajWStringu(url)
    if len(tmpUrl) > 0:
      url = tmpUrl
    
    if bledneDomeny(url):
      wszystkieDomenyOut_list.append([url, 'AWARIA'])
      #print(licz, ' AWARIA ', url)
      continue
    
    licz += 1
    try:
      #print(licz, url)
      #url_tmp_list = url.split(' ')
      #if len(url_tmp_list) > 1:
      #  url = url_tmp_list[0]                      # obsluga wyjatkow gdzie sa dodane 2 domeny w jednym ciagu
      #  print(licz, url, sep=' <== ')
      try:
        #status_code = socketWebRequest(url)
        status_code = webRequest(url)
        wszystkieDomenyOut_list.append([url, status_code[0]])
        #print(licz, ' Sprawdzam status code dla domeny:', url, '==>', status_code[0])
      except ValueError:
        status_code = [500, 'ERROR']
        wszystkieDomenyOut_list.append([url, status_code[0]])
        #print(licz, ' Problem z domeną:', url, ' ==> HTTP status code:', status_code[0])
      
      # wyswietl info o postepach co 50 rekordow
      if licz % 50 == 0:
        print('Już ',licz,' domen za nami.')
      
      #time.sleep(2)
      if status_code[0] == 200:
        status_ok_count += 1

      if all_status_code_list.count(status_code[0]) == 0:
        all_status_code_list.append(status_code[0])
      
      if status_code[0] != 200:
        status_code2_list.append([status_code[0],url])
      
      clearUrlList.append([url, status_code[0]])

    except ValueError:
      print(url)
      print("*****************************************\n*****************************************\n  Oops! ", ValueError)

    
    #time.sleep(2)                               # Pause 2 seconds
    #if ( licz == 100 ):
    #  break
  
  #print("Koniec -> all_status_code_list=",all_status_code_list)
  #print("*******************************************************************************")
  #print("*******************************************************************************")
  #print("*******************************************************************************")
  #print("*******************************************************************************")
  #print("Koniec -> status_code2_list=",status_code2_list)
  
  return [clearUrlList, licz, status_ok_count, all_status_code_list, status_code2_list]

def main():
  print('')
  print('       ****** Zobaczmy co my tu mamy ... ')
  link = 'http://zajecia-programowania-xd.pl/flagi'
  print('       ****** URI strony z flagami: ',link)
  print('')
  # uruchamiamy nasz program
  val_list = flagsList(link)
  res = ' '.join([str(item) for item in val_list[0]])
  #print(len(res))
  #print(len(val_list[0]))
  flags_list = val_list[0]
  #for val in flags_list:
  #  print(val)
    
  print('')
  print('')
  str_out = "Ilość wszystkich stron: " + str(val_list[1])
  print(str_out, val_list[2], sep='\n Stron ze statusem 200: ')
  print('')
  # pokaz jakie wystapily odpowiedzi
  html_resp_code = set(val_list[3])
  if len(html_resp_code) > 0:
    print('Kody odpowiedzi serwerów: ', html_resp_code)
  
  print('')
  print('Strony z błędnymi odpowiedziami: ')
  # pokaz strony z blednymi odpowiedziami
  for val in val_list[4]:
    print(val[0],' URl:',val[1])

  print(bledneDomeny('list_out'))
  print('')
  print('')

if __name__ == '__main__':
  main()
