# Registro progetti — decisioni e informazioni

Base di conoscenza unica, alimentata da **email** e **riunioni**.
La struttura delle sezioni rispecchia le cartelle della casella di posta; dentro
ogni ramo la suddivisione è per **area / item**.

**Convenzioni**

- Ogni voce riporta la **fonte** (mittente + data) così è sempre ricostruibile.
- `DECISIONE` = punto chiuso · `APERTO` = da risolvere · `VINCOLO` = requisito imposto.
- I valori non confermati sono marcati `[DA CONFERMARE]`.
- I **commenti per singolo item** (codici `5_19_...`) stanno in **MR - Design Concept § Registro item**.
- Ultimo aggiornamento: **25/07/2026**.

**Copertura attuale** — tutte le sottocartelle di `MOUNTAIN RETREAT`:

| Cartella | Email | Stato |
|---|---|---|
| MR - BIM | 2 | ✅ |
| MR - BOQ RFQ | 15 | ✅ |
| MR - BREEAM | 12 | ✅ |
| MR - Budget | 34 | ✅ |
| MR - Ceiling | 12 | ✅ |
| MR - Claddings Portals | 25 | ✅ |
| MR - Design Concept | 1 | ✅ |
| MR - Design Development | 0 | vuota |
| MR - Doors | 98 | ✅ |
| MR - Fire | 36 | ✅ |
| MR - Flooring | 5 | ✅ |
| MR - Lighting | 34 | ✅ |
| MR - Logistic | 11 | ✅ |
| MR - Offer Approvals | 3 | ✅ |
| MR - Planning | 0 | vuota |
| MR - Stones | 2 | ✅ |
| MR - Suppliers / MR - ALART | 35 | ✅ |
| MR - Suppliers / MR - APIR | 1 | ✅ |
| MR - Suppliers / MR - BERGAMASCHI | 18 | ✅ |
| MR - Suppliers / MR - HAUTE · LUALDI · PEDRETTI | 0 | vuote |
| MR - Various UNPROCESSED | 885 | ⏸ non processata (vedi §finale) |

---

# WORK - PROJECTS

## MOUNTAIN RETREAT

### Anagrafica del progetto

- **Committente / veicolo di fatturazione:** Rauðukambar ehf. — ID 510816-0640,
  Urriðaholtsstræti 2-4, 210 Garðabær, Islanda.
- **Sito:** paese più vicino **Árnes**, porto più vicino **Þorlákshöfn**
  (⚠️ *non* Grindavík, che è Blue Lagoon — vedi MR - Logistic).
- **Nome storico del progetto:** *Mountain Baths* / *Highland Baths* (fase concept 2017–2022).

**Interlocutori ricorrenti**

| Persona | Ruolo | Organizzazione |
|---|---|---|
| Hartmann Kárason | Director of Constructions | Blue Lagoon |
| Sigurður Þorsteinsson (Siggi) | Direzione | Blue Lagoon |
| Jón Bjarni Jóhannsson (Nonni) | Project manager | Blue Lagoon |
| Carol Tayar | Lead Designer | Blue Lagoon Design, Milano |
| Fabrizia Sabatino | Senior Designer | Blue Lagoon Design, Milano |
| Marcos Zotes · Perla Dís Kristinsdóttir | Partner / Architect | Basalt |
| André Motta Vieira · Guðjón Kjartansson · Magda Soja · Óliver Ás Kristjánsson | Architetti | Basalt |
| Guðrún Júlía Þórðardóttir | Fire engineer — **il fire consultant** | EFLA |
| Sigurður Loftur Thorlacius | Consulente BREEAM | EFLA |
| Pétur Jónsson | Landscape architect | EFLA |
| Sigurdur Lárus Holm (Lárus) | Cost consultant | Consulto |
| Simone Cariboni · Isabel Jimenez · Santoro | Coordinamento | D'Alesio & Santoro |
| Matteo Ariosto | Titolare | Alart |
| Giuseppe Pruneri · Francesco Saccaro · Marina De Paoli | Referenti | Haute Material (BDM sas) |
| Giovanni · Egidio · Benedetta Bergamaschi | Titolari | Bergamaschi F.lli |
| Ada Pugi · Marco Delli Noci | Sales / tecnico | DGA S.p.A. |
| Lorenzo Angelini · Marco Giorgini | Referenti | Apir |
| Sara Sarni | Retail Int. Sales | Forma Lighting |
| — | General contractor islandese | **Javerk** |

---

### MR - Fire

#### 1. Quadro normativo — classi di reazione al fuoco

| Ambito | Classe richiesta | Fonte |
|---|---|---|
| Claddings, porte, cielini nelle aree marcate | **B-s1,d0** (fire class 1, K²10 B-s1,d0) | Perla Dís / EFLA, 08.04.2024 |
| Pavimenti in generale | **Dfl-s1** | Perla Dís, 13.11.2024 — conf. Guðrún 14.11.2024 |
| Pavimenti nei vani scala | **Cfl-s1** | idem — riconfermato Guðrún 21.07.2025 |
| Porte — resistenza al fuoco | EI30 / EI60 | — |

`VINCOLO` La classe **B-s1,d0 si applica al cladding (strato esterno della parete)**,
non alla sola verniciatura. La vernice non è inclusa nel computo *a meno che* non sia
una vernice ignifuga specifica, pensata per portare a norma un cladding che da solo non
raggiunge la B-s1,d0. — *Guðrún Júlía (EFLA), 21.07.2025*

`VINCOLO` Anche le **strutture di supporto** del cladding (es. telaio dei pannelli di
controsoffitto sopra le porte camera in corridoio) devono essere **B-s1,d0**.
— *Guðrún Júlía, 21.07.2025*

`APERTO` **Contraddizione da sanare:** Marcos (Basalt, 19.11.2024) sostiene che il
requisito **non** si applichi al sistema di aggancio dietro i claddings Haute *se chiuso
e non direttamente raggiungibile dal fuoco*, e che il fire engineer debba valutare i
dettagli finali. Guðrún (21.07.2025) afferma invece che i telai di supporto **sono**
soggetti. Le due posizioni non sono mai state riconciliate esplicitamente.

`DECISIONE` **EI30/EI60 è tema distinto e risolto**: riguarda il passaggio del fuoco,
non la reazione al fuoco. — *Carlo, 20.01.2026*

**Glossario operativo** (ricostruito da Carlo, 23.10.2024)
- `EI-30 / EI-60` — integrità strutturale e limitazione del passaggio di fiamme e gas caldi.
- `Classe 0 / Classe 1` — reazione al fuoco: propagazione della fiamma e carico d'incendio.
- `B-s1,d0` — **B**: contributo al fuoco molto limitato · **s1**: fumo scarso ·
  **d0**: nessun gocciolamento incandescente.
- Le tre nomenclature **non sono intercambiabili né paragonabili**.

`NOTA` L'edificio ha **impianto sprinkler** (verificato già in gen. 2024 — Fabrizia,
22.01.2024, all. `230119 - sprinkler system.pdf`). È il presupposto che nel 2026 apre
alla possibilità di declassare le pareti a B,s2-d0 (§8).

---

#### 2. Zonizzazione — dove serve la protezione

