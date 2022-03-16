try:
	from moje_biblioteki import convertListToJsonString
except:
	def convertListToJsonString(input_list="",extra_para=""):

		wrap_json_list = ""
		prep_json_str = ""
		prep_json_list = []
		
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

		else:
			json_str_list = []
			yy = 0
			for item in input_list:
				#if yy > 0: break
				#print(yy,'==========')
				#print(item)
				#print(yy,'==========')
		
				if len(item) > 0:
					xx = 0
					
					while xx < len(item):
						json_parent = ""
						json_child = ""
						prep_json_str = ""
						#if xx > 0: prep_json_str+= ', '
						if len(item[xx]) == 1:
							xx+= 1
							continue
						if type(item[xx][1]) == list:
							#print('pass',len(item[xx][1]),item[xx][1])
							zz = 0
							prep_json_str = ""
							tmp_str_pun_list = []
							while zz < len(item[xx][1]):
								key = item[xx][1][zz][0]
								val = item[xx][1][zz][1]

								prep_json_str = {
									key:val
								}
								tmp_str_pun_list.append(prep_json_str)
								zz+= 1
							json_child = prep_json_str
							#print('11==>',tmp_str_pun_list)
							prep_json_list.append(tmp_str_pun_list)
				
						else:
							key = item[xx][0]
							val = item[xx][1]

							prep_json_str = {
								key:val
							}
							prep_json_list.append(prep_json_str)

							#print('22==>',prep_json_str)

						#print('33==>',prep_json_list)
						xx+= 1
					prep_json_list_str = ', '.join(map(str,prep_json_list))
					#print('44==>',prep_json_list_str)
					#json_obj = json.dumps(prep_json_list_str, indent = 4)
					#print('55==>',json.loads(json_obj))
					json_str_list.append(prep_json_list)
				else:
					break

				yy+= 1

				return json_str_list

def getRandomPythonExampleCode():
	import random
	
	example_item_list = pythonCodeExampleList()
	rand_num = random.randrange(len(example_item_list))

	return example_item_list[rand_num]

def showRandomPythonCode(output_type="html"):
	
	if output_type == "html":

		code_list = getRandomPythonExampleCode()
		print(code_list)
  
	else:
		licz = 0
		start = True
		while start:
			if licz > 0:
				if input("Wylosować kolejny przykład (T/N) ? ") not in ("T","t", ""):
					break
			licz+= 1
			print('\t\t\t ******** Losowanie nr: %i *******' %licz)
			
		code_list = getRandomPythonExampleCode()
		

		try:
			method_list = [code_list[0][1],code_list[0][0]]
		except:
			method_list = []
		try:
			name_list = [code_list[1][1],code_list[1][0]]
		except:
			name_list = []
		try:  
			syntax_list = [code_list[2][1],code_list[2][0]]
		except:
			syntax_list = []
		try:
			parameters_list = code_list[3][1]
		except:
			parameters_list = []
		try:
			use_examples_list = code_list[4][1]
		except:
			use_examples_list = []
		try:
			example_return_list = code_list[5]
		except:
			example_return_list = []

		renderRandomPythonCodeConsoleOutput(method_list, name_list, syntax_list, parameters_list, use_examples_list, example_return_list)
		

def renderRandomPythonCodeConsoleOutput(method_list, name_list, syntax_list, parameters_list, use_examples_list, example_return_list):

		if method_list[0] not in ("Others"):
			print('\n\n\n\t'+'*'*6,method_list[0]+':',name_list[0]+'() ****\n')
		else:
			print('\n\n\n\t'+'*'*6,name_list[0]+' ****\n')
		
		if len(syntax_list) > 0:
			print('\t'+syntax_list[1]+': '+syntax_list[0])

		if len(parameters_list) > 0:
			print('')
			#print('\tParameters type is %s and length: %i ' %(type(parameters_list),len(parameters_list)))
			print('\t'+'_ '*30,'\n')
			print('\tParameter\tDescription')
			print('\t'+'_ '*30,'\n')
			xx = 0
			for val in parameters_list:
				if xx > 0: print()
				print('\t'+val[0]+'\t\t'+val[1])
				xx+= 1

		#print('')
		xx = 0
		while xx < len(use_examples_list):
			if xx == 0: print('\t'+'_ '*30,'\n')
			elif xx > 0: print('')
			print('\t| Example description:',use_examples_list[xx][0])
			print('\t'+'_ '*30)
			print('\n\t| ',use_examples_list[xx][1].replace('\n','\n\t|  '))
			print('\t'+'_ '*30)
			if len(example_return_list) > 1:
				try:
					example_return_info_list = example_return_list[1]
				except:
					example_return_info_list = []
				print()
				print('\t'+example_return_info_list[0][0]+':',example_return_info_list[0][1])
				print('\t'+example_return_info_list[1][0]+':',example_return_info_list[1][1])
				example_return_info_list.clear()
			xx+= 1
	
		print('\n\n')
		
def renderRandomPythonCodeWebsiteOutput(method_list, name_list, syntax_list, parameters_list, use_examples_list, example_return_list):

	return method_list, name_list, syntax_list, parameters_list, use_examples_list, example_return_list


