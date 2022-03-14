import threading
import time
import datetime

def timeNow(format=""):
  from datetime import datetime
  if format == "":
    now = datetime.now()
    return now.strftime("%M:%S")
  else:
    #datetime(1987, 12, 30, 17, 50, 14)
    return datetime.now()

def activeThreadingCheck(count=1,main_time_start=timeNow('ddn')):
  while threading.activeCount() > count:
    main_time_finish = timeNow('ddn')
    c = main_time_finish-main_time_start
  return c

qq_list = []
def test(url):
  start_time = timeNow()
  time.sleep(url[0])
  end_time = timeNow()
  qq_list.append([start_time, end_time, url[1], url[0]])
  print('\t'*6,end_time,'test('+url[1]+')')


#########################################################
#########################################################
#########################################################

import logging
import logging.handlers
from flask_server.app_files.moje_biblioteki import *

def log_setup():
  log_file_name = "output.log"
  log_handler = logging.handlers.WatchedFileHandler('output.log')
  formatter = logging.Formatter(
      '%(asctime)s program [%(process)d]: %(message)s',
      '%b %d %H:%M:%S')
  formatter.converter = time.gmtime  # if you want UTC time
  log_handler.setFormatter(formatter)
  logger = logging.getLogger()
  logger.addHandler(log_handler)
  logger.setLevel(logging.DEBUG)
log_setup()

def webRequest(url):
  import requests
  import urllib3

  urllib3.disable_warnings()
  try:
    resp = requests.get(url, verify=False, timeout=10)
    return [resp.status_code, url]
  except requests.exceptions.HTTPError as e: 
    return [e, "Error"]

def webRequestOK(url):
  import requests
  import urllib3
  logging.info('========= START2 ========== '+str(url[0]))
  urllib3.disable_warnings()
  try:
    resp = requests.get(url)
    if resp.ok:
      return [200,url]
    else:
      return webRequest(url)
  except requests.exceptions.InvalidSchema as e:
    return [e, "Error 1x11"]
  except requests.exceptions.HTTPError as e: 
    return [e, "Error 2x11"]

########################################################
########################################################
########################################################

  
def flagsList():  
  url_list1 = [[4, "http://test-4.pl"], [5, "http://test-5.pl"], [3, "http://test-3.pl"]]
  url_list2 = [[2, "http://test-2.pl"], [5, "http://test-5.pl"], [3, "http://test-3.pl"]]
  url_list = url_list1+url_list2

  main_time_start = timeNow('ddn')
  threads_response_list = list()
  for url in url_list:
    print(threading.activeCount(),"=====>>> create and start thread %s." %url)
    if threading.activeCount() >= 3:
      print(threading.activeCount(),"=====>>> too much thread %s." %url)
      while threading.activeCount() > 3:
        pass
    
    t1 = threading.Thread(target=webRequestOK, args=(url,))
    
    threads_response_list.append(t1)
    t1.start()

  print("\n\n\tThreads count:%i\n" %len(threads_response_list))


  for qq in qq_list:
    print('aa',qq)

  c = activeThreadingCheck(1,main_time_start)

  print('\tMethod 2 -> Koniec th count: %i ==> %s sec \n\n' %(threading.activeCount(),c))
  print('\n\n\t\t','*'*47,'\n\t\t * We are the champion my friend\'s ... hehe ;) *\n\t\t','*'*47)
  #print('\t\t\t',main_time_finish-main_time_start)
  #print('\t',main_time_start,main_time_finish,getDifference(main_time_finish,main_time_start,'sec'))

flagsList()
