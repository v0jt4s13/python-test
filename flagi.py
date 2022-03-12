from operator import truediv
import urllib.request
import json
import re
import datetime
import time
from datetime import date, timedelta
import sys
# modules dla kolorowania textow
from rich import print
from rich.console import Console
# creating the console object
console = Console(width=120)

import logging
import logging.handlers
from moje_biblioteki import *

def log_setup():
  log_file_name = "output.log"
  log_handler = logging.handlers.WatchedFileHandler('output.log')
  formatter = logging.Formatter(
      '%(asctime)s program [%(process)d]: %(message)s',
      '%b %d %H:%M:%S')
  formatter.converter = time.gmtime  # if you want UTC time
  log_handler.setFormatter(formatter)
  logger = logging.getLogger()
  logger.addHandler(log_handler)
  logger.setLevel(logging.DEBUG)
log_setup()

timeLoad_list = []

def current_milli_time():
	return round(time.time() * 1000)

def getDifference2(then, now = current_milli_time()):
	duration = now - then
	return duration

################################# ``` ```
# funkcja wyszukajUrlWStringu
# wyszukiwanie fragmentu adresu url w dostarczonej tablicy stringow
# if 'http://' in str
#################################
def wyszukajUrlWStringu(str):
  em = re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",str)
  if len(em) > 0:
    #print('==================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  em=',em[0])
    return em[0]
  else:
    print('String nie jest poprawnym adresem URI: ',str)
    return ""

#################################
# funkcja webRequest
# odpytanie za pomoca biblioteki requests domeny - oczekiwana odpowiedz 200
# import requests czy import urllib.request - czy nie wystarczy 1  z tych linii ??
#################################
def webRequest(url):
  import requests
  import urllib3

  urllib3.disable_warnings()
  try:
    resp = requests.get(url, verify=False, timeout=10)
    return [resp.status_code, url]
  except requests.exceptions.HTTPError as e: 
    return [e, "Error"]

def webRequestOK(url):
  import requests
  import urllib3

  urllib3.disable_warnings()
  try:
    resp = requests.get(url)
    if resp.ok:
      return [200,url]
    else:
      return webRequest(url)
    
  except requests.exceptions.HTTPError as e: 
    return [e, "Error"]

def showLogs(n, str):
  if n == 1:
    print(str)
    
