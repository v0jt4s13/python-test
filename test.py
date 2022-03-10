import subprocess
import os

def check_code_safety(file_path):
    code_lines = open(file_path).readlines()
    code_lines = [l.strip() for l in code_lines]
    banned_libraries = ['os', 'subprocess']
    # allowed_libraries = ['random', 'string'] # ta linia jest niepotrzebna
    file_name = file_path.split('/')[-1]
    for l in code_lines:
      l = l.strip(' ')
      l_list = l.split(' ')
      for word in l_list:
            if word in banned_libraries:
              if "import" in l_list:
                print('W pliku: '+file_name+' ==> znalezione zostało słowo: '+word+' w linii: '+l)
                return False
    return True


def check_code_safety_orig(file_path):
    save = False # True

    code_lines = open(file_path).readlines()
    code_lines = [l.strip() for l in code_lines]

    for l in code_lines:

        # Downloads.
        download_words = ['']
        for word in download_words:
            if word in l:
                return False

        # Polecenie remove.

        banned_words = ['']
        for word in banned_words:
            if word in l:
                return False
        # Sudo
        banned_words = ['sudo', 'su']
        for word in banned_words:
            if word in l:
                return False

        # Polecenia os, popen, sys = [ ]

        # Lista zbanowanych bibliotek.
        banned_libraries = ['os', 'subprocess', '']
        allowed_libraries = ['random', 'string']
        for word in banned_words:
            if word in l:
                return False


    return True

lista_plikow = subprocess.check_output('ls').decode().split('\n')
xx = 0

licz_files = 0
licz_save = 0
licz_nosave = 0
for plik in lista_plikow:
  plik_ext = plik.split('.')[-1]
  if type(plik) == str and plik_ext == "py":
    licz_files+= 1
    if check_code_safety(os.getcwd()+"/"+plik):
      licz_save+= 1
    else:
      licz_nosave+= 1
    xx+= 1

print('Przeszukanych plikow:',licz_files)
print('Bezpiecznych plikow:',licz_save)
print('Niebezpiecznych plikow:',licz_nosave)

def getWebPage(link):
  import requests
  website_response = requests.get(link)
  website_tekst = website_response.text

  website_lista_prep = website_tekst.split('\n')

  return website_lista_prep

def parseAdUrlFromAdsList(listing_page_url):
  from bs4 import BeautifulSoup
  #print(len(listing_page_url))
  website_lista_prep = getWebPage(listing_page_url)
  for tmp_str in website_lista_prep:
    #print(type(tmp_str),tmp_str)
    try:
      soup = BeautifulSoup(tmp_str, "lxml")
      href = soup.a['href']
    except:
      pass

  return href

lista = "https://londynek.net/buysell/view-ads?cat=1&start=1"
print(parseAdUrlFromAdsList(lista))