Mappa fornita dal fire consultant EFLA, girata da Basalt.
*(Marcos Zotes, 12.11.2024 — con correzioni in rosso di Guðrún Júlía, 13.11.2024)*

**Regola generale:** tutti i **claddings in legno, porte e cielini dei corridoi hotel**
devono essere trattati con vernice ignifuga.

| Piano | Aree soggette |
|---|---|
| **1°** | Cladding + porta *laundry shaft* · Cladding + porta *VIP entrance* |
| **2°** | Cladding + porta *office space* · Cladding, cielino + porte *bar area* · Cladding + porte *zona ascensori* · **prima parte corridoio hotel** |
| **3°** | Cladding + porte *library* · Cladding, cielino + porte *zona ascensori* · **prima parte corridoio hotel** |

`DECISIONE` **Correzione EFLA:** Basalt riteneva che la prima parte del corridoio hotel
(2° e 3° piano) non necessitasse di trattamento. Guðrún ha corretto: **serve anche lì**,
perché i rivestimenti nelle vie di esodo devono avere contributo limitato al carico
d'incendio. — *13.11.2024*

`DECISIONE` I **cielini** (incluse le cornici/coves in legno dei controsoffitti Clipso in
office space) vanno trattati per raggiungere **almeno B-s1,d0**. — *Guðrún, 13.11.2024*

`DECISIONE` La **library** rientra perché ha una **via di esodo sul balcone**: la via
principale è lunga e complessa, la seconda è un margine di sicurezza per rallentare la
propagazione nei primi minuti. Il requisito riguarda **solo il cladding**, non gli
arredi fissi. — *Guðrún, 21.07.2025*

`DECISIONE` La **scala fra ristorante e lobby** era stata omessa per errore dalla zona
verde: va inclusa, con pavimentazione **Cfl-s1**. — *Guðrún, 21.07.2025*

`NOTA` Disegni aggiornati con le aree B-s1,d0 ricevuti il **23.07.2025**
(`2. hæð - svæði 1`, `3. hæð - svæði 1`, `3. hæð - svæði 2`, rev. 250722).

---

#### 3. Claddings a parete — legno Haute

**Materiale** *(offerta Haute, via Carol 12.11.2024)*

| Voce | Valore |
|---|---|
| Codice | E-07 rovere evaporato nodato |
| Spessore | **16 mm** = 12 mm compensato pino cileno + 4 mm impiallacciatura rovere |
| Larghezze | 120 / 150 / 180 / 210 mm ca. |
| Lunghezze | 1.500 – 3.000 mm |
| Giunto | maschio-femmina, fuga **2 mm** per doga |
| Fornitura | grezzo |
| Quantità | 2.300 mq × € 75,00 = **€ 172.500** |

`DECISIONE` La vernice ignifuga si applica su **legno grezzo**, non sopra i cicli
esistenti. — *Carlo, 12.11.2024*

`DECISIONE` Aree non soggette a classe → finitura uguale al pavimento. Aree fire-rated
(corridoi) → vernice speciale applicata **in fabbrica**, insieme alle porte camera.
— *Carol, 12.11.2024*

`DECISIONE` **Elementi coinvolti:** ① cielino orizzontale del portale d'ingresso camera
② montante verticale attorno alla porta ③ pannello porta lato corridoio. Per uniformità
estetica si fa verniciare **① e ② (o anche ③) dallo stesso produttore delle porte**.
— *Carlo, 12.11.2024*

`ATTENZIONE` La vernice ignifuga ha resa più **"plastica"** e perdita del poro.
Campionatura raccomandata. — *Carlo, 12.11.2024 e 20.01.2026*

---

#### 4. Pavimenti in legno

`VINCOLO` Pavimenti **Dfl-s1**; vani scala **Cfl-s1**.

`APERTO` **Il pavimento Haute soddisfa Cfl-s1?** Domanda di Perla a Fabrizia e Carol del
**14.11.2024** — nessuna risposta conclusiva in cartella.

| Voce | mq | €/mq | Totale |
|---|---|---|---|
| Fornitura pavimento | 2.000 | 75,00 | € 150.000 |
| Ciclo misto (primer Renner acqua + Natural Living) | 2.000 | 25,00 | € 50.000 |
| Ciclo acrilico (primer + acrilico opaco alta resistenza) | 2.000 | 17,00 | € 34.000 |

`DECISIONE` Il parquet arriva **già verniciato dalla fabbrica** col ciclo misto.
— *Carol, 12.11.2024*

**Posa e sottofondo** *(Giuseppe / Haute, via Carlo 03.01.2025)*
- Massetto: planare nelle due direzioni, senza avvallamenti, compatto, asciutto.
  Specifica di progetto **max 2 mm su 3 m**.
- **Primer** sul cemento per compattare e garantire adesione (recepito da Basalt nello
  spec book — *Perla, 06.01.2025*).
- Posa **incollata OBBLIGATORIA** con riscaldamento a pavimento.
- Posa **flottante** dove serve isolamento acustico, con underlay specifico.

