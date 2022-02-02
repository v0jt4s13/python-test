from operator import truediv
import urllib.request
import time
import json
import re

#################################
# ?? funkcja/procedura ??
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
# ?? funkcja/procedura ??
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

# ?? funkcja/procedura ??
# pobranie listy domen, obrobienie stringow zawierajacych adresy stron (URI) i dodanie ich do tablic oraz wywołań (request) domen 
#################################
def flagsList(link):
  import requests
  
  wszystkieDomenyOut_list = []
  flagi_response = requests.get(link)
  flagi_tekst = flagi_response.text
  #print(flagi_tekst) 
  
  flagi_lista = flagi_tekst.split('</p>')
  all_status_code_list = []
  status_code2_list = []
  clearUrlList = ['website url', 'status']
  clearUrlList.clear()
  licz = 0
  status_ok_count = 0
  
  for url in flagi_lista:
    tmpUrl = wyszukajUrlWStringu(url)
    if len(tmpUrl) > 0:
      url = tmpUrl
    
    licz += 1
    try:
      try:
        status_code = webRequest(url)
        wszystkieDomenyOut_list.append([url, status_code[0]])
        #print(licz, ' Sprawdzam status code dla domeny:', url, '==>', status_code[0])
      except ValueError:
        status_code = [500, status_code]
        wszystkieDomenyOut_list.append([url, status_code[0]])
        #print(licz, ' Problem z domeną:', url, ' ==> HTTP status code:', status_code[0])
      except:
        status_code = [999, status_code]
        wszystkieDomenyOut_list.append([url, status_code[0]])

      # wyswietl info o postepach co 50 rekordow
      if licz % 50 == 0:
        print('Już ',licz,' domen za nami.')

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

  return [clearUrlList, licz, status_ok_count, all_status_code_list, status_code2_list]

# ?? funkcja/procedura ??
# uruchomienie procedur main()
#################################
def main():
  print('')
  print('       ****** Zobaczmy co my tu mamy ... ')
  link = 'http://zajecia-programowania-xd.pl/flagi'
  print('       ****** URI strony z flagami: ',link)
  print('')
  # uruchamiamy nasz program
  val_list = flagsList(link)
  print('')
  print('')
  str_out = "Ilość wszystkich domen: " + str(val_list[1])
  print(str_out, val_list[2], sep='\n Domeny ze statusem 200: ')
  print('')
  # pokaz jakie wystapily odpowiedzi
  html_resp_code = set(val_list[3])
  if len(html_resp_code) > 0:
    print('Kody odpowiedzi serwerów: ', html_resp_code)
  
  print('')
  print('Domeny z błędnymi odpowiedziami: ')
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
