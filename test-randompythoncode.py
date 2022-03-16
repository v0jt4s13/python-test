try:
  from flask_server.app_files.random_python_code import getRandomPythonExampleCode
except:
  from app_files.random_python_code import getRandomPythonExampleCode
  
# [['Type', 'Metoda'], ['Name', 'Sort'], ['Syntax', 'list.sort(reverse=True|False, key=myFunc)'], 
#   ['ParameterValue', [
#     ['reverse', 'Optional. reverse=True will sort the list descending. Default is reverse=False'], 
#     ['key', 'Optional. A function to specify the sorting criteria(s)']
#   ]], 
#   ['UseExample', [
#     ['Sort the list descending', 'numbers = [5, 1, 4]\n\nnumbers.sort(reverse=True)']
#   ]], 
#   ['Return', [
#     ['ReturnType', 'list'], 
#     ['ReturnValue', '[1, 4, 5]']
#   ]]
# ]

#showRandomPythonCode()

if 1 == 1:
  
  getRandomPythonExampleCode()

else:
  
  licz = 0
  start = True
  while start:
    if licz > 0:
      if input("Wylosować kolejny przykład (T/N) ? ") not in ("T","t", ""):
        break

    licz+= 1
    show_code_list = getRandomPythonExampleCode()
    #print(show_code_list[0][0])
    print('\t\t\t ******** Losowanie nr: %i *******' %licz)

    try:
      method_list = [show_code_list[0][1],show_code_list[0][0]]
    except:
      method_list = []
    try:
      name_list = [show_code_list[1][1],show_code_list[1][0]]
    except:
      name_list = []
    try:  
      syntax_list = [show_code_list[2][1],show_code_list[2][0]]
    except:
      syntax_list = []
    try:
      parameters_list = show_code_list[3][1]
    except:
      parameters_list = []
    try:
      use_examples_list = show_code_list[4][1]
    except:
      use_examples_list = []

    #print(name_list)
    #print(method_list)
    #print(syntax_list)
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

      if len(show_code_list[5]) > 1:
        try:
          example_return_info_list = show_code_list[5][1]
        except:
          example_return_info_list = []
        print()
        print('\t'+example_return_info_list[0][0]+':',example_return_info_list[0][1])
        print('\t'+example_return_info_list[1][0]+':',example_return_info_list[1][1])
        example_return_info_list.clear()
      xx+= 1
  
    print('\n\n')
    

