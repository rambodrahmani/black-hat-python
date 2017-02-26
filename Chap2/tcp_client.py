# tcp_client.py

# Il codice mosta l'implementazione di una delle tipologie di client TCP
# piu' semplici che si possano creare, che si rivela tuttavia essere
# la tipologia che maggiormente vi ritroverete ad utilizzare durante un
# test di penetrazione.
# L'utilizzo che ne viene fatto e' quello di eseguire test per servizio
# in esecuzione sulla macchina penetrata, inviare dati spazzatura e
# altre differenti funzionalita'.
# L'utilizzo del presente codice sorgente e' da abbinarsi con una istanza
# di tcp_server.py. Le istruzioni per una corretta esecuzione dell'istanza
# Server e di quella Client sono riportate in tcp_server.py.

import socket

target_host = "0.0.0.0"
target_port = 9999

# Creazione di un oggetto socket con i parametri AF_INET (indica che
# utilizzeremo un indirizzo IPv4 standard) e SOCK_STREAM (indica
# che vogliamo creare un client TCP)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecttiamo quindi il client al server
client.connect((target_host, target_port))

# Invio di alcuni dati al server
client.send("GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")

# Ricezione dei dati e successiva stampa della risposta.
response = client.recv(4096)

print(response)
