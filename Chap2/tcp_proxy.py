# tcp_proxy.py

# Esistono differenti ragioni per cui potreste aver bisogno
# un Proxy TCP: sia per eseguire il forwarding del traffico,
# ma anche per accedere ad applicazioni web. Quando eseguite
# un test di penetrazione in un ambiente aziendale, spesso
# non potrete eseguire Wireshark, non potrete caricare drivers
# per sniffare il traffico su sistemi Windows, e la
# segmentazione della rete non vi permettera' di eseguire
# diversi software direttamente sull'host obbiettivo. Si
# presentano differenti occasioni in cui avrete bisogno di
# implementare un proxy python per comprendere protocolli
# sconosciuti, modificare il traffico inviato ad un'applicazione
# e creare casi test.

# La maggior parte del codice sorgente che segue dovrebbe
# esservi familiare se avete gia' studiato i precedenti codici
# sorgenti: vengono letti alcuni parametri e viene avviato un Server
# in loop che rimane in attesa di connessioni.

# ---------------------------
# Il proxy realizzato si occupa di sniffare il trafico
# in una comunicazione tra l'host sul quale viene avviato e un host
# remoto con cui la macchina penetrata si sta comunicando.
# Il servizio da sniffare puo' essere un Server FTP o SFTP o qualsiasi
# altro tipo di canale di comunicazione tra host.
#
# Nel seguente esempio viene eseguito lo sniffing di una comunicazione SFTP
# tra il Server 188.165.251.105 e l'host locale.
#
# Per avviare il proxy utilizziamo il seguente comando:
# sudo python tcp_proxy.py 127.0.0.1 22 188.165.251.105 22 True
#
# A questo punto aprite il vostro client FTP (ad esempio Filezilla),
# impostate il proxy da utilizzare in "generic proxy" su 127.0.0.1:22.
#
# Effettuate una connessione al Server SFTP e il terminale su cui
# avete avviato il nostro proxy python stamper' i dati sniffati.
# ---------------------------

import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server.bind((local_host, local_port))
	except:
		print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
		print("[!!] Check for other listening sockets or correct permissions.")
		sys.exit(0)

	print("[*] Listening on %s:%d" % (local_host, local_port))

	server.listen(5)

	while True:
		client_socket, addr = server.accept()

		# Stampa delle informazioni relative alla connessione locale.
		print("[==>] Received incoming connection from %s:%d" % (addr[0], addr[1]))

		# Avvio di un thread per comunicare con l'host remoto.
		proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))

		proxy_thread.start()

def main():
	# Lettura degli argomenti da linea di comando, ed eventuale
	# stampa di un messaggio di aiuto in caso di parametri errati.
	if len(sys.argv[1:]) != 5:
		print("Usage python tcp_proxy.py [localhost] [localport] [remotehost] [remoteport] [receivefirst]")
		print("Example: python tcp_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
		sys.exit(0)

	# Configurazione dei parametri del Server locale.
	local_host = sys.argv[1]
	local_port = int(sys.argv[2])

	# Configurazione dei parametri dell'host remoto.
	remote_host = sys.argv[3]
	remote_port = int(sys.argv[4])

	# La seguente riga di codice specifica di connettersi
	# all'host remoto e riceve eventuali dati prim di inviarne alcuno.
	receive_first = sys.argv[5]

	if "True" in receive_first:
		receive_first = True
	else:
		receive_first = False

	# Avvio del socket in ascolto.
	server_loop(local_host, local_port, remote_host, remote_port, receive_first)

# Questa e' la funzione che contiene la logica di funzionamenti
# del nostro proxy.
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
	# Connessione all'host remoto.
	remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	remote_socket.connect((remote_host, remote_port))

	# Ricezione dei dati dall'host remoto e, se necessario
	if receive_first:
		remote_buffer = receive_from(remote_socket)
		hexdump(remote_buffer)

		# si invia la risposta all'handler.
		remote_buffer = response_handler(remote_buffer)

		# invio dei dati al client locale, se necessario
		if len(remote_buffer):
			print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
			client_socket.send(remote_buffer)

	# Il seguente loop si occupa, in loop, di leggere i dati locali,
	# inviare all'host remoto e a quello locale, pulire
	# le variabili e ripetere il loop.
	while True:
		# Lettura dall'host locale.
		local_buffer = receive_from(client_socket)

		if len(local_buffer):
			print("[==>] Received %d bytes from localhost." % len(local_buffer))
			hexdump(local_buffer)

			# Invio dei dati letti all'handler delle richieste.
			local_buffer = request_handler(local_buffer)

			# Invio dei dati all'host remoto.
			remote_socket.send(local_buffer)
			print("[==>] Sent to remote host.")

		# Ricezione della risposta dall'host remoto.
		remote_buffer = receive_from(remote_socket)

		if len(remote_buffer):
			print("[<==] Received %d bytes from remote." % len(remote_buffer))
			hexdump(remote_buffer)

			# Invio all'handler delle risposte.
			remote_buffer = response_handler(remote_buffer)

			# Invio della risposta al socket locale.
			client_socket.send(remote_buffer)

			print("[<==] Sent to localhost")

		# Se non sono presenti dati su entrambi i lati, chiudi la connessione.
		if not len(local_buffer) or not len(remote_buffer):
			client_socket.close()
			remote_socket.close()
			print("[*] No more data. Closing connections.")

			break

# Funzione hex presa direttamente dai commenti qui:
# http://code.activestate.com/recipes/142812-hex-dumper/
def hexdump(src, length=16):
	result = []
	digits = 4 if isinstance(src, unicode) else 2

	for i in xrange(0, len(src), length):
		s = src[i:i+length]
		hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
		text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
		result.append(b"%04X  %-*s  %s" % (i, length*(digits + 1), hexa, text))

	print(b'\n'.join(result))

def receive_from(connection):
	buffer = ""

	# impostiamo un timeout di 2 secondi; questi dipende dal
	# vostro target e potrebbe aver bisogno di modifiche.
	connection.settimeout(2)

	try:
		# Continua a leggere dal buffer sino a che
		# non vi sono altri dati, oppure si raggiunge il timeout.
		while True:
			data = connection.recv(4096)

			if not data:
				break

			buffer += data
	except:
		pass

	return buffer

# Modifica di qualsiasi richiesta destinata all'host remoto
def request_handler(buffer):
	# esecuzione della modifica dei pacchetti.
	return buffer

# Modifica di qualsiasi richiesta destinata all'host locale
def response_handler(buffer):
	# esecuzione della modifica dei pacchetti.
	return buffer

main()
