#!/usr/bin/python3

#coding=utf
from asyncore import ExitNow
import glob
import chardet

import io
import os, sys
import re
import json
import time
from sty import fg, bg, ef, rs
import shutil, os

def current_milli_time():
	return round(time.time() * 1000)

def getDifference2(then, now = current_milli_time()):
	duration = now - then
	return duration

'''
Replace a set of multiple sub strings with a new string in main string.
'''
def replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    for elem in toBeReplaces :
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)

    return  mainString

def extractEmailsFromFile(text_list, find_text, method):

	exclude_domains_arr = ["@h1b01.londynek.net", "@h1b03.londynek.net", "@h2b03.londynek.net", "@h1b04.londynek.net", "@h2b04.londynek.net"]
	extract_char_arr = ["to:<", "\":", "\"", "<", ">", ":", ";", "(", ")", "'"]

	emails = []
	emails_obj = {}
	#emails_obj_err = {}

	emails_re_out_arr = []
	emails_out_arr = []

	# arr - tablica pojedynczych stringow
	arr = text_list # text.split()

	licz_all = 0
	licz = 0
	licz_err = 0
	for val in arr:
		licz_all += 1

		skip_value = 1
		find_inline = 0
		if ( val.find(find_text) > 0 ):
			# excluded domain search
			for domain_to_check in exclude_domains_arr:
				skip_value = 0
				find_inline = val.find(domain_to_check)
				#if ( licz_all < 100 ) : print("%s, Szukam: %s w %s.find(%s)" %(licz_all, domain_to_check, domain_to_check, val))
				if ( find_inline > 0 ):
					#if ( licz_all < 100 ) : print("%s, 2 Nie znaleziono: %s w linii: %s" %(licz_all, domain_to_check, val))
					skip_value = 1
					break

			if ( skip_value == 0 ):
				# remove specified char in email from array
				email = val
				email_new = ""
				#if ( licz_all < 100 ) : print("1. Znalazlem email-string: %s " %email)

				email_tmp = email
				if ( method == "substr" ):
					for chara in extract_char_arr:
						pos = email_tmp.find(chara)
						if ( pos == 0 ):
							email_tmp = email_tmp[len(chara):]
							#print("P1. Znak: %s(%s) w miejscu: %s ==> %s ====> %s" %(chara, len(chara), str(pos), email, email_tmp))
						if ( pos > 0 ):
							email_tmp = email_tmp[:pos]
							#print("P2. Znak: %s(%s) w miejscu: %s ==> %s ====> %s" %(chara, len(chara), str(pos), email, email_tmp))
					email_new = email_tmp
					#print("1. Znalazlem email-string: %s " %email_new)
				if ( method == "replace" ):
					email_tmp = email
					for chara in extract_char_arr:
						chara_str = str(chara)
						chara_split = list(chara_str)
						email_tmp = replaceMultiple(email_tmp, chara_split, "")
						#print("replaceMultiple ==> %s, %s ====> %s" %(email, chara_split, email_tmp))
					email_new = email_tmp
					#print("1. Znalazlem email-string: %s " %email_new)
				elif ( method == "regex" ):
					em = re.findall(r"^[\w.-]+@[\w.-]+\.\w+$",email)
					email_new = ''.join(em)
					#emails_re_out_arr.append(em)
				elif ( method == "regex2" ):
					em = re.findall(r"(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]+(?::\d{1,5})?$",email) 
					email_new = ''.join(em)
					#emails_re_out_arr.append(em)

				if email_new in emails_obj:
					licz_err += 1
					#obj_str = {email_new:licz_err}
					#emails_err.append(obj_str)
					#emails_obj_err.update(obj_str)
				elif email_new != "":
					licz += 1
					obj_str = {email_new:licz}
					emails.append(obj_str)
					emails_obj.update(obj_str)

		#if ( licz > 5 ): break

	json_arr = []
	#json_arr = [{"Znalezionych adresow email": licz},{"Odrzucone emaile (duplikaty)": licz_err},{"Lista adresow": emails_obj}]
	tmp_obj_str = licz
	json_arr.append(tmp_obj_str)
	tmp_obj_str = licz_err
	json_arr.append(tmp_obj_str)
	tmp_obj_str = emails_obj
	json_arr.append(tmp_obj_str)

	print("===> %s znalezionych pozycji - duplikatow: %s " %(licz, licz_err))
	return json_arr

	#emails_arr = [{"Metoda: " + method: json_arr}]
	#return emails_arr

