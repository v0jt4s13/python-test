from moje_biblioteki import convertListToJsonString

def getRandomPythonExampleCode():
	import random
	
	rand_num = random.randrange(len(example_item_list))
	example_item_list = pythonCodeExampleList()

	return example_item_list[rand_num]

def showRandomPythonCode(output_type="html"):
	
	licz = 0
	start = True
	while start:
		if output_type == "console":
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


		renderRandomPythonCodeConsoleOutput(method_list, name_list, syntax_list, parameters_list, use_examples_list)
		

def renderRandomPythonCodeConsoleOutput(method_list, name_list, syntax_list, parameters_list, use_examples_list):

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
			if len(code_list[5]) > 1:
				try:
					example_return_info_list = code_list[5][1]
				except:
					example_return_info_list = []
				print()
				print('\t'+example_return_info_list[0][0]+':',example_return_info_list[0][1])
				print('\t'+example_return_info_list[1][0]+':',example_return_info_list[1][1])
				example_return_info_list.clear()
			xx+= 1
	
		print('\n\n')
		
def renderRandomPythonCodeWebsiteOutput(method_list, name_list, syntax_list, parameters_list, use_examples_list):

	return method_list, name_list, syntax_list, parameters_list, use_examples_list


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
		if len(code_list[5]) > 1:
			try:
				example_return_info_list = code_list[5][1]
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
