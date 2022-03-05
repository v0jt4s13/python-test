import json
import os

def flagiIloscTopDomenPl(domeny_ext_list="",domeny_full_json=""):
	#print(domeny_full_json[0]['domena'])
	pl_ext_count = 0
	top_lvl_domain = ['.agro.pl','.aid.pl','.atm.pl','.augustow.pl','.auto.pl','.babia-gora.pl','.bedzin.pl','.beskidy.pl','.bialowieza.pl','.bialystok.pl','.bielawa.pl','.bieszczady.pl','.biz.pl','.boleslawiec.pl','.bydgoszcz.pl','.bytom.pl','.cieszyn.pl','.com.pl','.czeladz.pl','.czest.pl','.dlugoleka.pl','.edu.pl','.elblag.pl','.elk.pl','.glogow.pl','.gmina.pl','.gniezno.pl','.gorlice.pl','.grajewo.pl','.gsm.pl','.ilawa.pl','.info.pl','.jaworzno.pl','.jelenia-gora.pl','.jgora.pl','.kalisz.pl','.karpacz.pl','.kartuzy.pl','.kaszuby.pl','.katowice.pl','.kazimierz-dolny.pl','.kepno.pl','.ketrzyn.pl','.klodzko.pl','.kobierzyce.pl','.kolobrzeg.pl','.konin.pl','.konskowola.pl','.kutno.pl','.lapy.pl','.lebork.pl','.legnica.pl','.lezajsk.pl','.limanowa.pl','.lomza.pl','.lowicz.pl','.lubin.pl','.lukow.pl','.mail.pl','.malbork.pl','.malopolska.pl','.mazowsze.pl','.mazury.pl','.media.pl','.miasta.pl','.mielec.pl','.mielno.pl','.mil.pl','.mragowo.pl','.naklo.pl','.net.pl','.nieruchomosci.pl','.nom.pl','.nowaruda.pl','.nysa.pl','.olawa.pl','.olecko.pl','.olkusz.pl','.olsztyn.pl','.opoczno.pl','.opole.pl','.org.pl','.ostroda.pl','.ostroleka.pl','.ostrowiec.pl','.ostrowwlkp.pl','.pc.pl','.pila.pl','.pisz.pl','.podhale.pl','.podlasie.pl','.polkowice.pl','.pomorskie.pl','.pomorze.pl','.powiat.pl','.priv.pl','.prochowice.pl','.pruszkow.pl','.przeworsk.pl','.pulawy.pl','.radom.pl','.rawa-maz.pl','.realestate.pl','.rel.pl','.rybnik.pl','.rzeszow.pl','.sanok.pl','.sejny.pl','.sex.pl','.shop.pl','.sklep.pl','.skoczow.pl','.slask.pl','.slupsk.pl','.sos.pl','.sosnowiec.pl','.stalowa-wola.pl','.starachowice.pl','.stargard.pl','.suwalki.pl','.swidnica.pl','.swiebodzin.pl','.swinoujscie.pl','.szczecin.pl','.szczytno.pl','.szkola.pl','.targi.pl','.tarnobrzeg.pl','.tgory.pl','.tm.pl','.tourism.pl','.travel.pl','.turek.pl','.turystyka.pl','.tychy.pl','.ustka.pl','.walbrzych.pl','.warmia.pl','.warszawa.pl','.waw.pl','.wegrow.pl','.wielun.pl','.wlocl.pl','.wloclawek.pl','.wodzislaw.pl','.wolomin.pl','.wroclaw.pl','.zachpomor.pl','.zagan.pl','.zarow.pl','.zgora.pl','.zgorzelec.pl']
	qq = []
	if len(domeny_ext_list) > 0:
		for ext in domeny_ext_list:
			if ext[0] == "pl":
				pl_ext_count+= 1
	if len(domeny_full_json) > 0:
		licz = 0
		while licz < len(domeny_full_json):
			domena = domeny_full_json[licz]['domena']
			ext_pl = domena.split('.')[-1]
			ext_pl2 = domena.split('.')[-2]
			#if ext_pl == "pl" and len(domena.split('.')) > 2:
				#print(str(len(domena.split('.')))+" ==> "+domena)
			if ext_pl == "pl" and len(domena.split('.')) > 2 and "."+ext_pl2+"."+ext_pl in top_lvl_domain:
				if domena not in qq:
					qq.append(domena)
				pl_ext_count+= 1
			licz+= 1
	#print(qq)
	return [pl_ext_count, qq]


