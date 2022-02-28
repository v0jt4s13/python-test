import requests
import urllib3


import requests

#enter a wrong url:
url = 'http://pythonprogrowanie.pl'

x = requests.get(url)

print(x.raise_for_status())





url_list = ["http://pp.marzec.eu/kubus_puchatek","http://pythonprogrowanie.pl"]
urllib3.disable_warnings()

for url in url_list:
    try:
        resp = requests.get(url, verify=False, timeout=10)
        err = ""
        resp.raise_for_status()
        print('\n\n')
        print("     Domain:",url)
        print('     respHTTP:',resp.status_code)
        print('     headers :',resp.headers)
        print('     content :',resp.content)
        print('     elapsed :',resp.elapsed)
        #json = resp.json()
        #print('     json :',json)
        print('     ok :',resp.ok)
        print('     reason :',resp.reason)
        print('     request :',resp.request)
        print('     text :',resp.text)
        print('     url :',resp.url)
    except requests.exceptions.HTTPError as e:
        #try:
            print("Error 1:")
        #except ValueError:
        #    print("Error 2")
    except:
        #resp = requests.get(url, verify=False, timeout=10)
        HTTP_code = resp.status_code
        print('\n\n')
        print("     Error 3:",url)
        print('     respHTTP:',HTTP_code)
        print('     headers :',resp.headers)
        print('     content :',resp.content)
        print('     elapsed :',resp.elapsed)
        #json = resp.json()
        #print('     json :',json)
        print('     ok :',resp.ok)
        print('     reason :',resp.reason)
        print('     request :',resp.request)
        print('     text :',resp.text)
        print('     url :',resp.url)
        print('\n\n')
        