`DECISIONE` **Lobby, restaurant e library**: underlay **Damtec black uni 2 mm**
(indicazione dell'acoustic engineer), pavimento **flottante con riscaldamento**.
— *Perla, 06.01.2025*

**Vernici ignifughe** *(Haute / consulenti Renner, 08.01.2025)* — finitura **10 gloss**,
tre cicli campionati su rovere evaporato nodato: ① **BFL-S1** ② **B-S1,D0** ③ **ciclo
misto** (riferimento estetico). Ogni configurazione anche al 50% della grammatura.

---

#### 5. Porte → dettaglio completo in **MR - Doors**

`VINCOLO` Porte nelle aree marcate: **B-s1,d0** in reazione al fuoco, oltre a EI30/EI60.

`DECISIONE` Trattamento ignifugo di porte e portali affidato al **produttore delle porte**.

`DECISIONE` **Questione "porte da spedire in Danimarca" chiarita**: la norma citata da
Javerk **non si applica a Bergamaschi**. Riguarda solo i fornitori islandesi, o chi vuole
immettere porte sul mercato islandese **senza avere le licenze**. Bergamaschi dovrebbe
averle tutte. — *Hartmann Kárason, 22.05.2026*

`APERTO` **Inviare a Bergamaschi** le linee guida islandesi tradotte
(`Fire_Resistant_Internal_Doors_Guidelines_EN.pdf`, ricevuto 22.05.2026).

`NOTA` Matteo (Alart): *"EI si usa solo sulle porte"*; per gli altri elementi il fire
consultant deve indicare classe 0 o 1. — *via Carlo, 23.10.2024*

---

#### 6. Scale, parapetti e bachelite

`APERTO` Delle **due scale**, solo una è campita nelle tavole fireproof. **Entrambe hanno
la bachelite, ma è soprattutto quella campita a dover essere fireproof.** — *Carol, 21.10.2024*

**Materiale parapetti:** stratificato **HPL (ABET PRINT HPL)**, inizialmente creduto
resina fenolica. — *Matteo (Alart), via Carlo 23.10.2024*

`DECISIONE` **Sopra i 6 mm di spessore** si raggiunge la classe corretta. — *Carol, 23.10.2024*

`APERTO` Chiarire cosa siano le categorie **CGF e CGS** in scheda tecnica — nessuna risposta.

`NOTA` Le schede HPL non riportano EI60: i disegni si riferiscono probabilmente alla
**parte strutturale** della scala, non ai parapetti.

---

#### 7. Arredi fissi — ⚠️ regola diversa fra Fire e BREEAM

`DECISIONE` **Lato FUOCO gli arredi NON devono rispettare alcuna classe.** Il vincolo
riguarda solo il legno Haute per **boiserie e pavimento**. — *Carol, 13.11.2024*,
confermato da EFLA per la library (21.07.2025).

⚠️ **Attenzione:** lato **BREEAM** vale l'opposto — gli arredi **fissi** (avvitati o
inchiodati all'edificio) **sono inclusi** in Hea02 e Mat03. Vedi *MR - BREEAM §2*.
Le due regole convivono e non vanno confuse.

`NOTA` Carlo aveva proposto (13.11.2024) di coinvolgere un **consulente italiano** per
verificare tutto sul lato arredo. Proposta decaduta perché gli arredi erano risultati
fuori ambito *fuoco* — ma la successiva scoperta BREEAM (feb. 2025) ha riaperto di fatto
il tema su un altro fronte.

---

#### 8. Nodo critico — la prova al fuoco (gen–feb 2026)

**Il problema, come posto da Carlo il 20.01.2026:**

1. Alart porta evidenza da un proprio cantiere: **rovere lastronato + vernice ICA
   fireproof** ha raggiunto **B-s2** dopo prova al fuoco.
2. Mountain richiede **B-s1,d0** per claddings, porte e cielini.
3. Scoperta chiave: la verniciatura ignifuga **non conferisce automaticamente la classe**.
   Le normative europee richiedono una **prova al fuoco effettiva**, ed è quella a
   determinare e certificare il grado.
4. Conseguenza: **il solo fatto di usare legno è sufficiente a non rispettare B-s1,d0.**
5. Haute conferma: i tentativi sul **massello** con bagni chimici **non** hanno alzato il
   rating — ed era Haute stesso ad aver indirizzato verso la verniciatura ignifuga.
6. Rilievo di Carlo: il fire consultant avrebbe dovuto allertare il team molto prima.

**Risposta EFLA — Guðrún Júlía, 06.02.2026** *(giudicata evasiva da Carol)*

| Domanda | Risposta |
|---|---|
| Serve la prova al fuoco? | **Nessun requisito specifico di test** se la vernice ha già una **classificazione certificata** B,s2 o B,s1-d0 |
| Certificazione per componente? | **Non necessaria** per ogni componente |
| Valutazione localizzata / B-s2? | **Sì per le pareti**: grazie agli **sprinkler** è possibile un assessment per accettare **B,s2-d0 sul cladding a parete** |
| Cielini | **Sempre B,s1-d0**, nessuna deroga |

`DECISIONE` **Si separa il destino di pareti e cielini**: pareti verso B,s2-d0 (via
assessment); **cielini vincolati a B,s1-d0**.

`APERTO` **Prodotto alternativo suggerito da EFLA: `Protega Novatherm 1FR`** — verificare
se consente B,s1-d0 dove serve. **Nessuna risposta successiva: aperto da oltre 5 mesi.**

`NOTA POSITIVA` A marzo 2026 il campione reale di verniciatura ignifuga sulle porte
camera ha dato **ottimo risultato estetico** — vedi *MR - Doors §5*.

---

#### 9. Punti aperti — Fire

| # | Punto | Dal | Owner |
|---|---|---|---|
| 1 | **Protega Novatherm 1FR**: fattibilità per B,s1-d0 (cielini) | 06.02.2026 | Carlo / EFLA |
| 2 | Formalizzare l'**assessment B,s2-d0 pareti** sfruttando gli sprinkler | 06.02.2026 | EFLA |
| 3 | Inviare a **Bergamaschi** le linee guida porte tradotte | 22.05.2026 | Carlo / Carol |
| 4 | Confermare se il **pavimento Haute soddisfa Cfl-s1** | 14.11.2024 | Fabrizia / Carol |
| 5 | Riconciliare la **contraddizione sul sistema di aggancio** (Marcos vs Guðrún) | 19.11.2024 | Carlo / EFLA |
| 6 | Chiarire categorie **CGF / CGS** della bachelite HPL | 23.10.2024 | Carol |

---

### MR - Doors

#### 1. Storia della fornitura

| Fase | Fornitore | Esito |
|---|---|---|
| 2023 | **Lualdi** | Prime liste e preventivi; abaco porte set. 2023 |
| 2024 | **Lualdi** (prev. lug. 2024) → **Bergamaschi** | Passaggio a Bergamaschi da nov. 2024 |
| 2025–26 | **Bergamaschi F.lli** | Progettazione + offerte 358 / 368 / 383 |
| mar. 2026 | ⚠️ riapertura | Si valutano offerte alternative (vedi §4) |

`DECISIONE` **Lualdi non poteva realizzare i due risalti laterali** della parete in
calcestruzzo attorno alla porta: li avrebbe fatti in legno, che **non raggiunge la classe
al fuoco richiesta**. Non è obbligatorio farli in calcestruzzo — il contractor può usare
altri materiali di pari classe. — *Carol, 07.06.2023*

`NOTA` Quei risalti servono a mantenere l'isolamento acustico e **non possono far parte
della porta**: vanno installati prima. Compaiono nei dwg per via dello spessore del
cladding; tornando al disegno precedente il cladding sporge **20 mm invece di 50**.

`DECISIONE` **Porta d'ingresso camera: 42 dB** certificati in laboratorio (Lualdi),
mantenuti con posa corretta. — *Fabrizia, 07.06.2023*

#### 2. Bergamaschi — progettazione e offerte

- **Progettazione porte: € 4.500**, pagata il 31.07.2025. Quattro tipologie:
  ① interne a vetro ad anta (senza telaio) ② interne a vetro scorrevoli (senza telaio)
  ③ interne in legno ad anta con telaio ④ interne in legno scorrevoli. — *Giovanni B., 27.01.2025*
- **Offerte:** n°358 porte interne (nov. 2024 → agg. gen. 2026 → agg. giu. 2026 con abaco
  aperture motorizzate) · n°368 porte esterne · n°383 "3rd part" (dic. 2024).

#### 3. Dettagli costruttivi

`DECISIONE` **Il falso telaio va mantenuto**: è importante per l'allineamento della porta
rispetto alla boiserie esterna. — *Giovanni Bergamaschi, 04.08.2025*

`NOTA` **Luce netta**: originale 835 mm; a porta aperta a 90° gli spigoli si allineano e
il passaggio scende a **~820 mm**. — *Egidio Bergamaschi, 01.08.2025*

`VINCOLO` Richieste di Carlo sul costruttivo (01.08.2025): il **portale in corridoio deve
essere staccato dal muro**; lavorare a parità di rustico; indicare la porta aperta per
rilevare la luce netta; usare lo stesso disegno del costruttivo boiserie interna/esterna;
indicare spessori del legno Haute e stratigrafia.

`DECISIONE` **Pareti Lemga** (gasbeton, divisori camera/bagno): i portali in bachelite si
possono **ancorare direttamente con tasselli e viti tradizionali, senza controtelaio** —
purché si usino viti e cappucci corretti. — *Óliver Ás / Marcos (Basalt), 26.08.2025*

`DECISIONE` **Serrature: sistema TESA i-minimal** per le porte hotel. — *Fabrizia, 25.11.2025*

#### 4. Snodo di marzo 2026 — costo e secondo fornitore

`ATTENZIONE` L'ultima offerta Bergamaschi vale **≈ 840.000 €**. Hartmann la giudica molto
alta; il board ha chiesto se ci fossero sempre state due offerte. **Javerk** si è offerto
di procurare l'offerta di un contractor che produce porte su misura.

`DECISIONE` **Tenere aperta la possibilità di cambiare fornitore porte fino alla firma
dell'offerta finale**; procurarsi almeno un'altra offerta verificando la qualità.
— *Hartmann Kárason, 18.03.2026*

#### 5. Verniciatura ignifuga — esito del campione

`DECISIONE` **Il campione è riuscito bene.** Processo validato:
Haute invia le doghe a Bergamaschi → Bergamaschi **fresa le fughe** fra le doghe, le
**assembla su un pannello di supporto** e applica la **vernice ignifuga**.
Un secondo pannello non trattato va ad Alart per la finitura protettiva interna
(non ignifuga), così da confrontare le due finiture affiancate. — *Carol, 18.03.2026*

`DECISIONE` **Fare il test Xeno** per la protezione dall'ingiallimento UV: *"Its so
important for the future operation to make sure we are getting long lasting coating that
doesn't get yellow after few years"*. Carol deve procurare le offerte.
— *Hartmann, 18.03.2026*

`APERTO` Budget del test Xeno: va incluso nel pacchetto mock-up room? Nessuna risposta.

`APERTO` Rivedere anche il **campione finale del pavimento ignifugo** verniciato
direttamente da Haute: servono **due classi diverse** (scale e pavimenti aree comuni) e la
classe è cambiata rispetto al campione precedente.

#### 6. Abachi e liste

- **MR_2025.10_Doors Schedule** (14.10.2025): due liste Excel delle porte da produrre
  Bergamaschi (in verde quelle già nelle loro offerte). ⚠️ Serve un controllo: alcune
  porte sono state aggiunte rispetto alla quotazione, altre hanno **codici errati**.
  Planimetrie con codici porte interne/esterne + abaco completo. Dettagli nel CAD
  `5_03_XX_01` per la mock-up room; nuovo disegno per la porta di connessione **#QQC 5.170**.
- **Liste 14.11.2025** per l'incontro Bergamaschi (colonne ridotte, meno islandese).

`APERTO` Da chiarire con Bergamaschi (dal 14.10.2025):
- come realizzare le **porte esterne SPA con contrappeso** (peso al posto del chiudiporta)
- come intendono realizzare le **porte d'ingresso principali** di SPA e Hotel

#### 7. Modifiche porte esterne

`DECISIONE` **#QQC 7.303** → cambiata in **porta in alluminio**, fornita dal contractor
(corridoio hotel 3° piano, accanto alla suite). — *Guðjón (Basalt), 17.11.2025*

`DECISIONE` **#QQC 7.111** → rivestita internamente in legno da sauna (porta esterna della
sauna grande nella grotta). **Carol: va fatta in Islanda, non da Bergamaschi.** — *20.11.2025*