def kira_encoding_function(files_list):
    """Check encoding and convert to UTF-8, if encoding no UTF-8."""
    for filename in files_list:

        # Not 100% accuracy:
        # https://stackoverflow.com/a/436299/5951529
        # Check:
        # https://chardet.readthedocs.io/en/latest/usage.html#example-using-the-detect-function
        # https://stackoverflow.com/a/37531241/5951529
        with open(filename, 'rb') as opened_file:
            bytes_file = opened_file.read()
            chardet_data = chardet.detect(bytes_file)
            fileencoding = (chardet_data['encoding'])
            print('fileencoding: ', fileencoding)

            if fileencoding in ['utf-8', 'ascii']:
                print(filename + ' in UTF-8 encoding')
            else:
                # Convert file to UTF-8:
                # https://stackoverflow.com/a/191403/5951529
                with codecs.open(filename, 'r') as file_for_conversion, codecs.open(filename, 'w', 'utf-8') as converted_file:
                    read_file_for_conversion = file_for_conversion.read()
                    converted_file.write(read_file_for_conversion)
                print(filename +
                      ' in ' +
                      fileencoding +
                      ' encoding automatically converted to UTF-8')


def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False

def arr_diff(arr1, arr2):
	arr3 = []
	licz = 0
	for val in arr1:
		if search(arr2, val):
			#print("search(arr2, %s)" %val)
			qq = val
		else:
			#print(val)
			licz += 1
			obj_str = {val:licz}
			arr3.append(obj_str)

	return arr3

def try_read_file(file_to_read):
	coding1 = "utf-8"
	coding2 = "iso-8859-1"
#	try:
	if 1 == 1:
		#f = open(file_to_read, 'r', encoding=coding1).read()
		#f.close()
		line_list = []
		line_list2 = []
		with open(file_to_read, 'rb') as file:
			c = 0
			while True:
				c+= 1
				#try:
				#	line_list.append(file.readline())
				#except:
				output_json = chardet.detect(file.readline())
				line_list2.append(output_json)
				if not file.readline():
					break

		print('c=',c,len(line_list),len(line_list2))
		print(line_list2[0],line_list2[100],line_list2[1000])

		#print("Rozpoznano kodowanie pliku",output_json['encoding'])

		return open(file_to_read, 'r', encoding=output_json['encoding']).read()
	# except:
	# 	try:
	# 		f = open(file_to_read, 'r', encoding=coding1)
	# 		content = f.read()
	# 		f.close()
	# 		new_file = file_to_read+'.'+coding1+'_'+coding2
	# 		f_new = open(file_to_read+'.'+coding1+'_'+coding2, 'w', encoding=coding2)
	# 		f_new.write(content)
	# 		f_new.close()
	# 		print("Pomyślnie skopiowano plik ("+coding1+"=>"+coding2+")")
	# 		print(file_to_read+' do '+new_file)
	# 		return open(new_file).read()
	# 	except:
	# 		try:
	# 			import pandas as pd
	# 			print('Try use pandas to read file')
	# 			f = pd.read_csv(file_to_read,encoding='utf-8')
	# 			return open(f).read()
	# 		except:
	# 			print('Pandas nie wspołpracuje z tym plikiem')
	# 			try:
	# 				import codecs
	# 				with codecs.open(file_to_read, 'r', encoding='utf-8',
	# 					errors='ignore') as f:
	# 						return open(f).read()
	# 			except:
	# 				print('Jesze proba z kira_encoding_function()')
	# 				files_list = [file_to_read]
	# 				return kira_encoding_function(files_list)

	return 0

