# tcp_serer.py

# Creare Server TCP in python e' semplice tanto quanto la
# creazione del client TCP che abbiamo gia' visto in tcp_client.py.

# Per utilizzare tcp_client.py e tcp_server.py utilizzare i seguenti comandi su terminare:

# -------------------------------
# Avvio del Server TCP:
# $ python tcp_server.py
# [*] Listening on 0.0.0.0:9999

# Avvio del Client TCP
# $ python tcp_client.py 
# ACK!

# Output finale del Server TCP:
# [*] Accepted connection from 127.0.0.1:59544
# [*] Received: GET / HTTP/1.1
# Host: www.google.com
# -------------------------------


import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

# Creazione di un Socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Definizione dell'indirizzo IP e della porta su cui eseguire
# il Server.
server.bind((bind_ip, bind_port))

# Inizio ricezione delle connessioni da parte dei Clients
# con un backlog di 5.
server.listen(5)

# Server avviato: viene stampato l'indirizzo IP e la porta
# su cui il Server si trova in ascolto.
print("[*] Listening on %s:%d" % (bind_ip, bind_port))

# La funzione che si occupa di gestire le connessioni in
# arriva dei Clients esegue una semplice ricezione e invio del messaggio "ACK!".
def handle_client(client_socket):
	# Stampa del messaggio ricevuto dal Client.
	request = client_socket.recv(1024)
	print("[*] Received: %s" % request)

	# Invio di un pacchetto al Client contenente il messaggio "ACK!"
	client_socket.send("ACK!")

	client_socket.close()

# A questo punto il Server entra nel suo ciclo while principale. Quando
# un client si connette riceviamo il socket in una variabile di nome
# client e i dettaggli relativi alla connessione remote vengono salvati in addr. In seguito viene creato un oggetto thread collegato alla funzione handle_client.
while True:
	client, addr = server.accept()

	print("[*] Accepted connection from %s:%d" % (addr[0], addr[1]))

	# Creazione del thread con passaggio dell'oggetto socket salvato nella variabili client al momento della ricezione della connessione.
	client_handler = threading.Thread(target=handle_client,args=(client,))
	client_handler.start()

# Questo e' tutto: il codice sorgente e' molto semplice ma si rivela essere davvero utile. La presentazione implementazione verra' ampliata nelle sezioni successive quando verra' implementato un sostituto del famosissimo strumenti di networking netcat scritto in Python.