---

### MR - Claddings Portals

#### 1. Allineamento tecnico Basalt ↔ Haute (nov. 2024)

`ATTENZIONE` **Discrepanza di spessore.** Il modello Basalt aveva pannelli Haute da
**20 mm**; la doga reale è da **16 mm** (12 compensato + 4 rovere). Impatta su
**ceiling plans, dettagli porte e altro**. — *Marcos Zotes, 19.11.2024*

`ATTENZIONE` **Rischio imbarcamento.** Una doga Haute da 900 mm nell'ufficio Basalt
risulta già **visibilmente imbarcata**. Marcos chiede se la posa proposta lo prevenga nel
tempo. — *19.11.2024* — nessuna risposta tecnica conclusiva in cartella.

**Posa** *(Carlo, 18.11.2024)*: si fissa prima la struttura, poi si fissano le doghe alla
struttura. Separazione pannello/muro in cls: **15 mm**.

**Angoli e terminali:** si assume taglio a **45°** o pezzo d'angolo massello `[DA CONFERMARE]`.

`APERTO` **Claddings in zone umide (*wet areas*)**: il trattamento differisce da quello dei
corridoi, o è identico a meno del fire rating? Domanda di Perla del **19.11.2024**, senza
risposta.

`DECISIONE` **Metodo di comunicazione con Alart:** Alart non parla inglese, quindi niente
call collettive. Basalt raccoglie **tutte le domande in un unico pacchetto**, con un
**file separato per le domande sulla vernice ignifuga** (conversazione a sé, che coinvolge
il fornitore della vernice e Haute). — *Carol, 19.11.2024*

#### 2. Quantità cladding

`DECISIONE` **Il cladding fireproof è compreso nel totale, non aggiuntivo:**

```
Wall cladding totale        2.527,82 m²
  di cui fireproof            288,51 m²
  ordinario (per differenza) 2.239,31 m²
```
— *Magda Soja (Basalt), 05.03.2025; confermato da Fabrizia il 14.03.2025*

`NOTA` Il fire-rated cladding delle *connection* è disponibile anche **suddiviso per
piano** (13.03.2025), necessario per allocare i mq nel budget.

#### 3. Portali e RFI

`APERTO` **RFI 198** (21.05.2026): il contractor chiede il disegno **5-19-XX-04**
(finitura del vano porta fra camera e vanity), **mai pubblicato**. I disegni 5-04-XX-26 e
5-04-XX-75 vi fanno riferimento. Serve per definire lo spessore materiali e la dimensione
del foro **prima di iniziare la piastrellatura**. Marcos segnala che lo spessore è
comunque indicato in `5_03_XX_01` dettaglio 1.

`NOTA` Thread *MR-ROOMS Portal DT DRW* (27–28.05.2026) e riunione Teams **"Per portali"**
del 28.05.2026 fra Carol, Carlo e Fabrizia.

---

### MR - Ceiling

`DECISIONE` Nella quotazione vanno inclusi anche i **ceiling slits (legno e metallo)** —
verificato con Hartmann. — *Fabrizia, 17.03.2025*

**Quantificazione cielini** *(Magda Soja, Basalt, 18.03.2025 — `Ceiling quantification.xlsx`)*
- *Interior slit ceiling*: suddiviso **per aree**.
- *Exterior slit ceiling*: calcolato **senza suddivisione**, tranne la super suite (separabile su richiesta).
- Il cielino Haute è conteggiato **dentro il file wall cladding**, non a parte.

**Wooden coves — quantità a modello** *(André Motta Vieira, Basalt, 04.05.2026;
lunghezza totale, non superficie)*