def search_for_in_list(find_text,text_list,method_name="substr"):

	search_output_list = []
	line = 1
	print('============================',len(text_list))
	#print(text_list[0:50])
	#search_output_list.append(search_method(method_name,text_list,find_text))
	return search_method(method_name,text_list,find_text)
 
	# for text in text_list:
		
   
   
	# 	line+= 1
	# 	if line > 20: break
	# 	text = text.lower()
	# 	search_output_list.append(search_method(method_name,text,find_text))


	#emails_arr = []
	#emails_arr = {"Metoda": search_output_list}

	#print(emails_arr)
	#wyjscie = open("emails_list", "w")
	#wyjscie.write(json.dumps(emails_arr, sort_keys=True, indent=2))
  

def search_method(method_name,text,find_text):
	
	arr_substr = []
	if method_name == "substr":
		############ \\_?_// metoda 1 - substr
		startDateTime1 = current_milli_time()
		emails_substr_arr = extractEmailsFromFile(text, find_text, "substr")
		endDateTime1 = current_milli_time()
		print("extractEmailsFromFile - method substr: %s ms." %str(getDifference2(startDateTime1, endDateTime1)))
		arr_substr.append({"substr": obj_to_arr(emails_substr_arr,str(getDifference2(startDateTime1, endDateTime1)))})


	if method_name == "replace":
		############ \\_?_// metoda 2 - replace
		startDateTime2 = current_milli_time()
		emails_replace_arr = extractEmailsFromFile(text, find_text, "replace")
		endDateTime2 = current_milli_time()
		print("extractEmailsFromFile - method replace %s ms." %str(getDifference2(startDateTime2, endDateTime2)))
		#print(arr_diff(list(emails_substr_obj), list(emails_replace_obj)))
		arr_substr.append({"replace": obj_to_arr(emails_replace_arr,str(getDifference2(startDateTime2, endDateTime2)))})

	if method_name == "regex":
		############ \\_?_// metoda 3 - regex
		startDateTime3 = current_milli_time()
		emails_regex_obj = extractEmailsFromFile(text, find_text, "regex")
		endDateTime3 = current_milli_time()
		print("extractEmailsFromFile - method regex %s ms." %str(getDifference2(startDateTime3, endDateTime3)))
		arr_substr.append({"regex": obj_to_arr(emails_regex_obj,str(getDifference2(startDateTime3, endDateTime3)))})

	if method_name == "regex2":
		############ \\_?_// metoda 4 - regex2
		startDateTime4 = current_milli_time()
		emails_regex2_obj = extractEmailsFromFile(text, find_text, "regex2")
		endDateTime4 = current_milli_time()
		print("extractEmailsFromFile - method regex2 %s ms." %str(getDifference2(startDateTime4, endDateTime4)))
		arr_substr.append({"regex2": obj_to_arr(emails_regex2_obj,str(getDifference2(startDateTime4, endDateTime4)))})

	return arr_substr

	#"aaaaa" {"asdasd": emails_substr_obj[0]}}
	#print(emails_arr)


def obj_to_arr(emails_arr, time):
	licz_arr = 0
	tmp_emails_obj = {}
	tmp_emails_arr = []
	obj_val = {"Czas":time}
	tmp_emails_arr.append(obj_val)
	for val in emails_arr:
		if ( licz_arr == 0 ): obj_val = {"Znalezionych":val}
		if ( licz_arr == 1 ): obj_val = {"Duplikaty":val}
		if ( licz_arr == 2 ): obj_val = {"Emaile":val}
		tmp_emails_obj.update(obj_val)
		tmp_emails_arr.append(obj_val)
		licz_arr += 1
	return tmp_emails_arr

