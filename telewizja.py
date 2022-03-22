Telewizja = []
Telewizja.append(['nazwa', 'film1', 'start', 9, 'end', 12])
Telewizja.append(['nazwa', 'film2', 'start', 15, 'end', 17])
Telewizja.append(['nazwa', 'film3', 'start', 11, 'end', 16])
Telewizja.append(['nazwa', 'film4', 'start', 12, 'end', 14])
Telewizja.append(['nazwa', 'film5', 'start', 11.5, 'end', 12.5])
# Telewizja = [{'nazwa': 'film1', 'start': 9, 'end': 12},
#              {'nazwa': 'film2', 'start': 15, 'end': 17},
#              {'nazwa': 'film3', 'start': 11, 'end': 16},
#              {'nazwa': 'film4', 'start': 12, 'end': 14},
#              {'nazwa': 'film5', 'start': 11.5, 'end': 12.5}]            

def Convert(lst):
    print('Convert START=',len(lst))
    res_dct_lst = []
    for wew_list in lst:
      lst_to_dict = {wew_list[i]: wew_list[i + 1] for i in range(0, len(wew_list), 2)}
      res_dct_lst.append(lst_to_dict)
    print('Convert End=',res_dct_lst)
    res_dct = res_dct_lst
    return res_dct
  
def in_rangeA(a,b,c):
    if int(a['start'])*10 not in range(int(b['start'])*10,int(b['end'])*10) and int(a['end'])*10 not in range(int(b['start'])*10,int(b['end'])*10):
        c.append(a)
        print(c)
    return c
def in_rangeB(nr,a,b,TV): #Funkcja która usuwa z TV nakładające sie programy na najkrotszy z nich(a - film który sprawdzamy, najkrotszy program, lista z której usuwamy)
    # print(f'funkcja in_rangeB ==>',a,b,TV)
    #W funkcji sprawdzam czy poczatek lub koniec sprawdzanego programu zawiera sie w przedziale (poczatek najkrotszego programu i koniec najkrotszego programu)
    #Oraz czy poczatek lub koniec najkrotszego programu zawiera sie w przedziale (poczatek sprawdzanego programu,koniec sprawdzanego programu)
    #Pomnozone *10 żeby uniknąć floatów.
    if a['start']*10 in range(int(b['start']*10),int(b['end']*10)) \
      or a['end']*10 in range(int(b['start']*10),int(b['end']*10)) \
      or int(b['start']*10) in range(int(a['start']*10),int(a['end']*10)) \
      or int(b['end']*10) in range(int(a['start']*10),int(a['end']*10)):
        print(f' ---------- usuwanie {a} ----------- ',len(TV))
        print('.remove('+str(type(a))+')')
        #TV.pop(nr)
        TV.remove(a)
        zwieksz_licznik = 0
    else:
        zwieksz_licznik = 1
        
    return TV, zwieksz_licznik

def alg_A(TV):
    max = TV[0]
    watch = []
    for film in TV:
        if film['end'] - film['start'] == max['end'] - max['start']:
            if film['end'] < max['end']:
                max = film
        if film['end'] - film['start'] > int(max['end'] - max['start']):
            max = film
    print(max)
    for film in TV:
        in_rangeA(film,max,watch)
    return watch

def alg_B(TV):
    
    min = TV[0]
    print('alg_b=',TV,'\nmin=',min)
    watch = []
    for film in TV: #Tutaj jest wybór najkrótszego programu, jest wszystko git
        # print('for film in TV',film)
        # print('if ',film['end'],' - ',film['start'],' == ',min['end'],' - ',min['start'])
        if film['end'] - film['start'] == min['end'] - min['start']:
            # print('if ',film['end'],' < ',min['end'])
            if film['end'] < min['end']:
                min = film
        if (film['end'] - film['start'])*10 < (min['end'] - min['start'])*10:
            min = film
        # print('min=',min)
        
    # print('TV.remove(min)=',min)
    TV.remove(min)
    # print('------------------')
    # print(f'TV=',TV) # Program telewizyjny bez najkrotszego programu
    # print('-------ilosc kanalow: ',len(TV),'-----\n0=',TV[0],'\n1=',TV[1],'------\n\n')
    #for nr, filmm in enumerate(TV): #Iteruje po liście programów bez najkrótszego
    xx = 0
    licznik = 0
    max = len(TV)
    while True:
        print(f' ------ =============== {xx} iteracja ================ ------- ')
        print(f'\t\tTV====>{TV}\n\t\tfilm==>{TV[licznik]}')
        watch_lst = in_rangeB(xx,TV[licznik],min,TV)
        #watch = in_rangeB(nr,filmm,min,TV) #Film z listy programów bez najkrotszego programu,najkrotszy program, Program telewizyjny bez najkrotszego programu
        watch = watch_lst[0]
        licznik = licznik+watch_lst[1]
        xx+= 1
        if xx >= max: break

    watch.append(min) #Dodaje min do listy programów
    print('\n\n Koniec watch: ',watch)
    print(min)
    
    return watch #Zwraca liste programów które mozna obejrzec.



#print(alg_B(Telewizja))
print(alg_B(Convert(Telewizja)))