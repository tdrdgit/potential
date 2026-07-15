# Regole email & progetti — Carlo Casagrande

> File di regole vivo: lo miglioriamo nel tempo. È servito dal connettore tramite il
> comando `get_email_rules`. Quando l'utente scrive **"Recap email"**, segui la
> procedura qui sotto.

## Caselle da consultare
- **`carlo@carlocasagrande.com`** — su Aruba → usa questo connettore
  (`list_unread_emails`, `list_recent_emails`, `search_emails`, `get_email`).
- **`carlo@potential.contractors`** — su Google Workspace → usa il **connettore Gmail**
  (deve essere collegato nell'app Claude). Se il connettore Gmail non è disponibile,
  segnalalo e prosegui con la sola casella Aruba.

## Progetti in corso
Referenti **cliente** e **fornitore** per ciascun progetto. Nota: alcuni referenti
sono **condivisi** tra progetti → da soli NON bastano per attribuire una mail.

### 1. Mountain Retreat
- **Cliente:** Fabrizia Sabatino, Carol Tayar
- **Fornitori:** Matteo Ariosto (Alart), Giuseppe Pruneri (Haute),
  Giovanni Bergamaschi (Bergamaschi), Formalighting, DGA

### 2. Blue Lagoon Retreat Improvements
- **Cliente:** Fabrizia Sabatino, Carol Tayar
- **Fornitori:** Matteo Ariosto (Alart), Giuseppe Pruneri (Haute),
  Giovanni Bergamaschi (Bergamaschi)

### 3. Trenitalia
- **Cliente:** Paolo Priolo
- **Fornitore:** Matteo Ariosto (Alart)

## Come attribuire una mail a un progetto
I referenti condivisi (es. Fabrizia Sabatino, Carol Tayar, Matteo Ariosto) NON sono
sufficienti da soli. Attribuisci in quest'ordine:
1. **Parole‑chiave / nome progetto** nell'oggetto o nel corpo — es. "Mountain
   Retreat", "Blue Lagoon", "Trenitalia", nomi di località, codice/numero commessa,
   nome del cantiere o della fornitura.
2. **Contesto del thread** — oggetto ricorrente, allegati, riferimenti a ordini o
   preventivi già associati a un progetto.
3. **Combinazione referente + fornitore + argomento** quando i punti sopra non
   bastano (es. Paolo Priolo → quasi sempre Trenitalia; Formalighting/DGA → Mountain
   Retreat).
4. Se resta **ambiguo**, NON forzare: metti la mail sotto **"⚠️ Progetto incerto"**,
   elenca gli indizi trovati e **chiedi conferma** all'utente.

## Procedura "Recap email"
Trigger: l'utente scrive **"Recap email"**.
1. **Leggi** le mail non lette + recenti di **entrambe** le caselle (vedi sopra).
2. **Raggruppa** e presenta in quest'ordine:
   - **📁 Progetti** — con **sotto‑raggruppamento per progetto** (Mountain Retreat,
     Blue Lagoon Retreat Improvements, Trenitalia, ed eventuale "⚠️ Progetto incerto").
   - **👤 Personali** — mail personali/non di lavoro.
   - **🗂️ Altre mail / Spam** — newsletter, promozioni, notifiche, sospette.
   Per ogni mail mostra: **mittente**, **oggetto**, **data**, e **casella** di
   provenienza (carlocasagrande / potential).
3. **Attendi istruzioni.** Dopo il recap, l'utente potrà chiederti di:
   - **segnare come lette** alcune mail (`mark_email_read`);
   - **spostarle** in cartelle specifiche (`move_email`; crea la cartella con
     `create_folder` se non esiste). Sul lato Gmail (potential) usa il connettore
     Gmail per etichettare/archiviare.
   Non segnare come letto né spostare **nulla** finché l'utente non lo chiede.

## Note / da migliorare
- Aggiungere qui alias e parole‑chiave specifiche man mano che emergono (nomi
  cantiere, codici commessa, indirizzi email esatti dei referenti).
- Definire, quando l'utente le comunicherà, i nomi esatti delle **cartelle** di
  destinazione per progetto.
