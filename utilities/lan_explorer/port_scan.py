#!/usr/bin/env python
import socket
import subprocess
import sys
import os
from datetime import datetime
import logging
import requests
from getmac import get_mac_address as gma

def clear_screen():
	# Clear the screen
	subprocess.call('clear', shell=True)

#print(socket.gethostbyname('localhost'))

def port_scanner(ip):
	#logging.info("Scanned port for IP:", ip)
	#print("Scanned port for IP:", ip)
	#print("-" * 60)
 	# Check what time the scan started
	t1 = datetime.now()
	# Using the range function to specify ports (here it will scans all ports between 1 and 1024)
	# We also put in some error handling for catching errors
	open_ports_list = []
	try:
		#for port in range(1,65535):
		for port in range(1,535): #1535
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			socket.setdefaulttimeout(1)
			result = sock.connect_ex((ip, port))
			if result == 0:
				open_ports_list.append(port)
				#print("Port {}: 	 Open".format(port))
			sock.close()

	except KeyboardInterrupt:
		print("\n\t You pressed Ctrl+C")
		sys.exit()

	except socket.gaierror:
		#logging.info('Hostname could not be resolved. Exiting')
		sys.exit()

	except socket.error:
		#logging.info("Couldn't connect to server")
		sys.exit()

	# Checking the end time
	t2 = datetime.now()

	# Calculates the difference of time, to see how long it took to run the script
	total =  t2 - t1

	# Printing the information to screen
	#logging.info('Scanning Completed.\nOpened ports:', open_ports_list,'\nScanning time:',total,'\n\n')

	return [ip,open_ports_list,total]

def get_mac(ip_addr):
	
	cmd = 'cat /proc/net/arp'
	arp_output = subprocess.getoutput(cmd)
	arp_list = arp_output.splitlines()
	#ipmac_dict_list = [[[r.strip() for r in l.split('  ') if r][0],[r.strip() for r in l.split('  ') if r][3]] for idx,l in enumerate(arp_list) if idx > 0]
	ipmac_dict_list = []
	#print(arp_list)
	local_mac = gma()
	for idx,l in enumerate(arp_list):
		r_list = [r.strip() for r in l.split(' ') if r]
		if idx > 0:
			ipmac_dict_list.append([r_list[0],r_list[3]])

	if ip_addr == 0 or len(ipmac_dict_list) == 0:
		return local_mac
	else:
		mac_from_ip = dict(ipmac_dict_list).get(ip_addr)
		if mac_from_ip == None:
			return local_mac
		else:
			return mac_from_ip

#print(get_mac(0))

def get_mac_details(mac_address):
	# We will use an API to get the vendor details
	url = "https://api.macvendors.com/"
	# Use get method to fetch details
	print('url+mac_address:',url,mac_address)
	response = requests.get(url+mac_address)
	if response.status_code != 200:
		return ''
		#raise Exception("[!] Invalid MAC Address!")
	return response.content.decode()

def check_mac():
	mac_address = '00:11:22:33:44:55'
	print("[+] Checking Details...")
	try:
		vendor_name = get_mac_details(mac_address)
		print("[+] Device vendor is "+vendor_name)
	except:
		# Incase something goes wrong
		print("[!] An error occured. Check "
			"your Internet connection.")
		

###########################################################################
## ponizsza funkcja pobiera argument przy wywolaniu pliku z argumentem   
## np. python nazwapliku.py -m jakisArgument
###########################################################################
def get_arguments():
		# This will give user a neat CLI
		parser = argparse.ArgumentParser()
		# We need the MAC address
		parser.add_argument("-m", "--macaddress",
												dest="mac_address",
												help="MAC Address of the device. "
												)
		options = parser.parse_args()
		# Check if address was given
		if options.mac_address:
				return options.mac_address
		else:
				parser.error("[!] Invalid Syntax. "
										 "Use --help for more details.")
	
