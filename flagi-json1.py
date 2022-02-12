import json
# Opening JSON file
#with open('test_test_file.json', 'w') as json_file:
#	print(type(json_file))
#data = json.load(json_file)
#print(data)
try:
	#json_file = json.dumps(open("test_test_file.json"))
	#json_file = json.dump("test_test_file.json","r")
	with open("test_test_file.json", "r") as myfile:
    #data=myfile.read()
		print(type(myfile))
		print(myfile)
	print('***************************')
	#print(json_file)
except ValueError as e: 
	print(e)

if 1 == 2:
	# for reading nested data [0] represents
  # the index value of the list
  print(data['ListaDomen'][0])

  # for printing the key-value pair of
  # nested dictionary for loop can be used
  print("\nPrinting nested dictionary as a key-value pair\n")
  for i in data['ListaDomen']:
    print("Domena:", i['domena'])
    print("Data:", i['data'])
    print("ID:", i['data'][0])
    print()