| Codice | Tipo | Lunghezza |
|---|---|---|
| 5.2.10.2 | L cove 150×200 mm | 80,1 m |
| 5.2.10.3 | L curtain cove 220×200 mm | 97,0 m |
| 5.2.10.4 | **H cove 190×200 mm** | **232,9 m** |
| 5.2.10.5 | L curtain cove 240×175 mm | 7,3 m |
| 5.2.10.6 | L curtain cove 170×165 mm | 120,0 m |

⚠️ Per la **H cove** ci saranno "boxes" per calare gli impianti: **non inclusi** nel calcolo.

**Riferimenti disegno coves** *(André, 16.06.2026)*
- Piante controsoffitto: `5_06_01_04`, `5_06_02_04`, `5_06_02_06`, `5_06_03_04` — riportano
  la posizione di tutte le coves.
- Dettagli: `5_03_XX_14` (profili 5.2.10.4 e 5.2.10.6) · Sezione `7_03_XX_92` (profilo 5.2.10.3).
- I profili **5.2.10.2 e 5.2.10.5 non hanno dettaglio**: sono varianti dimensionali degli altri.

`DECISIONE` Thread coves chiuso: *"Carol ha in mano l'offerta, i numeri erano giusti e i
disegni li avevamo"*. — *Carlo, 16.06.2026*

---

### MR - Flooring

**Quantità a modello ARK** *(Perla Dís, 28.10.2024)*

```
Pavimento in legno              714,74 m²
  + su scale                    112,16 m²
Wood cladding (totale)        2.283,04 m²
```

⚠️ **Non incluso:** pannelli a soffitto Haute ed esterni.

`NOTA` **Discrepanza di lettura:** Carlo calcolava 1.940 m² di cladding. Perla spiega che
i numeri non sono confrontabili: la lista Carlo include **claddings a parete + porte +
mobili**, mentre il modello ARK conta **solo i claddings appesi alle pareti** — non il
rivestimento porte (estraibile dal modello) né i mobili (non a modello).

`DECISIONE` Serve un **breakdown** e una riunione di coordinamento sul workflow di
quantità e prezzi. — *Perla, 28.10.2024* → sfociato nei breakdown di marzo 2025 (§Claddings).

---

### MR - Stones

**Requisiti di spessore** *(Pétur Jónsson, landscape architect EFLA, via Marcos 28.11.2025)*

| Ambito | Spessore |
|---|---|
| Pietre carrabili (auto) | **70 mm** |
| Aree pedonali (ingressi 1° e 3° piano, bike room) | **50 mm** |
| Balconi edificio principale e super suite | 30 mm (idealmente 50) |

⚠️ **Vincolo strutturale:** per far entrare 50 mm nella bike room e negli ingressi hotel
occorre **abbassare la soletta in calcestruzzo** — la distanza attuale non basta.
**Va confermato subito.**

**Superfici** *(Carol, 28.11.2025)*

```
tunnel            347 m²   parzialmente carrabile (ruote auto vicino alla piazzola)
balconi           362 m²   solo pedonale
equipment room    142 m²   solo pedonale
```

**Posizione fornitore (Pedretti)** *(via Carlo, 28.11.2025)*
- **2/5 cm è la variabilità dello spessore**, non una misura: la pietra esce a spacco e
  viene divisa fra sottili e spesse.
- Il **porfido valtellinese** si posa su base di sabbia-cemento e si mette a pari con un
  martelletto di legno.

`DECISIONE (proposta Carlo)` Fissare **2/5 cm pedonale e carrabile** · **4/8 cm giganti**.
**7 cm non è un'opzione.**

`APERTO` ① Le pietre in foto richiedono necessariamente 2/5? ② Gli islandesi hanno capito e
accettano la **variabilità di spessore**? ③ Ingombro totale dei pavimenti inclusi gli
inerti di sottofondo. ④ Cosa si intende per "pezzatura normale"?

---

### MR - BREEAM

#### 1. Certificazioni dei materiali

| Fornitore | EPD | ISO 14001 | FSC / altro |
|---|---|---|---|
| **Haute Material** | ❌ | ❌ | ✅ **FSC** (azienda) |
| **Gruppo Emilceramica** (piastrelle) | ✅ | ✅ | — |

- Haute è certificata **FSC come azienda**; i singoli materiali si certificano
  individuando la partita in approvvigionamento. In una dichiarazione **FSC Mix** la
  quota certificata/riciclata non può scendere sotto il **70%** — requisito rispettato.
  Coperti in particolare **abete e rovere** → ok per i legni ossidati selezionati.
  — *Francesco Saccaro (Haute), 30.01.2023 e 30.08.2023*
- **Legni finalisti:** E07 rovere nodoso evaporato · A12 rovere di palude ·
  A-04 abete ossidato grigio · A16 ontano ossidato.
- **Meccanica del punteggio** *(Carlo, 30.08.2023)*: per BREEAM servono **minimo 14
  materiali in EPD**; si contano i prodotti (2 essenze = 2 punti) e conta la quantità.
  ISO14001 è più lunga da ottenere ma vale come coefficiente. All'epoca **ne mancavano 4**.
- `DECISIONE` Lato piastrelle **siamo ok**: tutto il gruppo Emilceramica ha EPD e ISO14001.
  — *Carol, 30.08.2023*

#### 2. ⚠️ Svolta di febbraio 2025 — gli arredi fissi rientrano in BREEAM

Fino a quel momento il team assumeva che **solo le finiture interne** dovessero
rispettare i requisiti, non gli arredi custom.

`DECISIONE` **Gli arredi fissi SONO inclusi** in Hea 02 e Mat 03. Risposta ufficiale BRE:
*"Integral fittings" = tutti i fitting integrati/fissati (avvitati o inchiodati)
all'edificio*. Solo l'arredo **freestanding** è escluso (scrivanie, sedie, scaffalature
mobili). — *Sigurður Loftur Thorlacius (EFLA), 03.02.2025*

⚠️ **Non confondere con la regola FUOCO**, dove invece gli arredi sono esclusi (*MR - Fire §7*).

**Hea 02 — Qualità dell'aria interna (limiti di emissione)**

| Tipo prodotto | Formaldeide | TVOC | Cancerogeni 1A/1B |
|---|---|---|---|
| Vernici e rivestimenti interni | ≤ 0,06 mg/m³ | ≤ 1,0 mg/m³ | ≤ 0,001 mg/m³ |
| Prodotti a base legno (incl. pavimenti) | ≤ 0,06 (non-MDF) / ≤ 0,08 (MDF) | ≤ 1,0 | ≤ 0,001 |
| Materiali per pavimentazione | ≤ 0,06 | ≤ 1,0 | ≤ 0,001 |
| Cielini, pareti, isolanti acustici/termici | ≤ 0,06 | ≤ 1,0 | ≤ 0,001 |
| Adesivi e sigillanti interni | ≤ 0,06 | ≤ 1,0 | ≤ 0,001 |

Le vernici devono inoltre rispettare i **limiti di contenuto TVOC** (tab. 19): pareti e
soffitti opachi 10 g/l · lucidi 40 · vernici per legno e metallo 90 · primer 15 ·
coating bicomponenti per pavimenti 80. Le vernici in **ambienti umidi** devono proteggere
dalla muffa.