def	remove_char(tmp_email_str):
	tmp_email_str = tmp_email_str.replace('&lt;','').replace('&gt;','').replace('<','').replace('>','').replace(';','')
	tmp_email_str = tmp_email_str.replace('TO:','').replace(':','').replace('(','').replace(')','').replace('"','').replace('/s=','')
	tmp_email_str = tmp_email_str.replace('/td','').replace('/b/a','').replace('style=\'color#212121text-decorationnone\'','')
	tmp_email_str = tmp_email_str.replace('/b/a.','').replace('=','').replace('&quot','')
	tmp_email_str = tmp_email_str.rstrip('.').lstrip('.').rstrip('=').lstrip('=')
 
	excluded_strings_list = ["wmarzec@wp.pl", "webmaster@londynek.net", "customersupport@londynek.net", "=@londynek.net", \
   	"Daemon@londynek.net", "redakcja@londynek.net", "1.londynek.net", "3.londynek.net", "4.londynek.net", "test90@londynek.net", \
  	"@aolserver4-production", "@exim4-fd", "jdubanik@jdblayer.com", "test5@londynek.net", "test8@londynek.net", "test2@londynek.net", \
    "kgraf@londynek.net", "error@londynek.net", "no-reply@londynek.net", "tomersupport@londynek.net", "@mx.google.com"]
	for str in excluded_strings_list:
		if str in tmp_email_str:
			return None
 
	return tmp_email_str

# def extractEmailsFromFile - koniec

#################################################################################################################
#################################################################################################################
#############		NAPOTKANE KOMUNIKATY BLEDOW														                              #############
#################################################################################################################
#############	1. SyntaxError: invalid syntax														                            #############
#############	t=t.append('''   +:-`_____`-.---------------------------.-`_____`-:+''')			        #############
#############					  ^																	                                          #############
#############																						                                            #############
#############	2. SyntaxError: EOL while scanning string literal									                    #############
#############	t=t.append('     / _____ \                             / _____ \')					          #############
#############                                                                    ^					        #############
#############																						                                            #############
#############																						                                            #############
#################################################################################################################
#################################################################################################################

