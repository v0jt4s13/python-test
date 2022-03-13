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

def getDifference(then, now, interval = "secs"):
    if now == "":
      now = datetime.datetime.now()
    duration = now - then
    duration_in_s = duration.total_seconds() 
    
    #Date and Time constants
    yr_ct = 365 * 24 * 60 * 60 #31536000
    day_ct = 24 * 60 * 60 			#86400
    hour_ct = 60 * 60 					#3600
    minute_ct = 60 
    
    def yrs():
      return divmod(duration_in_s, yr_ct)[0]

    def days():
      return divmod(duration_in_s, day_ct)[0]

    def hrs():
      return divmod(duration_in_s, hour_ct)[0]

    def mins():
      return divmod(duration_in_s, minute_ct)[0]

    def secs(): 
      return duration_in_s

    return {
        'yrs': int(yrs()),
        'days': int(days()),
        'hrs': int(hrs()),
        'mins': int(mins()),
        'secs': int(secs())
    }[interval]
  

qq_list = []
def test(url):
  start_time = timeNow()
  time.sleep(url[0])
  end_time = timeNow()
  qq_list.append([start_time, end_time, url[1], url[0]])
  print('\t'*6,end_time,'test('+url[1]+')')

url_list1 = [[4, "http://test-4.pl"], [5, "http://test-5.pl"], [3, "http://test-3.pl"]]
url_list2 = [[2, "http://test-2.pl"], [5, "http://test-5.pl"], [3, "http://test-3.pl"]]
url_list = url_list1+url_list2

main_time_start = timeNow('ddn')
c = 0
threads = list()
for url in url_list:
  c+= url[0]
  print("Start thread %s." %url)
  t1 = threading.Thread(target=test, args=(url,))
  threads.append(t1)
  t1.start()
  t1.join()

main_time_finish = timeNow('ddn')
print("\n\n\tThreads count:%i\n" %len(threads))
for qq in qq_list:
  print(qq)
print('\tMethod 1 -> Koniec ==> %i sec\n' %c)

#print('\t\t\t',main_time_finish-main_time_start)
#print('\t',main_time_start,main_time_finish,getDifference(main_time_finish,main_time_start,'sec'))

print('\n\n')
qq_list.clear()

main_time_start = timeNow('ddn')
threads = list()
for url in url_list:
  print("=====>>> create and start thread %s." %url)
  t1 = threading.Thread(target=test, args=(url,))
  threads.append(t1)
  t1.start()

print("\n\n\tThreads count:%i\n" %len(threads))

for qq in qq_list:
  print(qq)

main_time_finish = timeNow('ddn')
c = main_time_finish-main_time_start
print('\tMethod 2 -> Koniec ==> %s sec ... nie do konca jest to prawdą :/ \n' %c)

#print('\t\t\t',main_time_finish-main_time_start)
#print('\t',main_time_start,main_time_finish,getDifference(main_time_finish,main_time_start,'sec'))
