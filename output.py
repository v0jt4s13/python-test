import datetime

import time
import logging
import logging.handlers

def log_setup():
    log_handler = logging.handlers.WatchedFileHandler('output.log')
    formatter = logging.Formatter(
        '%(asctime)s program_name [%(process)d]: %(message)s',
        '%b %d %H:%M:%S')
    formatter.converter = time.gmtime  # if you want UTC time
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)

log_setup()
logging.info('Hello, World!')
import os
#os.rename('my.log', 'my.log-old')
logging.info('Hello, New World!')


log_file = open("output.log", 'a+')
ctime = time.ctime()
print("Plik:%s >> mode:%s >> tell:%s" %(log_file.name,str(log_file.mode),log_file.tell()))
licz = 0
while licz <= 5:
	licz+= 1
	line_to_write = "===>"+str(licz)+"<=== "+str(datetime.datetime.now())
	logging.info(line_to_write)
	time.sleep(0.5)

log_file.close()

