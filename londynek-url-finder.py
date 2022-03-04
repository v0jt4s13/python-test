from operator import truediv
import urllib.request
import json
import re
import datetime
import time
from datetime import date, timedelta
import sys
# modules dla kolorowania textow
from rich import print
from rich.console import Console
# creating the console object
console = Console(width=120)

import logging
import logging.handlers

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
	import requests
	import urllib3

	urllib3.disable_warnings()
	try:
		resp = requests.get(url, verify=False, timeout=10)
		return [resp.status_code, resp.headers]
	except requests.exceptions.HTTPError as e: 
		return [e, "Error"]

def showLogs(n, str):
	if n == 1:
		print(str)

def urlsList(link,resp_count,base_url):
	import requests
	import json
	import os

	website_response = requests.get(link)
	website_tekst = website_response.text

	website_lista_prep = website_tekst.split('\n')

	url_list = ""
	list_left = ""
	list_right = ""
	xx = 0
	all_c = 0
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
				url_build = base_url+"/ad?ad_id="+str(ad_id)
				url_list = url_build
				curl_url = "curl -sIS " + url_list
				print(url_list)
#				os.system(curl_url)

			if xx >= resp_count and resp_count > 0:
				break

	print('Linkow: %i' %xx)

	return url_list

def urlsPaginationList(link,resp_count,base_url):
	import requests
	import json
	import os

	website_response = requests.get(link)
	website_tekst = website_response.text

	website_lista_prep = website_tekst.split('\n')

	all_c = 0
	for tmp_str in website_lista_prep:
		all_c+= 1
		err = 0
		if 'info-pagination' in tmp_str:
			line_list1 = tmp_str.split('info-pagination')[1].split('/span')
			#print(all_c,line_list1[0].lstrip('">').rstrip('<'))
			tmp_fist_last_page_count_str = line_list1[0].lstrip('">').rstrip('<')
			tmp_fist_last_page_count_list = tmp_fist_last_page_count_str.split('/')
			last_page_nr = int(tmp_fist_last_page_count_list[1].strip())
			break

	print('Stron do przetworzenia: %i' %last_page_nr)
	yy = 0
	#last_page_nr = 1
	tmp_url = base_url+"/view-ads?start="+str(yy)+"&cat=1"
	
	print('urlsList('+tmp_url+',',resp_count,','+base_url+')')
	urlsList(tmp_url,resp_count,base_url)
 
	while yy < last_page_nr:
		yy+= 1
		tmp_url = base_url+"/view-ads?start="+str(yy)+"&cat=1"
		#urlsList(tmp_url,resp_count,base_url)

	print('Przetworzonych stron: %i' %yy)

def main(argv):
	console.clear()
 
	if len(argv) == 3:
		resp_count = int(argv[1])
		if argv[2] in ("j","J","t","T","y","Y"):
			output_type = "json"
		else:
			output_type = ""
	else:
		print('\n\n')
		resp_count = console.input("\t\t\t\t*** Ilość wierszy do przeszukania?\n\t\t\t\t\t (0-max; Enter-10) :smiley: ")
		if resp_count == "":
			resp_count = 10
		elif resp_count != 0:
			#print(resp_count,type(int(resp_count)))
			if type(int(resp_count)) != type(1):
				resp_count = 10

	resp_count = int(resp_count)
	#print('resp_count==>',resp_count,' type=',type(resp_count))
	print('\n')
	if argv[1] == "ads":
		ads_section_list = {
      		"accommodation" : ["cat=1", "start="],
      		"accommodation" : ["cat=2", "start="],
      		"accommodation" : ["cat=3", "start="],
      		"accommodation" : ["cat=4", "start="],
			"jobs" : ["start="],
			"jobseekers" : ["start="],
			"business" : ["index", "start="],
			"automotive" : ["cat=1", "start="],
			"automotive" : ["cat=2", "start="],
			"automotive" : ["cat=3", "start="],
			"buysell" : ["cat=1", "start="],
			"buysell" : ["cat=2", "start="],
			"personals" : ["start="],
		}
  
	base_url = "https://627-dev.aws.londynek.net/"+argv[1]
	link = base_url+'/view-ads'
	#link = 'http://localhost/narzedzia/local/flagi'
	# uruchamiamy nasz program
	startDateTime = current_milli_time()
	timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
	#print('                                 ',timeLoad_list[0][1])
	console.print(timeLoad_list[0][1],"\t\t\t\t", justify="left")
	console.rule("[bold red]Wystartowalim ...")
	##################################################################
	##################### urlsPaginationList #########################
	##################################################################
	print(ads_section_list)
	#val_list = urlsPaginationList(link,resp_count,base_url)

	##################################################################
	##################### urlsPaginationList #########################
	##################################################################
	timeLoad_list.append([time.time_ns(),datetime.datetime.now()])
	#print('                                 ',timeLoad_list[-1][1])
	console.print(timeLoad_list[-1][1],"\t\t\t\t", justify="right")
	console.rule("[bold red]Koniec ...")
	endDateTime = current_milli_time()
	#wyszukajUrlWStringu
	#print(val_list)

if __name__ == '__main__':
	main(sys.argv)
