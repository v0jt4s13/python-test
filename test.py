import requests
import urllib3

url_list = ["http://pp.marzec.eu","http://pythonprogrowanie.pl"]
urllib3.disable_warnings()

for url in url_list:
    try:
        resp = requests.get(url, verify=False, timeout=10)
        try:
            #r.raise_for_status()
            print('\n\n\n\n\n')
            print('     respHTTP:',resp.status_code)
            print('     headers :',resp.headers)
            print('\n\n\n\n\n\n')
        except ValueError:
            print("Error 0")
    except requests.exceptions.HTTPError as e: 
        try:
            print("Error 1")
        except ValueError:
            print("Error 2")
    except:
        print("Error 3",url)
        pass