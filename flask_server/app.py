from flask import Flask, render_template, url_for
from flask import request
from py_terminal_app_run import runAppInsideScript
from app_files.moje_biblioteki import mainPageMenuList


app=Flask(__name__)

@app.route('/')
def index():
	text = open('domain.txt').read()
	li_list = mainPageMenuList()
	return render_template("index.html", text=text, li_list=li_list)

@app.route('/doc')
def doc():
	text = open('domain.txt').read()
	return render_template("doc.html", text=text)

@app.route('/kubus_puchatek')
def kubus_puchatek():
	return render_template("kubus_puchatek.html")

@app.route('/flagi')
def flagi():
	return render_template("flagi.html")

@app.route('/flaga-dla-ukrainy')
def flaga_dla_ukrainy():
	return render_template("flaga-dla-ukrainy.html")

@app.route('/pass-generator', methods=['GET','POST'])
def pass_generator():
	from app_files.password_generator import password_generator
		
	pass_rendered = ""
	try:
		if request.method == 'GET':
			cc = int(request.args.get('char_count'))
		elif request.method == 'POST':
			cc = int(request.form['char_count'])
			pass_rendered = password_generator(cc)
		else:
			cc = 0
	except ValueError as e:
		cc = "Error "+request.form['char_count']
	except:
		cc = "Still errors occurs"
	
	return render_template("pass-generator/index.html", pass_rendered=pass_rendered)

@app.route('/app-run', methods=['GET','POST'])
def py_terminal_app_run():
		
	try:
		if request.method == 'GET':
			text = request.args.get('term_text')
		elif request.method == 'POST':
			text = request.form['linia1']
			text_list = text.split('\n')
			text_kolejny = runAppInsideScript(text)
		else:
			text = "NO_GET"
	except ValueError as e:
		text = "Noting to declare "+request.form['linia1']
	except:
		text = "Same błędy w kodzie ... ;/ \n<br>Zaraz wracam i to poprawie ..."

	return render_template("app-run/index.html", text_list=text_list, text_kolejny=text_kolejny)

@app.route('/py-terminal', methods = ['POST','GET'])
def py_terminal():
	return render_template("py-terminal/index.html")

@app.route('/py-terminal2')
def py_terminal2():
	return render_template("py-terminal2/index.html")

if __name__=="__main__":
	app.run()