def main(argv):

	t = """      _=====_                               _=====_
			/ _____ \                             / _____ \\
		+:-'_____'-.---------------------------.-'_____'-:+
		/   |     |  '.        S O N Y        .'  |  _  |   \\
	/ ___| /|\ |___ \                     / ___| /_\ |___ \\
	/ |      |      | ;  __           _   ; | _         _ | ;
	| | <---   ---> | | |__|         |_:> | ||_|       (_)| |
	| |___   |   ___| ;SELECT       START ; |___       ___| ;
	|\    | \|/ |    /  _    ___       _   \    | (X) |    /|
	| \   |_____|  .','" "' |___|   ,'" "', '.  |_____|  .' |
	|  '-.______.-' /       \ANALOG/       \  '-._____.-'   |
	|               |       |------|       |                |
	|              /\       /      \       /\               |
	|             /  '.___.'        '.___.'  \              |
	|            /                            \             |
	\          /                              \           /
		\________/                                \_________/
											PS2 CONTROLLER"""


	text = fg(144, 238, 144) + t + fg.rs
	print( text )

	path = "/home/voj/projects/python-xD/python-test/fromgithub/8571150/"
	find_text = "@" #input()
 
	if len(argv) > 1 and argv[1] == "copy":
		file_to_read = '/home/voj/.icedove/chbv6831.default/ImapMail/imap.gmail-3.com/INBOX.sbd/MailDeliveryFail2'
		file_to_read = '/home/voj/projects/python-xD/DeliveryStatusNotification'
		file_to_write = 'test_emails_file.log'

		shutil.copy(file_to_read, file_to_write)
		print("=====================================")
		print("    Skopiowany plik: %s  do %s" %(file_to_read, file_to_write))
		print("=====================================")

		raise SystemExit

	else:
		read_file = input(" Podaj pelna sciezke dostepu lub nazwe pliku do przeszukania. \n Pozostaw puste aby przeszukac scieżkę:\n"+path+" ")

		file_name_out = "emails_list.log.json"
		if read_file == "":
			file_to_read = path
		else:
			file_to_read = read_file

		if file_to_read == path:
			print('Przeszukuje katalog: %s' %file_to_read)
		else:
			print('Przeszukuje plik: %s' %file_to_read)

		startDateTime3 = current_milli_time()
		clear_emails_list = []
		lst = []
		dir_list = os.listdir(path)
		#print(dir_list)
		search_output_list = []
		xx = 0
		for file_to_read in dir_list:
			text_list = []
			#text_list = try_read_file(file)
			if ".log" in file_to_read:
				with open(path+file_to_read, 'r') as file:
					text_list = file.readlines()

			#print(len(text_list))
			text_list_str = ' '.join(text_list)
			lst.append(re.findall('\\S+@\\S+', text_list_str))

			#search_output_list.append(search_for_in_list(find_text,text_list,method_name))
			#print(search_output)

			# print("=====================================")
			# print("    Emaile z pliku : %s  " %file_to_read)
			# print("    Szukany string : %s  " %find_text)
			# print("    Plik na wyjsciu: %s  " %file_name_out)
			# print("=====================================")

			# print(len(text_list))
			# #print(text_list)

			#print('len(lst)=',len(lst[xx]))
			#if len(lst[xx]) < 0 and len(lst[xx]) == len(set(lst[xx])): print('duplikaow nie ma')
			#else: print('duplikaty sa')
			for tmp_email_str in lst[xx]:
				## clear email string
				tmp_email_str = remove_char(tmp_email_str)
				if tmp_email_str is None:
					continue
				# if "gmr@mx.google.com" in tmp_email_str:
				# 	continue
				if "@londynek.net" in tmp_email_str:
					print(tmp_email_str)

				clear_emails_list.append(tmp_email_str.lower())
      
			#print('len(set(lst))=',len(set(lst[xx])))
   
			xx+= 1
			#if len(clear_emails_list) > 2000: break
   
		#print(lst)
	print('emails count:',len(clear_emails_list))
	print('emails count:',len(set(clear_emails_list)))
	clear_emails_list = list(set(clear_emails_list))
	#print(clear_emails_list)
	endDateTime3 = current_milli_time()
 
	#emails_arr = []
	#arr_substr = []
	#arr_substr.append({"substr": obj_to_arr(emails_substr_arr,str(getDifference2(startDateTime1, endDateTime1)))})
	#arr_substr.append({"replace": obj_to_arr(emails_replace_arr,str(getDifference2(startDateTime2, endDateTime2)))})
	#arr_substr.append({"regex": obj_to_arr(clear_emails_list,str(getDifference2(startDateTime3, endDateTime3)))})
	#arr_substr.append({"regex2": obj_to_arr(emails_regex2_obj,str(getDifference2(startDateTime4, endDateTime4)))})
	#emails_arr = {"Metoda": arr_substr}
	#"aaaaa" {"asdasd": emails_substr_obj[0]}}
	#print(emails_arr)
	tmp_emails_arr = []
	tmp_emails_arr.append({"Emaile":clear_emails_list})
	print(tmp_emails_arr)
 
	wyjscie = open("emails_list", "w")
	wyjscie.write(json.dumps(tmp_emails_arr, sort_keys=True, indent=2))

	#print(clear_emails_list)
	#raise SystemExit

if __name__ == "__main__":
    main(sys.argv)
    
    
