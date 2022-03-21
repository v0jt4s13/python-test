import threading
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
from flask_server.app_files.moje_biblioteki import *
import requests
import urllib3

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

def timeNow(format=""):
  from datetime import datetime
  if format == "":
    now = datetime.now()
    return now.strftime("%M:%S")
  else:
    #datetime(1987, 12, 30, 17, 50, 14)
    return datetime.now()

def activeThreadingCheck(count=1,main_time_start=timeNow('ddn')):
  while threading.activeCount() > count:
    main_time_finish = timeNow('ddn')
    c = main_time_finish-main_time_start
  return c

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

##########################################
############ output lists ################
##########################################
wszystkieDomenyOut_list = []
status_code2_list = []
all_status_code_list = []
clearUrlList = []
json_list = []
  
def buildRespList(status_code,url,extra="200"):
  if status_code == 200:
    wszystkieDomenyOut_list.append([url, 200])

  else:
    wszystkieDomenyOut_list.append([url, status_code])
    status_code2_list.append([status_code,url])
            
    if all_status_code_list.count(status_code) == 0:
      all_status_code_list.append(status_code)

  today = date.today()
  str_list = [{
    'date':today,
    'status_code':status_code,
    'description':'Status code dla domeny',
    'extra':status_code
  }] #, 'output':curl_url}]
  #str_list = [['id','licznik'], ['status_code',status_code], ['description','Status code dla domeny'], ['extra',200]] #, 'output':curl_url}]
  clearUrlList.append([url, status_code])
  json_list.append({'domena':url, 'data':str_list})
  #json_list.append([["domena",url], ["data",str_list]])

#################################
# funkcja webRequest
# odpytanie za pomoca biblioteki requests domeny - oczekiwana odpowiedz 200
# import requests czy import urllib.request - czy nie wystarczy 1  z tych linii ??
#################################
def webRequest(url):
  #logging.info('========= START3 ========== '+str(url))
  urllib3.disable_warnings()
  try:
    resp = requests.get(url, verify=False, timeout=3)
    buildRespList(resp.status_code, url)
    #return [resp.status_code, url]
  except requests.exceptions.HTTPError as e: 
    buildRespList(e,"Error 0x11")
    #return [e, "Error"]

def webRequestOK(url):
  #logging.info('========= START2 ========== '+str(url))
  urllib3.disable_warnings()
  try:
    #logging.info('========= START2 22 ========== '+str(url))
    resp = requests.get(url)
    if resp.ok:
      buildRespList(200,url)
    else:
      return webRequest(url)
  except requests.exceptions.ConnectTimeout as e:
    buildRespList(e.errno,url,e)
  except requests.exceptions.ConnectionError as e:
    buildRespList(e.errno,url,e)
  except requests.exceptions.InvalidSchema as e:
    buildRespList(e.errno,url,e)
  except requests.exceptions.HTTPError as e: 
    buildRespList(e.errno,url,e)
  except:
    buildRespList(999,url,999)
    
def showLogs(n, str):
  if n == 1:
    print(str)
    
