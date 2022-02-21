import requests
import os
import sys

link = 'https://zajecia-programowania-xd.pl/kubus_puchatek'
kubus_raw = requests.get(link)
kubus_text = kubus_raw.text #.encode('utf-8'))

kubus_linie_b = kubus_text.split('</p>')

# Czyszczenie.
kubus_linie = []
for l in kubus_linie_b:
    l = l.strip()
    kubus_linie.append(l)

# Czyszczenie: alternatywa 🙂
kubus_linie = [l.strip() for l in kubus_text.split('</p>')]

start = 1000
end = 1100
str_out = 'Działa jak natura chciała ;) '
tajemniczy_bohater = 'Cyber Przemo'
bohater_2 = 'dot MS'
bohater_3 = 'Sylwia W'
new_krzys = 'Wojtek'
new_krzys2 = "Wojtka"
for index, linia in enumerate( kubus_linie):
    if index >= start and index < end:

        linia = linia.replace('Kubuś', tajemniczy_bohater)
        linia = linia.replace('Puchatek', tajemniczy_bohater)
        linia = linia.replace('Królik', bohater_2)
        linia = linia.replace('Prosiaczek', bohater_3)
        linia = linia.replace('Krzyś', new_krzys)
        linia = linia.replace('Krzysia', new_krzys2)
        str_out = str_out+linia+'</p>'

str_out = str_out+'<p>Czytała Krystyna Czubówna</p>'
#print( len( kubus_linie ) ) 
with open('/var/www/flaga/templates/kubus_puchatek.html','w') as file: 
    file.write(str_out)
#file.close()
#f = open("/home/ubuntu/python-test/kubus_puchatek.html", "w")
#f.write(str_out)
#f.close()
print('Zapisane, trwa reboot serwera .... Encoding: ', sys.getfilesystemencoding())
#os.system('')
os.system('sudo systemctl daemon-reload')
os.system('sudo systemctl restart nginx')
os.system('sudo systemctl restart flaga.service')
#os.system('sudo systemctl status flaga.service')
file.close()