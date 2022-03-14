"""
def flagiIloscTopDomenPl(domeny_ext_list="",domeny_full_json=""):
	- project xD - Top lvl .pl domain list from provided list of domain
def flagiBuildPageFromJson(filename='test_test_file.json'):
	- project xD - some info about provided list of domain from json file
def flagiBuildWebpage():
	- project xD - build and save page with list of domain
def flagiIloscDomenPl(domeny_ext_list="",domeny_full_json=""):
	- project xD - simply .pl domain count
def flagiIloscZnakow(domeny_list="",domeny_full_json=""):
	- project xD - count 'a' characters in all provided domains 
def flagiDlugoscDomeny(domeny_list="",domeny_full_json=""):
	- project xD - count longest and shortest domains
def rebootFlask():
	- project xD - flask and nginx reload script
def removeDuplicatesFromMixedList(val_list):
	- remove duplicates from flatten mixed list
def drawTriangles():
	- just draw a triangle for fun ;)
def saveJsonStringToFile(file_name,json_str):
	- save provided json string to .json file
def convertListToJsonString():
	- convert list to json string and save it to .json file
"""

import json
import os
from sre_compile import isstring
from xxlimited import new

def flagiIloscTopDomenPl(domeny_ext_list="",domeny_full_json=""):
	#print(domeny_full_json[0]['domena'])
	pl_ext_count = 0
	top_lvl_domain = ['.agro.pl','.aid.pl','.atm.pl','.augustow.pl','.auto.pl','.babia-gora.pl','.bedzin.pl','.beskidy.pl','.bialowieza.pl','.bialystok.pl','.bielawa.pl','.bieszczady.pl','.biz.pl','.boleslawiec.pl','.bydgoszcz.pl','.bytom.pl','.cieszyn.pl','.com.pl','.czeladz.pl','.czest.pl','.dlugoleka.pl','.edu.pl','.elblag.pl','.elk.pl','.glogow.pl','.gmina.pl','.gniezno.pl','.gorlice.pl','.grajewo.pl','.gsm.pl','.ilawa.pl','.info.pl','.jaworzno.pl','.jelenia-gora.pl','.jgora.pl','.kalisz.pl','.karpacz.pl','.kartuzy.pl','.kaszuby.pl','.katowice.pl','.kazimierz-dolny.pl','.kepno.pl','.ketrzyn.pl','.klodzko.pl','.kobierzyce.pl','.kolobrzeg.pl','.konin.pl','.konskowola.pl','.kutno.pl','.lapy.pl','.lebork.pl','.legnica.pl','.lezajsk.pl','.limanowa.pl','.lomza.pl','.lowicz.pl','.lubin.pl','.lukow.pl','.mail.pl','.malbork.pl','.malopolska.pl','.mazowsze.pl','.mazury.pl','.media.pl','.miasta.pl','.mielec.pl','.mielno.pl','.mil.pl','.mragowo.pl','.naklo.pl','.net.pl','.nieruchomosci.pl','.nom.pl','.nowaruda.pl','.nysa.pl','.olawa.pl','.olecko.pl','.olkusz.pl','.olsztyn.pl','.opoczno.pl','.opole.pl','.org.pl','.ostroda.pl','.ostroleka.pl','.ostrowiec.pl','.ostrowwlkp.pl','.pc.pl','.pila.pl','.pisz.pl','.podhale.pl','.podlasie.pl','.polkowice.pl','.pomorskie.pl','.pomorze.pl','.powiat.pl','.priv.pl','.prochowice.pl','.pruszkow.pl','.przeworsk.pl','.pulawy.pl','.radom.pl','.rawa-maz.pl','.realestate.pl','.rel.pl','.rybnik.pl','.rzeszow.pl','.sanok.pl','.sejny.pl','.sex.pl','.shop.pl','.sklep.pl','.skoczow.pl','.slask.pl','.slupsk.pl','.sos.pl','.sosnowiec.pl','.stalowa-wola.pl','.starachowice.pl','.stargard.pl','.suwalki.pl','.swidnica.pl','.swiebodzin.pl','.swinoujscie.pl','.szczecin.pl','.szczytno.pl','.szkola.pl','.targi.pl','.tarnobrzeg.pl','.tgory.pl','.tm.pl','.tourism.pl','.travel.pl','.turek.pl','.turystyka.pl','.tychy.pl','.ustka.pl','.walbrzych.pl','.warmia.pl','.warszawa.pl','.waw.pl','.wegrow.pl','.wielun.pl','.wlocl.pl','.wloclawek.pl','.wodzislaw.pl','.wolomin.pl','.wroclaw.pl','.zachpomor.pl','.zagan.pl','.zarow.pl','.zgora.pl','.zgorzelec.pl']
	top_lvl_domain_list = []
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
				if domena not in top_lvl_domain_list:
					top_lvl_domain_list.append(domena)
				pl_ext_count+= 1
			licz+= 1
	#print(qq)
	return [pl_ext_count, top_lvl_domain_list]

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
		procent_str = "Projektów niedostępnych: <span>"+str(procent)+"%</span>"
		#print(procent)
		str_to_html_list.append('<div class="line1-wrap"><div class="line1">Wszystkich domen: %s</div><div class="line1">Błędnych domen: %s</div>' %(wszystkich_domen,bledne_domeny))

		ilosc_domen_pl = flagiIloscDomenPl("", file_data['ListaDomen'])
		ilosc_znakow = flagiIloscZnakow("",file_data['ListaDomen'])
		str_to_html_list.append('<div class="line1">Wszystkich domen .pl: %s</div><div class="line1">Ilość znaków \'a\': %s</div>' %(ilosc_domen_pl,ilosc_znakow))
		min_len,shortest,max_len,longest = flagiDlugoscDomeny("",file_data['ListaDomen'])
		str_to_html_list.append('<div class="line1">Najkrótsza domena (%i znaków): %s</div><div class="line1">Najdłuższa domena (%i znaków): %s</div></div>' %(min_len,'; '.join(shortest),max_len,'; '.join(longest)))

		str_to_html_list.append('<div class="line-procent center">%s</div>' %procent_str)
		domeny_pl_list = flagiIloscTopDomenPl("", file_data['ListaDomen'])
		domeny_top_lvl_str = ""
		for url_item in domeny_pl_list[1]:
			domeny_top_lvl_str = domeny_top_lvl_str+'<div class="display-inline-block padding-10"><a href="'+url_item+'" target="_blank">'+url_item+'</a></div>'
   
		#str_to_html_list.append('<div class="padding-10"><span style="background-color:#1e1acf;padding:15px;">Wszystkich domen .pl - TOP-LVL: %i </div><div id="top-lvl-list padding-10"> %s </div>' %(domeny_pl_list[0],domeny_top_lvl_str))

		wall_of_weeping_str = '<span style="background-color:#1e1acf;padding:15px;">-</span><span style="background-color:#1e1acf;padding:15px;">a wall of weeping</span>'
		str_to_html_list.append('<div class="padding-10 center" style="font-size:xx-large;"><span class="bledne-domeny-title">Błędne domeny</span>'+wall_of_weeping_str+'</div>')

		#file_data['Statusy']
		new_status_list = []
		new_status_list_count = []
		for resp_code in file_data['ListaDomen']:
			#print(str(resp_code['data'][0]['status_code']))
			status_code = resp_code['data'][0]['status_code']
			#if status_code == None:	status_code = 999
			new_status_list.append(str(status_code))
		
		tmp_str = ""
		continue_loop = True
		#print('Lista in',new_status_list)
		new_status_list.sort()
		#print('Lista sort',new_status_list)
		while continue_loop:
			if len(new_status_list) > 0:
				el = new_status_list[0]
				c = new_status_list.count(el)
				if tmp_str != "":
					tmp_str+= "; "
				#tmp_str+= str(c)+' domeny z błędem: '+str(el)
				tmp_str+= 'Status: '+str(el)+' ==> '+str(c)+' domen'
				new_status_list_count.append(tmp_str)
				while new_status_list.count(el) > 0:
					new_status_list.remove(el)
			else:
				continue_loop = False

		str_to_html_list.append('<div class="padding-10 center"><span class="bledne-domeny-short">'+tmp_str+'</span></div>')
		#print(new_status_list_count)
    
		str_to_html_list.append('<div class="display-inline-block padding-10">')
		while licz < len(file_data['BledneDomeny']):
			status_code = file_data['BledneDomeny'][licz][0]
			domena = file_data['BledneDomeny'][licz][1]
			str_to_html = '<div class="padding-10 float-left"><span class="domena"><a href="'+domena+'" target="_blank">'+domena+'</a></span><span class="status-code">'+str(status_code)+'</span></div>'
			str_to_html_list.append(str_to_html)
			licz+= 1

		str_to_html_list.append('</div><div class="display-inline-block padding-10">')
		licz = 0
		while licz < 0: # len(file_data['ListaDomen']):
			status_code = file_data['ListaDomen'][licz]['data'][0]['status_code']
			domena = file_data['ListaDomen'][licz]['domena']
			extra = file_data['ListaDomen'][licz]['data'][0]['extra']
			#print(domena,status_code,extra)
			str_to_html = '<div class="padding-10 float-left"><span class="domena">'+domena+'</span><span class="status-code">'+str(status_code)+'</span><span class="status-code2">'+str(extra)+'</span></div>'
			str_to_html_list.append(str_to_html)
			#print(file_data['ListaDomen'][1]['domena'])
			licz+= 1
		str_to_html_list.append('</div>')

	file.close()

	return str_to_html_list

