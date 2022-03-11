from flask import Flask, render_template, url_for
from flask import request
from py_terminal_app_run import runAppInsideScript

app=Flask(__name__)

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


if __name__=="__main__":
    app.run()