#################################
# funkcja flagsList
# pobranie listy domen, obrobienie stringow zawierajacych adresy stron (URI) i dodanie ich do tablic oraz wywołań (request) domen 
#################################
def flagsList(link,resp_count):
  import json
  import os
  
  #############################################################
  maximumThreadsCount = 10 # ????? ile mozna zapuscic max ????
  #############################################################
  
  domena_str = ""
  tmpDomeny_list = []
  tmpDomenyExt_list = []
  
  flagi_response = requests.get(link)
  flagi_tekst = flagi_response.text

  lista_flag = re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",flagi_tekst)
  flagi_lista_prep = flagi_tekst.split('</p><p>')
  
  main_time_start = timeNow('ddn')
  threads_response_list = list()
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
  
  licz = 0

  if 1 == 1:
    print(len(tmpDomeny_list),len(tmpDomenyExt_list))
    #print(tmpDomenyExt_list)
    ilosc_domen_pl = []
    ilosc_znakow = []
    ilosc_domen_pl.append(flagiIloscDomenPl(tmpDomenyExt_list,""))
    ilosc_znakow.append(flagiIloscZnakow(tmpDomeny_list,""))

  #if 1 == 2:
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
          #logging.info('========= START ========== '+url)
          if threading.activeCount() >= maximumThreadsCount:
            logging.info('========= POSTóJ ========== '+str(threading.activeCount()))
            while threading.activeCount() > maximumThreadsCount:
              pass

          #logging.info('t1 = webRequestOK('+url+')')
          t1 = threading.Thread(target=webRequestOK, args=(url,))
          threads_response_list.append(t1)           
          t1.start()

        except ValueError:
          logging.info('============================================================= 1111111111 ======> '+url)
          buildRespList(500,url)
            
        except:
          logging.info('============================================================ 222222222222 ======> '+url)
          buildRespList(999,url)
            
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
        
      except ValueError as e:
        print(url)
        print("*****************************************\n*****************************************\n  Oops! ", e)
        break
  ######################################################
  # Czekaj az ilosc aktywnych procesów zejdzie do zera #
  ######################################################
  c = activeThreadingCheck(1,main_time_start)
  
  status_ok_count = 0
  for item in clearUrlList:
    if item[1] == 200:
      status_ok_count+= 1
  
  #print('clearUrlList=',clearUrlList)
  #print('licz=',licz, 'status_ok_count=',status_ok_count)
  #print('all_status_code_list=',all_status_code_list)
  #print('status_code2_list=',status_code2_list)
  #print('json_list=',json_list)
  #print('timeLoad_list=',timeLoad_list)
  #print('ilosc_domen_pl=',ilosc_domen_pl)
  #print('ilosc_znakow=',ilosc_znakow)
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
    job_direction_ask = int(console.input("\t\t *** Co będziemy robić? \n\n\t\t1. Generowanie strony html z domenami z pliku json \n\t\t2. Aktualizacja dostępności domen\n\n\t\tTwój wybór to: "))

  json_file_name='flagi_file.json'
  
  ############################################################################
  #       ############# test flow - 10, 15 ###########################       #
  ############################################################################
  if job_direction_ask >= 10:
    if job_direction_ask == 10:
      startDateTime = current_milli_time()
      timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
      #print('                                 ',timeLoad_list[0][1])
      console.print(timeLoad_list[0][1],"\t\t", justify="left")
      console.rule("[bold red]Wystartowalim ...")
      val_list = flagsList('http://zajecia-programowania-xd.pl/flagi',0)
      timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
      #print('                                 ',timeLoad_list[-1][1])
      console.print(timeLoad_list[-1][1],"\t\t", justify="right")
      console.rule("[bold red]Koniec ...")

    if job_direction_ask == 15:
      json_file_name='flagi_file.json'    
      with open(json_file_name,'r+') as file:
        file_data = file.read()
        #print(type(file_data))
        file_data_json = file_data.replace("'", "\"")
        file_data = json.loads(file_data_json)
        licz = 0
        print(flagiIloscZnakow("",file_data['ListaDomen']))
  ############################################################################
  #       ############# test flow - 10, 15 ###########################       #
  ############################################################################

  if job_direction_ask == 1:
    #json_file_name = "flagi_file.json"
    flagiBuildWebpage(json_file_name)
    rebootFlask()
    
  if job_direction_ask == 2:
    print('\n\n')
    resp_count = console.input("\t\t *** Ilość wierszy do przeszukania?\n\t\t\t (0-max; Enter-10) :smiley: ")
    if resp_count == "":
      resp_count = 10
    elif resp_count != 0:
      #print(resp_count,type(int(resp_count)))
      if type(int(resp_count)) != type(1):
        resp_count = 10
    
    resp_count = int(resp_count)
    #print('resp_count==>',resp_count,' type=',type(resp_count))
    
    output_type = console.input("\n\t\t *** Wynik zapisać jako plik .json?\n\t\t\t (y-tak; Enter-pokaż wynik na ekranie): ")
    if output_type in ["y","Y","t","T"]:
      output_type = "json"
    print('\n')
    
    link = 'http://zajecia-programowania-xd.pl/flagi'
    #link = 'http://localhost/narzedzia/local/flagi'
    # uruchamiamy nasz program
    startDateTime = current_milli_time()
    timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
    #print('                                 ',timeLoad_list[0][1])
    console.print(timeLoad_list[0][1],"\t\t", justify="left")
    console.rule("[bold red]Wystartowalim ...")
    val_list = flagsList(link,resp_count)
    timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
    #print('                                 ',timeLoad_list[-1][1])
    console.print(timeLoad_list[-1][1],"\t\t", justify="right")
    console.rule("[bold red]Koniec ...")
    endDateTime = current_milli_time()
    #wyszukajUrlWStringu
    #print(val_list)

  #if 1 == 2:
    if output_type == "json":
      #print("*****************************************")
      #print("*****************************************")
      
      lista_domen_json = {
        'ListaDomen':val_list[5],
        'IloscDomen':val_list[1],
        'Status200':val_list[2],
        'Statusy':val_list[3],
        'BledneDomeny':val_list[4]
      }
      #lista_domen_list = "{'ListaDomen':"+str(val_list[5])+",'IloscDomen':"+str(val_list[1])+",'Status200':"+str(val_list[2])+","
      #lista_domen_list = lista_domen_list+"'Statusy':"+str(val_list[3])+",'BledneDomeny':"+str(val_list[4])+"}"
      #lista_domen_json = lista_domen_list.replace("'", '"')
      #print('\t\t ****************************************\n\t\t *********** supa json ******************\n\t\t ****************************************\n')
      #print(lista_domen_json)
      #print(json.dumps(lista_domen_json))
      #print('\t\t ****************************************\n\t\t ****************************************\n\t\t ****************************************\n')
      
      #json_file_name = 
      #save_to_file_output_str = 
      #with open(json_file_name, 'w') as file:
      #  file.write(lista_domen_json)

      #file.close()
      from flask_server.app_files.moje_biblioteki import saveJsonStringToFile
      if saveJsonStringToFile(json_file_name,lista_domen_json):
        print("\t\t","*"*65)
        print("\t\t *** Zapisane do pliku:[bold blue] %s [/bold blue]" %json_file_name)
        print("\t\t","*"*65)
      else:
        print("\t\t","*"*65)
        print("\t\t *** Wystąpił błąd podczas zapisu do pliku:[bold blue] %s [/bold blue]" %json_file_name)
        print("\t\t","*"*65)
            
    else:
      print('')
      print('\t\t ****** Zobaczmy co my tu mamy ... ')
      print('\t\t ****** URI strony z flagami: ',link)
      print('')
    
    if 1 == 1:    
      print('')
      print('\t\t ******************************************************')
      str_out = "\t\t *** Ilość wszystkich domen: " + str(val_list[1])
      print(str_out, str(val_list[2]), sep='\n\t\t *** Domeny ze statusem 200: ')
      print('\t\t ******************************************************')
      # pokaz jakie wystapily odpowiedzi
      html_resp_code = val_list[3] #set(val_list[3])
      if len(html_resp_code) > 0:
        print('\t\t *** Kody odpowiedzi serwerów: %s' %html_resp_code)
      
      print('\t\t ******************************************************')
      print('\t\t *** Domeny z błędnymi odpowiedziami: ')
      # pokaz domeny z blednymi odpowiedziami
      for val in val_list[4]:
        print('\t\t *** %s URl:%s' %(val[0],val[1]))

      print('\n\n\t\t ******************************************************')
      print('\t\t *** I to by było na tyle ... ',)
      print('\t\t ******************************************************')
      print('\t\t ****** Oddano do użytku w zaledwie %s sekundy' %str(int(getDifference2(startDateTime, endDateTime)/1000)))
      print('\t\t\t *** by v0jt4s *** \n\n')
      
      def read_json(json_file_name='flagi_file.json'):
        liczcz = 0
        with open(json_file_name,'r+') as file:
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




