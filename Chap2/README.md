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
 * TCP e' un protocollo orientato alla connessione, ovvero prima di poter trasmettere dati deve stabilire la comunicazione, negoziando una connessione tra mittente e destinatario, che rimane attiva anche in assenza di scambio di dati e viene esplicitamente chiusa quando non piu' necessaria. Esso quindi possiede le funzionalita' per creare, mantenere e chiudere/abbattere una connessione.
 * TCP e' un protocollo affidabile: garantisce la consegna dei segmenti a destinazione attraverso il meccanismo degli acknowledgements.
 * Il servizio offerto da TCP e' il trasporto di un flusso di byte bidirezionale tra due applicazioni in esecuzione su host differenti. Il protocollo permette alle due applicazioni di trasmettere contemporaneamente nelle due direzioni, quindi il servizio puo' essere considerato "Full-duplex" anche se non tutti i protocolli applicativi basati su TCP utilizzano questa possibilita'.
 * Il flusso di byte viene frazionato in blocchi per la trasmissione dall'applicazione a TCP (che normalmente e' implementato all'interno del sistema operativo), per la trasmissione all'interno di segmenti TCP, per la consegna all'applicazione che lo riceve, ma questa divisione in blocchi non e' necessariamente la stessa nei diversi passaggi.
 * TCP garantisce che i dati trasmessi, se giungono a destinazione, lo facciano in ordine e una volta sola ("at most once"). Piu' formalmente, il protocollo fornisce ai livelli superiori un servizio equivalente ad una connessione fisica diretta che trasporta un flusso di byte. Questo e' realizzato attraverso vari meccanismi di acknowledgment e di ritrasmissione su timeout.
 * TCP offre funzionalita' di controllo di errore sui pacchetti pervenuti grazie al campo checksum contenuto nella sua PDU.
 * TCP possiede funzionalita' di controllo di flusso tra terminali in comunicazione e controllo della congestione sulla connessione, attraverso il meccanismo della finestra scorrevole. Questo permette di ottimizzare l'utilizzo dei buffer di ricezione/invio sui due end devices (controllo di flusso) e di diminuire il numero di segmenti inviati in caso di congestione della rete.
 * TCP fornisce un servizio di multiplazione delle connessioni su un host, attraverso il meccanismo delle porte.

### UDP
In telecomunicazioni lo User Datagram Protocol (UDP) e' uno dei principali protocolli di trasporto della suite di protocolli Internet. E' un protocollo di livello di trasporto a pacchetto, usato di solito in combinazione con il protocollo di livello di rete IP.
A differenza del TCP, l'UDP e' un protocollo di tipo connectionless, inoltre non gestisce il riordinamento dei pacchetti ne' la ritrasmissione di quelli persi, ed e' perciò generalmente considerato di minore affidabilita'. In compenso e' molto rapido (non c'e' latenza per riordino e ritrasmissione) ed efficiente per le applicazioni "leggere" o time-sensitive. Ad esempio, e' usato spesso per la trasmissione di informazioni audio-video real-time come nel caso delle trasmissioni Voip.
Infatti, visto che le applicazioni in tempo reale richiedono spesso un bit-rate minimo di trasmissione, non vogliono ritardare eccessivamente la trasmissione dei pacchetti e possono tollerare qualche perdita di dati, il modello di servizio TCP puo' non essere particolarmente adatto alle loro caratteristiche.
L'UDP fornisce soltanto i servizi basilari del livello di trasporto, ovvero:
 * multiplazione delle connessioni, ottenuta attraverso il meccanismo di assegnazione delle porte;
 * verifica degli errori (integrità dei dati) mediante una checksum, inserita in un campo dell'intestazione (header) del pacchetto, mentre TCP garantisce anche il trasferimento affidabile dei dati, il controllo di flusso e il controllo della congestione.
L'UDP e' un protocollo stateless, ovvero non tiene nota dello stato della connessione dunque ha, rispetto al TCP, meno informazioni da memorizzare: un server dedicato ad una particolare applicazione che scelga UDP come protocollo di trasporto puo' supportare quindi molti piu' client attivi.

### UDP vs TCP
Le principali differenze tra TCP e UDP (User Datagram Protocol), l'altro principale protocollo di trasporto della suite di protocolli Internet, sono:
 * TCP e' un protocollo orientato alla connessione. Pertanto, per stabilire, mantenere e chiudere una connessione, e' necessario inviare pacchetti di servizio i quali aumentano l'overhead di comunicazione. Al contrario, UDP e' senza connessione ed invia solo i datagrammi richiesti dal livello applicativo;
 * UDP non offre nessuna garanzia sull'affidabilità della comunicazione ovvero sull'effettivo arrivo dei segmenti, sul loro ordine in sequenza in arrivo; al contrario il TCP tramite i meccanismi di acknowledgement e di ritrasmissione su timeout riesce a garantire la consegna dei dati, anche se al costo di un maggiore overhead (raffrontabile visivamente confrontando la dimensione delle intestazioni dei due protocolli);
 * l'oggetto della comunicazione di TCP e' il flusso di byte mentre quello di UDP e' il singolo datagramma.