`NOTA OPERATIVA` Conviene cercare le **etichette ambientali riconosciute** invece di
chiedere i test di laboratorio: Blue Angel, Danish Indoor Climate Labelling (Cl. 1 e 2),
eco-INSTITUT, EMICODE EC1PLUS/EC1/EC2, FloorScore, GREENGUARD (Certified e Gold), GUT,
Indoor Advantage Gold, Indoor Air Comfort (e Gold/USA), M1, natureplus, TÜV SÜD.
*(dettagli in `GN22`, allegato alla mail del 03.02.2025)*

**Mat 03 — Approvvigionamento responsabile**
- **Tutto il legno deve avere certificazione PEFC o FSC.**
- Punti aggiuntivi se il produttore ha **ISO 14001 / EMAS**, preferibilmente anche a monte.
- I **materiali riusati** danno il punteggio massimo.

#### 3. VOC — intersezione con Fire e Flooring

`VINCOLO` Oli, vernici e collanti di **tutti i pavimenti fissi e i rivestimenti a parete**
devono rispettare i requisiti VOC **HEA02 criterio 10**. — *Perla Dís, 06.01.2025*

`DECISIONE` Haute conferma che **entrambi i cicli proposti soddisfano** i requisiti VOC
HEA02 criterio 10. — *via Carlo, 08.01.2025*

`APERTO` **Schede tecniche in inglese.** Le schede inviate erano in italiano; Perla le ha
richieste in inglese (16.01.2025 e 19.02.2025): *"I unfortunately do not understand
italian nor does Breeam"*. Serve anche indicare **dove sono i valori VOC** nella scheda.
Nessun seguito.

---

### MR - Budget

#### 1. Budget preliminare 2024 (Carlo)

Impianto del dataset consegnato a Blue Lagoon il 28.10.2024 — **~4 M€**:

| Colonna | Valori |
|---|---|
| `SCOPE` | **SCOPE1** = arredo (come i B&B del Retreat) · **SCOPE2** = riferito all'edificio ed extra · **OUT OF SCOPE** = costi monitorati, fuori dai 4 M€ |
| `STATUS` | **ESTIMATION** (stima Carlo) · **QUANTIFIED** (dal fornitore, al mq) · **QUANTIFIED IN DETAIL** (focus specifico + disegno tecnico → costo esatto) · **OFFER** (offerta ufficiale) |

`ATTENZIONE` Avvertenza esplicita di Carlo: *"APPLY A CONTINGENCY ON IT, SINCE IT WAS
BASED ON PLACEHOLDER DESIGN VOLUMES, NOT ON TECH DRAWINGS"*. Il budget era costruito sul
**modello Rhino 3D**, non aggiornato né dettagliato. Per una stima corretta servono
pacchetto disegni e BOQ.

**Note dello stesso invio:**
- **Haute claddings nelle camere: il costo potrebbe dimezzarsi (~200 K€ di risparmio)**
  usando **doghe di parquet invece di pannelli**. Da approfondire.
- **Porte NON incluse** — il costo reale è il doppio di quanto a listino nella presentazione.
- Le camere sono quotate in dettaglio; il resto è stima preliminare al mq.
- I *loose* sono numeri placeholder: nessun arredo era ancora selezionato.

#### 2. Budget list 2025

`DECISIONE` Struttura della lista (Rev 01, 05.03.2025): un record per item con
**dimensioni** e **data di revisione** — al rilascio successivo, se la data cambia
significa che c'è stata una modifica. Allegate le planimetrie con le etichette dei custom
per piano.

`APERTO` Manca il **codice numerico di Hartmann** come colonna a sé — necessario per
comparare i dataset. — *Carlo, 04.03.2025*

#### 3. Cost control 2026 — Lárus (Consulto)

Da giugno 2026 la stima generale dei costi passa a **Sigurdur Lárus Holm (Consulto)**,
che costruisce il *Dashboard* e la cost estimation per la banca.

`DECISIONE` **Contingency applicate da Lárus:** **5%** produzione · **7%** spedizione ·
**10%** vitto e alloggio. — *via Carol, 26.06.2026*

`DECISIONE` La **spedizione** in budget è aggiornata con le stime di Blue Lagoon, quindi
**più alte del preventivo di Matteo**.

`APERTO` **Stima delle ore-uomo** da adesso a fine costruzione / fine 2027 — richiesta da
Lárus, non ancora consegnata. — *15.06.2026*

`APERTO` **Idea per ridurre i costi di vitto/alloggio:** dare a tutti i montatori un
**intero rifugio con cucina**; Blue Lagoon fornisce la materia prima e cucinano da soli.
Motivazione dichiarata: *"Il cibo di Javerk fa veramente orrore, nessuno di noi ha mai
osato avvicinarsi"*. Carol chiede a Carlo se è fattibile. — *26.06.2026*

`NOTA` **Javerk deve movimentare** e posizionare le casse dell'arredo al piano giusto
dell'hotel con **gru** o altro mezzo — da tenere nei costi.

`APERTO` Porte: mancano ancora **3 porte di Javerk** nei conteggi. — *26.06.2026*

---

### MR - BOQ RFQ

#### 1. Pacchetti inviati ad Alart (mag–giu 2026)

| Data | Contenuto |
|---|---|
| 25.05.2026 | `MR_lista materiali` |
| 26.05.2026 | `MR_materiali e lista cladding` |
| 29.05.2026 | **Aggiornamento BOQ** (correzione codici) |
| 04.06.2026 | Ripubblicazione pacchetto disegni — cartella unica *Custom Furniture drawings* |

#### 2. ⚠️ Correzione codici BOQ

`DECISIONE` Riscontrate **incongruenze fra i codici dei disegni e quelli della BOQ**.
I **disegni trasmessi sono corretti**; il problema riguarda solo alcuni codici in BOQ.
Excel di raccordo con codifica a colori:

```
rosso    codici errati
verde    codici corretti da usare in sostituzione
azzurro  codici aggiunti
```

Inoltre **4 disegni non erano stati inclusi nell'esportazione** per errore.
— *Fabrizia, 29.05.2026*

#### 3. Disegni mancanti

`DECISIONE` Verificato che tutti i disegni ci sono, tranne tre — **correttamente assenti
perché quegli item non vanno quotati ora, mancando il disegno**:

```
5_19_03_43   H_BS battery shelf
5_19_03_76   H_YR low cabinet
5_19_03_19   R_SS Fireplace
```
— *Fabrizia, 04.06.2026* — coerente con i flag `NO DRAWING` nella BOQ Excel.

---

### MR - Offer Approvals

#### Mock-up room Alart — iter di approvazione (lug. 2026)

| Data | Evento |
|---|---|
| 16.06.2026 | Preventivo **162** Rif. Montain Mock Up Room |
| 18.06.2026 | **Rev 2** — annulla e sostituisce la precedente |
| 16.07.2026 | Offerta **firmata da Hartmann** |
| 16.07.2026 | Carlo trasmette ad Alart l'offerta approvata **con esclusioni** |
| 17.07.2026 | Alart emette **fattura d'acconto nr. 0000139** (50%) |
| 20.07.2026 | **Pagamento confermato** da Jón Bjarni (Nonni) |

