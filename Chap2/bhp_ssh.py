# bhp_ssh.py

import sys
import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
	client = paramiko.SSHClient()
	# notice that paramiko supports authentication with keys
	# client.load_host_keys('/home/justin/.ssh/known_hosts')
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip, username = user, password = passwd)

	ssh_session = client.get_transport().open_session()

	if ssh_session.active:
		ssh_session.exec_command(command)
		print ssh_session.recv(1024)

	return

# prints usage arguments and examples
def usage():
	print("Usage python bhp_ssh.py [ip] [user] [password] [command]")
	print("Example python bhp_ssh.py 192.168.1.1 justin lovethepython id")

# edited to pass ssh connection paramters using command line arguments
#
# *** Python sys.argv ***
# to make it easier to read, let's just shorten this to:
#
# C:\> hello.py John
#
# argv represents all the items that come along via the command-line input,
# but counting starts at zero (0) not one (1): in this case, "hello.py"
# is element 0, "John" is element 1
#
# In other words, sys.argv[0] == 'hello.py' and sys.argv[1] == 'John' ...
# but look, how many elements is this? 2, right! so even though the numbers
# are 0 and 1, there are 2 elements here.
#
def main():
	if not len(sys.argv) == 5:
		usage()
		sys.exit(0)

	ssh_command(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
main()
