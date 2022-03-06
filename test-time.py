import time

def current_milli_time():
	return round(time.time() * 1000)

t1 = current_milli_time()


# kod ###############

t = current_milli_time()-t1
print(t)