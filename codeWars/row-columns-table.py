

def herodisiac(n,m):
  rows = n
  col = m
  a = 9
  for i in range(rows):
      temp = []
      for j in range(col):
          a += 1
          temp.append(a%10)
      print(*temp)

def Artur_Babinskicrown1(n,m):

  def tablica(rows, columns):
      numbers_list = [i % 10 for i in range(rows * columns)]
      result = [[] for row in range(rows)]  # create list of empty lists (each list is a row)
      [result[index // columns].append(str(number)) for index, number in enumerate(numbers_list)]  # fill the lists
      for lst in result:  # display the table 
          print(' '.join(lst))
  tablica(n,m)
  
def Artur_Babinskicrown2(n,m):

  def tablica2(rows, columns):
      numbers_list = [i % 10 for i in range(rows * columns)]
      for i in range((rows * columns) // columns):
          print(*numbers_list[i * columns:(i + 1) * columns])

  
  print('********************************')
  tablica2(n,m)


def Bartek(n=0,m=0):
  from tkinter import N  
  def kolejna(liczba):
    wynik = 0
    if liczba + 1 > 9:
        wynik = 0
    else:
        wynik = liczba + 1
    return wynik

  if n+m > 0:
    wiersz = n
    kolumna = m
  else:
    wiersz = int(input('Ile wierszy: '))
    kolumna = int(input('Ile kolumn: '))
  lista = ''

  zmienna = 0

  while wiersz != 0:

      for i in range(kolumna):
          wynik = zmienna
          lista = lista + str(wynik) + ' '
          zmienna = kolejna(zmienna)

      print(lista)
      lista = ''
      wiersz -= 1


def Boomer(n,m):

  kolumny = n
  wiersze = m

  def prs(kol, wier):
    str = "" 
    arr = [i%10 for i in range(kol*wier)]
    for j in range(len(arr)):
        str += "{0}, ".format(arr[j])
        if j%kol==kol-1 and j>0:
          str += "\n"
    str_d = str.replace(',', '')
    return str_d

  print(prs(kolumny, wiersze))


def Czarny(n,m):
  
  def gen_table(row, col):
      from itertools import cycle
      steps = 10 * row * col//10
      iter_cycle = cycle(range(10))

      for i in range(steps):
          if i % col == 0 and i != 0:
              print()
          print(next(iter_cycle), end=" ")

  gen_table(n,m)


def ika(n=0,m=0):
  from itertools import cycle
  if n+m > 0: 
    rows = n
    columns = m
  else:
    rows = int(input("Ile wierszy: "))
    columns = int(input("Ile kolumn: "))
  number_cycle = cycle('0123456789')
  for i in range(rows):
      row = []
      for j in range(columns):
          row.append(next(number_cycle))
      print(' '.join(row))


def RafalK(n,m):
  
  def funkcja(r, c):
    i=0
    for a in range(0, r):
        temp=[]
        for b in range(0, c):
          temp.append(i)
          if i ==9:
              i=0
          else:
              i +=1
        print(*temp)
        temp.clear()

  funkcja(n,m)
  

def SebastianK(n,m):

  def arr(w, k):
      i = 0
      for y in range(w):
          for x in range(k):
              print(i, end=" ")
              i += 1
              if i == 10:
                  i = 0
          print()
  arr(n,m)


def svenson(n,m):

  def tablica(inputTable):
      numberOfALL = inputTable[0]*inputTable[1]
      tempDigit = 0

      for i in range(1, numberOfALL+1):
          if i % inputTable[1] == 0:
              print(tempDigit)
          else:
              print(tempDigit, end=' ')

          tempDigit += 1
          if tempDigit > 9:
              tempDigit = 0


  tablica([n,m])

def Urbid(n,m):

  def tablica (n, m):
    ret = []
    nice_list = [(lambda x: str(x%10))(x) for x in list(range(0,n*m+1))]
    start, end = 0, m

    for _ in range(n):
      ret.append(" ".join(nice_list[start:end]))
      start, end = end, end+m

    return "\n".join(ret)
  
  return tablica(n,m)
  
  
n = 50
m = 50

print('\n\n','-'*42,'\n','*'*10,'Urbid'.center(20),'*'*10,'\n')
print(Urbid(n,m))

print('\n\n','-'*42,'\n','*'*10,'svenson'.center(20),'*'*10,'\n')
svenson(n,m)

print('\n\n','-'*42,'\n','*'*10,'SebastianK'.center(20),'*'*10,'\n')
SebastianK(n,m)

print('\n\n','-'*42,'\n','*'*10,'RafalK'.center(20),'*'*10,'\n')
RafalK(n,m)

print('\n\n','-'*42,'\n','*'*10,'ika'.center(20),'*'*10,'\n')
ika(n,m)

print('\n\n','-'*42,'\n','*'*10,'Boomer'.center(20),'*'*10,'\n')
Boomer(n,m)

print('\n\n','-'*42,'\n','*'*10,'Czarny'.center(20),'*'*10,'\n')
Czarny(n,m)

print('\n\n','-'*42,'\n','*'*10,'Bartek'.center(20),'*'*10,'\n')
Bartek(n,m)

print('\n\n','-'*42,'\n','*'*10,'Artur_Babinskicrown'.center(20),'*'*10,'\n')
Artur_Babinskicrown1(n,m)
Artur_Babinskicrown2(n,m)

print('\n\n','-'*42,'\n','*'*10,'herodisiac'.center(20),'*'*10,'\n')
herodisiac(n,m)
