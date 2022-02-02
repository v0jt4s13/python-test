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
    print('==================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  em=pty=>',str)
    #return False
    return ""

def wyszukajWStringu_depr(str):
  if 'http://' in str:
    return True
  elif 'https://' in str:
    return True
  else:
    return False

def progressBar(initInt):
  # importing modules
  from tqdm import tqdm
  from time import sleep
   
  # creating loop
  for i in tqdm(range(0, 100), initial = initInt, 
              desc ="Text You Want"):
    # slowing the for loop
    sleep(0.1)
        

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

def socketWebRequest(url):
  import socket
  import sys
  
  HOST = url                # The remote host
  PORT = 80         #50007  # The same port as used by the server
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
      s.connect((HOST, PORT))
      s.sendall(b'Hello, world')
      data = s.recv(1024)
      print('Received', repr(data))
      return [200, 'OK']
    except OSError as msg:
        s = None
        print('Error', msg)
        return [msg, msg]
  
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
  bledne_domeny_list.append("http://botul.tech")
  if str in bledne_domeny_list:
    #print('***********************************************************************************\n!!!!!==',str,' in ',bledne_domeny_list,'==!!!!!\n********************************************************************')
    return True
  else:
    return False

def flagsList():
  import requests
  wszystkieDomenyOut_list = []
  
  link = 'http://zajecia-programowania-xd.pl/flagi'
  flagi_response = requests.get(link)
  flagi_tekst = flagi_response.text
  #print(flagi_tekst) 
                                  #==> Zawisło 762 Flag.<p>http://awojcieszek.pl</p><p>http://neftays.pl</p><p>http://www.cyberprzemo.pl</p><p>http://www.agentdkkabelek.pl</p><p>http://pythonprogramowanie.pl</p><p>http://www.joanna-portfolio.pl</p><p>http://czysteuprawy.pl</p><p>http://jjtest.pl</p><p>http://macijawo.pl</p>
  
  elem = re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",flagi_tekst)
  print('                                              ********************************                                   ')
  print('                                              ********************************                                   ')
  print('                                              ********************************                                   ')
  print('                                              *******elem=',len(elem),'***************                                   ')
  print('                                              ********************************                                   ')
  print('                                              ********************************                                   ')
  print('                                              ********************************                                   ')
  print('                                              ********************************                                   ')
  print('                                              ********************************                                   ')
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
      initInt = int(100/licz)
      progressBar(initInt)
      try:
        #status_code = socketWebRequest(url)
        status_code = webRequest(url)
        wszystkieDomenyOut_list.append([url, status_code[0]])
        #print(licz, ' Sprawdzam status code dla domeny:', url, '==>', status_code[0])
      except ValueError:
        wszystkieDomenyOut_list.append([url, status_code[0]])
        #print(licz, ' Problem z domeną: ', url)
      
      if licz % 50 == 0:
        print(licz, ' URL: ', url)
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
    if ( licz == 100 ):
      break
  
  return [clearUrlList, licz, status_ok_count]

def findRemainder(n, k):
    
  for i in range(1, n + 1):
    # rem will store the remainder 
    # when i is divided by k.
    rem = i % k  
      
    print(i, "mod", k, "=", 
          rem, sep = " ")
  
def main():
  # function calling
  findRemainder(10, 3)

  val_list = flagsList()
  res = ' '.join([str(item) for item in val_list[0]])
  print(len(res))
  print(len(val_list[0]))
  flags_list = val_list[0]
  for val in flags_list:
    print(val)
    
  print('')
  print('')
  str_out = "Ilość wszystkich stron: " + str(val_list[1])
  print(str_out, val_list[2], sep='\n Stron ze statusem 200: ')

if __name__ == '__main__':
  main()
