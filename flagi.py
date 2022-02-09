from operator import truediv
import urllib.request
import json
import re
import datetime
import time
from datetime import date, timedelta

# modules dla kolorowania textow
from rich import print
from rich.console import Console
# creating the console object
console = Console(width=120)

import logging
import logging.handlers

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
    return [resp.status_code, resp.headers]
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
  
  tmpDomeny_list = []
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
        tmpDomeny_list.append(tmp_str.split(' ')[1])
      #else:
        #print(xx,tmp_str,re.findall(r"(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str))
    elif re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str):
      tmpDomeny_list.append(re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str)[0])
    else:
      if re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str.split('</p>')[0]):
        tmpDomeny_list.append(re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str.split('</p>')[0])[0])
      #else:
        #print(xx,tmp_str,re.findall(r"(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",tmp_str))
  
  all_status_code_list = []
  status_code2_list = []
  json_list = []
  json_str_list = []
  clearUrlList = ['website url', 'status']
  clearUrlList.clear()
  licz = 0
  status_ok_count = 0
    
  if 1 == 1:
    for url in tmpDomeny_list:
      tmpUrl = wyszukajUrlWStringu(url)
      if len(tmpUrl) > 0:
        url = tmpUrl
      
      datetime_now_str = str(datetime.datetime.now())
      licz += 1
      try:
        try:
          url = "http://"+url
          status_code = webRequest(url)
          #print(url)
          wszystkieDomenyOut_list.append([url, status_code[0]])
          curl_url = "curl -i " + url
          str_list = [{'id':licz, 'status_code':status_code[0],'description':'Status code dla domeny', 'extra':200}] #, 'output':curl_url}]
          #str_list = [["id", licz], ["status_code", status_code[0]], ["description", 'Status code dla domeny'], ["url", url], ["extra",200], ["output",curl_url]] #, ["json_resp", status_code[1]]
          #[1, 200, {'Server': 'nginx/1.14.0 (Ubuntu)', 'Date': 'Wed, 02 Feb 2022 22:10:57 GMT', 'Content-Type': 'text/html; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip'}, 'Status code dla domeny', 'http://www.roszkov.pl']
          #showLogs(1, str)
          #print(js["Server"])
        except ValueError:
          #status_code = [500, status_code]
          wszystkieDomenyOut_list.append([url, status_code[0]])
          #print(licz,';',status_code[0],';',status_code[1],';Problem z domeną;   curl -i ', url)
          curl_url = "curl -i " + url
          str_list = [{'id':licz, 'status_code':status_code[0],'description':'Problem z domeną', 'extra':0}] #, 'output':curl_url}]
          #str_list = [["id", licz], ["status_code", status_code[0]], ["description", 'Problem z domeną'], ["url", url], ["extra",0], ["output",curl_url]] #, ["json_resp", status_code[1]]
          #print(str_list)
        except:
          #status_code = [999, status_code]
          wszystkieDomenyOut_list.append([url, status_code[0]])
          #print(licz,';',status_code[0],';',status_code[1],';Nieudokumentowany problem z domeną;   curl -i ', url)
          curl_url = "curl -i " + url
          str_list = [{'id':licz, 'status_code':status_code[0],'description':'Nieudokumentowany problem z domeną', 'extra':0}] #, 'output':curl_url}]
          #str_list = [["id", licz], ["status_code", status_code[0]], ["description", 'Nieudokumentowany problem z domeną'], ["url", url], ["extra",0], ["output",curl_url]] #, ["json_resp", status_code[1]]
          #print(str_list)
        
        #print(json.dumps(str_list))
        # wyswietl info o postepach co 50 rekordow
        if licz % 50 == 0:
          number = int(licz/10)
          licz_wew = int(licz/50)
          while number < licz_wew:
            licz_wew += 1
          timeLoad_list.append([time.time_ns(),datetime.datetime.now()])          
          print('\t\t%s >>> Już %s domen za nami. <<< ' %(datetime_now_str,licz))

        if status_code[0] == 200:
          status_ok_count += 1

        if all_status_code_list.count(status_code[0]) == 0:
          all_status_code_list.append(status_code[0])
        
        if status_code[0] != 200:
          status_code2_list.append([status_code[0],url])
        
        clearUrlList.append([url, status_code[0]])
        json_list.append({"domena":url, "data":str_list})
        
        full_line = "'domena':"+url+", 'data':"+str(str_list)+"}"
        logging.info(url)
        
        if resp_count != 0:
          if licz >= int(resp_count):        # na czas testow ogranicznie ilosci wyswietlania linków
            break
        #print("url {}".format("test"))

        
      except ValueError as e:
        print(url)
        print("*****************************************\n*****************************************\n  Oops! ", e)

  #print('1',clearUrlList)
  #print('2',licz)
  #print('3',status_ok_count)
  #print('4',all_status_code_list)
  #print('5',status_code2_list)
  #print("*****************************************\n*****************************************")
  #print("*****************************************\n*****************************************")
  #print("*****************************************\n*****************************************")
  timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
  return [clearUrlList, licz, status_ok_count, all_status_code_list, status_code2_list, json_list, timeLoad_list]

#################################
# funkcja main
# uruchomienie procedur main()
#################################
def main():
  
  console.clear()
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
  
  if output_type == "json":
    #print("*****************************************")
    #print("*****************************************")
    
    lista_domen_list = "{'ListaDomen':"+str(val_list[5])+"},{'IloscDomen':"+str(val_list[1])+"},{'Status200':"+str(val_list[2])+"},"
    lista_domen_list = lista_domen_list+"{'Statusy':"+str(val_list[3])+"},{'BledneDomeny':"+str(val_list[4])+"}"
    lista_domen_json = lista_domen_list #json.dumps(lista_domen_list)
    #print('\t\t****************************************\n\t\t*********** supa json ******************\n\t\t****************************************\n')
    #print(lista_domen_json)
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
      #print(json.dumps(file_data))
      #print(file_data)
      
    file.close()
        
if __name__ == '__main__':
  main()