"""
2022-03-12 14:38:55.550352                                                                                              
────────────────────────────────────────────────── Wystartowalim ... ───────────────────────────────────────────────────
803 803
                2022-03-12 14:39:28.822657 >>> Już 50 domen za nami. <<< 
                2022-03-12 14:40:56.938785 >>> Już 100 domen za nami. <<< 
                2022-03-12 14:42:35.178781 >>> Już 150 domen za nami. <<< 
                2022-03-12 14:44:01.494316 >>> Już 200 domen za nami. <<< 
                2022-03-12 14:44:28.468579 >>> Już 250 domen za nami. <<< 
                2022-03-12 14:44:58.062751 >>> Już 300 domen za nami. <<< 
                2022-03-12 14:46:09.388035 >>> Już 350 domen za nami. <<< 
                2022-03-12 14:46:40.884057 >>> Już 400 domen za nami. <<< 
                2022-03-12 14:48:51.341509 >>> Już 450 domen za nami. <<< 
                2022-03-12 14:50:31.917244 >>> Już 500 domen za nami. <<< 
                2022-03-12 14:51:58.793099 >>> Już 550 domen za nami. <<< 
                2022-03-12 14:53:07.087389 >>> Już 600 domen za nami. <<< 
                2022-03-12 14:54:27.830410 >>> Już 650 domen za nami. <<< 
                2022-03-12 14:56:57.494508 >>> Już 700 domen za nami. <<< 
                2022-03-12 14:58:57.753846 >>> Już 750 domen za nami. <<< 
                2022-03-12 15:02:31.541113 >>> Już 800 domen za nami. <<< 
                                                                                              2022-03-12 15:03:02.129279
────────────────────────────────────────────────────── Koniec ... ──────────────────────────────────────────────────────

2022-03-13 22:01:27.484527                                                                                              
────────────────────────────────────────────────── Wystartowalim ... ───────────────────────────────────────────────────
803 803
                2022-03-13 22:01:28.297472 >>> Już 50 domen za nami. <<< 
                2022-03-13 22:03:38.800255 >>> Już 100 domen za nami. <<< 
                2022-03-13 22:03:41.240881 >>> Już 150 domen za nami. <<< 
                2022-03-13 22:05:52.665401 >>> Już 200 domen za nami. <<< 
                2022-03-13 22:05:55.255100 >>> Już 250 domen za nami. <<< 
                2022-03-13 22:08:01.340815 >>> Już 300 domen za nami. <<< 
                2022-03-13 22:08:05.896924 >>> Już 350 domen za nami. <<< 
                2022-03-13 22:10:12.455644 >>> Już 400 domen za nami. <<< 
                2022-03-13 22:12:23.330858 >>> Już 450 domen za nami. <<< 
                2022-03-13 22:14:35.224326 >>> Już 500 domen za nami. <<< 
                2022-03-13 22:14:42.905958 >>> Już 550 domen za nami. <<< 
                2022-03-13 22:16:47.665728 >>> Już 600 domen za nami. <<< 
                2022-03-13 22:18:15.343340 >>> Już 650 domen za nami. <<< 
                2022-03-13 22:21:09.686240 >>> Już 700 domen za nami. <<< 
                2022-03-13 22:23:20.780081 >>> Już 750 domen za nami. <<< 
                2022-03-13 22:27:42.962923 >>> Już 800 domen za nami. <<< 
                                                                                              2022-03-13 22:29:59.856969
────────────────────────────────────────────────────── Koniec ... ──────────────────────────────────────────────────────

2022-03-12 14:38:55.550352                                                                                              
────────────────────────────────────────────────── Wystartowalim ... ───────────────────────────────────────────────────
803 803
                2022-03-12 14:39:28.822657 >>> Już 50 domen za nami. <<< 
                2022-03-12 14:40:56.938785 >>> Już 100 domen za nami. <<< 
                2022-03-12 14:42:35.178781 >>> Już 150 domen za nami. <<< 
                2022-03-12 14:44:01.494316 >>> Już 200 domen za nami. <<< 
                2022-03-12 14:44:28.468579 >>> Już 250 domen za nami. <<< 
                2022-03-12 14:44:58.062751 >>> Już 300 domen za nami. <<< 
                2022-03-12 14:46:09.388035 >>> Już 350 domen za nami. <<< 
                2022-03-12 14:46:40.884057 >>> Już 400 domen za nami. <<< 
                2022-03-12 14:48:51.341509 >>> Już 450 domen za nami. <<< 
                2022-03-12 14:50:31.917244 >>> Już 500 domen za nami. <<< 
                2022-03-12 14:51:58.793099 >>> Już 550 domen za nami. <<< 
                2022-03-12 14:53:07.087389 >>> Już 600 domen za nami. <<< 
                2022-03-12 14:54:27.830410 >>> Już 650 domen za nami. <<< 
                2022-03-12 14:56:57.494508 >>> Już 700 domen za nami. <<< 
                2022-03-12 14:58:57.753846 >>> Już 750 domen za nami. <<< 
                2022-03-12 15:02:31.541113 >>> Już 800 domen za nami. <<< 
                                                                                              2022-03-12 15:03:02.129279
────────────────────────────────────────────────────── Koniec ... ──────────────────────────────────────────────────────
                                ******************************************************
                                *** Zapisane do pliku: test_test_file.json 
                                ******************************************************

                                ******************************************************
                                *** Ilość wszystkich domen: 803
                                *** Domeny ze statusem 200: 725
                                ******************************************************
                                *** Kody odpowiedzi serwerów: [200, 502, 500, 404]
                                ******************************************************
                                *** Domeny z błędnymi odpowiedziami: 
                                *** 502 URl:http://dbys.pl
                                *** 502 URl:http://moje-programowanie.pl
                                *** 502 URl:http://lounalevittoux.pl
                                *** 502 URl:http://trellomorelo.pl
                                *** 502 URl:http://dominikak.pl
                                *** 500 URl:http://laboratorium-projektu.pl
                                *** 502 URl:http://robiefajnerzeczywpythonie.pl
                                *** 404 URl:http://3dradar.pl
                                *** 500 URl:http://rafalbryzek.pl
                                *** 502 URl:http://kilokota.pl
                                *** 404 URl:http://virgointhesky.pl
                                *** 502 URl:http://kacper-potocki.pl
                                *** 502 URl:http://kasia-python.pl
                                *** 502 URl:http://eultramax.pl
                                *** 502 URl:http://pythonfun.pl
                                *** 502 URl:http://test-klaudia-app.herokuapp.com
                                *** 502 URl:http://tsyhankova.pl
                                *** 502 URl:http://dandi-design.pl
                                *** 502 URl:http://olaponeta.pl
                                *** 502 URl:http://klaudianiemcewicz.pl
                                *** 502 URl:http://skepticalsnek.pl
                                *** 502 URl:http://programowanie.czest.pl
                                *** 404 URl:http://artbit.com.pl
                                *** 502 URl:http://bogdangpython.com.pl
                                *** 502 URl:http://kacpertest.pl
                                *** 502 URl:http://iwicher.pl
                                *** 502 URl:http://programistamati.pl
                                *** 502 URl:http://r3dwood.pl
                                *** 502 URl:http://kondiu.online
                                *** 502 URl:http://andzejem.pl
                                *** 404 URl:http://alawicki.pl
                                *** 502 URl:http://spiekanie.pl
                                *** 502 URl:http://angelzak.pl
                                *** 502 URl:http://tajny-kot.pl
                                *** 500 URl:http://popanato.bieda.it
                                *** 502 URl:http://sebasbobik.pl
                                *** 502 URl:http://milkatech.pl
                                *** 502 URl:http://tresmil.pl
                                *** 502 URl:http://la-cozja.pl
                                *** 502 URl:http://guayaba.pl
                                *** 404 URl:http://hauas.pl
                                *** 404 URl:http://miksawero.pl
                                *** 502 URl:http://roszkowska-it.com.pl
                                *** 502 URl:http://panidanych.pl
                                *** 502 URl:http://lukasz-motm.pl
                                *** 502 URl:http://programowanie.fun
                                *** 502 URl:http://cryptonft.com.pl
                                *** 502 URl:http://wysocmac.tk
                                *** 502 URl:http://jsjdhd.online
                                *** 502 URl:http://python-master.pl
                                *** 502 URl:http://panna-hakasse.plp
                                *** 502 URl:http://glodnapirania.pl
                                *** 502 URl:http://glodnapirania.pl
                                *** 502 URl:http://basia-zxd.pl
                                *** 502 URl:http://cardecor.pl
                                *** 502 URl:http://infiniteloop.site
                                *** 502 URl:http://python-nanotechnologia.pl
                                *** 502 URl:http://tengel.pl
                                *** 502 URl:http://bzentkow.pl
                                *** 404 URl:http://adekdevcode.pl
                                *** 404 URl:http://sulomon.pl
                                *** 502 URl:http://infmagazine.pl
                                *** 502 URl:http://ichimokumaster.pl
                                *** 502 URl:http://rob3rt.pl
                                *** 502 URl:http://digitalsoup.pl
                                *** 404 URl:http://onlyfansfilomenka.pl
                                *** 404 URl:http://teszka.pl
                                *** 502 URl:http://theriddle.pl
                                *** 500 URl:http://alemery.pl
                                *** 500 URl:http://test4kuba.pl
                                *** 502 URl:http://wiseowlstudio.xyz
                                *** 502 URl:http://hello-dev.pl
                                *** 502 URl:http://piotrorlinski.pl
                                *** 502 URl:http://testowanie-i-programowanie.pl
                                *** 502 URl:http://despresso.pl
                                *** 502 URl:http://jestemjonson.pl
                                *** 502 URl:http://puunina.szczecin.pl
                                *** 502 URl:http://edukodu.pl

"""