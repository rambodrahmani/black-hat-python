# Capitolo 2 - La Rete: Concetti Basilari

Il Capitolo 2 introduce i concetti relativi alla programmazione Python di rete.

Lo scenario da prendere in considerazione e' quella di un hacker che e' riuscito a compremettere la rete di una grande azienda. A questo punto tuttavia si ritrova con funzionalita' limitate all'interno dei sistemi bucati, non ha gli strumenti per eseguire ulteriori attacchi di rete dato che non sono installati di default su queste macchine. No netcat, no wireshark, no compiler e nessuna via per installare nuovo software. Tuttavia, rimarrete sorpresi di torvare, nella maggior parte dei casi, un'installazione di Python che potete utilizzare per creare gli strumenti di cui avete bisogno.
Si parte da questo scenario per studiare l'implementazione di alcuni degli strumenti piu' utilizzati dagli hacker direttamente in linguaggio Python.
Il codice di tale implementazioni e' scritto in "fretta e furia", senza curarsi troppo degli standard del linguaggio Python, ma solamente per poter fare quello che si desidera fare in maniera piu' veloce possibile, che e' ovviamente lo scenario in cui si trova a lavorare un pen tester.

I concetti che vengono introdotti in questo capitolo sono molteplici: si parte dal protocollo UDP per arrivare a tirare su un proxy TCP. Poi viene mostrato come utilizzare l'SSH, il Reverse SSH e infine l'SSH Tunneling.

Ci sono una serie di concetti che credo debbano essere approfonditi prima di poter passare alla lettura dei codici sorgente del capitolo e sono i seguenti.

### Protocollo
I  protocolli  definiscono  formato  e ordine  dei  messaggi  spediti  e ricevuti tra entita' della rete, e le azioni  da  compiere  in  seguito  alla ricezione  e/o  trasmissione  dei messaggi o di altri eventi.
Quindi un protocollo determina come due entita' debbano comunicare, proprio come le regole della grammatica della lingua italiana parlata.

[INSERIRE IMMAGINE PROTOCOLLO]

In particolare un protocollo prevede la definizione dei linguaggi costituiti dai messaggi scambiati, messaggi che devono potersi interpretare correttamente. L'aderenza ai protocolli garantisce che due software in esecuzione su diverse macchine possano comunicare efficacemente, anche se sono stati realizzati indipendentemente cioè interoperabilita'.
In senso piu' lato, un protocollo di comunicazione si puo' definire come un insieme di regole che vengono stabilite per instaurare una comunicazione corretta: ad esempio due persone di differenti madrelingue potrebbero mettersi d'accordo nell'utilizzo della lingua inglese per comunicare.

### Protocollo di Comunicazione
In informatica un protocollo di comunicazione e' un insieme di regole formalmente descritte, definite al fine di favorire la comunicazione tra una o piu' entita'. Tutte queste regole sono definite mediante specifici protocolli, dalle tipologie piu' varie e ciascuno con precisi compiti/finalita', a seconda delle entita' interessate e il mezzo di comunicazione. Se le due entita' sono remote, si parla di protocollo di rete.

### Protocollo di Rete
Nelle telecomunicazioni, per protocollo di rete si intende un particolare tipo di protocollo di comunicazione preposto al funzionamento di una rete informatica ovvero la definizione formale a priori delle modalita' di interazione che due o piu' apparecchiature elettroniche collegate tra loro devono rispettare per operare particolari funzionalita' di elaborazione necessarie all'espletamento di un certo servizio di rete.
L'implementazione informatica dei protocolli di rete definisce, all'interno dell'architettura di rete, il cosiddetto software di rete, presente usualmente all'interno del sistema operativo ed elaborato dalla scheda di rete.

### Suite di Protocolli Internet
Una suite di protocolli Internet, in informatica e in telecomunicazioni, indica un insieme di protocolli di rete su cui si basa il funzionamento logico della rete Internet. A volte, per sineddoche, e' chiamata suite di protocolli TCP/IP, in funzione dei due piu' importanti protocolli in essa definiti: il Transmission Control Protocol (TCP) e l'Internet Protocol (IP).

### TCP
In telecomunicazioni e informatica il Transmission Control Protocol (TCP), anche chiamato Transfer Control Protocol, e' un protocollo di rete a pacchetto di livello di trasporto, appartenente alla suite di protocolli Internet, che si occupa di controllo di trasmissione ovvero rendere affidabile la comunicazione dati in rete tra mittente e destinatario.
#### Caratteristiche principali
&nbsp;&nbsp;&nbsp;&nbsp;1. TCP e' un protocollo orientato alla connessione, ovvero prima di poter trasmettere dati deve stabilire la comunicazione, negoziando una connessione tra mittente e destinatario, che rimane attiva anche in assenza di scambio di dati e viene esplicitamente chiusa quando non piu' necessaria. Esso quindi possiede le funzionalita' per creare, mantenere e chiudere/abbattere una connessione.
&nbsp;&nbsp;&nbsp;&nbsp;2. TCP e' un protocollo affidabile: garantisce la consegna dei segmenti a destinazione attraverso il meccanismo degli acknowledgements.
&nbsp;&nbsp;&nbsp;&nbsp;3. Il servizio offerto da TCP e' il trasporto di un flusso di byte bidirezionale tra due applicazioni in esecuzione su host differenti. Il protocollo permette alle due applicazioni di trasmettere contemporaneamente nelle due direzioni, quindi il servizio puo' essere considerato "Full-duplex" anche se non tutti i protocolli applicativi basati su TCP utilizzano questa possibilita'.
&nbsp;&nbsp;&nbsp;&nbsp;4. Il flusso di byte viene frazionato in blocchi per la trasmissione dall'applicazione a TCP (che normalmente e' implementato all'interno del sistema operativo), per la trasmissione all'interno di segmenti TCP, per la consegna all'applicazione che lo riceve, ma questa divisione in blocchi non e' necessariamente la stessa nei diversi passaggi.
&nbsp;&nbsp;&nbsp;&nbsp;5. TCP garantisce che i dati trasmessi, se giungono a destinazione, lo facciano in ordine e una volta sola ("at most once"). Piu' formalmente, il protocollo fornisce ai livelli superiori un servizio equivalente ad una connessione fisica diretta che trasporta un flusso di byte. Questo e' realizzato attraverso vari meccanismi di acknowledgment e di ritrasmissione su timeout.
&nbsp;&nbsp;&nbsp;&nbsp;6. TCP offre funzionalita' di controllo di errore sui pacchetti pervenuti grazie al campo checksum contenuto nella sua PDU.
&nbsp;&nbsp;&nbsp;&nbsp;7. TCP possiede funzionalita' di controllo di flusso tra terminali in comunicazione e controllo della congestione sulla connessione, attraverso il meccanismo della finestra scorrevole. Questo permette di ottimizzare l'utilizzo dei buffer di ricezione/invio sui due end devices (controllo di flusso) e di diminuire il numero di segmenti inviati in caso di congestione della rete.
&nbsp;&nbsp;&nbsp;&nbsp;8. TCP fornisce un servizio di multiplazione delle connessioni su un host, attraverso il meccanismo delle porte.


### UDP

### UDP vs TCP

### Netcat

### Proxy

### TCP Proxy

### Paramiko

### SSH

### SSH Reverse

### SSH Tunneling

--

Rambod Rahmani <<rambodrahmani@autistici.org>>