#mails count: 3645
#emails count: 322    
    
    

    
#'"231387@wp.pl"', 'tommasadams122@i.ua', 'o777maria@hotmail.com', 'wikyor.jendrzejczak10@onet.pl', 'dluzenwieslaw2@gmail.com', 'E1lvkiL-00EfOz-O0@ecbiz289.inmotionhosting.com', 'ross@glenrands.co.uk', 'supremepaintingandecorating@gmail.com', 'bartlomiej250683@wp.pl', 'new_buisnesspartner@yahooo.com', 'eliza.domanska2@wp.pl', 'pablogodlike@gmial.com', 'czarneoczy27@onet.pl', 'noa091970@gmail.COM', 'lucyna1@gagatko.pl', 'kotozerca80@wp.pl', 'steamcleaning@yahoo', 'info@roundwoodestates.co.uk', 'test5@londynek.net', 'ewaczerniak46@gmail.com', '19winona20@gmail.COM', 'AS8PR08MB58785C3435FB399505A5B5B0B82C9@AS8PR08MB5878.eurprd08.prod.outlook.com', 'krzych13@icloud.com', 'postmaster@atl4mhob05.registeredsite.com', 'romekbox24@gmail.co', 'sabina@okconstruction.co.uk', 'E1mab4n-007ZQx-W5@ecbiz289.inmotionhosting.com', '181220@mail.uk', 'dominikalonca@gmail.COM', '"bartlomiej250683@wp.pl"', 'E1mQPrI-002eMy-UY@ecbiz289.inmotionhosting.com', '231387@wp.pl', 'tonydv_5@hotmeil.com', 'crpmloclfszqcbucax@mhzayt.COM', 'aleksandra.ostanowka@hotmail.com', 'tristiantristian12345@gmail.COM', 'beata-kurtys@o2.pl', 'header.i=@danwood1.onmicrosoft.com', 'postmaster@ecbiz158.inmotionhosting.com', 'dawidszymek@yahoo.co.uk', 'maciekmilewski@interia.pl', 'bernadeta.b@mail.com', 'webdevnow@mazur.co.uk', 'xx4@topkobiety.co.uk', 'tristiantristian12345@gmail.com', '20210805230059.C37BDCBE73@smtp.cmp.livemail.co.uk', 'noa091970@gmail.com', 'postmaster@bosmailout08.eigbox.net', 'rfc822k...g@o2.pl', 'miriamglow@hotmail.COM', 'janwaldi@gmail.com', 'joanna.pokoje@interia.pl', 'postmaster@smtp.cmp.livemail.co.uk', 'v0jt3k@gmail.com', 'poaqrhemaxgvtpyvhe@mhzayt.COM', 'k...g@o2.pl', 'rfc822tia@roundwoodestates.co.uk', 'aghpropeties8@gmail.COM', 'E1mOpWy-0007Zv-HM@51-89-246-158.cprapid.com', 'duskrzysztf911ab@gmail.COM', 'E1lUn1B-002NRu-6t@ecbiz158.inmotionhosting.com', '"karolina.info@wp.pl"', 'stabilac3@wp.pl', 'E1mOpWg-0007Zf-1o@51-89-246-158.cprapid.com', 'postmaster@kedantransport.co.uk', 'email_lewandowski@yahoo.com', 'plotajurek@gmail.COM', 'Mailer-Daemon@eigbox.net', '82714486@gmail.com', 'pshunka123@outlook.com', 'E1mab4o-007ZR2-1B@ecbiz289.inmotionhosting.com', '(jdubanik@jdblayer.com', '"maciej@kedantransport.co.uk/td', 'tjgasplumber78@yahoo.co.uk', 'jakubowskam48@qmail.com', 'jtthduk@gmail.com', 'jprf5@btinternet.com', 'aleksandra.ostanowka@hotmail.COM', 'SRS0=nwcw=M4=londynek.net=webmaster@mail-redirect-04.cmp.livemail.co.uk', '82714486@gmail.COM', 'massage91tamara@gmail.COM', 'milena.tomanek1@wp.pl', 'iewtpgkmhdoybbqxkr@mhzayt.COM', 'slawekjga@gimail.COM', 'rfc822paulina.osakowicz@danwood.pl', 'roman.grabowski1@o2.pl', 'luke@gmail.COM', 'tomersupport@londynek.net/td', 'postmaster@eur04-db3-obe.outbound.protection.outlook.com', 'adam@proinstall.uk', 'dariuszskupin@qmail.com', 'slawekjga@gimail.com', 'emmyson@o2.pl', '20210805230059.AD63ECBE84@smtp.cmp.livemail.co.uk', 'stabilac1@wp.pl', 'forever20together@outlook.com', 'piotr45@yahoo.com', 'E1mPC0B-0007Lp-3d@51-89-246-158.cprapid.com', 'adamt@interia.pl', 'mp.builders@live.com', 'rafalbartczak1989@gmail.com', 'SRS0=blxK=M5=londynek.net=webmaster@mail-redirect-01.cmp.livemail.co.uk', 'massage91tamara@gmail.com', 'E1m5ODU-00Axg7-T2@ecbiz289.inmotionhosting.com', 'mariuszmankowski1976@gimail.COM', 'robertmclean1@yahoo.com', 'info@barnet-motors.com', 'Mailer-Daemon@ecbiz158.inmotionhosting.com', 'nuna.huczko111@outlook.com', 'niunio1970@wp.pl', 'aghpropeties8@gmail.com', 'rfc822gr.backup.mail@gmail.com', 'swiatjeansu99@gmail.com.pl', 'SRS0=blxK=M5=londynek.net=webmaster@mail-redirect-02.cmp.livemail.co.uk', 'lukaplo20@gamil.com', '"maciej@kedantransport.co.uk/sp=', 'verastyle.strews@gmail.com', 'arkadiuszlewszynski@gmail.COM', 'E1lowKa-0003ag-08@bosmailscan02.eigbox.net', 'admlondon85@hotmail.com', 'emilia97@hotmail.co.uk', 'admin@bapassioncars.com', 'employaagent.uk@gmail.com', 'perfectwindowslondon@gmail.COM', 'laslondon@interia.pl', 'postmaster@danwood1.onmicrosoft.com', 'test2@londynek.net', 'rfc822nelly@roundwoodestates.co.uk', 'rob22@onet.eu', 'magda@topmedicalclinic.co.uk', 'suzukidrz@interia.pl', 'romeospraca@wp.pl', 'jprf5@btinternet.COM', 'iewtpgkmhdoybbqxkr@mhzayt.com', 'b0778f47-8b7a-41a9-ac77-57bea971cce8@AM6PR10MB3031.EURPRD10.PROD.OUTLOOK.COM', 'rfc822www.sales@goodchoicejoinery.co.uk', 'MAILER-DAEMON@auth-smtp-proxy-01.cmp.livemail.co.uk', 'pazmenss@gmail.COM', 'anna1@ltctraining.co.uk', 'header.i=@eigbox.net', 'fajnaona2@interia.pl', 'E1mkb2s-005Qwt-80@ecbiz289.inmotionhosting.com', 'iwona.porrbska1977@gmail.com', 'adam@taksowki.ilawa.pl', 'contact@apornclip.com', 'SRS0=nwcw=M4=londynek.net=webmaster@mail-redirect-03.cmp.livemail.co.uk', 'eowoo@wp.pl', 'anna27@topkobiety.co.uk', 'E1n5BpK-000Itr-0I@www50.jnb2.host-h.net', 'www.m.amoss@yahoo.com', 'anna@anne4ka.int.pl', 'grabonpawe6l@gmail.COM', 'andrzejpabianice@interia.pl', 'root\\@localhost', 'wojtek@marzec.eu', 'v0jt3k@gmail.COM', 'postmaster@ecbiz289.inmotionhosting.com', 'rfc822info@sparklecleaning.biz', '"romeospraca@wp.pl"', 'g27414486@gmail.com', 'E1n5CTe-000DlQ-HL@www50.jnb2.host-h.net', 'brown.eyelets@intera.pl', '"milena.tomanek1@wp.pl"', 'tp.nav@outlook.com', 'dalkowsko@gmail.com', 'jpszuba@wp.pl', 'dalkowsko@gmail.COM', 'verastyle.strews@gmail.COM', 'kamilkrzystof1996@gmail.com', 'thebjmiller@hotmail.com', 'rfc822magda@topmedicalclinic.co.uk', 'malekuu@o2.pl', 'victor.dyduch@outlook.com', 'they_are_comming@yahoo.com', '"kotozerca80@wp.pl"', 'admin@aahomesandhosuing.com', 'plotajurek@gmail.com', 'justynagrzybek1@wp.pl', 'izunia666@hotmail.COM', 'swider.maciek@gmail.COM', 'MAILER-DAEMON@auth-smtp-proxy-04.cmp.livemail.co.uk', 'supremepaintingandecorating@gmail.COM', 'E1lg7Pr-0000pN-Sx@bosmailscan02.eigbox.net', 'sabina@okconstrcution.co.uk', 'MAILER-DAEMON@mail.hostingplatform.com', 'gr.backup.mail@gmail.com', 'error@londynek.net', 'steve.morren@lockmetal.com', 'rafalbartczak1989@gmail.COM', 'MAILER-DAEMON@auth-smtp-proxy-02.cmp.livemail.co.uk', 'poaqrhemaxgvtpyvhe@mhzayt.com', 'prodecopainter@hotmail.COM', 'lunazbozowska@yahoo.co.uk', 'majcherczak@hotmail.COM', 'info@windowsgroup.co.uk', 'karolina.info@wp.pl', 'pshunka123@outlook.COM', 'przemyslawmateusiak1906@yahoo.com', 'sadcmltd@gmail.COM', 'w.mlynski@musialgroup.pl', 'no-reply@londynek.net', 'kamilkrzystof1996@gmail.COM', 'prodecopainter@hotmail.com', 'aga.w@hotmail.co.uk', 'postmaster@bosmailout06.eigbox.net', 'istokrotka30@gmail.com', 'ostryczosnek123@gmail.COM', 'iwona.porrbska1977@gmail.COM', 'lombard@lombard.uk.com', 'info@eeconstruction.co.uk', '202106241501.15OF1a0Q014853@atl4mhob05.registeredsite.com', '19winona20@gmail.com', 'lula711@wp.pl', 'postmaster@eur02-ve1-obe.outbound.protection.outlook.com', 'aldysmyks@gmail.com', 'miriamglow@hotmail.com', 'piotr23391@wp.pl', 'recurrent.recuritmentuk@yahoo.co.uk', 'italiaviva12@interia.pl', '"eowoo@wp.pl"', 'Mailer-Daemon@51-89-246-158.cprapid.com', 'pomocuk@mail.com', 'E1liMnR-0005lC-Kf@bosmailscan04.eigbox.net', 'bounce@ipage.com', 'maciej@kedantransport.co.uk', 'ewaczerniak46@gmail.COM', 'rafaldrozd444@gamil.com', 'postmaster@bosmailout03.eigbox.net', 'crpmloclfszqcbucax@mhzayt.com', '"paulina.osakowicz@danwood.pl/td', 'postmaster@www50.jnb2.host-h.net', 'info@sparklecleaning.biz', 'info@bfurnishedlondon.com', 'gastom@live.co.uk', 'victor.dyduch@outlook.COM', 'info@cleanerski.com', 'rfc822maciej@kedantransport.co.uk', 'postmaster@mail.topmedicalclinic.co.uk', 'kwas517@wp.pl', 'morzechowski@vantastaffing.co.uk', '"eliza.domanska2@wp.pl"', 'thebjmiller@hotmail.COM', 'Mailer-Daemon@www50.jnb2.host-h.net', 'jksbest2001@interia.eu', 'contact@pbbuilder.net', 'cleanerski@gmail.com', 'praca.lon@yahoo.com', 'info@greyoak.co.uk', 'office@lonodn-joinery.com', 'mielec21@interia.pl', 'sadcmltd@gmail.com', 'f.renata@interia.uk', 'justynaserdakowska123@gmail.combrBody', 'test8@londynek.net', '"roman.grabowski1@o2.pl"', 'employaagent.uk@gmail.COM', 'mp.builders@live.COM', 'greco1@op.pl', 'E1lxGMm-003d2g-9W@ecbiz289.inmotionhosting.com', 'tia@roundwoodestates.co.uk', 'dluzenwieslaw2@gmail.COM', 'hilda2020321@gmail.co.uk', 'kassinska@wp.pl', 'terry@bownbuilds.com', '(kgraf@londynek.net', '20210806230058.81493C5A25@smtp.cmp.livemail.co.uk', 'nelly@roundwoodestates.co.uk', 'duskrzysztf911ab@gmail.com', 'jarecki2110@op.pl', 'ks@uk2.net', 'taterecruitment38@outlook.com', 'header.i=@kedantransport.onmicrosoft.com', '20210806230058.570D8C5A25@smtp.cmp.livemail.co.uk', 'dominikalonca@gmail.com', 'ar2work@yahoo.co.uk', 'dystkretny86wwa@gmail.com', 'pitradamberkowicz@gmail.com', 'emilmartyniuk@g.mail.com', 'windsor9@wp.pl', 'info_sparklecleaningbiz_if@pop.ipage.com', 'thomasinio71@wp.pl'}