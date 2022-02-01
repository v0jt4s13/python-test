import requests

link = 'http://zajecia-programowania-xd.pl/flagi'
flagi = requests.get(link)
print(flagi.text.encode('utf-8'))

lista = [1,2,3,4]
for i in lista:
	print(i)
