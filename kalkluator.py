# kalkluator

history_list = []
while True:
  r = input("Wpisz równanie (+,-,/,*): ")
  w = ""
  w_str = ""
  if "+" in r:
    w = "+"
    w_str = "dodawania"
  elif "-" in r:
    w = "-"
    w_str = "odejmowania"
  elif "/" in r:
    w = "/"
    w_str = "dzielenia"
  elif "*" in r:
    w = "*"
    w_str = "mnożenia"

  if w == "":
    wynik = 'Błędne równanie'
  else:
    r_list = r.split(w)
    if r_list[0].isnumeric() and r_list[0].isnumeric():
      if w == "+": wynik = int(r_list[0])+int(r_list[1])
      elif w == "-": wynik = int(r_list[0])-int(r_list[1])
      elif w == "/": wynik = int(r_list[0])/int(r_list[1])
      elif w == "*": wynik = int(r_list[0])*int(r_list[1])
    else:
      wynik = wynik = 'Podane wartości nie są cyframi'

  if w_str != "":
    print('Wynik',w_str,'to:', wynik)
  else:
    print('Nie jestem w stanie tego policzyć.')
  
  str_oblicz = str(r)+'='+str(wynik)
  history_list.append(str_oblicz)
  if input("Liczymy dalej? (T/N) ") not in ["t","T",""]:
    break

print('\n\nHistoria obliczeń:')
print('\n'.join(history_list))