#################################
# funkcja flagsList
# pobranie listy domen, obrobienie stringow zawierajacych adresy stron (URI) i dodanie ich do tablic oraz wywołań (request) domen 
#################################
def flagsList(link,resp_count,json_file_name):
  import requests
  import json
  import os
  import threading
  
  domena_str = ""
  tmpDomeny_list = []
  tmpDomenyExt_list = []
  wszystkieDomenyOut_list = []
  flagi_response = requests.get(link)
  flagi_tekst = flagi_response.text

  lista_flag = re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",flagi_tekst)
  flagi_lista_prep = flagi_tekst.split('</p><p>')
  
  xx = 0
  for tmp_str in flagi_lista_prep:
    xx+= 1
    if tmp_str[:1] == "-":
      if re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str.split(' ')[1]):
        domena_str = tmp_str.split(' ')[1]
      #else:
        #print(xx,tmp_str,re.findall(r"(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str))
    elif re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str):
      domena_str = re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str)[0]
    else:
      if re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str.split('</p>')[0]):
        domena_str = re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str.split('</p>')[0])[0]
      #else:
        #print(xx,tmp_str,re.findall(r"(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str))
    if domena_str.strip() == "":
      continue
    
    tmpDomeny_list.append(domena_str)
    try:
      d_ext = ""
      tmp_list = domena_str.split('.')
      if len(tmp_list) > 1:
        d_ext = tmp_list[-1]
        if d_ext == "pl" and tmp_list[-2] == "com":
          d_ext = tmp_list[-2]+"."+tmp_list[-1]
        #else:
        #  d_ext = "error"
    except:
      d_ext = "error"
    
    tmpDomenyExt_list.append([d_ext,domena_str])
  
  
  all_status_code_list = []
  status_code2_list = []
  json_list = []
  clearUrlList = ['website url', 'status']
  clearUrlList.clear()
  licz = 0
  status_ok_count = 0

  if 1 == 1:
    print(len(tmpDomeny_list),len(tmpDomenyExt_list))
    #print(tmpDomenyExt_list)
    ilosc_domen_pl = []
    ilosc_znakow = []
    ilosc_domen_pl.append(flagiIloscDomenPl(tmpDomenyExt_list,""))
    ilosc_znakow.append(flagiIloscZnakow(tmpDomeny_list,""))

  #if 1 == 2:
    tt1 = 0
    for url in tmpDomeny_list:
      tmpUrl = wyszukajUrlWStringu(url)
      if len(tmpUrl) > 0:
        url = tmpUrl
      
      datetime_now_str = str(datetime.datetime.now())
      licz += 1
      try:
        try:
        #if 1 == 1:
          url = "http://"+url
          logging.info('========= START ========== '+url)
          if tt1 == 0:
            tt1 = 1
            logging.info('t1 = webRequestOK('+url+')')
            t1 = threading.Thread(target=webRequestOK, args=url)
            continue
          
          tt1 = 0
          logging.info('t2 = webRequestOK('+url+')')
          t2 = threading.Thread(target=webRequestOK, args=url)
            
          t1.start()
          #logging.info(url)
          t2.start()
          #logging.info(url)
          
          status_code = t1.join()
          if status_code[0] == 200:
            wszystkieDomenyOut_list.append([status_code[1], 200])
            status_ok_count += 1
          else:
            wszystkieDomenyOut_list.append([status_code[1], status_code[0]])
            status_code2_list.append([status_code[0],url])
          
          if all_status_code_list.count(status_code[0]) == 0:
            all_status_code_list.append(status_code[0])
          str_list = [{'id':licz-1, 'status_code':status_code[0],'description':'Status code dla domeny', 'extra':200}] #, 'output':curl_url}]
          clearUrlList.append([url, status_code[0]])
          json_list.append({"domena":url, "data":str_list})
          
          status_code = t2.join()
          if status_code[0] == 200:
            wszystkieDomenyOut_list.append([status_code[1], 200])
            status_ok_count += 1
          else:
            wszystkieDomenyOut_list.append([status_code[1], status_code[0]])
            status_code2_list.append([status_code[0],url])

          if all_status_code_list.count(status_code[0]) == 0:
            all_status_code_list.append(status_code[0])
          str_list = [{'id':licz-1, 'status_code':status_code[0],'description':'Status code dla domeny', 'extra':200}] #, 'output':curl_url}]
          clearUrlList.append([url, status_code[0]])
          json_list.append({"domena":url, "data":str_list})

          #str_list_json = {'id':licz, 'status_code':status_code[0],'description':'Status code dla domeny', 'extra':200}
          #str_list = [["id", licz], ["status_code", status_code[0]], ["description", 'Status code dla domeny'], ["url", url], ["extra",200], ["output",curl_url]] #, ["json_resp", status_code[1]]
          #[1, 200, {'Server': 'nginx/1.14.0 (Ubuntu)', 'Date': 'Wed, 02 Feb 2022 22:10:57 GMT', 'Content-Type': 'text/html; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip'}, 'Status code dla domeny', 'http://www.roszkov.pl']
          #showLogs(1, str)
          #print(js["Server"])

        except ValueError:
          logging.info('============================================================= 1111111111 ======> '+url)
          status_code = [500, url]
          
          wszystkieDomenyOut_list.append([url, status_code[0]])
          #print(licz,';',status_code[0],';',status_code[1],';Problem z domeną;   curl -i ', url)
          curl_url = "curl -i " + url
          str_list = [{'id':licz, 'status_code':status_code[0],'description':'Problem z domeną', 'extra':0}] #, 'output':curl_url}]
          #str_list_json = {'id':licz, 'status_code':status_code[0],'description':'Problem z domeną', 'extra':0}
          #str_list = [["id", licz], ["status_code", status_code[0]], ["description", 'Problem z domeną'], ["url", url], ["extra",0], ["output",curl_url]] #, ["json_resp", status_code[1]]
          #print(str_list)
          if status_code[0] == 200:
            status_ok_count += 1
            
        except:
          logging.info('============================================================ 222222222222 ======> '+url)
          status_code = [999, url]
          
          wszystkieDomenyOut_list.append([url, status_code[0]])
          #print(licz,';',status_code[0],';',status_code[1],';Nieudokumentowany problem z domeną;   curl -i ', url)
          curl_url = "curl -i " + url
          str_list = [{'id':licz, 'status_code':status_code[0],'description':'Nieudokumentowany problem z domeną', 'extra':0}] #, 'output':curl_url}]
          #str_list_json = {'id':licz, 'status_code':status_code[0],'description':'Nieudokumentowany problem z domeną', 'extra':0}
          #str_list = [["id", licz], ["status_code", status_code[0]], ["description", 'Nieudokumentowany problem z domeną'], ["url", url], ["extra",0], ["output",curl_url]] #, ["json_resp", status_code[1]]
          #print(str_list)
          if status_code[0] == 200:
            status_ok_count += 1
            
        #print(json.dumps(str_list))
        # wyswietl info o postepach co 50 rekordow
        if licz % 50 == 0:
          number = int(licz/10)
          licz_wew = int(licz/50)
          while number < licz_wew:
            licz_wew += 1
          timeLoad_list.append([time.time_ns(),datetime.datetime.now()])          
          print('\t\t%s >>> Już %s domen za nami. <<< ' %(datetime_now_str,licz))

        #logging.info(url)
        
        if resp_count != 0:
          if licz >= int(resp_count):        # na czas testow ogranicznie ilosci wyswietlania linków
            break
        #print("url {}".format("test"))
        
      except ValueError as e:
        print(url)
        print("*****************************************\n*****************************************\n  Oops! ", e)
        break

  timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
  return [clearUrlList, licz, status_ok_count, all_status_code_list, status_code2_list, json_list, timeLoad_list, ilosc_domen_pl, ilosc_znakow]

