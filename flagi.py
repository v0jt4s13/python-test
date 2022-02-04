from operator import truediv
import urllib.request
import time
import json
import re

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
def flagsList(link,resp_count):
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
  
  for url in tmpDomeny_list:
    tmpUrl = wyszukajUrlWStringu(url)
    if len(tmpUrl) > 0:
      url = tmpUrl
    
    licz += 1
    try:
      try:
        url = "http://"+url
        status_code = webRequest(url)
        wszystkieDomenyOut_list.append([url, status_code[0]])
        curl_url = "curl -i " + url
        str_list = [{'id':licz, 'status_code':status_code[0],'description':'Status code dla domeny', 'extra':200, 'output':curl_url}]
        #str_list = [["id", licz], ["status_code", status_code[0]], ["description", 'Status code dla domeny'], ["url", url], ["extra",200], ["output",curl_url]] #, ["json_resp", status_code[1]]
        #[1, 200, {'Server': 'nginx/1.14.0 (Ubuntu)', 'Date': 'Wed, 02 Feb 2022 22:10:57 GMT', 'Content-Type': 'text/html; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip'}, 'Status code dla domeny', 'http://www.roszkov.pl']
        #showLogs(1, str)
        #print(js["Server"])
      except ValueError:
        #status_code = [500, status_code]
        wszystkieDomenyOut_list.append([url, status_code[0]])
        #print(licz,';',status_code[0],';',status_code[1],';Problem z domeną;   curl -i ', url)
        curl_url = "curl -i " + url
        str_list = [{'id':licz, 'status_code':status_code[0],'description':'Problem z domeną', 'extra':0, 'output':curl_url}]
        #str_list = [["id", licz], ["status_code", status_code[0]], ["description", 'Problem z domeną'], ["url", url], ["extra",0], ["output",curl_url]] #, ["json_resp", status_code[1]]
        #print(str_list)
      except:
        #status_code = [999, status_code]
        wszystkieDomenyOut_list.append([url, status_code[0]])
        #print(licz,';',status_code[0],';',status_code[1],';Nieudokumentowany problem z domeną;   curl -i ', url)
        curl_url = "curl -i " + url
        str_list = [{'id':licz, 'status_code':status_code[0],'description':'Nieudokumentowany problem z domeną', 'extra':0, 'output':curl_url}]
        #str_list = [["id", licz], ["status_code", status_code[0]], ["description", 'Nieudokumentowany problem z domeną'], ["url", url], ["extra",0], ["output",curl_url]] #, ["json_resp", status_code[1]]
        #print(str_list)
      
      #print(json.dumps(str_list))
      # wyswietl info o postepach co 50 rekordow
      if licz % 50 == 0:
        number = int(licz/10)
        licz_wew = int(licz/50)
        while number < licz_wew:
          licz_wew += 1
          
        print('Już ',licz,' domen za nami.')

      if status_code[0] == 200:
        status_ok_count += 1

      if all_status_code_list.count(status_code[0]) == 0:
        all_status_code_list.append(status_code[0])
      
      if status_code[0] != 200:
        status_code2_list.append([status_code[0],url])
      
      clearUrlList.append([url, status_code[0]])
      json_list.append({'domena':url, "data":str_list})
      
      if resp_count != 0:
        if licz > int(resp_count):        # na czas testow ogranicznie ilosci wyswietlania linków
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
  return [clearUrlList, licz, status_ok_count, all_status_code_list, status_code2_list, json_list]

#################################
# funkcja main
# uruchomienie procedur main()
#################################
def main():
  
  resp_count = input("        Ilość wierszy do przeszukania?\n        (0-max; Enter-10) ")
  if resp_count != 0:
    print(resp_count,type(int(resp_count)))
    if type(int(resp_count)) != type(1):
      resp_count = 10
  print(resp_count,type(resp_count))
  
  output_type = input("        Wynik zapisać jako plik .json?\n        (y-tak; Enter-pokaż wynik na ekranie) ")
  if output_type in ["y", "t"]:
    output_type = "json"
  
  #link = 'http://zajecia-programowania-xd.pl/flagi'
  link = 'http://localhost/narzedzia/local/flagi'
  # uruchamiamy nasz program
  
  val_list = flagsList(link,resp_count)
  #wyszukajUrlWStringu
  #print(val_list)

  if output_type == "json":
    #print("*****************************************")
    #print("*****************************************")
    lista_domen = json.dumps([{'ListaDomen':val_list[5]},
                              {'IloscDomen':val_list[1]},
                              {'Status200':val_list[2]},
                              {'Statusy':val_list[3]},
                              {'BledneDomeny':val_list[4]},
                              ])
    #print(lista_domen)
    json_file_name = "test_file.json"
    with open(json_file_name, 'w') as file:
      json.dump([{'ListaDomen':val_list[5]},
                              {'IloscDomen':val_list[1]},
                              {'Status200':val_list[2]},
                              {'Statusy':val_list[3]},
                              {'BledneDomeny':val_list[4]},
                              ],file)
    print("       *****************************************")
    print("       *** Zapisane do pliku: ",json_file_name)
    print("       *****************************************")
    
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
    print('       ****** Zobaczmy co my tu mamy ... ')
    print('       ****** URI strony z flagami: ',link)
    print('')
  
  if 1 == 1:    
    print('')
    print('')
    str_out = "       Ilość wszystkich domen: " + str(val_list[1])
    print(str_out, val_list[2], sep='\n       Domeny ze statusem 200: ')
    print('')
    # pokaz jakie wystapily odpowiedzi
    html_resp_code = set(val_list[3])
    if len(html_resp_code) > 0:
      print('       Kody odpowiedzi serwerów: ', html_resp_code)
    
    print('')
    print('       Domeny z błędnymi odpowiedziami: ')
    # pokaz domeny z blednymi odpowiedziami
    for val in val_list[4]:
      print(val[0],' URl:',val[1])

    print('')
    print('')
    print('       ****** I to by było na tyle ... ')
    print('       ********************************')
    print('                                    *** by v0jt4s ***')

if __name__ == '__main__':
  main()
