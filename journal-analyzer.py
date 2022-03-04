import subprocess
import os

def readJournalctl(line_count):
	#execute_line = "journalctl |head -"+str(line_count)
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
	for line in out_list:
		
		line_left = line.split('[')[0]
		line_right = line.split('[')[0]
		executed_metod = line_left.split(' ')[-1]
		if executed_metod in ("sshd"): #, "systemd"):
			right_list = line_right.split(' ')
			if right_list[0] == "Invalid":
				xx = 0
				for tmp_line in right_list:
					if len(tmp_line.split('.')) == 3:
						if right_list[xx+1] == "port":
							if right_list[xx] not in ip_list:
								ip_list.append(right_list[xx])
								break
				xx+= 1

			print(line_left)

	print('\n'.join(ip_list))

def main():
	line_count = 10000
	print('******************')
	readJournalctl(line_count)

if __name__ == '__main__':
	main()