L'utilizzo del protocollo TCP rispetto a UDP e', in generale, preferito quando e' necessario avere garanzie sulla consegna dei dati o sull'ordine di arrivo dei vari segmenti (come per esempio nel caso di trasferimenti di file). Al contrario UDP viene principalmente usato quando l'interazione tra i due host e' idempotente o nel caso si abbiano forti vincoli sulla velocita' e l'economia di risorse della rete (es. streaming).

### Netcat
Netcat e' un programma open source a riga di comando di comunicazione remota, utilizzabile sia col protocollo TCP sia col protocollo UDP.
Netcat e' stato pensato per essere utilizzato facilmente da altri programmi o scripts. Allo stesso tempo puo' essere uno strumento utilissimo per l'amministrazione di rete e di investigazione.
Nel 2000 Netcat fu votata da www.insecure.org come il secondo migliore programma per la sicurezza informatica. Anche nel 2003 e nel 2006 raggiunse il quarto posto per la stessa categoria. Netcat viene spesso chiamato come "il coltellino svizzero delle reti TCP/IP". Puo' essere utilizzato per moltissime funzioni: eseguire una scansione sulle porte di un computer remoto o ascoltare in locale, trasferire file, essere usato come una chat o persino per la creazione di una backdoor.

### Proxy
In informatica e telecomunicazioni, un server proxy e' un server (inteso come sistema informatico o applicazione) che funge da intermediario per le richieste da parte dei client alla ricerca di risorse su altri server, disaccoppiando l'accesso al web dal browser. Un client si connette al server proxy, richiedendo qualche servizio (ad esempio un file, una pagina web o qualsiasi altra risorsa disponibile su un altro server), e quest'ultimo valuta ed esegue la richiesta in modo da semplificare e gestire la sua complessità. I proxy sono stati inventati per aggiungere struttura e incapsulamento ai sistemi distribuiti.
Ad oggi, i server proxy vengono utilizzati per svariati impieghi come:
 * Fornire l'anonimato durante la navigazione internet (es. sistema TOR)
 * Memorizzare una copia locale degli oggetti web richiesti in modo da poterli fornire nuovamente senza effettuare altri accessi ai server di destinazione (HTTP caching proxy)
 * Creare una "barriera di difesa" (Firewall) verso il web, agendo da filtro per le connessioni entranti ed uscenti e monitorando, controllando e modificando il traffico interno

### TCP Proxy
Il proxy TCP e' un processo proxy che pu' essere avviato in uno stream TCP, come ad esempio una connessione HTTP tra il vostro browser e un server. It filters the request and response streams, sending the results to the terminal window (stdout). You can control its behaviour by specifying different filters.

### Paramiko
Paramiko e' un'implementazione Python (2.6+, 3.3+) del protocollo SSHv2, che fornisce  funzionalita' sia lato client che server. Utilizza una estensione Python C per gestire la crittografia a basso livello, e fornisce una completa interfaccia Python per operazioni SSH di rete.

