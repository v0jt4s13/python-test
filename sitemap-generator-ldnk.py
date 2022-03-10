from ast import Expression
from curses.panel import new_panel
from operator import truediv
import urllib.request
import json
import re
import datetime
import time
from datetime import date, timedelta
import sys
import os
# modules dla kolorowania textow
from rich import print
from rich.console import Console
# creating the console object
console = Console(width=100)

import logging
import logging.handlers
import requests
import urllib3
from bs4 import BeautifulSoup

from vslib_url_parse import parseUrlChangeParamValue, putUrlListToFile

domain = "https://londynek.net"
section_list = []
section_list.append(["business","accommodation","jobs","jobseekers","automotive","buysell","personals"])
section_list.append(["wiadomosci"])

def log_setup():
	log_file_name = "output.log"
	log_handler = logging.handlers.WatchedFileHandler('output.log')
	formatter = logging.Formatter(
		'%(asctime)s program [%(process)d]: %(message)s',
		'%b %d %H:%M:%S')
	formatter.converter = time.gmtime  # if you want UTC time
	log_handler.setFormatter(formatter)
	logger = logging.getLogger()
	logger.addHandler(log_handler)
	logger.setLevel(logging.DEBUG)
log_setup()

timeLoad_list = []


def current_milli_time():
	return round(time.time() * 1000)


def getDifference2(then, now = current_milli_time()):
	duration = now - then
	return duration

################################# ``` ```
# funkcja wyszukajUrlWStringu
# wyszukiwanie fragmentu adresu url w dostarczonej tablicy stringow
# if 'http://' in str
#################################

def wyszukajUrlWStringu(str):
	em = re.findall(r"(?:http(?:s?)://)?(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",str)
	if len(em) > 0:
		#print('==================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  em=',em[0])
		return em[0]
	else:
		print('String nie jest poprawnym adresem URI: ',em)
		return ""

#################################
# funkcja webRequest
# odpytanie za pomoca biblioteki requests domeny - oczekiwana odpowiedz 200
# import requests czy import urllib.request - czy nie wystarczy 1  z tych linii ??
#################################

def webRequest(url):

	urllib3.disable_warnings()
	try:
		resp = requests.get(url, verify=False, timeout=10)
		return [resp.status_code, resp.headers]
	except requests.exceptions.HTTPError as e: 
		return [e, "Error"]



def showLogs(n, str):
	if n == 1:
		print(str)



def getWebPage(link):
	#print('\t\tAAAAAAAAAA link=',link)
	website_response = requests.get(link)
	website_tekst = website_response.text
	website_lista_prep = website_tekst.split('\n')
	return website_lista_prep



def urlsList(link,resp_count,base_url,section):

	url_list = ""
	list_left = ""
	list_right = ""
	xx = 0
	all_c = 0
	website_lista_prep = getWebPage(link)
	for tmp_str in website_lista_prep:
		all_c+= 1
		err = 0
		if "js-ellipsis" in tmp_str:
			xx+= 1
			#print('%s======> %s ===> %s' %(xx,str(len(tmp_str.split('ad?ad'))),tmp_str))
			line_list = tmp_str.split('ad?ad')
			ad_id = 0
			if len(line_list) == 1:
				line_list = tmp_str.split('ad?so')
				try:
					list_right = line_list[1].split('"')[0].split('=')[-1]
					ad_id = int(list_right)
				except:
					#list_right = "r-Błąd: "+str(line_list)
					err = 2
			else:
				try:
					list_left = line_list[0].split('/')[-2]
				except:
					#list_left = "l-Błąd: "+str(line_list)
					err = 1
				try:
					list_right = line_list[1].split('"')[0].split('=')[1]
					ad_id = int(list_right)
				except:
					#list_right = "r-Błąd: "+str(line_list)
					err = 2

			#print('AdID: %i\nLewa: %s\nPrawa: %s' %(ad_id,list_left,list_right))
			if ad_id > 0:
				url_build = base_url+section+"/ad?ad_id="+str(ad_id)
				url_list = url_build
				curl_url = "curl -sIS " + url_list
				#print('\t*',all_c,xx,url_list)