"""
def chwilowa():
	output_str = ""
	if method_list[0] not in ("Others"):
		print('\n\n\n\t'+'*'*6,method_list[0]+':',name_list[0]+'() ****\n')
		output_str = '\n\n\n\t'+'*'*6,method_list[0]+':',name_list[0]+'() ****\n'
	else:
		print('\n\n\n\t'+'*'*6,name_list[0]+' ****\n')
		output_str = '\n\n\n\t'+'*'*6,name_list[0]+' ****\n'
	
	if len(syntax_list) > 0:
		print('\t'+syntax_list[1]+': '+syntax_list[0])
		output_str = '\t'+syntax_list[1]+': '+syntax_list[0]

	if len(parameters_list) > 0:
		print('')
		#print('\tParameters type is %s and length: %i ' %(type(parameters_list),len(parameters_list)))
		print('\t'+'_ '*30,'\n')
		print('\tParameter\tDescription')
		print('\t'+'_ '*30,'\n')
		output_str = '\t'+'_ '*30,'\n'
		output_str = '\tParameter\tDescription'
		output_str = '\t'+'_ '*30,'\n'
		xx = 0
		for val in parameters_list:
			if xx > 0: print()
			print('\t'+val[0]+'\t\t'+val[1])
			output_str = '\t'+val[0]+'\t\t'+val[1]
			xx+= 1

	#print('')
	xx = 0
	while xx < len(use_examples_list):
		if xx == 0: print('\t'+'_ '*30,'\n')
		elif xx > 0: print('')
		print('\t| Example description:',use_examples_list[xx][0])
		print('\t'+'_ '*30)
		print('\n\t| ',use_examples_list[xx][1].replace('\n','\n\t|  '))
		print('\t'+'_ '*30)
		output_str = '\t| Example description:',use_examples_list[xx][0]
		output_str = '\n\t| ',use_examples_list[xx][1].replace('\n','\n\t|  '
		if len(example_return_list) > 1:
			try:
				example_return_info_list = example_return_list[1]
			except:
				example_return_info_list = []
			print()
			print('\t'+example_return_info_list[0][0]+':',example_return_info_list[0][1])
			print('\t'+example_return_info_list[1][0]+':',example_return_info_list[1][1])
			output_str = '\t'+example_return_info_list[0][0]+':',example_return_info_list[0][1]
			output_str = '\t'+example_return_info_list[1][0]+':',example_return_info_list[1][1]
			example_return_info_list.clear()
		xx+= 1

		print('\n\n')

	return output_str
	"""
	
def pythonCodeExampleList():

	example_item_list = []

	example_item_list.append([["Type","Metoda"],["Name","String center"],["Syntax","string.center(length, character)"],["ParameterValue",
									 	[
										 ["length","Required. The length of the returned string"],
										 ["character","Optional. The character to fill the missing space on each side. Default is \" \" (space)"]
										]
									],["UseExample",
										[
										 ["Using the char \"+_\" as the padding character:", "text = \"powidła\"\n\nx = text.center(20, \"+_\")"]
										]
									],["Return","String"]])

	example_item_list.append([["Type","Metoda"],["Name","randrange"],["Syntax","random.randrange(start, stop, step)"],["ParameterValue",
									 	[
										 ["start","Optional. An integer specifying at which position to start. Default 0"],
										 ["stop","Required. An integer specifying at which position to end."],
										 ["step","Optional. An integer specifying the incrementation. Default 1"]
										]
									],["UseExample",
										[
										 ["Return a number between 0 and 5", "import random\n\nprint(random.randrange(0, 5))"]
										]
									],["Return"]])
 
	example_item_list.append([["Type","Metoda"],["Name","Sort"],["Syntax","list.sort(reverse=True|False, key=myFunc)"],["ParameterValue",
									 	[
										 ["reverse","Optional. reverse=True will sort the list descending. Default is reverse=False"],
										 ["key","Optional. A function to specify the sorting criteria(s)"]
										]
									],["UseExample",
										[
										 ["Sort the list descending", "numbers_list = [5, 1, 4]\n\nnumbers_list.sort(reverse=True)"]
										]
									],["Return",
									 	[
											["ReturnType","list"],
											["ReturnValue","[1, 4, 5]"]
										]
									]])
	#print('len:',len(example_item_list),example_item_list[-1][0])
	
	example_item_list.append([["Type","Others"],["Name","Change List Items"],["Syntax"],["ParameterValue"],["UseExample",
										[
										 ["Change second item value", "pisaki_list = [\"pióro\", \"oliwa\", \"długopis\", \"ołówek\"]\n\npisaki_list[1] = \"mazak\""],
										 ["Change a Range of Item Values", "pisaki_list = [\"pióro\", \"oliwa\", \"burak\", \"ołówek\"]\n\npisaki_list[1:3] = [\"mazak\",\"długopis\"]"]
										]
									],["Return"]])
 
	convertListToJsonString(example_item_list)

	return example_item_list