#################################
# funkcja main
# uruchomienie procedur main()
#################################
def main(argv):
  console.clear()
  
  if len(argv) == 3:
    resp_count = int(argv[1])
    if argv[2] in ("j","J","t","T","y","Y"):
      output_type = "json"
    else:
      output_type = ""
  else:
    job_direction_ask = int(console.input("\t\t\t\t*** Co będziemy robić? \n\n\t\t\t\t1. Generowanie strony html z domenami z pliku json \n\t\t\t\t2. Aktualizacja dostępności domen\n\n\t\t\t\tTwój wybór to: "))

  if job_direction_ask == 0:
    startDateTime = current_milli_time()
    timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
    #print('                                 ',timeLoad_list[0][1])
    console.print(timeLoad_list[0][1],"\t\t\t\t", justify="left")
    console.rule("[bold red]Wystartowalim ...")
    val_list = flagsList('http://zajecia-programowania-xd.pl/flagi',0,'test_file.json')
    timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
    #print('                                 ',timeLoad_list[-1][1])
    console.print(timeLoad_list[-1][1],"\t\t\t\t", justify="right")
    console.rule("[bold red]Koniec ...")

  if job_direction_ask == 5:
    filename='test_test_file.json'    
    with open(filename,'r+') as file:
      file_data = file.read()
      #print(type(file_data))
      file_data_json = file_data.replace("'", "\"")
      file_data = json.loads(file_data_json)
      licz = 0
      print(flagiIloscZnakow("",file_data['ListaDomen']))
    
  if job_direction_ask == 1:
    
    flagiBuildWebpage()
    rebootFlask()
    
  if job_direction_ask == 2:
    print('\n\n')
    resp_count = console.input("\t\t\t\t*** Ilość wierszy do przeszukania?\n\t\t\t\t\t (0-max; Enter-10) :smiley: ")
    if resp_count == "":
      resp_count = 10
    elif resp_count != 0:
      #print(resp_count,type(int(resp_count)))
      if type(int(resp_count)) != type(1):
        resp_count = 10
    
    resp_count = int(resp_count)
    #print('resp_count==>',resp_count,' type=',type(resp_count))
    
    output_type = console.input("\n\t\t\t\t*** Wynik zapisać jako plik .json?\n\t\t\t\t\t (y-tak; Enter-pokaż wynik na ekranie): ")
    if output_type in ["y","Y","t","T"]:
      output_type = "json"
    print('\n')
    
    json_file_name = "test_file.json"
    link = 'http://zajecia-programowania-xd.pl/flagi'
    #link = 'http://localhost/narzedzia/local/flagi'
    # uruchamiamy nasz program
    startDateTime = current_milli_time()
    timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
    #print('                                 ',timeLoad_list[0][1])
    console.print(timeLoad_list[0][1],"\t\t\t\t", justify="left")
    console.rule("[bold red]Wystartowalim ...")
    val_list = flagsList(link,resp_count,json_file_name)
    timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
    #print('                                 ',timeLoad_list[-1][1])
    console.print(timeLoad_list[-1][1],"\t\t\t\t", justify="right")
    console.rule("[bold red]Koniec ...")
    endDateTime = current_milli_time()
    #wyszukajUrlWStringu
    #print(val_list)

  #if 1 == 2:
    if output_type == "json":
      #print("*****************************************")
      #print("*****************************************")
      
      lista_domen_list = "{'ListaDomen':"+str(val_list[5])+",'IloscDomen':"+str(val_list[1])+",'Status200':"+str(val_list[2])+","
      lista_domen_list = lista_domen_list+"'Statusy':"+str(val_list[3])+",'BledneDomeny':"+str(val_list[4])+"}"
      lista_domen_json = lista_domen_list #json.dumps(lista_domen_list)
      #print('\t\t****************************************\n\t\t*********** supa json ******************\n\t\t****************************************\n')
      #print(json.loads(lista_domen_json))
      #print('\t\t****************************************\n\t\t****************************************\n\t\t****************************************\n')
      
      json_file_name = "test_test_file.json"
      with open(json_file_name, 'w') as file:
        file.write(lista_domen_json)

      file.close()
      
      print("\t\t\t\t******************************************************")
      print("\t\t\t\t*** Zapisane do pliku:[bold blue] %s [/bold blue]" %json_file_name)
      print("\t\t\t\t******************************************************")
      #print("*****************************************\n*****************************************\n")
      #print(json.dumps(val_list[0]));
      #print("*****************************************\n*****************************************\n")
      #print(json.dumps(val_list[1]));
      #print("*****************************************\n*****************************************\n")
      #print(json.dumps(val_list[2]));
      #print("*****************************************\n*****************************************\n")
      #print(json.dumps(val_list[3]));
      #print("*****************************************\n*****************************************\n")
      #print(json.dumps(val_list[4]));
      #print("*****************************************\n*****************************************\n")
    
    else:
      print('')
      print('\t\t\t\t****** Zobaczmy co my tu mamy ... ')
      print('\t\t\t\t****** URI strony z flagami: ',link)
      print('')
    
    if 1 == 1:    
      print('')
      print('\t\t\t\t******************************************************')
      str_out = "\t\t\t\t*** Ilość wszystkich domen: " + str(val_list[1])
      print(str_out, str(val_list[2]), sep='\n\t\t\t\t*** Domeny ze statusem 200: ')
      print('\t\t\t\t******************************************************')
      # pokaz jakie wystapily odpowiedzi
      html_resp_code = val_list[3] #set(val_list[3])
      if len(html_resp_code) > 0:
        print('\t\t\t\t*** Kody odpowiedzi serwerów: %s' %html_resp_code)
      
      print('\t\t\t\t******************************************************')
      print('\t\t\t\t*** Domeny z błędnymi odpowiedziami: ')
      # pokaz domeny z blednymi odpowiedziami
      for val in val_list[4]:
        print('\t\t\t\t*** %s URl:%s' %(val[0],val[1]))

      print('\n\n\t\t\t\t******************************************************')
      print('\t\t\t\t*** I to by było na tyle ... ',)
      print('\t\t\t\t******************************************************')
      print('\t\t\t\t****** Oddano do użytku w zaledwie %s sekundy' %str(int(getDifference2(startDateTime, endDateTime)/1000)))
      print('\t\t\t\t\t\t\t*** by v0jt4s *** \n\n')
      
      def read_json(filename='test_test_file.json'):
        liczcz = 0
        with open(filename,'r+') as file:
          liczcz+= 1
          # First we load existing data into a dict.
          file_data = file.read() #json.load(file)
          
          '''
          print('****** data z pliku ponizej ********')
          print('****** json.dumps(file_data) ********')
          print(json.dumps(file_data))
          print()
          print()
          print('****** data z pliku ponizej ********')
          print('****** file_data ********')
          print(file_data)
          '''
          
        file.close()
      read_json()


if __name__ == '__main__':
  main(sys.argv)