#				os.system(curl_url)

			if xx >= resp_count and resp_count > 0:
				break

	print('\n\t* Linkow: %i' %xx)

	return url_list



def parseAdUrlFromAdsList(listing_page_url):


	####################################
	########### nieuzywana #############
	####################################
 
	#print('parseAdUrlFromAdsList(',listing_page_url,')')
	print(len(listing_page_url), listing_page_url)
 
	raise SystemExit

	website_lista_prep = getWebPage(listing_page_url)
	xx = 0
	while xx < 5:
		print(website_lista_prep[xx])
		xx+= 1
	print(type(website_lista_prep))
	soup = BeautifulSoup(' '.join(website_lista_prep), "lxml")
	print(type(soup))
	href = soup.a['href']
	print(href)

	return href
    


def parseListPage(resp_count,url_to_parse,section,website_lista_prep):
	
	#print(website_lista_prep[440:445])
	#print('\t*','* '*5,url_to_parse,' *'*5)
	all_c = 0
	last_page_nr = 1
	start_parse = 0
	url_list = []
	ad_url_list = []
	new_page_fragment_list = []

	for tmp_str in website_lista_prep:
		tmp_str = tmp_str.strip()
		all_c+= 1
		err = 0
		#if all_c > 400 and all_c < 550:
		#	print(all_c,tmp_str)

		if 'section-categories' in tmp_str:
			start_parse = 1
		if 'jd-cf-list' in tmp_str:
			start_parse = 1
			#print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
		if 'jd-pagination' in tmp_str:
			#print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
			line_list1 = tmp_str.split('info-pagination')[1].split('/span')
			#print(all_c,line_list1[0].lstrip('">').rstrip('<'))
			tmp_fist_last_page_count_str = line_list1[0].lstrip('">').rstrip('<')
			tmp_fist_last_page_count_list = tmp_fist_last_page_count_str.split('/')
			last_page_nr = int(tmp_fist_last_page_count_list[1].strip())
			#print('last_page_nr='+str(last_page_nr))
			break
		if start_parse == 1 and "href" in tmp_str:
			new_page_fragment_list.append(tmp_str)
			soup = BeautifulSoup(tmp_str, "lxml")
			href = soup.a['href']

			new_href = ""
			if section in section_list[0] or section in section_list[1]:
				part_href_list = href.split(',')
				if len(part_href_list) >= 2:
					new_href+= domain+part_href_list[-1]
				else:
					print('Co to za url ? ==> ',href)

			if new_href != "" and new_href not in url_list:
				url_list.append(new_href)

			#ad_url_list.append(href)

	#print('111===>',len(url_list),last_page_nr)
	#print(url_list)
	return [url_list, last_page_nr]



