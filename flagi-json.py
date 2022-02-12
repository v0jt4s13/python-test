import json

def read_json(filename='test_test_file.json'):
	liczcz = 0
	with open(filename,'r+') as file:
		liczcz+= 1
		# First we load existing data into a dict.
		#print(file)
		file_data = file.read()
		#print(type(file_data))
		file_data_json = file_data.replace("'", "\"")
		file_data = json.loads(file_data_json)
		#print(type(file_data))
		#print(file_data['ListaDomen'])
		print(file_data['ListaDomen'][0]['domena'])
		print(file_data['ListaDomen'][0]['data'][0]['description'])

		print()
		print()
		print('****** data z pliku ponizej ********')
		print('****** file_data ********')
		#print(file_data)
		print()
		print()
				
	file.close()

data = read_json()






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
