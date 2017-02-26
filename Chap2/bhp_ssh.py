# bhp_ssh.py

# Un dei metodi per proteggere con crittografia il traffico
# delle vostre comunicazioni con host remoti e' quello ti
# utilizzare l'SSH (Secure Shell). Tuttavia, com pensate di fare
# nel caso in cui il vostro host obbiettivo non ha un client SSH
# (come ad esempio il 99.8 per cento dei sistemi Windows)?
# Potete in questi casi utilizzare il python per creare un client
# SSH o server. Paramiko, utilizzando PyCrypto vi fornisce accesso
# semplificato al protocollo SSH2.

# Prima di procedere dovete installare paramiko utilizzando l'installer
# pip con il seguente comando da linea di comando:
# $ pip install paramiko

# -----------------------------
# Esempio di utilizzo:
# $ python bhp_ssh.py 127.0.0.1 rambodrahmani password ls
# -----------------------------

import sys
import threading
import paramiko
import subprocess

# Il programma che segue e' abbastanza semplice.
# Viene creata una unica funzione che si connette al Server SSH specificato
# ed esegue un singolo comando.
def ssh_command(ip, user, passwd, command):
	client = paramiko.SSHClient()
	# Paramiko supporta l'autenticazione anche con l'utilizzo di chiavi SSH
	# client.load_host_keys('/home/justin/.ssh/known_hosts')
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip, username = user, password = passwd)

	ssh_session = client.get_transport().open_session()

	if ssh_session.active:
		ssh_session.exec_command(command)
		print ssh_session.recv(1024)

	return

# Il codice sorgente seguente e' stato modificato rispetto
# a quello originario per implementare funzioni non previste
# dal libro.
def usage():
	print("Usage python bhp_ssh.py [ip] [user] [password] [command]")
	print("Example python bhp_ssh.py 192.168.1.1 justin lovethepython id")

# edited to pass ssh connection paramters using command line arguments
#
# *** Python sys.argv ***
# -----------------------
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