### SSH
In informatica e telecomunicazioni SSH (Secure SHell, shell sicura) e' un protocollo che permette di stabilire una sessione remota cifrata tramite interfaccia a riga di comando con un altro host di una rete informatica. E' il protocollo che ha sostituito l'analogo, ma insicuro, Telnet.
Il client SSH ha un'interfaccia a riga di comando simile a quella di telnet e rlogin, ma l'intera comunicazione (ovvero sia l'autenticazione - mutua - che la sessione di lavoro) avviene in maniera cifrata. Per questo motivo, SSH e' diventato uno standard di fatto per l'amministrazione remota di sistemi UNIX e di dispositivi di rete, rendendo obsoleto il protocollo telnet, giudicato troppo pericoloso per la sua mancanza di protezione contro le intercettazioni.
Il client ed il server SSH sono installati o installabili su molte versioni di UNIX, GNU/Linux, macOS e Microsoft Windows. Inoltre e' disponibile come strumento di amministrazione su alcuni apparati di rete. La IANA (Internet Assigned Numbers Authority) ha assegnato al servizio SSH la porta 22 TCP e UDP, anche se e' comunque possibile implementare il servizio SSH su altre porte non definite dalla IANA.

### Tunneling
Nelle reti di calcolatori, il termine tunneling si riferisce a un insieme di tecniche di trasmissione dati per cui un protocollo viene incapsulato in un altro protocollo per realizzare configurazioni particolari ovvero inserire funzionalità protocollari aggiuntive di elaborazione non presenti nel protocollo iniziale, ma presenti in altri protocolli.
Nelle configurazioni normali, un protocollo viene incapsulato in un altro protocollo di livello inferiore. Ad esempio, IP viene incapsulato in ethernet.
 * Un insieme importante delle tecniche di tunneling sono quelle usate per realizzare VPN, in cui IP viene incapsulato in IP, TCP o UDP, inserendo uno strato di crittografia. In queste tecniche, due reti IP, o due parti della stessa rete IP, entrambe connesse ad Internet, vengono interconnesse facendo passare il traffico all'interno di una connessione che viene trasmessa su Internet.
 * La funzionalita' di port forwarding di SSH consente di inoltrare connessioni TCP tra host arbitrari all'interno di una connessione SSH, che a sua volta viaggia su TCP. In questo modo si riesce facilmente a proteggere un protocollo applicativo insicuro per farlo transitare su una rete non fidata, oppure ad aggirare limitazioni realizzate attraverso firewall o configurazioni di routing che non permetterebbero a due host di comunicare direttamente.
 * L'utilizzo di protocolli di livello di rete per trasportare IP, che a sua volta e' un protocollo di livello rete, e' a sua volta una forma di tunneling. L'esempio tipico e' la connessione di due reti IP attraverso una galleria ATM: in tal caso, il pacchetto IP viene inserito (e opportunamente frammentato) all'interno del campo dati della cella ATM, trasmesso attraverso la rete e quindi spacchettato e ricomposto all'arrivo. In questo modo, gli switch ATM non si renderanno conto di cosa stanno trasmettendo, perche' il campo dati e' trasmesso così com'è, senza dover essere interpretato. Ai capi della galleria e' necessario inserire router multiprotocollo, che siano in grado di compiere le operazioni di impacchettamento dei dati.
 * Per trasportare il protocollo IPv6 all'interno di IPv4, o viceversa, si usano delle gallerie. Un insieme di tecniche di tunneling sono state previste per gestire la transizione da IPv4 a IPv6.


### SSH Tunneling
Quando si e' connessi da una rete pubblica o non sicura, per proteggere la vostra privacy e quella dei vostri clienti.
Ci sono svariate ragioni per cui si dovrebbe scegliere di utilizzare un tunnel sicuro, ma la principale e' ovviamente la sicurezza. Utilizzare un tunnel cifrato ti mette al sicuro dalla possibilita' che la comunicazione venga intercettata nella rete in cui transita. Questo e' particolarmente utile se si e' connessi tramite wifi, reti pubbliche, aziendali, e in generale da reti non sicure dove terzi potrebbero sniffare il contenuto delle connessioni. Usando un tunnel cifrato ben configurato ed utilizzando chiavi firmate e' anche possibile rendere piu' difficili gli attacchi MITM (Man In The Middle).
Esistono poi protocolli non sicuri che e' meglio veicolare in una connessione cifrata appena possibile.
Ad esempio, si supponga di avere un server remoto con un database SQL che accetta solo connessioni da localhost. Supponiamo anche di voler effettuare manutenzione e query senza usare un'interfaccia web come phpMyadmin, ed usare invece un bel client locale. Come fare? Di certo non e' cosa intelligente aprire il database a chiunque, d’altro canto siccome il server accetta solo connessioni locali sembrerebbe impossibile ottenere il risultato sperato.
La soluzione e' il tunneling ssh della connessione al database. Infatti e' possibile incapsulare la connessione al database in una SSH verso l’host che poi la reindirizza localmente alla porta del server di database, e cosi' facendo si ottengono 2 vantaggi :
 * L’host remoto non deve accettare connessioni SQL da terzi
 * La nostra connessione e' sicura e cifrata fino all’host di destinazione
Ricapitolando, mediante il tunneling ssh e' possibile proteggere e cifrare una connessione dal pc su cui lavoriamo fino ad un host che riteniamo sicuro. Oltre alla sicurezza, un’altra ragione per voler utilizzare un tunnel ssh e' la possibilita' di eludere regole di routing restrittive e firewall che incitano alla violenza. Infatti e' possibile incapsulare tutto il proprio traffico HTTP, FTP o connessioni di altro tipo, in un tunnel che attraversa la rete con regole restrittive fino ad un host fidato in una rete di cui si ha il controllo (ad esempio il proprio pc di casa, o una VPS in un datacenter fidato). Su quell’host il traffico lascia il tunnel e viene rispedito come se l’origine fosse l’host stesso.
In questa maniera si puo' attraversare la rete insicura o con restrizioni mediante una singola connessione cifrata, una volta raggiunto l’host fidato il traffico sarà reindirizzato verso le destinazioni volute, e le risposte saranno convogliate attraverso il tunnel fino alla vostra posizione.

### SSH Reverse
SSH reverse tunneling permette di collegarsi ad un server remoto (dotato di servizio ssh) e dirgli di inviare/inoltrare tutte le connessioni TCP ricevute su una porta, ad un altro host in rete.
Vediamo un esempio per rendere l’idea.
Ammettiamo di avere un computer collegato dietro una NAT, ad esempio come accade per i clienti Fastweb. Questo computer avra' quindi un IP privato e non potra' quindi ricevere connessioni in ingresso da Internet.
Ammettiamo pero' di avere anche accesso SSH ad un server esterno alla rete Fastweb, dotato di normale indirizzo IP pubblico, ed in grado di ricevere connessioni in ingresso da Internet.

--

Rambod Rahmani <<rambodrahmani@autistici.org>>
