from pickle import NONE
import subprocess
import os

def readJournalctl(line_count,order_by,output_type):
	if order_by == "o":
		execute_line = "journalctl |head -"+str(line_count)
	else:
		execute_line = "journalctl |tail -"+str(line_count)
	#out = os.system(execute_line)

	out_list = subprocess.getoutput(execute_line).split('\n')
	
	"""
  Mar 03 22:56:19 ip-172-31-29-165 sshd[156049]: error: kex_exchange_identification: Connection closed by remote host
	Mar 03 23:05:56 ip-172-31-29-165 sshd[157797]: Invalid user pradeep from 143.244.163.14 port 36702
	Mar 03 23:05:56 ip-172-31-29-165 sshd[157797]: Received disconnect from 143.244.163.14 port 36702:11: Bye Bye [preauth]
	Mar 03 23:05:56 ip-172-31-29-165 sshd[157797]: Disconnected from invalid user pradeep 143.244.163.14 port 36702 [preauth]
	Mar 03 23:06:18 ip-172-31-29-165 sshd[157866]: Received disconnect from 51.161.70.95 port 41064:11: Bye Bye [preauth]
	Mar 03 23:06:18 ip-172-31-29-165 sshd[157866]: Disconnected from authenticating user root 51.161.70.95 port 41064 [preauth]
	Mar 03 23:08:30 ip-172-31-29-165 sshd[158261]: Invalid user oracle from 93.149.180.144 port 56818
	Mar 03 23:08:30 ip-172-31-29-165 sshd[158261]: Received disconnect from 93.149.180.144 port 56818:11: Bye Bye [preauth]
	Mar 03 23:08:30 ip-172-31-29-165 sshd[158261]: Disconnected from invalid user oracle 93.149.180.144 port 56818 [preauth]
  Mar 04 00:05:41 ip-172-31-29-165 sshd[168787]: Disconnected from authenticating user root 43.225.53.38 port 37402 [preauth]
	Mar 04 00:06:11 ip-172-31-29-165 sshd[168877]: Invalid user zong from 147.182.214.53 port 60894
	Mar 04 00:06:11 ip-172-31-29-165 sshd[168877]: Received disconnect from 147.182.214.53 port 60894:11: Bye Bye [preauth]
	Mar 04 00:06:11 ip-172-31-29-165 sshd[168877]: Disconnected from invalid user zong 147.182.214.53 port 60894 [preauth]
	Mar 04 00:09:07 ip-172-31-29-165 sshd[169325]: Connection closed by 20.124.128.248 port 38234 [preauth]
	Mar 04 00:17:01 ip-172-31-29-165 CRON[170801]: pam_unix(cron:session): session opened for user root by (uid=0)
	Mar 04 00:17:01 ip-172-31-29-165 CRON[170802]: (root) CMD (   cd / && run-parts --report /etc/cron.hourly)
	Mar 04 00:17:01 ip-172-31-29-165 CRON[170801]: pam_unix(cron:session): session closed for user root
	Mar 04 00:17:39 ip-172-31-29-165 systemd[1]: Starting Message of the Day...
	Mar 04 00:17:39 ip-172-31-29-165 systemd[1]: Starting Cleanup of rTemporary Directories...
	"""
	ip_list = []
	just_ip_list = []
	start_date = ""
	end_date = ""
	xx = 0
	for line in out_list:
		cut_line = line.split('[')
		line_left = cut_line[0]

		line_left_split = line_left.split(' ')
		if start_date == "" and xx > 0:
			start_date = line_left_split[0]+" "+line_left_split[1]+" "+line_left_split[2]
		end_date = line_left_split[0]+" "+line_left_split[1]+" "+line_left_split[2]
		try:
			line_right = cut_line[1]
		except:
			line_right = ""
   
		executed_metod = line_left.split(' ')[-1]
		if executed_metod in ("sshd"): #, "systemd"):
			right_list = line_right.split(' ')

			try:			
				if right_list[1] == "Invalid":
					#print(right_list)
					xx = 0
					while xx < len(right_list):
						
						if len(right_list[xx].split('.')) == 4:
							#print(len(right_list[xx].split('.')),right_list[xx+1])
							if right_list[xx+1] == "port":
								if right_list[xx] not in just_ip_list:
									ip_list.append([right_list[xx], right_list[xx-2]])
									just_ip_list.append(right_list[xx])
									break
						xx+= 1
			except:
				pass

	print('\t\t*** Przetworzonych linii:',len(out_list),'***')
	if output_type in ("T","t"):
		print('\t*** '+start_date+' ***\n')
		for line in ip_list:
			print('\n\t\t** '+line[0]+' \t\t'+line[1])
	print('\n\t*** '+start_date+' - '+end_date+' ',len(ip_list),'roznych IP ***')

def main():
	print('\t*','*'*55)
	line_count = input("\t* Ilosc linii kodu do analizy (default: 2500): ")
	if line_count == "":
		line_count = 2500
	order_by = input("\t* Sprawdzac od najnowszych(n) czy od najstarszych(o)? ")
	if order_by == "":
		order_by = "n"
	output_type = input("\t* Pokazać liste IP (T/N)? ")
	if output_type == "":
		output_type = "N"

	print('\t*','*'*55)
	readJournalctl(line_count,order_by,output_type)

if __name__ == '__main__':
	main()
