
from threading import Thread, Lock
from time import perf_counter
from sys import stderr
from time import sleep
import socket
import subprocess
import os
import sys
try:
	from app_code.file_explorer.port_scan import port_scanner, clear_screen, get_mac, get_mac_details
except:
  from port_scan import port_scanner, clear_screen, get_mac, get_mac_details
# I changed this from "192.168.1.%i" to "192.168.0.%i"
BASE_IP = "192.168.0.%i"
PORT = 80

class Threader:
	"""
	This is a class that calls a list of functions in a limited number of
	threads. It uses locks to make sure the data is thread safe.
	Usage:
			from time import sleep

			def function(i):
					sleep(2)
					with threader.print_lock:
							print(i)

			threader = Threader(10) # The maximum number of threads = 10
			for i in range(20):
					threader.append(function, i)
			threader.start()
			threader.join()

	This class also provides a lock called: `<Threader>.print_lock`
	"""
	def __init__(self, threads=30):
		self.thread_lock = Lock()
		self.functions_lock = Lock()
		self.functions = []
		self.threads = []
		self.nthreads = threads
		self.running = True
		self.print_lock = Lock()

	def stop(self) -> None:
		# Signal all worker threads to stop
		self.running = False

	def append(self, function, *args) -> None:
		# Add the function to a list of functions to be run
		self.functions.append((function, args))

	def start(self) -> None:
		# Create a limited number of threads
		for i in range(self.nthreads):
			thread = Thread(target=self.worker, daemon=True)
			# We need to pass in `thread` as a parameter so we
			# have to use `<threading.Thread>._args` like this:
			thread._args = (thread, )
			self.threads.append(thread)
			thread.start()

	def join(self) -> None:
		# Joins the threads one by one until all of them are done.
		for thread in self.threads:
			thread.join()

	def worker(self, thread:Thread) -> None:
		# While we are running and there are functions to call:
		while self.running and (len(self.functions) > 0):
			# Get a function
			with self.functions_lock:
				function, args = self.functions.pop(0)
			# Call that function
			function(*args)

		# Remove the thread from the list of threads.
		# This may cause issues if the user calls `<Threader>.join()`
		# But I haven't seen this problem while testing/using it.
		with self.thread_lock:
			self.threads.remove(thread)

def connect(hostname, port):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			result = sock.connect_ex((hostname, port))
			#print('sock result:',result)
		with threader.print_lock:
			if result == 0:
				stderr.write(f"[{perf_counter() - start:.5f}] Found {hostname} {port}\n")

def network_scan(output='web'):
	start = perf_counter()
	# I didn't need a timeout of 1 so I used 0.1
	socket.setdefaulttimeout(0.1)

	threader = Threader(10)
	i = 1
	command = 'nmap -sn '+BASE_IP%i+'/24'
	nmap_return = subprocess.getoutput(command)
	nmap_return_list = nmap_return.split('\n')
	ip_list = [(nmap_return_list[l].split(' '))[-1] for l in range(1,len(nmap_return_list)-1,2)]
	found_ips_info = str(len(ip_list))+'ip respond. Start scanning their ports.'
	scanned_ips_list = []

	try:
		if output != 'web':
			clear_screen()

			t_columns = int(os.get_terminal_size().columns)-3
			t_lines = os.get_terminal_size().lines
			term_size_str = 'Lines:'+str(t_lines)+'\tColumns:'+str(t_columns)+'\n'
			print(term_size_str.center(t_columns))

			print(found_ips_info)

		for i in ip_list:
			if output != 'web':
				print(i, end=' ')
			#scanned_ips_list.append(threader.append(port_scanner, i))
			mac_from_ip = get_mac(i)
			mac_details = get_mac_details(mac_from_ip)
			scanned_ips_list.append([port_scanner(i),mac_from_ip,mac_details])

		if output != 'web':
			print('\nFinish port scanning.\n')
	
	except KeyboardInterrupt:
			print("\n\t You pressed Ctrl+C")
			sys.exit()

	threader.start()
	threader.join()

	if output == 'web':
   
		return scanned_ips_list
   
	else:
   
		t_sie_col = t_columns-4
		t_columns = t_columns-18
		#print('* ' * int(t_sie_col/2))
		#print(len(scanned_ips_list),type(scanned_ips_list))
		t_columns = t_columns-70
		c1 = 10
		c2 = 20+int(t_columns/3)
		c3 = 20+int(t_columns/3)
		c4 = 20+int(t_columns/3)

		print('\n'+'-'*t_sie_col)
		print('ID'.center(c1), end=' | ')
		print('IP'.center(c2), end=' | ')
		print('Mac address'.center(c3), end=' | ')
		print('Executed time'.center(c4), end=' | ')

		print('\n'+'-'*t_sie_col)
		for l in scanned_ips_list:
			
			if len(l[0][1]) > 0: ports_list = str(l[0][1])
			else: ports_list = ''
			executed_time = str(l[0][2])
			ip = str(l[0][0])
			mac_from_ip = l[1]
			mac_details = l[2]
			
			print(str(scanned_ips_list.index(l)+1).center(c1), end=' | ')
			print(ip.center(c2), end=' | ')
			print(mac_from_ip.center(c3), end=' | ')
			print(executed_time.center(c4), end=' | ')
			print('\n'+' '.center(c1), end=' | ')
			print(ports_list.center(c2), end=' | ')
			#print(mac_details.center(c3+c4), end=' | ')
			print(mac_details)
			print(str('-'*t_sie_col))

		print()
		print('* ' * int(t_sie_col/2))
		print()
		print()
		input("Press enter to exit.\n? ")

network_scan('desk')