def flagiBuildWebpage(filename="test_file.json"):
	data_style = "<style>\n\t\tbody{background-color:#111;color:#eee;}\n\t\t.domena{margin-right:20px;}\n\t\t.status-code{margin-right:20px;}"
	data_style = data_style+"\n\t\t.line1{float:left;padding:10px;}\n\t\t.status-code2{margin-right:20px;}\n\t\t.center{text-align:center}"
	data_style = data_style+"\n\t\t.line1-wrap{display: inline-block;}\n\t\t.line-procent{padding: 10px;}"
	data_style = data_style+"\n\t\t.line-procent span{font-size: xx-large;text-align:center}\n\t\t.display-inline-block{display:inline-block}"
	data_style = data_style+"\n\t\t.padding-10{padding:10;line-height:2.5}\n\t\t.float-left{float:left}\n\t\ta{color:aliceblue;}"
	data_style = data_style+"\n\t\t.bledne-domeny-title{background-color:#1e1acf;padding:15px;font-size:xx-large;width:100vw;text-align:center;}"
	data_style = data_style+"\n\t\t.bledne-domeny-short{background-color:#1e1acf;padding:10px;font-size:large;width:100vw;text-align:center;}</style>"
	data_head = "<html>\n\t<head>\n\t\t%s\n\t</head>\n\t<body>\n\t\t" %data_style

	data_footer = "\n\t</body>\n</html>"
	data_list = flagiBuildPageFromJson(filename)
	data_str = '\n\t\t'.join(data_list)
	try:
		with open('/var/www/flaga/templates/flagi.html','w') as file: 
			file.write(data_head)
			file.write(data_str)
			file.write(data_footer)
	except:
		with open('flagi.html','w') as file: 
			file.write(data_head)
			file.write(data_str)
			file.write(data_footer)
   
	return 'Zapisane, trwa reboot serwera ....'

