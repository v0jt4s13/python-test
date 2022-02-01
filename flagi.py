from operator import truediv
import requests
import urllib.request
import time
import json

def wyszukajWStringu(str):
  if 'http://' in str:
    return True
  elif 'https://' in str:
    return True
  else:
    return False

def webRequest(url):
  try:
    r = requests.get(url, verify=False, timeout=10)
    r.raise_for_status()
    return [r.status_code, r.headers]
  except requests.exceptions.HTTPError as e: 
    return [e, "Error"]

def flagsList():
  link = 'http://zajecia-programowania-xd.pl/flagi'
  flagi_response = requests.get(link)
  flagi_tekst = flagi_response.text
  #print(flagi_tekst) ==> <p>http://www.testowanie-i-programowanie.pl</p><p>http://www.fermenciarz.pl</p>
  
  bledne_flagi_list = ["http://www.marcyg.pl", "http://martaitwaw.pl"]
  flagi_lista = flagi_tekst.split('</p>')
  status_code_list = []
  status_code2_list = []
  clearUrlList = ['website url', 'status']
  clearUrlList.clear()
  licz = 0
  status_ok_count = 0
  for url in flagi_lista:
    if url in bledne_flagi_list:
      continue
    
    licz += 1
    #print(type(url))
    if licz == 1:
      pierwszy_url = url.split('<p>')
      url = pierwszy_url[1]
    elif wyszukajWStringu(url):
      url = url[3:]
    try:
      url_tmp_list = url.split(' ')
      if len(url_tmp_list) == 1:
        print(url)
      else:
        url = url_tmp_list[0]
        print(url)
      status_code = webRequest(url)
      if status_code[0] == 200:
        status_ok_count += 1

      status_code_list.append(status_code[0])
      status_code_str = status_code_list[licz-1]
      sc_str = " " + str(status_code[0]) + " "
      sc_str = sc_str + " ==> " + url
      status_code2_list.append(sc_str)
      clearUrlList.append([url, status_code[0]])

    except ValueError:
      continue
      print(url)
      print("*****************************************\n*****************************************\n  Oops! ", ValueError)

    
    #time.sleep(2)                               # Pause 5.5 seconds
    #if ( licz == 3 ):
    #  break
  
  return [clearUrlList, licz, status_ok_count]

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