`DECISIONE` **Item esclusi** dall'offerta approvata (non barrati nel documento, quindi da
segnalare esplicitamente):
- `5-6-1-1` **Room Entrance Door**
- `5_19_XX_44` **ST_CO Cleaning Trolley Cabinet**

`VINCOLO` **Intestazione fattura obbligatoria:** Rauðukambar ehf. · ID 510816-0640 ·
Urriðaholtsstræti 2-4 · 210 Garðabær · Iceland. Serve fattura **NON pro forma**.

`NOTA` Urgenza dichiarata: sbloccare l'**ingegnerizzazione** e rispettare le tempistiche
**prima della chiusura estiva italiana**. — *Hartmann e Fabrizia, 16.07.2026*

---

### MR - Design Concept

#### Registro item — commenti e modifiche per singolo codice

> Questa è la sezione dove confluiscono **tutti i commenti per item**, qualunque sia la
> cartella d'origine della mail.

**`5_19_XX_12` — R_SU sofa sideboard (Suite)** · BOQ: 9 pz · 4.260 €/pz · 38.340 €

| Data | Evento |
|---|---|
| 17.07.2026 (BOQ) | Flag **"FORSE DA ELIMINARE"** |
| 16.07.2026 | **Carol:** non lo facciamo, per via del divano letto scelto che è molto profondo. Da aggiornare il cladding dietro al divano e verificare le prese |
| 17.07.2026 | **Fabrizia:** non si può eliminare del tutto se vogliamo mantenere le prese elettriche. Verrà modificato in revisione → **mantenerlo nel costo per ora** |
| 23.07.2026 | **Emesso disegno V2** `5_19_XX_12-R_SU_sofa sideboard_V2` (PDF + DWG). Revisione resa necessaria dall'aggiornamento del modello di divano. **Sostituisce integralmente la versione precedente**: per la mock-up room fare riferimento **solo alla V2** |

**`5_19_XX_44` — ST_CO cleaning trolley cabinet (corridoio)**
`DECISIONE` **Passa a Javerk**, esce dallo scope Alart. In BOQ risulta `DELETED`
(mail 16.07.2026), COUNT azzerato da 9 a 0. — *Carol e Fabrizia, 16–17.07.2026*

**`5-6-1-1` — Room entrance door**
`DECISIONE` **Cancellata da Hartmann.** Escluso anche il **montaggio delle porte
d'ingresso camere** dallo scope Alart.

**`5_19_XX_90` — R_ST/SU shower shelf**
`DECISIONE` Falso allarme: Carol segnalava un doppio conteggio (4 = 2+2 invece di 2), ma
Fabrizia ha verificato che **nell'offerta firmata sono già conteggiate correttamente**.

**`5_19_XX_96` — R_SU rectangular mirror** *(nuovo item)*
`DECISIONE` Aggiunto uno **specchio supplementare**, fattura simile a quello del bagno ma
proporzioni diverse. Disegnato da Fabrizia il 17.07.2026 (PDF + DWG) e inviato ad Alart
per quotazione e produzione.
`VINCOLO` **Carol:** verificare l'allineamento fra specchio bagno e specchio camera;
mantenere la **stessa larghezza**, cambiare **solo la lunghezza**.

**`5_19_XX_94` — R_BTH rectangular mirror** · BOQ: 39 pz · 446 €/pz · 17.394 €
`APERTO` Flag BOQ **"DRW Modifiche dim"** (mail 17.07.2026): disegno da aggiornare con le
nuove dimensioni e quotazione da riverificare.

**`5_19_03_43` H_BS battery shelf · `5_19_03_76` H_YR low cabinet · `5_19_03_19` R_SS Fireplace**
`APERTO` **NO DRAWING** — non quotati. Vanno prodotti disegno e quotazione, o va
confermata l'esclusione.

**`5_19_01_51` — S_CR changing rooms locker (SPA)** · 144 pz
`APERTO` **Due opzioni economiche aperte in BOQ**, differenza ~113 K€:
- base **1.445 €/pz** → 208.080 € (box HPL-ARPA, facce Fenix full colour)
- alternativa **660 €/pz** (MDF hydro plated, box laminato, bordi ABS, facce Fenix HPL, lighting escluso)

**`#QQC 7.303` / `#QQC 7.111`** → vedi *MR - Doors §7*.
**`#QQC 5.170`** — porta di connessione, nuovo dettaglio nel CAD `5_03_XX_01`.

`NOTA` Il file **`MR_Casework list_V3.xlsx`** (allegato 23.07.2026) è la **lista interna
che tiene il conto di tutte le modifiche richieste finora**: è il riferimento da usare
per la tracciabilità delle revisioni item.

---

### MR - Lighting

#### 1. Attori

| Fornitore | Ambito |
|---|---|
| **DGA S.p.A.** | Apparecchi illuminanti **custom** (es. *Tono Jack*, faretto testaletto, luci lettura) |
| **Forma Lighting** | **Millwork luminaires** — lampade integrate nei mobili |
| **Apir** | Placche (interruttori, testata letto) rivestite in pelle |
| **D'Alesio & Santoro** | Coordinamento lighting |

#### 2. Ordine Forma Lighting

`DECISIONE` Offerta **26/01618** → ordine **26/01278**. Fatturazione a
**Rauðukambar / Islanda**, consegna a **ALART, Via Grigna 4, 22060 Figino Serenza (CO)**.
Pagamento confermato 03.07.2026. **Spedizione 15.07.2026 — DHL tracking 5846516174**.
⚠️ Forma Lighting chiusa per ferie **10–14 agosto**.

#### 3. Mock-up room — DGA

`DECISIONE` DGA ha **già prodotto tutte le componenti** degli apparecchi del mock-up ed è
**in attesa delle piastre complete di pelle** per ultimare il montaggio. — *Ada Pugi, 22.07.2026*

`DECISIONE` DGA invia il **DWG del Tono Jack** e può spedire un **campione grezzo** di
scatola posteriore + piastra assemblati. — *22.07.2026*

`APERTO` Confermare a DGA l'**indirizzo di spedizione** del campione e le **tempistiche di
riconsegna** delle piastre. ⚠️ DGA chiusa **10–21.08.2026**, ultime spedizioni **04.08**.

#### 4. Ripartizione placche Apir / DGA

`DECISIONE` Chiarito un fraintendimento: **l'interruttore centrale lo fa Apir**, pelle
compresa. Quello che Apir **non** riesce a fare sono le **2 luci lettura prodotte da DGA**.
**Alart si occupa solo di queste**, con la stessa pelle usata da Apir. Ne consegue che ad
Alart **il campione dell'interruttore non serve**. — *Carol Tayar, 20.07.2026*

`NOTA` Blue Lagoon ha già una placca Apir molto simile (con un solo switch, completa di
modulo posteriore): Carol la porta di persona, invece di aspettare la produzione di quella
definitiva. Serve comunque come **riferimento di misure e ingombri**. — *Fabrizia, 20.07.2026*

#### 5. ⚠️ Rischi tecnici sollevati da Carlo (20.07.2026)

Richiesta di metodo: **ogni elemento da integrare va fornito in almeno 1 campione
completo**, cavetti e driver inclusi, così da provare anche l'effetto luminoso.
*"Così evitiamo comunicazioni, rework e sorprese."*

