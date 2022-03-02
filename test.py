#import json
#import subprocess
from lista_flag import stworz_liste_flag

def najdluzsza_najkrotsza_domena(lista_flag):
  n_dlugosc_max = 0 
  dlugie_domeny = []
  najdluzsza_domena = [] 
  n_dlugosc_min = 0 
  krotkie_domeny = [] 
  najkrotsza_domena = []

  ### Najdłuższa domena 
  for flaga in lista_flag:
    if len(flaga) > n_dlugosc_max: 
      n_dlugosc_max = len(flaga)
      dlugie_domeny.append(flaga)

  for flaga in dlugie_domeny:
    if len(flaga) == n_dlugosc_max:
      najdluzsza_domena.append(flaga)

  ### Najkrótsza domena
  n_dlugosc_min = n_dlugosc_max

  for flaga in lista_flag:
    if len(flaga) <= n_dlugosc_min and len(flaga) > 0:
      n_dlugosc_min = len(flaga)
      krotkie_domeny.append(flaga)

  for flaga in krotkie_domeny:
    if len(flaga) == n_dlugosc_min: 
      najkrotsza_domena.append(flaga)

  wynik = 'Najdłuższa domena to: ', najdluzsza_domena,', a najkrótsza domena to:', najkrotsza_domena

  return wynik




def najdluzsza_najkrotsza_domena1 (lista_flag):
  n_dlugosc_max = 0 
  dlugie_domeny = []
  najdluzsza_domena = [] 
  n_dlugosc_min = 0 
  krotkie_domeny = [] 
  najkrotsza_domena = []

  ### Najdłuższa domena 
  for flaga in lista_flag:
    flaga_len = len(flaga)
    if flaga_len > 0:
      if flaga_len > n_dlugosc_max: 
        n_dlugosc_max = flaga_len
        dlugie_domeny.append(flaga)
      elif flaga_len <= n_dlugosc_min or n_dlugosc_min == 0:
        n_dlugosc_min = flaga_len
        krotkie_domeny.append(flaga)
  
  print('\nIlość znaków (%i) najdłuższej domeny: %s \nIlość znaków (%i) najkrótszej domeny: %s \n\n' %(len(dlugie_domeny[-1]),dlugie_domeny[-1], len(krotkie_domeny[-1]),krotkie_domeny[-1]))
  
  for flaga in dlugie_domeny:
    if len(flaga) == n_dlugosc_max:
      najdluzsza_domena.append(flaga)

  for flaga in krotkie_domeny:
    if len(flaga) == n_dlugosc_min: 
      najkrotsza_domena.append(flaga)
  
  wynik = 'Najdłuższa domena, '+str(len(najdluzsza_domena[0]))+' znaków, to: '
  wynik+= ', '.join(najdluzsza_domena)+'\n'
  wynik+= 'Najkrótsza domena, '+str(len(najkrotsza_domena[0]))+' znaków, to: '
  wynik+= ', '.join(najkrotsza_domena)

  return wynik

url = "https://zajecia-programowania-xd.pl/flagi"
lista_flag = stworz_liste_flag(url)
wynik = najdluzsza_najkrotsza_domena1(lista_flag)
print(wynik)


"""
print('ls -d */')
main_dir_list = subprocess.check_output('ls -d */', shell=True).decode().split('\n')
print(main_dir_list)
print('* '*30)
print('* '*30)
for dir in main_dir_list:
	
	try:
		print(subprocess.check_output('ls '+dir+'*.py', shell=True).decode().split('\n'))
	except:
		print('ls '+dir+'*.py')


#dir_list = subprocess.check_output('ls -d rsync-home-directory/*', shell=True)

git_out = "" #subprocess.check_output('git clone https://github.com/v0jt4s13/python-test ./github-clone/', shell=True)

rsync_executed_line = 'rsync -Pavp --rsh="ssh -i ~/.ssh/aws-python-xd.pem" '+const_var('USER')+'@'+const_var('DOMAIN')+':~/ ./rsync-home-directory/'
#print('rsync -Pavp --rsh="ssh -i ~/.ssh/aws-python-xd.pem" ubuntu@pp.marzec.eu:~/python-test/ ./rsync-files/')

#rsync_wynik = subprocess.check_output(rsync_executed_line, shell=True)
#import_lines_list = subprocess.check_output('less github-clone/*.py |grep import', shell=True)

#print(rsync_wynik)


#print(git_out,rsync_wynik,import_lines_list)
#Usage: rsync [OPTION]... SRC [SRC]... DEST
#  or   rsync [OPTION]... SRC [SRC]... [USER@]HOST:DEST
#  or   rsync [OPTION]... SRC [SRC]... [USER@]HOST::DEST
#  or   rsync [OPTION]... SRC [SRC]... rsync://[USER@]HOST[:PORT]/DEST
#  or   rsync [OPTION]... [USER@]HOST:SRC [DEST]
#  or   rsync [OPTION]... [USER@]HOST::SRC [DEST]
#  or   rsync [OPTION]... rsync://[USER@]HOST[:PORT]/SRC [DEST]
#The ':' usages connect via remote shell, while '::' & 'rsync://' usages connect
#to an rsync daemon, and require SRC or DEST to start with a module name.

"""