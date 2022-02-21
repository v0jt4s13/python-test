import os
from rich import print
from rich.console import Console
# creating the console object
console = Console(width=120)

def main():
	console.clear()

	print('\n\n')
	file_name = console.input("\t\t\t\t*** Podaj nazwe pliku html?\n\t\t\t\t*** ")
	templates_path = "/var/www/flaga/templates/"
	file_path = templates_path+""+file_name+".html"

	html_str = "<html>\n\t<head>\n\t\t<style>\n\n\t\t</style>\n\t</head>\n\t<body>"+file_name+".html {text}\n\n\t</body>\n</html>"

	with open(file_path, 'w') as file:
		file.write(html_str)
	file.close()
	print('Zapisane, trwa reboot serwera .... ')
	#os.system('')
	os.system('sudo chown ubuntu.www-data '+file_path)
	os.system('sudo systemctl daemon-reload')
	os.system('sudo systemctl restart nginx')
	os.system('sudo systemctl restart flaga.service')

	print(os.system('ls -la '+templates_path))
	print(os.system('nano '+file_path))


if __name__ == '__main__':
	main()
