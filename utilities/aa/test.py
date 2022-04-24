import random

lista = [6444, 2377, 8237, 6814, 8537, 2701, 7377, 7409, 8220, 8559, 2480, 6010, 624, 1702, 9699, 8425, 1499, 6201, 4448, 2111, 8054, 2433, 5417, 7797, 8283, 2096, 5962, 9503, 9998, 3660, 1780, 3346, 4216, 1365, 1655, 4130, 2294, 1783, 3935, 9614, 2696, 9149, 1087, 1238, 2145, 1584, 6789, 5763, 9036, 7196, 8493, 8673, 4487, 1106, 1677, 7221, 3577, 9660, 1184, 7506, 2034, 5535, 2395, 6451, 2229, 8738, 4859, 4876, 2071, 8213, 9414, 8888, 2132, 1106, 1715, 3065, 3127, 1274, 7034, 1034, 1030, 8957, 7801, 4553, 9554, 5188, 5613, 8716, 2898, 8584, 4143, 1849, 3074, 1749, 8780, 7778, 4804, 1777, 7627, 5003, 6223, 3096, 5951, 3528, 7063, 8732, 2832, 3389, 1889, 596, 9795, 1586, 4710, 7185, 7708, 9419, 7446, 3236, 4115, 5087, 3333, 4037, 4776, 2258, 5001, 7108, 4725, 8659, 1353, 3258, 2510, 3415, 6309, 2899, 7408, 8759, 6336, 7180, 7942, 656, 2004, 6218]
print(len(lista))
# f_lista = []
# l = 0
# for n in range(1,1000):
#   f_lista.append(random.choice(range(300,10000)))

def f0(lista):
  c = 0
  with open('data.file','r') as file:
    while not file:
      if file.readline() in lista:
        lista.pop(c)
      c+= 1

    return lista

def f1(lista):
  c = 0
  while True:
    with open('data.file','r') as file:
      if file.readline() in lista:
        lista.pop(c)
      c+= 1
  
    return lista

def f2(lista):
  with open('data.file','r') as file:
    f_lista = file.readlines()
    for i,line in enumerate(f_lista):
      if  line in lista:
          lista.pop(i)
  
  return lista
      
def f3(lista):
  with open('data.file','r') as f_lista:
    [lista.remove(s) for s in [l for l in f_lista if l in lista]]
    return lista
    
  
def f4(lista):
  with open('data.file','r') as f_lista:
    for s in f_lista:
      try: lista.remove(s)
      except: pass
  
  return lista
    

print(len(f0(lista)))
print(len(f1(lista)))
print(len(f2(lista)))
print(len(f3(lista)))
print(len(f4(lista)))