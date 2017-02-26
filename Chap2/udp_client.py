# udp_client.py

# A partire dal codice sorgente tcp_client.py si ottiene
# il seguente codice per un client UDP con poche modifiche.
# In questo e negli altri esempi, come e' evidente dalla struttura
# del codice sorgente, l'obbiettivo non e' quello di essere programmatori
# di rete con capacita' avanzate, ma quello di essere veloci, semplici
# e affidabili a sufficienza da portare avanti la penetrazione.

import socket

target_host = "127.0.0.1"
target_port = 80

# Creazione di un oggetto socket: il tipo di socket e'
# cambiato in SOCK_DGRAM.
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# UDP e' un protocollo connectionless, quindi non abbiamo
# bisogno di instaurare una connessione con il Server.

# Invio di dati.
client.sendto("AAABBBCCC", (target_host, target_port))

# Ricezione dei dati inviati.
data, addr = client.recvfrom(4096)

print(response)
