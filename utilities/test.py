import random

lista = [1,2,3,4,5,6,6,7,9]

f_lista = []
l = 0
for n in range(1,1000):
  f_lista.append(random.choice(range(300,10000)))

print(f_lista)


def f1(lista,file):
  c = 0
  while True:
    if file.readline() in lista:
        lista.pop(c)
        break
    c+= 1
  return 

def f2(lista,file):
  f_lista = file.readlines()
  for i,line in enumerate(f_lista):
    if  line in lista:
        lista.pop(i)
        break
    
def f3(lista,file):
  [lista.remove(s) for s in [l for l in f_lista if l in lista]]
  
  
def f4(lista,file):
  for s in f_lista:
    try: lista.remove(s)
    except: pass
    