def flagiBuildPageFromJson(filename='test_test_file.json'):
	liczcz = 0
	str_to_html_list = []
	with open(filename,'r+') as file:
		liczcz+= 1
		# First we load existing data into a dict.
		#print(file)
		file_data = file.read()
		#print(type(file_data))
		file_data_json = file_data.replace("'", "\"")
		file_data = json.loads(file_data_json)
		#print(type(file_data))
		licz = 0
		# IloscDomen':759,'Status200':714,'Statusy':[200, 502, 404, 500],'BledneDomeny
		wszystkich_domen = file_data['IloscDomen']
		domeny_ok = file_data['Status200']
		bledne_domeny = wszystkich_domen-domeny_ok

		procent = int(int(bledne_domeny*100)/int(wszystkich_domen))
		procent_str = "Procent nieukończonych projektów: "+str(procent)+"%"
		#print(procent)
		str_to_html_list.append('<p>Wszystkich domen: %s; błędnych domen: %s; %s' %(wszystkich_domen,bledne_domeny,procent_str))

		ilosc_domen_pl = flagiIloscDomenPl("", file_data['ListaDomen'])
		ilosc_znakow = flagiIloscZnakow("",file_data['ListaDomen'])
		str_to_html_list.append('<br/>Wszystkich domen .pl: %s; Ilość znaków \'a\': %s' %(ilosc_domen_pl,ilosc_znakow))
		domeny_pl_list = flagiIloscTopDomenPl("", file_data['ListaDomen'])
		str_to_html_list.append('<br/><span style="background-color: silver">Wszystkich domen .pl - TOP-LVL: %i ===> %s </span>' %(domeny_pl_list[0],' '.join(domeny_pl_list[1])))
  
		min_len,shortest,max_len,longest = flagiDlugoscDomeny("",file_data['ListaDomen'])

		#short_domain_char = 0
		str_to_html_list.append('<br/>Najkrótsza domena (%i znaków): %s<br/>Najdłuższa domena (%i znaków): %s' %(min_len,'; '.join(shortest),max_len,'; '.join(longest)))

		#print(len(file_data['BledneDomeny']))
		#print(file_data['BledneDomeny'][0][1])
		while licz < len(file_data['BledneDomeny']):
			#print(file_data['BledneDomeny'])
			status_code = file_data['BledneDomeny'][licz][0]
			domena = file_data['BledneDomeny'][licz][1]
			str_to_html = "<div><span class=\"domena\">"+domena+"</span><span class=\"status-code\">"+str(status_code)+"</span></div>"
			str_to_html_list.append(str_to_html)
			licz+= 1
		
		licz = 0
		while licz < 0: # len(file_data['ListaDomen']):
			status_code = file_data['ListaDomen'][licz]['data'][0]['status_code']
			domena = file_data['ListaDomen'][licz]['domena']
			extra = file_data['ListaDomen'][licz]['data'][0]['extra']
			#print(domena,status_code,extra)
			str_to_html = "<div><span class=\"domena\">"+domena+"</span><span class=\"status-code\">"+str(status_code)+"</span><span class=\"status-code2\">"+str(extra)+"</span></div>"
			str_to_html_list.append(str_to_html)
			#print(file_data['ListaDomen'][1]['domena'])
			licz+= 1

	file.close()

	return str_to_html_list

def flagiBuildWebpage():
	data_style = "<style>.domena{margin-right:20px;}.status-code{margin-right:20px;}.status-code2{margin-right:20px;}</style>"
	data_head = "<head><html>%s</html><body>" %data_style

	data_footer = "</body></html>"
	data_list = flagiBuildPageFromJson()
	data_str = ''.join(data_list)
	with open('/var/www/flaga/templates/flagi.html','w') as file: 
		file.write(data_head)
		file.write(data_str)
		file.write(data_footer)

	return 'Zapisane, trwa reboot serwera ....'

def flagiIloscDomenPl(domeny_ext_list="",domeny_full_json=""):
	#print(domeny_full_json[0]['domena'])
	pl_ext_count = 0
	if len(domeny_ext_list) > 0:
		for ext in domeny_ext_list:
			if ext[0] == "pl":
				pl_ext_count+= 1
	if len(domeny_full_json) > 0:
		licz = 0
		while licz < len(domeny_full_json):
			domena = domeny_full_json[licz]['domena']
			ext_pl = domena.split('.')[-1]
			#if ext_pl == "pl" and len(domena.split('.')) > 2:
				#print(str(len(domena.split('.')))+" ==> "+domena)
			if ext_pl == "pl":
				pl_ext_count+= 1
			licz+= 1

	return pl_ext_count

def flagiIloscZnakow(domeny_list="",domeny_full_json=""):
	a_char_count = 0
	if len(domeny_list) > 0:
		a_char_count = ' '.join(domeny_list).count('a')
	if len(domeny_full_json) > 0:
		licz = 0
		while licz < len(domeny_full_json):
			a_char_count+= domeny_full_json[licz]['domena'].count('a')
			licz+= 1

	return a_char_count

def flagiDlugoscDomeny(domeny_list="",domeny_full_json=""):
	a_char_count = 0
	
	max_len = 0
	longest = []
	min_len = 0
	shortest = []
	if len(domeny_list) > 0:
		for domain in domeny_list:
			domain = domain.replace('https://','')
			domain_len = len(domain.replace('http://',''))
			if domain_len >= max_len:
				max_len = domain_len
				longest.append(domain)
			if domain_len <= min_len or min_len == 0:
				min_len = domain_len
				shortest.append(domain)

	if len(domeny_full_json) > 0:
		licz = 0
		while licz < len(domeny_full_json):
			domain = domeny_full_json[licz]['domena'].replace('https://','')
			domain = domain.replace('http://','')
			domain_len = len(domain)
			if domain_len >= max_len:
				if len(longest) > 0:
					if domain_len > len(longest[0]):
						longest.clear()
				max_len = domain_len
				longest.append(domain)
			if domain_len <= min_len or min_len == 0:
				if len(shortest) > 0: 
					if domain_len < len(shortest[0]):
						shortest.clear()
				min_len = domain_len
				shortest.append(domain)
			licz+= 1
			#print(domain_len,len(shortest[0]),len(shortest),len(longest[0]),len(longest))

	return (min_len,shortest,max_len,longest)

def rebootFlask():
	os.system('sudo systemctl daemon-reload')
	os.system('sudo systemctl restart nginx')
	os.system('sudo systemctl restart flaga.service')

	return 'Restart serwera zakonczony ....'



if 1 == 2:
	# for reading nested data [0] represents
	# the index value of the list
	print(data['ListaDomen'][0])

	# for printing the key-value pair of
	# nested dictionary for loop can be used
	print("\nPrinting nested dictionary as a key-value pair\n")
	for i in data['people1']:
		print("Name:", i['name'])
		print("Website:", i['website'])
		print("From:", i['from'])
		rrprint()
