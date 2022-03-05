

rodzin_list = [["Wojtek","Marzec",["Maja","Julia"]],
               ["Ania","Marzec",["Maja","Julia"]],
               ["Michał","Kowalski",[]],
               ["Andrju","Nowak",["Kamil"]],
               ]
command_list = []
command = {
	"imie" : None,
	"nazwisko" : None,
	"imiona_dzieci" : []
}

for tmp_list in rodzin_list:

	existing_commands = [c['nazwisko'] for c in command_list]

	if command['nazwisko'] in existing_commands:
		print('jest')
	else:
		print('nie ma, dodaje')
		command['imie'] = tmp_list[0]
		command['nazwisko'] = tmp_list[1]
		command['imiona_dzieci'].append(tmp_list[2])
  