- **Spinotto femmina del jack DGA** — influisce sulla costruzione del mobile e della barra.
  Va definito il **processo di sostituzione in caso di danneggiamento**.
- ⚠️ **Dall'esperienza Trenitalia quel dettaglio si danneggia frequentemente.** Va testato
  ora, altrimenti DGA rischia di dover cambiare il sistema più avanti.
- **Magneti**: potrebbero essere troppo forti o troppo deboli — da provare sul riscontro
  verniciato.
- Se la **barra sarà in alluminio** servirà un **riscontro in ferro**: influisce sullo sviluppo.

---

### MR - Suppliers

#### MR - ALART — *Alart Wood Special Contract*
Via Grigna 4a, 22060 Figino Serenza (CO) · Matteo Ariosto · +39 393 9277458

**Preventivi 2026** (rif. commessa 2026/260111)

| N° | Oggetto | Data |
|---|---|---|
| 142 | Montain | 22.05 → 27.05 (intestazione corretta + traduzione EN) |
| 147 | Montain | 27.05 |
| 152 | Montain | 04.06 |
| 153 | **Claddings** | 05.06 |
| 154 | **Casework** | 05.06 |
| 162 | **Mock Up Room** → Rev 2 | 16.06 → 18.06 |

`DECISIONE` **Stima installazione** *(Matteo, 06.06.2026)* — ipotizzando **10 persone da
subito**:

```
Notti      118  (su 5 camere doppie)
Pasti    2.360  totali
Voli            compresi nel preventivo
Esclusi         eventuale tecnico Alart + Carlo
```

`APERTO` **Date trasferta Islanda**: Carlo propone partenza **ven 26**, rientro **dom 28**
(o 29). Matteo chiede quanto impiega un camion dedicato per l'Islanda — **7 giorni?**

`DECISIONE` **Pelle:** Alart sta lavorando **sia ecopelle sia pelle vera**. — *21.07.2026*

`NOTA` Alart ha inviato le **schede HPL** (23.10.2024) e i dettagli parete/portale (mag. 2026).

#### MR - APIR
Apir srl, Via Prato delle Valli 58, 47892 Acquaviva (RSM) · Lorenzo Angelini · rif. **BLUE LAGOON**

`DECISIONE` Fornitura pelle per le placche: **1 m² complessivo, spaccata 0,8 mm**
(non 1,0). **Alart fornisce solo il materiale**, taglio e applicazione li fa **Apir**.
Strisce da **45 cm** vanno bene: placca alta **82 mm**, larghezza variabile, con margine e
scarto. — *Lorenzo Angelini, 21–22.07.2026*

#### MR - BERGAMASCHI
Bergamaschi F.lli Srl, Via Cesare Pavese 470, 21042 Caronno Pertusella (VA)
→ contenuto operativo in **MR - Doors §2–5**

#### MR - HAUTE · MR - LUALDI · MR - PEDRETTI
Cartelle **vuote**: il materiale su questi fornitori è distribuito nelle cartelle
tematiche (Haute in Flooring/Claddings/BREEAM, Lualdi in Doors, Pedretti in Stones).

---

### MR - Logistic

#### 1. Spedizione container Italia → Islanda (giu. 2026)

**Preventivo via Alart:** **8–9 K€ per container** (fonte: Matteo, quantificato da
Gianesini). Assicurazione **esclusa**, in corso di quantificazione.

```
Resa          franco caricato su container a Figino Serenza → DAP destino
Container     H40'HC  (non "ice cube", troppo alto per l'uso)
Peso max      merce + tara ≤ 30 tonnellate
```

**Incluso:** posizionamento da Figino Serenza in intermodale su Rotterdam (2 h di
franchigia al carico, poi **€ 100/container/ora** + port congestion surcharge) · THC
d'imbarco + ISPS + B/L · operazioni doganali d'esportazione, tasse portuali e gate-in ·
nolo mare incl. addizionali VATOS · spese di sbarco a destino · delivery con 2 h di
franchigia allo scarico.

**Extra:** visite doganali · pesatura VGM **€ 200/container** se non effettuata da noi ·
dem/det/port storage a destino.

⚠️ **Operazioni doganali d'importazione, dazi e tasse sono a carico del cliente.**

**Routing:** partenze settimanali da Rotterdam **ogni mercoledì**.
Ultimo giorno utile di carico: mercoledì settimana A → partenza nave Rotterdam mercoledì
settimana B → arrivo porto di Reykjavík domenica settimana B.

#### 2. ⚠️ Correzione della destinazione

`DECISIONE` **DAP Grindavík è sbagliato.** *"Perché Grindavik? Non ha senso, non siamo in
Blue Lagoon. Devi dare il riferimento di Mountain."* Il paese più vicino è **Árnes**, il
porto più vicino è **Þorlákshöfn**. — *Carol Tayar, 25.06.2026*

`APERTO` Va stabilito se i **container restano in sito**, quanti e per quanto tempo — non
è considerato nel preventivo.

`NOTA` Contatto **DB Schenker** Jakob Hafstein non è più in azienda →
Nenad Srdic / `sala@torcargo.com`.

`NOTA` Feb. 2023 — logistica **pickup campioni Haute** gestita da Stefanía Huld
Gylfadóttir (Blue Lagoon).

---

### MR - BIM

`DECISIONE` Il **BIM manual** del progetto è `BEP_Mountain Baths_v1.1.pdf`, pubblicato su
**Ajour**. La versione originale era solo in islandese; la **versione inglese** è stata
caricata su Ajour da **Hjörtur Pálsson (Optimum)** il **01.09.2022** e girata al team DGI.

**Referenti BIM:** Optimum — Hjörtur Pálsson, Jóhann Guðmundsson, Ingvar Birgisson.

---

### MR - Design Development · MR - Planning

Cartelle **vuote**. Il contenuto di sviluppo progetto è di fatto distribuito fra
*Design Concept*, *Claddings Portals* e *Doors*.

---

### MR - Various UNPROCESSED ⏸

**885 email, 2017 → 2022.** È l'archivio della **fase concept** del progetto, quando si
chiamava *Mountain Baths* / *Highland Baths*: presentazioni DGI, coordinamento con Basalt
e Highland Baths (Magnús Orri Schram), lavorazioni su changing rooms, suite, mockup room,
scala, VR/Unreal, masterplan.

`APERTO` **Non processata in questa passata.** La cartella è esplicitamente etichettata
*UNPROCESSED* dall'utente e ha un ordine di grandezza (885 mail) e una natura (materiale
concept 2017–2022, in larga parte superato dalle fasi successive) diversi dalle cartelle
tematiche. Va deciso se, e con quale profondità, estrarne le decisioni storiche.

---

# WORK - PROJECTS (altri progetti)

## TRENITALIA

> Da popolare. Tema aperto noto: blocco condizionatore Freccia Point n.2 (gocciolamento
> dopo sostituzione motore) e ritiro del motore sostituito.

## RETREAT IMPROVEMENTS · JACOB&DAVID

> Da popolare.

# WORK - MANAGEMENT · WORK - VARIOUS

> Da popolare.
