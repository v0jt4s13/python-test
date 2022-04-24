import os 
import shutil 

# Wpisz sciezke do folderu który 
# chcesz posortować , 
# żeby posortować 

path = '/home/voj/Downloads/_wywalic'

# To robi organizacje listy z wszystkimi plikami 
# i je wyświetla 
list = os.listdir(path) 

# To działa na każdym pliku 
for file in list: 
    name, ext = os.path.splitext(file) 
    # to magazynuje końcówki 
    ext = ext[1:] 

    # jeżeli jest w bibliotece
    if ext == '': 
        continue

    # To przesunie do biblioteki ext jeżeli biblioteka istnieje
    if os.path.exists(path+'/'+ext): 
       print('mv',path+'/'+file+' '+path+'/'+ext+'/'+file)
       #shutil.move(path+'/'+file, path+'/'+ext+'/'+file) 
       
    # jezeli biblioteka nie istnieje to ją utworzy
    else: 
      print('mkdir',path+'/'+ext,'mv',path+'/'+file+' '+path+'/'+ext+'/'+file)
      #os.makedirs(path+'/'+ext) 
      #shutil.move(path+'/'+file, path+'/'+ext+'/'+file)
        