def flagiIloscDomenPl(domeny_ext_list="",domeny_full_json=""):

	pl_ext_count = 0
	if len(domeny_ext_list) > 0:
		for ext in domeny_ext_list:
			if ext[0] == "pl":
				pl_ext_count+= 1
	if len(domeny_full_json) > 0:
		licz = 0
		while licz < len(domeny_full_json):
			#print(domeny_full_json[licz])
			#print(domeny_full_json[licz]['data'][0]['status_code'])
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

def removeDuplicatesFromMixedList(val_list):
	data_list = []
	xx = 0
	max = int(len(val_list))
	#print(xx,max)
	while xx < max:
		if type(val_list[xx]) == list:
			if int(len(val_list[xx])) == 6:
				#print('lista 1:',val_list[xx])
				for v in val_list[xx]:
					data_list.append(v)
			else:
				#print('\t',type(val_list[xx]),len(val_list[xx]))
				for v in val_list[xx]:
					data_list.append(v)
		else:
			#print('string 1:',type(val_list[xx]),len(val_list[xx]))
			data_list.append(val_list[xx])

		xx+= 1

	len_before = len(data_list)
	deduplicated_list = list(set(data_list))
	#print('\n\n\t\t\t\t*** removeDuplicatesFromList ==>before:',len_before,' after:',len(deduplicated_list))
	
	return deduplicated_list

def drawTriangles():
	#print('resp_count==>',resp_count,' type=',type(resp_count))
	xx = 1
	zz = 1
	yy = 1
	row_max = 1
	str_draw = ""
	str_new_line = "\n\t\t"
	str_star = " *"
	max_row_col = 12
	while xx <= max_row_col:
		str_draw+= str_new_line #+str(xx) #+" ==> "
		while zz <= row_max:
			str_draw+= " * " #+str(zz) #str_star
			zz+= 1

		yy_max = max_row_col-row_max-1
		while yy <= yy_max:
			str_draw+= " " #+str(yy_max) #"  "
			yy+= 1

		zz = 1
		while zz <= row_max:
			str_draw+= " * " #+str(zz) #+str(zz) #str_star
			zz+= 1
		#if xx > 1: str_draw+= " ==> "+str(max_row_col)+'/'+str(xx)+"="+str(int(max_row_col/xx))
	
		xx+= 1
		zz = 1
		yy = xx
		if xx <= 6: row_max+= 1
		else: 
			row_max-= 1
			zz = 1
			yy = max_row_col-xx
	 
		#str_draw+= str(yy)
	
	return '\n\n'+str_draw+'\n\n'

def saveJsonStringToFile(file_name,json_str):
	try:
		# Serializing json 
		print('Save json',file_name,json_str)
		json_obj = json.dumps(json_str, indent = 4)
		with open(file_name, "w") as outfile:
			outfile.write(json_obj)
		outfile.close()

		return True
	except ValueError as e:	
		return "Error: "+e	

def convertListToJsonString(input_list="",extra_para=""):
	
	if input_list == "":
		input_list = ["Value1", "Value2", "Value3"]
	append_new_list = []
	for item in input_list:
		more_details_list = ["More details1", "More details2", "More details3"] #extended_list_function(item)
		if extra_para == "test":
			append_new_list.append({'Len':len(more_details_list),'Detail1':more_details_list[0],'DetailLast':more_details_list[-1]})
		else:
			append_new_list.append({'Detail1':more_details_list[0],'Detail2':more_details_list[1],'DetailLast':more_details_list[-1]})
	
	wrap_json_list = {'MainName':append_new_list}
	return wrap_json_list