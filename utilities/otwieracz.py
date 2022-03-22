#!/usr/bin/python3

#coding=utf
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

def extractEmailsFromFile(text, find_text, method):

	exclude_domains_arr = ["@h1b01.londynek.net", "@h1b03.londynek.net", "@h2b03.londynek.net", "@h1b04.londynek.net", "@h2b04.londynek.net"]
	extract_char_arr = ["to:<", "\":", "\"", "<", ">", ":", ";", "(", ")", "'"]

	emails = []
	emails_obj = {}
	#emails_obj_err = {}

	emails_re_out_arr = []
	emails_out_arr = []

	# arr - tablica pojedynczych stringow
	arr = text.split()

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

def kira_encoding_function():
    """Check encoding and convert to UTF-8, if encoding no UTF-8."""
    for filename in ALL_FILES:

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
#print( " Podaj pelna sciezke dostepu lub nazwe pliku do przeszukania. \n Pozostaw puste aby przeszukac plik: test_str_out.txt " )

try: input = raw_input
except NameError: pass

read_file = input(" Podaj pelna sciezke dostepu lub nazwe pliku do przeszukania. \n Pozostaw puste aby przeszukac plik: test_emails_file ")
print( " Jakiego textu szukasz? " )
find_text = input()

file_name_out = "emails_list.log.json"
file_to_read = '/home/voj/.icedove/chbv6831.default/ImapMail/imap.gmail-3.com/INBOX.sbd/MailDeliveryFail2'
#file_to_read = "test_emails_file"

if ( read_file == "0" ):
	shutil.copy(file_to_read, 'test_emails_file')
elif ( read_file == "1" ):

	coding1 = "utf-8"
	coding2 = "iso-8859-1"
	try:
		f= open(file_to_read, 'r', encoding=coding1)
		content= f.read()
		f.close()
		f= open(file_to_read, 'w', encoding=coding2)
		f.write(content)
		f.close()
		print("done")
		text = open(file_to_read).read()
	except:
		try:
			import pandas as pd
			f=pd.read_csv(file_to_read,encoding='utf-8')
			text = open(f).read()
		except:
			try:
				import codecs
				with codecs.open(file_to_read, 'r', encoding='utf-8',
					errors='ignore') as f:
						text = open(f).read()
			except:
				ALL_FILES = glob.glob(file_to_read)
				kira_encoding_function()

elif ( read_file == "2" ):
	try:
		text = open(file_to_read).read()
	except:
		text = open(file_to_read, encoding='utf-8').read()
else:
	text = open(file_to_read).read()

if ( read_file == "0" ):
	print("=====================================")
	print("    Skopiowany plik: %s  do %s" %(file_to_read, file_to_read))
	print("=====================================")

else:
	print("=====================================")
	print("    Emaile z pliku : %s  " %file_to_read)
	print("    Szukany string : %s  " %find_text)
	print("    Plik na wyjsciu: %s  " %file_name_out)
	print("=====================================")

	text = text.lower()
	#arr = ["<webmaster@londynek.net>", "to:<tommasadams122@i.ua>:"]


	exclude_domains_arr = ["@h1b01.londynek.net", "@h1b03.londynek.net", "@h2b03.londynek.net", "@h1b04.londynek.net", "@h2b04.londynek.net"]

	############ \\_?_// metoda 1 - substr
	startDateTime1 = current_milli_time()
	emails_substr_arr = extractEmailsFromFile(text, find_text, "substr")
	endDateTime1 = current_milli_time()
	print("extractEmailsFromFile - method substr: %s ms." %str(getDifference2(startDateTime1, endDateTime1)))

	############ \\_?_// metoda 2 - replace
	startDateTime2 = current_milli_time()
	emails_replace_arr = extractEmailsFromFile(text, find_text, "replace")
	endDateTime2 = current_milli_time()
	print("extractEmailsFromFile - method replace %s ms." %str(getDifference2(startDateTime2, endDateTime2)))
	#print(arr_diff(list(emails_substr_obj), list(emails_replace_obj)))

	############ \\_?_// metoda 3 - regexp
	startDateTime3 = current_milli_time()
	emails_regex_obj = extractEmailsFromFile(text, find_text, "regex")
	endDateTime3 = current_milli_time()
	print("extractEmailsFromFile - method regex %s ms." %str(getDifference2(startDateTime3, endDateTime3)))

	############ \\_?_// metoda 4 - regexp2
	startDateTime4 = current_milli_time()
	emails_regex2_obj = extractEmailsFromFile(text, find_text, "regex2")
	endDateTime4 = current_milli_time()
	print("extractEmailsFromFile - method regex2 %s ms." %str(getDifference2(startDateTime4, endDateTime4)))

	emails_arr = []


	arr_substr = []
	arr_substr.append({"substr": obj_to_arr(emails_substr_arr,str(getDifference2(startDateTime1, endDateTime1)))})
	arr_substr.append({"replace": obj_to_arr(emails_replace_arr,str(getDifference2(startDateTime2, endDateTime2)))})
	arr_substr.append({"regex": obj_to_arr(emails_regex_obj,str(getDifference2(startDateTime3, endDateTime3)))})
	arr_substr.append({"regex2": obj_to_arr(emails_regex2_obj,str(getDifference2(startDateTime4, endDateTime4)))})
	emails_arr = {"Metoda": arr_substr}
	#"aaaaa" {"asdasd": emails_substr_obj[0]}}
	#print(emails_arr)

	wyjscie = open("emails_list", "w")
	wyjscie.write(json.dumps(emails_arr, sort_keys=True, indent=2))
