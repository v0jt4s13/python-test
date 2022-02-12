import json
import os
def read_json(filename='test_test_file.json'):
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
		while licz < len(file_data['ListaDomen']):
			status_code = file_data['ListaDomen'][licz]['data'][0]['status_code']
			domena = file_data['ListaDomen'][licz]['domena']
			extra = file_data['ListaDomen'][licz]['data'][0]['extra']
			#print(domena,status_code,extra)
			str_to_html = "<p><span class=\"domena\">"+domena+"</span><span class=\"status-code\">"+str(status_code)+"</span><span class=\"status-code2\">"+str(extra)+"</span></p>"
			str_to_html_list.append(str_to_html)
			#print(file_data['ListaDomen'][1]['domena'])
			licz+= 1

	file.close()

	return str_to_html_list


data_style = "<style>.domena{margin-right:20px;}.status-code{margin-right:20px;}.status-code2{margin-right:20px;}</style>"
data_head = "<head><html>%s</html><body>" %data_style

data_footer = "</body></html>"
data_list = read_json()
data_str = ''.join(data_list)
with open('/var/www/flaga/templates/flagi.html','w') as file: 
		file.write(data_head)
		file.write(data_str)
		file.write(data_footer)

print('Zapisane, trwa reboot serwera .... Encoding: ')
#os.system('')
os.system('sudo systemctl daemon-reload')
os.system('sudo systemctl restart nginx')
os.system('sudo systemctl restart flaga.service')




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