def parseAdsListPage_depricated(resp_count,url_to_parse,section,website_lista_prep):
	#print(website_lista_prep[100:150])
	print('\t* ',url_to_parse)
	all_c = 0
	last_page_nr = 1
	start_parse = 0
	tmp_url = ""
	for tmp_str in website_lista_prep:
		tmp_str = tmp_str.strip()
		all_c+= 1
		err = 0

		if 'jd-ul-list' in tmp_str and section == "business":
			start_parse = 1
		if 'jd-content-3-1' in tmp_str and section == "business":
			break
		if start_parse == 1 and "href" in tmp_str:
			line_list1 = tmp_str.split('info-pagination')[1].split('"')
			print('SSSSSSSSSSSSSSSSs')
			tmp_url = tmp_url+line_list1[1]
		if 'canonical' in tmp_str:
			print('\t'+'**** '*14,'\n\t*',tmp_str,'\n\t'+'**** '*14)
		if 'info-pagination' in tmp_str:
			line_list1 = tmp_str.split('info-pagination')[1].split('/span')
			print(all_c,line_list1[0].lstrip('">').rstrip('<'))
			tmp_fist_last_page_count_str = line_list1[0].lstrip('">').rstrip('<')
			tmp_fist_last_page_count_list = tmp_fist_last_page_count_str.split('/')
			last_page_nr = int(tmp_fist_last_page_count_list[1].strip())
			break

	if tmp_url == "":
		print('\n\t* Stron do przetworzenia: %i' %last_page_nr)
		yy = 0
		#last_page_nr = 1
		if yy == 0:
			tmp_url = url_to_parse+"/view-ads?cat=1"
		else:
			tmp_url = url_to_parse+"/view-ads?start="+str(yy)+"&cat=1"
	else:
		tmp_url = tmp_url
	
	print('\t* urlsList('+tmp_url+',',resp_count,','+url_to_parse+')\n\t* last_page_nr:',last_page_nr)

	urlsList(tmp_url,resp_count,url_to_parse,section)
 
	while yy < last_page_nr:
		yy+= 1
		tmp_url = url_to_parse+"/view-ads?start="+str(yy)+"&cat=1"
		urlsList(tmp_url,resp_count,url_to_parse,section)

	print('\t* Przetworzonych stron: %i' %yy)



def urlsPaginationList(url_list,resp_count,section):

	print('\n\n\t\t\tlen url_list:',len(url_list),' ====> url_list:',url_list)
	resp_list = []
	new_url_list = []
	for val in url_list:
		link = val[0]
		if link.split('/')[-1] == "index":
			new_url_list.append(link)
			continue
		section = val[1]
		if section in section_list[1]:
			print('\n\n\t**** **** **** **** **** **** **** **** **** **** **** **** **** ****')
			print('\t1 ',section,'parseListPage(',resp_count,link,'list)')
			print('\t**** **** **** **** **** **** **** **** **** **** **** **** **** ****')

			xx = 1
			last_page_nr = 1
			while xx <= last_page_nr:
				resp_list.clear()
				tmp_url = link
				
				if xx > 1:
					tmp_url = parseUrlChangeParamValue(link,'start',xx)

				website_lista_prep = getWebPage(tmp_url)
				#print(website_lista_prep)
				# wyszukanie na stronie listy ogloszen linkow do ogloszen
				resp_list = parseListPage(resp_count,tmp_url,section,website_lista_prep)

				try:
					tmp_url_list = resp_list[0][0].split(section)
					tmp_url_str1 = tmp_url_list[0]+section+tmp_url_list[-1]
					tmp_url_list = resp_list[0][-1].split(section)
					tmp_url_str2 = tmp_url_list[0]+section+tmp_url_list[-1]
				except:
					tmp_url_str1 = ""
					tmp_url_str2 = ""
					if len(resp_list[0]) == 0:
						print('Brak wynikow ')

				print('\t\t\t',tmp_url,'\n''\t\t\t\t'+'* '*20,'\n\t\t\t\tStrona',xx,'z',resp_list[1],'; Pobranych linków:',len(resp_list[0]))
				print('\t\t\t 1.\t'+tmp_url_str1+'\n\t\t\t'+str(len(resp_list[0]))+'.\t'+tmp_url_str2)
				
				last_page_nr = resp_list[1]
				new_url_list.append(resp_list[0])
				xx+= 1


	#################################################
	########## test test test #######################
	#################################################
				#if xx >= 5: break
				#raise SystemExit
	#################################################
	########## test test test #######################
	#################################################

		if section in section_list[0]:
			print('\n\n\t**** **** **** **** **** **** **** **** **** **** **** **** **** ****')
			print('\t2 ',section,'parseListPage(',resp_count,link,'list)')
			print('\t**** **** **** **** **** **** **** **** **** **** **** **** **** ****')

			xx = 1
			last_page_nr = 1
			while xx <= last_page_nr:
				resp_list.clear()
				tmp_url = link
				
				if xx > 1:
					tmp_url = parseUrlChangeParamValue(link,'start',xx)

				website_lista_prep = getWebPage(tmp_url)
				# wyszukanie na stronie listy ogloszen linkow do ogloszen
				# resp_list =[url_list, last_page_nr]
				#print('111111=========>>>>>>>>>>>>>>parseListPage(',resp_count,tmp_url,section,'website_lista_prep)')
				new_url_list.append(tmp_url)
				resp_list = parseListPage(resp_count,tmp_url,section,website_lista_prep)
				#print('222222=========>>>>>>>>>>>>>>',resp_list)

				#raise SystemExit

				try:
					tmp_url_list = resp_list[0][0].split(section)
					tmp_url_str1 = tmp_url_list[0]+section+tmp_url_list[-1]
					tmp_url_list = resp_list[0][-1].split(section)
					tmp_url_str2 = tmp_url_list[0]+section+tmp_url_list[-1]
				except:
					tmp_url_str1 = ""
					tmp_url_str2 = ""
					if len(resp_list[0]) == 0:
						print('Brak wynikow ')
					#raise SystemExit
				print('\t\t\t',tmp_url,'\n''\t\t\t\t'+'* '*20,'\n\t\t\t\tStrona',xx,'z',resp_list[1],'; Pobranych linków:',len(resp_list[0]))
				print('\t\t\t 1.\t'+tmp_url_str1+'\n\t\t\t'+str(len(resp_list[0]))+'.\t'+tmp_url_str2)
				
				last_page_nr = resp_list[1]
				new_url_list+=resp_list[0]
				xx+= 1
    

	print('\n\n\t\t>>>>>>>>>>> KONIEC urlsPaginationList ',len(new_url_list),'<<<<<<<<<<<< ')
	#print('\n\turlsPaginationList(',url_list,resp_count,base_url,')')

	return new_url_list

#def logPrint(show_logs,ads_section_list[para_p]):
#    if show_log == 1:
#		# ?????????????????????????????????????????
#        print()

def registerSiteMaps(file_name):
	import xml.etree.cElementTree as ET
	import datetime

	root = ET.Element('urlset')
	root.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
	root.attrib['xsi:schemaLocation']="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
	root.attrib['xmlns']="http://www.sitemaps.org/schemas/sitemap/0.9"

	f = open(file_name, 'r')
	urls_list = f.readlines()
 
	for doc in urls_list:
		#print(doc)
		site_root = doc
		dt = datetime.datetime.now().strftime ("%Y-%m-%d")
		doc = ET.SubElement(root, "url")
		if "http" in site_root:
			ET.SubElement(doc, "loc").text = site_root
		else:
			ET.SubElement(doc, "loc").text = "http://pp.marzec.eu/"+site_root
		ET.SubElement(doc, "lastmod").text = dt
		ET.SubElement(doc, "changefreq").text = "daily"
		ET.SubElement(doc, "priority").text = "1.0"

	tree = ET.ElementTree(root)
	tree.write('sitemap.xml', encoding='utf-8', xml_declaration=True)
    

def main(argv):
	console.clear()
 
	if 1 == 2:
		if len(argv) == 3:
			resp_count = int(argv[1])
			if argv[2] in ("j","J","t","T","y","Y"):
				output_type = "json"
			else:
				output_type = ""
		else:
			print('\n\n')
			resp_count = console.input("\t\t\t\t*** Ilość wierszy do przeszukania?\n\t\t\t\t\t (0-max; Enter-30) :smiley: ")
			if resp_count == "":
				resp_count = 30
			elif resp_count != 0:
				#print(resp_count,type(int(resp_count)))
				if type(int(resp_count)) != type(1):
					resp_count = 10

		resp_count = int(resp_count)

	i = int(input("\n\n\n\t\t1. Generuj plik sitemap.xml \n\t\t2. Przygotuj liste url dla sitemap \n\n\t\t\t"))
	if i == 1:
		file_name = input('\n\n\t\tPodaj nazwę pliku z danymi: ')
		registerSiteMaps(file_name)
	elif i == 2:
		resp_count = 30
	
		#while xx >= 10: 
		#	print('\n\t','* '*xx)
		#	xx-= 5
	
		#if argv[1] == "ads":
		ads_section_list = {
			"wydarzenia" : ["index"],
			"ukipedia" : ["index"],
			"newslajt" : ["index"],
			"wiadomosci" : ["index", "start=", ["cat", 39, 40, 42, 45, 46]],
			"czytelnia" : ["index", ["cat", 47, 48, 50, 85]],
			"buysell" : ["start=", "cat=2", "offer"],
			"accommodation" : ["start=", "cat=4"],
			"automotive" : ["start=", "cat=3"],
			"business" : ["start=", "index"],
			"jobs" : ["start="],
			"jobseekers" : ["start="],
			"personals" : ["start="],
		}

		#raise SystemExit
		url_list = []
		base_url = "https://londynek.net/"

		if len(argv) > 1:
			para_p = argv[1]
			if para_p != "all" and para_p != "ads":
				ads_section_list = {
					para_p : ads_section_list[para_p]
				}
		print('\n\n')
		print('---'*30)
		for section in ads_section_list:
			tabs_short = "\t"
			if section == "jobs": tabs = "\t\t"
			elif section == "accommodation": tabs = ""
			else: tabs = "\t"

			tmp_str = ""
			for tmp in ads_section_list[section]:
				tmp_str+= str(type(tmp))+' '

			if ads_section_list[section][0][-1] == "=":
				print('|',section,tabs,len(ads_section_list[section]),tabs_short,ads_section_list[section][0][:-1],type(ads_section_list[section][-1]),'tmp_str=',tmp_str)
			else:
				print('|',section,tabs,len(ads_section_list[section]),tabs_short,ads_section_list[section][0],type(ads_section_list[section][-1]),'tmp_str=',tmp_str)
			try:
				print('|\t\t\t\t\t\t 1. ===> ',len(ads_section_list[section]),''.join(ads_section_list[section][0]),''.join(ads_section_list[section][-1]))
			except:
				print('|\t\t\t\t\t\t 2. ===> ',len(ads_section_list[section]),ads_section_list[section])
			print('---'*30)
			
			#raise SystemExit

		for section in ads_section_list:
			print('Sektor przetwarzany:',section,'==>',' '.join(ads_section_list[section][0]))
			#print('section: '+section+' ==> '+str(len(ads_section_list[section])))
			#print(ads_section_list[section])
			para_count = len(ads_section_list[section])
			url_str = base_url+section+"/"
			xx = 0
			#print('while',len(ads_section_list),ads_section_list[section],ads_section_list,section)
			while xx < len(ads_section_list[section]):
				#print('**************',ads_section_list[section][xx])
				url_str = base_url+section+"/"
				
				if ads_section_list[section][xx][:-1] == "start" and len(ads_section_list[section]) == 1:
					print('tu',len(ads_section_list[section]),ads_section_list[section][xx][:-1])
					url_list.append([url_str+"view-ads?start=1",section])
					xx+= 1
					continue

				#if ads_section_list[section][xx][:-1] == "start" and len(ads_section_list[section]) == 2:
				#	print('tu',len(ads_section_list[section]),ads_section_list[section][xx][:-1])
				#	url_list.append([url_str+"view-ads?start=1",section])
				#	xx+= 1
		
				if ads_section_list[section][xx] in ("index","offer"):
					url_list.append([url_str+ads_section_list[section][xx],section])
					xx+= 1
					continue
				#print('while=',xx,ads_section_list[section][xx],url_str+"index",type(ads_section_list[section][xx]))
				
				if type(ads_section_list[section][xx]) == list:
					#print('lista:',ads_section_list[section][xx][0],section,url_str)
					if ads_section_list[section][xx][0] == "cat" and section in ("wiadomosci", "czytelnia"):
						zz = 1
						while zz < len(ads_section_list[section][xx]):
							url_list.append([url_str+"cat?cat_id="+str(ads_section_list[section][xx][zz])+"&start=1",section])
							zz+= 1
				else:
					#if ads_section_list[section][xx][0] == "start=" and section in ("jobs", "business", "accommodation", "jobseekers", "automotive", "buysell", "personals"):
					#	url_para = "start="
					para_list = ads_section_list[section][xx].split('=')
					para_list2 = ads_section_list[section][1].split('=')
					try:
						#      try para_list==> 2 start index
						tmp_para_list_formated = para_list[0]+'=='+para_list[1]+' %%%%%% '+str(len(para_list))+' '+'^'.join(para_list)
						#print('\t\t\t\t***%%%%*** '+section+' try para_list==>',tmp_para_list_formated,'==>'+ads_section_list[section][xx]+'***%%%%***',xx,ads_section_list[section][0],ads_section_list[section][1])

						print('\n\n\n\t\t\t',para_list,'\t\t\tif "',para_list[0],'" == "start" and "',ads_section_list[section][1],'"\n\n\n')
		
						if para_list[0] == "start" and ads_section_list[section][1] == "index":
							if len(para_list) == 2 and para_list[1] == "":
								#tmp_url = url_str+"?start=1"
								url_list.append([url_str+"view-ads?start=1",section])
								url_str+= "view-ads?start=1"
							elif list(ads_section_list[section])[1] != "index":
								url_str+= "view-ads?start=1"
						if para_list[0] == "start" and para_list2[0] == "cat":
							max_cat_nr = int(para_list2[1])
							cat_nr = 1
							while cat_nr <= max_cat_nr:
								tmp_url = url_str+"view-ads?cat="+str(cat_nr)+"&start=1"
								url_list.append([tmp_url,section])
								cat_nr+= 1
					except:
						print('\t\t\t\t\t\t****** '+section+' except para_list==>',len(para_list),para_list[0],'********')
		
				xx+= 1
				#print(url_str)

		#base_url = "https://627-dev.aws.londynek.net/"+argv[1]
		#link = base_url+'/view-ads'
		#link = 'http://localhost/narzedzia/local/flagi'
		# uruchamiamy nasz program
		startDateTime = current_milli_time()
		timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
		#print('                                 ',timeLoad_list[0][1])
		console.print(timeLoad_list[0][1],"", justify="left")
		console.rule("[bold red]SiteMap builder ...")
		##################################################################
		##################### urlsPaginationList #########################
		##################################################################
		print('\t\t\t ****** go to urlsPaginationList(url_list',resp_count,base_url,') ******')

		#print(url_list)
	
		val_list_new = urlsPaginationList(url_list,resp_count,section)
	
		#print('\n\n\n*****************************************************\n\n\n')
		#print(url_list)
		#print('\n\n\n*****************************************************\n\n\n')
		#print(val_list_new)
		#print('\n\n\n*****************************************************\n\n\n')
		
		val_list = url_list+val_list_new
	
		##################################################################
		##################### urlsPaginationList #########################
		##################################################################
		timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
		#print('                                 ',timeLoad_list[-1][1])
		console.print(timeLoad_list[-1][1],"", justify="right")
		console.rule("[bold red]Koniec ...")
		endDateTime = current_milli_time()
		#wyszukajUrlWStringu
		#print(val_list)

		#################################
		#### to do - save to file
		#################################
		putUrlListToFile(section, val_list)
	
		if 1 == 2:
			xx = 0	
			for v_list in val_list:
				print('v_list['+str(xx)+'] count:',len(v_list[xx]),type(v_list[xx]))
				if xx == 5:
					print(v_list[xx][0],v_list[xx][5],v_list[xx][-1],v_list[xx])
				#print(type(v_list[xx]))
				xx+= 1

		#print(val_list)
		print('\n\t\t\t ********** main() ==> val_list_count='+str(len(val_list)),'*'*10)

	else:
		print('\n\n\n\t\t\tBłednie wybrana opcja.\n\n\n')
  
if __name__ == '__main__':
	main(sys.argv)

