#!/usr/bin/env python3
"""Compila RA-MR-ACTION TRACKER con i topic aperti, stile Potential."""

from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

# ---------------------------------------------------------------- brand
RED      = "C71617"   # primario Potential
GREY     = "D9D9D9"   # neutro secondario Potential
INK      = "000000"
WHITE    = "FFFFFF"
ZEBRA    = "F7F6F6"
SOFT_RED = "FBE9E9"

F = "Arial"
hdr_font  = Font(name=F, size=9,  bold=True, color=WHITE)
sub_font  = Font(name=F, size=9,  bold=True, color=INK)
body_font = Font(name=F, size=9,  color=INK)
mut_font  = Font(name=F, size=8.5, color="6E6664")
h1_font   = Font(name=F, size=16, bold=True, color=INK)
eyebrow   = Font(name=F, size=8,  bold=True, color=RED)

hdr_fill   = PatternFill("solid", fgColor=RED)
grey_fill  = PatternFill("solid", fgColor=GREY)
zebra_fill = PatternFill("solid", fgColor=ZEBRA)

thin = Side(style="thin", color="D6D2D1")
box  = Border(left=thin, right=thin, top=thin, bottom=thin)
top  = Alignment(vertical="top", wrap_text=True)
topl = Alignment(vertical="top", horizontal="left", wrap_text=True)
topc = Alignment(vertical="top", horizontal="center", wrap_text=True)

DATEFMT = "DD/MM/YYYY"

wb = Workbook()

# =================================================================== TO-DO
ws = wb.active
ws.title = "TO-DO"

TODO_COLS = [
    ("TO-DO ID", 10), ("AMBITO", 15), ("DATA RICHIESTA", 13),
    ("OWNER / DESTINATARIO", 22), ("RICHIESTA (azione attesa)", 62),
    ("ORIGINE (CH-xxx / mail / meeting)", 30), ("CANALE", 10),
    ("PRIORITA", 11), ("GG APERTO", 11), ("DUE DATE", 12), ("STATO", 12),
    ("DATA EVASIONE", 13), ("ULTIMO SOLLECITO", 15), ("NOTE", 46),
]

# id, ambito, data, owner, richiesta, origine, canale, prio, due, stato, note
TODO = [
 ("TD-001","FIRE",date(2026,2,6),"EFLA - Gudrun",
  "Confermare se Protega Novatherm 1FR consente di raggiungere B,s1-d0 sui cielini",
  "mail 06.02.2026 - Fire proof rating in corridors","Mail","ALTA",None,"Aperto",
  "Prodotto suggerito da EFLA. I cielini non hanno deroga. Nessuna risposta dopo il 6 febbraio."),
 ("TD-002","FIRE",date(2026,2,6),"EFLA - Gudrun",
  "Formalizzare l'assessment che accetta B,s2-d0 sul cladding a parete",
  "mail 06.02.2026 - Fire proof rating in corridors","Mail","ALTA",None,"Aperto",
  "Possibile grazie alla presenza dell'impianto sprinkler. Mai messo per iscritto."),
 ("TD-003","FIRE",date(2026,5,22),"CARLO",
  "Inoltrare a Bergamaschi le linee guida porte islandesi tradotte in inglese",
  "mail 22.05.2026 - Hartmann Karason","Mail","MEDIA",None,"Aperto",
  "All. Fire_Resistant_Internal_Doors_Guidelines_EN.pdf. La norma sulla Danimarca non si applica a Bergamaschi."),
 ("TD-004","FIRE",date(2024,11,14),"BL DESIGN - Fabrizia",
  "Confermare se il pavimento in legno Haute soddisfa la classe Cfl-s1",
  "mail 14.11.2024 - Perla Dis","Mail","MEDIA",None,"Aperto",
  "Domanda posta da Perla a BLD. Nessuna risposta conclusiva in archivio."),
 ("TD-005","FIRE",date(2024,11,19),"EFLA - Gudrun",
  "Riconciliare se il sistema di aggancio dietro i claddings debba essere B,s1-d0",
  "mail 19.11.2024 Marcos / 21.07.2025 Gudrun","Mail","MEDIA",None,"Aperto",
  "Basalt: non si applica se chiuso e non raggiungibile dal fuoco. EFLA: i telai di supporto sono soggetti."),
 ("TD-006","FIRE",date(2024,10,23),"BL DESIGN - Carol",
  "Chiarire con il referente islandese le categorie CGF e CGS della bachelite HPL",
  "mail 23.10.2024","Mail","BASSA",None,"Aperto",
  "Sopra i 6 mm di spessore la classe corretta e' comunque raggiunta."),

 ("TD-007","DOORS",date(2026,3,18),"BL - Hartmann",
  "Procurare una seconda offerta porte e decidere se confermare Bergamaschi",
  "mail 18.03.2026 - Hartmann Karason","Mail","ALTA",None,"Aperto",
  "Offerta Bergamaschi ~840.000 EUR. Javerk puo' procurare un'alternativa. Liberi di cambiare fino alla firma."),
 ("TD-008","DOORS",date(2026,3,18),"BL DESIGN - Carol",
  "Richiedere le offerte per il test Xeno sull'ingiallimento UV",
  "mail 18.03.2026 - Hartmann Karason","Mail","MEDIA",None,"Aperto",
  "Decidere se il costo entra nel pacchetto mock-up room."),
 ("TD-009","DOORS",date(2026,3,18),"HAUTE",
  "Produrre i campioni del pavimento ignifugo nelle due classi richieste",
  "mail 18.03.2026 - Carol Tayar","Mail","MEDIA",None,"Aperto",
  "Scale e aree comuni hanno classi diverse. La classe e' cambiata dopo il campione precedente."),
 ("TD-010","DOORS",date(2025,10,14),"BERGAMASCHI",
  "Definire come realizzare le porte esterne SPA con contrappeso",
  "mail 14.10.2025 - MR_2025.10 Doors Schedule","Mail","MEDIA",None,"Aperto",
  "Peso al posto del chiudiporta tradizionale."),
 ("TD-011","DOORS",date(2025,10,14),"BERGAMASCHI",
  "Definire come realizzare le porte d'ingresso principali di SPA e Hotel",
  "mail 14.10.2025 - MR_2025.10 Doors Schedule","Mail","MEDIA",None,"Aperto",
  "Modalita' realizzativa mai definita."),
 ("TD-012","DOORS",date(2025,10,14),"BL DESIGN - Fabrizia",
  "Verificare codici errati e porte aggiunte nelle liste rispetto alle offerte",
  "mail 14.10.2025 - MR_2025.10 Doors Schedule","Mail","MEDIA",None,"Aperto",
  "Alcune porte aggiunte dopo la quotazione, altre con codici sbagliati."),

 ("TD-013","CLADDINGS",date(2026,5,21),"BL DESIGN - Fabrizia",
  "Pubblicare il disegno 5-19-XX-04 richiesto dal contractor",
  "RFI 198 del 21.05.2026","RFI","ALTA",None,"Aperto",
  "BLOCCA L'INIZIO DELLA PIASTRELLATURA. Finitura vano porta camera/vanity. Spessori in 5_03_XX_01 dett.1."),
 ("TD-014","CLADDINGS",date(2024,11,19),"CARLO",
  "Chiudere la discrepanza di spessore cladding: 20 mm a modello vs 16 mm reali",
  "mail 19.11.2024 - Marcos Zotes","Mail","ALTA",None,"Aperto",
  "Impatta ceiling plans e dettagli porte. Sollevata da Basalt, mai chiusa formalmente."),
 ("TD-015","CLADDINGS",date(2024,11,19),"HAUTE",
  "Confermare che la posa prevenga l'imbarcamento delle doghe da 16 mm",
  "mail 19.11.2024 - Marcos Zotes","Mail","ALTA",None,"Aperto",
  "Una doga da 900 mm in Basalt risulta gia' visibilmente imbarcata. Nessuna risposta tecnica."),
 ("TD-016","CLADDINGS",date(2024,11,19),"HAUTE",
  "Chiarire se i claddings in zone umide richiedono un trattamento diverso",
  "mail 19.11.2024 - Perla Dis","Mail","MEDIA",None,"Aperto",
  "Differisce da quello dei corridoi o e' identico a meno del fire rating?"),

 ("TD-017","BOQ / ITEM",date(2026,7,25),"BL - Hartmann",
  "Scegliere l'opzione locker SPA 5_19_01_51: 1.445 EUR/pz o 660 EUR/pz",
  "BOQ RA-MR-PROJECT TRACKER","BOQ","ALTA",None,"Aperto",
  "144 pezzi. Differenza ~113.000 EUR. Base HPL-ARPA Fenix full colour vs MDF hydro laminato."),
 ("TD-018","BOQ / ITEM",date(2026,7,17),"BL DESIGN - Fabrizia",
  "Aggiornare il disegno 5_19_XX_94 con le nuove dimensioni e far riquotare",
  "BOQ / mail 17.07.2026","Mail","ALTA",None,"Aperto",
  "Specchio bagno. 39 pezzi per 17.394 EUR. Flag BOQ: DRW Modifiche dim."),
 ("TD-019","BOQ / ITEM",date(2026,7,16),"BL DESIGN - Carol",
  "Decidere in fase di revisione se 5_19_XX_12 sofa sideboard resta o esce",
  "mail 16.07.2026 - Carol Tayar","Mail","MEDIA",None,"Aperto",
  "Tenuto a costo per non perdere le prese elettriche. V2 emessa il 23.07 dopo il cambio di divano."),
 ("TD-020","BOQ / ITEM",date(2026,6,4),"BL DESIGN - Fabrizia",
  "Produrre i disegni mancanti o escludere formalmente i tre item non quotati",
  "mail 04.06.2026 - Fabrizia Sabatino","Mail","MEDIA",None,"Aperto",
  "5_19_03_43 battery shelf / 5_19_03_76 low cabinet / 5_19_03_19 fireplace."),
 ("TD-021","BOQ / ITEM",date(2026,7,25),"CARLO",
  "Mantenere aggiornato questo Action Tracker a ogni nuova azione o decisione",
  "Registro progetti","Interno","MEDIA",None,"In corso",
  "Regola di progetto: se una disposizione non e' nel registro, non esiste."),

 ("TD-022","LIGHTING",date(2026,7,22),"CARLO",
  "Confermare a DGA l'indirizzo campione e le tempistiche di rientro delle piastre",
  "mail 22.07.2026 - Ada Pugi","Mail","ALTA",date(2026,8,4),"Aperto",
  "DGA chiusa 10-21.08, ultime spedizioni 04.08. DGA ha gia' prodotto tutte le componenti."),
 ("TD-023","LIGHTING",date(2026,7,20),"DGA",
  "Fornire spinotto jack e campione completo di cavetti e driver per i test",
  "mail 20.07.2026 - Carlo Casagrande","Mail","ALTA",None,"Aperto",
  "Dall'esperienza Trenitalia il dettaglio si danneggia spesso. Va testato ora il processo di sostituzione."),
 ("TD-024","LIGHTING",date(2026,7,20),"DGA",
  "Verificare la forza dei magneti sul riscontro verniciato",
  "mail 20.07.2026 - Carlo Casagrande","Mail","MEDIA",None,"Aperto",
  "Se la barra sara' in alluminio serve un riscontro in ferro: influisce sullo sviluppo."),

 ("TD-025","STONES",date(2025,11,28),"BASALT",
  "Confermare l'abbassamento della soletta per accogliere pietre da 50 mm",
  "mail 28.11.2025 - Marcos Zotes","Mail","ALTA",None,"Aperto",
  "Bike room e ingressi hotel: la distanza attuale non basta. E' opera strutturale, serve conferma subito."),
 ("TD-026","STONES",date(2025,11,28),"BL DESIGN - Carol",
  "Far accettare al cliente la variabilita' di spessore 2/5 cm del porfido",
  "mail 28.11.2025 - Carlo Casagrande","Mail","MEDIA",None,"Aperto",
  "Proposta: 2/5 pedonale e carrabile, 4/8 giganti. 7 cm non e' un'opzione."),
 ("TD-027","STONES",date(2025,11,28),"PEDRETTI",
  "Fornire l'ingombro totale dei pavimenti inclusi gli inerti di sottofondo",
  "mail 28.11.2025 - Carol Tayar","Mail","MEDIA",None,"Aperto",
  "Chiarire anche cosa si intende per pezzatura normale."),

 ("TD-028","BUDGET",date(2026,6,15),"BL DESIGN - Carol",
  "Consegnare la stima delle ore-uomo da adesso a fine 2027",
  "mail 15.06.2026 - Sigurdur Larus Holm","Mail","ALTA",None,"Aperto",
  "Serve a Larus per la cost estimation destinata alla banca."),
 ("TD-029","LOGISTIC",date(2026,6,25),"ALART",
  "Correggere la destinazione del preventivo trasporti: da Grindavik ad Arnes",
  "mail 25.06.2026 - Carol Tayar","Mail","ALTA",None,"Aperto",
  "Grindavik e' Blue Lagoon, non Mountain. Porto corretto: Thorlakshofn."),
 ("TD-030","LOGISTIC",date(2026,6,25),"BL DESIGN - Carol",
  "Definire quanti container restano in sito e per quanto tempo",
  "mail 25.06.2026","Mail","MEDIA",None,"Aperto",
  "Non considerato nel preventivo da 8-9 KEUR a container."),
 ("TD-031","LOGISTIC",date(2026,6,25),"ALART",
  "Quantificare l'assicurazione sul trasporto",
  "mail 25.06.2026","Mail","MEDIA",None,"Aperto",
  "Esclusa dal preventivo, in corso di quantificazione."),
 ("TD-032","BUDGET",date(2026,6,26),"CARLO",
  "Valutare la fattibilita' del rifugio con cucina per i montatori",
  "mail 26.06.2026 - Carol Tayar","Mail","MEDIA",None,"Aperto",
  "BL fornisce la materia prima, i montatori cucinano. Ipotesi per abbattere i costi di vitto."),
 ("TD-033","BUDGET",date(2026,6,26),"JAVERK",
  "Fornire le tre porte mancanti nei conteggi del budget",
  "mail 26.06.2026 - Carol Tayar","Mail","MEDIA",None,"Aperto",
  "Il budget porte non e' chiudibile finche' non rientrano."),

 ("TD-034","BREEAM",date(2025,2,3),"BL DESIGN - Carol",
  "Verificare la conformita' BREEAM Hea02/Mat03 di tutti gli arredi fissi custom",
  "mail 03.02.2025 - Sigurdur Loftur Thorlacius","Mail","ALTA",None,"Aperto",
  "Da feb 2025 gli arredi avvitati o inchiodati all'edificio rientrano. Il team assumeva il contrario."),
 ("TD-035","SUPPLIERS",date(2026,7,22),"ALART",
  "Produrre e spedire ad Apir 1 mq di pelle spaccata 0,8 mm in strisce da 45 cm",
  "mail 22.07.2026 - Lorenzo Angelini","Mail","ALTA",None,"Aperto",
  "Taglio e applicazione sulle placche a cura di Apir. Rif. spedizione: BLUE LAGOON."),
 ("TD-036","BREEAM",date(2025,2,19),"HAUTE",
  "Fornire le schede tecniche in inglese con i valori VOC evidenziati",
  "mail 19.02.2025 - Perla Dis","Mail","MEDIA",None,"Aperto",
  "Le schede italiane non sono utilizzabili per BREEAM. Richieste due volte, nessun seguito."),
 ("TD-037","SUPPLIERS",date(2026,6,6),"ALART",
  "Confermare le date della trasferta in Islanda e la durata del trasporto",
  "mail 06.06.2026 - Matteo Ariosto","Mail","MEDIA",None,"Aperto",
  "Proposta partenza ven 26 / rientro dom 28-29. Camion dedicato: sette giorni?"),
]

# --- intestazione documento
ws["A1"] = "MOUNTAIN RETREAT  ·  FIT-OUT & CUSTOM INTERIORS"
ws["A1"].font = eyebrow
ws["A2"] = "Action Tracker — azioni aperte"
ws["A2"].font = h1_font
ws["A3"] = ("Ogni riga e' un'azione attesa da un destinatario preciso. "
            "GG APERTO e' calcolato: si aggiorna da solo a ogni apertura del file.")
ws["A3"].font = mut_font
ws.merge_cells("A1:N1"); ws.merge_cells("A2:N2"); ws.merge_cells("A3:N3")
for r in (1, 2, 3):
    ws.row_dimensions[r].height = {1: 14, 2: 24, 3: 14}[r]
for c in range(1, 15):
    ws.cell(row=4, column=c).fill = grey_fill
ws.row_dimensions[4].height = 4

HDR = 5
for i, (name, width) in enumerate(TODO_COLS, start=1):
    c = ws.cell(row=HDR, column=i, value=name)
    c.font, c.fill, c.border = hdr_font, hdr_fill, box
    c.alignment = topc if i in (7, 8, 9, 11) else topl
    ws.column_dimensions[get_column_letter(i)].width = width
ws.row_dimensions[HDR].height = 26

for n, row in enumerate(TODO):
    r = HDR + 1 + n
    tid, amb, dreq, own, req, orig, chan, prio, due, stato, note = row
    vals = [tid, amb, dreq, own, req, orig, chan, prio,
            f'=IF(C{r}="","",TODAY()-C{r})', due, stato, None, None, note]
    for i, v in enumerate(vals, start=1):
        c = ws.cell(row=r, column=i, value=v)
        c.font, c.border = body_font, box
        c.alignment = topc if i in (7, 8, 9, 11) else top
        if i in (3, 10, 12, 13):
            c.number_format = DATEFMT
        if n % 2 == 1:
            c.fill = zebra_fill
    ws.cell(row=r, column=1).font = Font(name=F, size=9, bold=True, color=INK)
    ws.row_dimensions[r].height = 30

LAST = HDR + len(TODO)
ws.freeze_panes = f"A{HDR+1}"
ws.auto_filter.ref = f"A{HDR}:N{LAST}"

# priorita' ALTA in rosso
ws.conditional_formatting.add(
    f"A{HDR+1}:N{LAST}",
    FormulaRule(formula=[f'$H{HDR+1}="ALTA"'],
                font=Font(name=F, size=9, bold=True, color=RED), stopIfTrue=False))
# fermo da oltre 180 giorni: fondo rosso tenue
ws.conditional_formatting.add(
    f"I{HDR+1}:I{LAST}",
    FormulaRule(formula=[f'AND($I{HDR+1}<>"",$I{HDR+1}>180)'],
                fill=PatternFill("solid", fgColor=SOFT_RED), stopIfTrue=False))
# righe chiuse in grigio
ws.conditional_formatting.add(
    f"A{HDR+1}:N{LAST}",
    FormulaRule(formula=[f'$K{HDR+1}="Evaso"'],
                font=Font(name=F, size=9, color="9A9A9A"), stopIfTrue=False))

OWNERS = ("BL DESIGN - Carol,BL DESIGN - Fabrizia,CARLO,ALART,HAUTE,BERGAMASCHI,"
          "DGA,APIR,PEDRETTI,FORMA LIGHTING,BASALT,EFLA - Gudrun,EFLA - Sigurdur,"
          "JAVERK,BL - Hartmann,BL - Nonni,BL - Siggi,BL - Lalli,CONSULTO - Larus")
dv_own = DataValidation(type="list", formula1=f'"{OWNERS}"', allow_blank=True)
dv_sta = DataValidation(type="list", formula1='"Aperto,In corso,Sollecitato,Bloccato,Evaso"', allow_blank=True)
dv_pri = DataValidation(type="list", formula1='"ALTA,MEDIA,BASSA"', allow_blank=True)
dv_amb = DataValidation(type="list", allow_blank=True, formula1=
          '"FIRE,DOORS,CLADDINGS,CEILING,FLOORING,STONES,LIGHTING,BOQ / ITEM,'
          'BUDGET,LOGISTIC,BREEAM,SUPPLIERS,DESIGN DEV,ALTRO"')
for dv, col in ((dv_own, "D"), (dv_sta, "K"), (dv_pri, "H"), (dv_amb, "B")):
    ws.add_data_validation(dv)
    dv.add(f"{col}{HDR+1}:{col}{LAST+120}")

# =================================================================== CHANGE LOG
cl = wb.create_sheet("CHANGE LOG")
CL_COLS = [
    ("CHANGE LOG ID", 13), ("AMBITO", 14), ("DATA COMUNICAZIONE", 15), ("CANALE", 10),
    ("RIFERIMENTO (oggetto mail / meeting)", 38), ("DA CHI", 22),
    ("SHEET NUMBER (item BOQ)", 18), ("DESCRIZIONE DEL CAMBIO", 62),
    ("IMPATTO COSTO EUR", 14), ("IMPATTO TEMPI", 14), ("TRACCIATO IN BOQ", 13),
    ("COMUNICATO A", 20), ("STATO", 12), ("NOTE", 34),
]
CHANGES = [
 ("CH-001","BOQ / ITEM",date(2026,7,16),"Mail","Richiesta fattura per avvio produzione mock-up Alart",
  "BL DESIGN - Carol","5_19_XX_44",
  "Il cleaning trolley cabinet passa a Javerk ed esce dallo scope Alart",
  None,None,"SI","ALART","Chiuso","In BOQ risulta DELETED, COUNT azzerato da 9 a 0"),
 ("CH-002","BOQ / ITEM",date(2026,7,16),"Mail","Richiesta fattura per avvio produzione mock-up Alart",
  "BL - Hartmann","5-6-1-1",
  "Porta ingresso camera cancellata. Escluso anche il montaggio delle porte camera",
  None,None,"SI","ALART","Chiuso","Non barrata nel documento: segnalata a voce ad Alart"),
 ("CH-003","BOQ / ITEM",date(2026,7,23),"Mail","MR_Drawing Revision V2 - Sofa Sideboard for Suites",
  "BL DESIGN - Fabrizia","5_19_XX_12",
  "Emessa revisione V2 a seguito dell'aggiornamento del divano scelto. Sostituisce integralmente la precedente",
  None,None,"NO","ALART","Aperto","Per la mock-up room usare solo la V2"),
 ("CH-004","BOQ / ITEM",date(2026,7,17),"Mail","Richiesta fattura per avvio produzione mock-up Alart",
  "BL DESIGN - Carol","5_19_XX_96",
  "Aggiunto specchio supplementare: stessa larghezza di quello bagno, lunghezza diversa",
  None,None,"NO","ALART","Aperto","Disegno emesso da Fabrizia il 17.07"),
 ("CH-005","DOORS",date(2025,11,17),"Mail","MR - Interior doors, drawings and schedule",
  "BASALT","QQC 7.303",
  "Porta cambiata in alluminio e fornita dal contractor",
  None,None,"NO","BERGAMASCHI","Chiuso","Corridoio hotel 3F, accanto alla suite"),
 ("CH-006","DOORS",date(2025,11,20),"Mail","exterior doors",
  "BL DESIGN - Carol","QQC 7.111",
  "Porta rivestita in legno sauna all'interno. Da realizzare in Islanda, non da Bergamaschi",
  None,None,"NO","BERGAMASCHI","Chiuso","Porta esterna della sauna grande nella grotta"),
 ("CH-007","FIRE",date(2025,7,21),"Mail","MR_Clarifications on Fire Resistance Requirements",
  "EFLA - Gudrun","-",
  "La scala fra ristorante e lobby entra in zona verde e richiede pavimento Cfl-s1",
  None,None,"NO","BLD","Chiuso","Era stata omessa per errore dalla zonizzazione"),
 ("CH-008","FIRE",date(2024,11,13),"Mail","MR - Haute flooring",
  "EFLA - Gudrun","-",
  "Anche la prima parte del corridoio hotel al 2F e 3F richiede trattamento ignifugo",
  None,None,"NO","BLD, ALART","Chiuso","Correzione a Basalt: le vie di esodo hanno carico d'incendio limitato"),
 ("CH-009","FIRE",date(2026,2,6),"Mail","Fire proof rating in corridors",
  "EFLA - Gudrun","-",
  "Le pareti possono puntare a B,s2-d0 grazie agli sprinkler. I cielini restano vincolati a B,s1-d0",
  None,None,"NO","BLD","Aperto","Separa il destino di pareti e cielini. Vedi TD-001 e TD-002"),
 ("CH-010","BREEAM",date(2025,2,3),"Mail","Mountain Retreat - BREEAM requirements for fixed furniture",
  "EFLA - Sigurdur","-",
  "Gli arredi fissi rientrano in BREEAM Hea02 e Mat03. Solo il freestanding e' escluso",
  None,None,"NO","BLD, ALART","Aperto","Ribalta l'assunzione precedente del team. Vedi TD-034"),
 ("CH-011","CLADDINGS",date(2025,3,5),"Mail","MR_breakdown cladding sqm",
  "BASALT","-",
  "Cladding a parete totale 2.527,82 mq DI CUI 288,51 mq fireproof: non sono additivi",
  None,None,"SI","BLD","Chiuso","Confermato da Fabrizia il 14.03.2025"),
 ("CH-012","DOORS",date(2026,3,18),"Mail","Cladding and flooring",
  "BL DESIGN - Carol","-",
  "Validato il processo di verniciatura ignifuga porte: Haute invia le doghe, Bergamaschi fresa, assembla e vernicia",
  None,None,"NO","TUTTI","Chiuso","Esito estetico giudicato molto buono"),
]

cl["A1"] = "MOUNTAIN RETREAT  ·  FIT-OUT & CUSTOM INTERIORS"; cl["A1"].font = eyebrow
cl["A2"] = "Change Log — decisioni e modifiche"; cl["A2"].font = h1_font
cl["A3"] = ("Registra le disposizioni ricevute e le decisioni prese. "
            "Si scrive qui prima di preparare qualsiasi comunicazione.")
cl["A3"].font = mut_font
cl.merge_cells("A1:N1"); cl.merge_cells("A2:N2"); cl.merge_cells("A3:N3")
cl.row_dimensions[2].height = 24
for c in range(1, 15):
    cl.cell(row=4, column=c).fill = grey_fill
cl.row_dimensions[4].height = 4

for i, (name, width) in enumerate(CL_COLS, start=1):
    c = cl.cell(row=HDR, column=i, value=name)
    c.font, c.fill, c.border = hdr_font, hdr_fill, box
    c.alignment = topc if i in (4, 9, 10, 11, 13) else topl
    cl.column_dimensions[get_column_letter(i)].width = width
cl.row_dimensions[HDR].height = 26

for n, row in enumerate(CHANGES):
    r = HDR + 1 + n
    for i, v in enumerate(row, start=1):
        c = cl.cell(row=r, column=i, value=v)
        c.font, c.border = body_font, box
        c.alignment = topc if i in (4, 9, 10, 11, 13) else top
        if i == 3:
            c.number_format = DATEFMT
        if i == 9:
            c.number_format = '#,##0;(#,##0);-'
        if n % 2 == 1:
            c.fill = zebra_fill
    cl.cell(row=r, column=1).font = Font(name=F, size=9, bold=True, color=INK)
    cl.row_dimensions[r].height = 30

CL_LAST = HDR + len(CHANGES)
cl.freeze_panes = f"A{HDR+1}"
cl.auto_filter.ref = f"A{HDR}:N{CL_LAST}"
cl.conditional_formatting.add(
    f"A{HDR+1}:N{CL_LAST}",
    FormulaRule(formula=[f'$M{HDR+1}="Aperto"'],
                font=Font(name=F, size=9, bold=True, color=RED), stopIfTrue=False))
dv_bo = DataValidation(type="list", formula1='"SI,NO"', allow_blank=True)
dv_cs = DataValidation(type="list", formula1='"Aperto,Chiuso"', allow_blank=True)
for dv, col in ((dv_bo, "K"), (dv_cs, "M")):
    cl.add_data_validation(dv); dv.add(f"{col}{HDR+1}:{col}{CL_LAST+120}")

# =================================================================== DASHBOARD
db = wb.create_sheet("DASHBOARD", 0)
db["A1"] = "MOUNTAIN RETREAT  ·  FIT-OUT & CUSTOM INTERIORS"; db["A1"].font = eyebrow
db["A2"] = "Action Tracker"; db["A2"].font = Font(name=F, size=22, bold=True, color=INK)
db["A3"] = "Stato delle azioni aperte, per ambito e per destinatario"
db["A3"].font = mut_font
db.merge_cells("A1:F1"); db.merge_cells("A2:F2"); db.merge_cells("A3:F3")
db.row_dimensions[2].height = 30
for c in range(1, 7):
    db.cell(row=4, column=c).fill = grey_fill
db.row_dimensions[4].height = 4

def kpi(col, label, formula, lead=False):
    v = db.cell(row=6, column=col, value=formula)
    v.font = Font(name=F, size=20, bold=True, color=WHITE if lead else INK)
    v.fill = PatternFill("solid", fgColor=RED if lead else GREY)
    v.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    l = db.cell(row=7, column=col, value=label)
    l.font = Font(name=F, size=8, bold=True, color=WHITE if lead else "3B3535")
    l.fill = PatternFill("solid", fgColor=RED if lead else GREY)
    l.alignment = Alignment(horizontal="left", vertical="top", indent=1)

kpi(1, "AZIONI APERTE", '=COUNTIF(\'TO-DO\'!K:K,"Aperto")+COUNTIF(\'TO-DO\'!K:K,"In corso")', lead=True)
kpi(2, "PRIORITA ALTA", '=COUNTIFS(\'TO-DO\'!H:H,"ALTA",\'TO-DO\'!K:K,"<>Evaso")')
kpi(3, "FERME DA > 180 GG", '=COUNTIFS(\'TO-DO\'!I:I,">180",\'TO-DO\'!K:K,"<>Evaso")')
kpi(4, "EVASE", '=COUNTIF(\'TO-DO\'!K:K,"Evaso")')
kpi(5, "CAMBI REGISTRATI", '=COUNTA(\'CHANGE LOG\'!A6:A500)')
kpi(6, "CAMBI DA CHIUDERE", '=COUNTIF(\'CHANGE LOG\'!M:M,"Aperto")')
db.row_dimensions[6].height = 32
db.row_dimensions[7].height = 16
for i in range(1, 7):
    db.column_dimensions[get_column_letter(i)].width = 21

def block(start, title, items, key_col, cols=("A", "B", "C")):
    t = db.cell(row=start, column=1, value=title)
    t.font = Font(name=F, size=10, bold=True, color=INK)
    db.cell(row=start, column=1).border = Border(bottom=Side(style="medium", color=INK))
    for k in range(2, 4):
        db.cell(row=start, column=k).border = Border(bottom=Side(style="medium", color=INK))
    hs = ["VOCE", "APERTE", "DI CUI ALTA"]
    for j, h in enumerate(hs):
        c = db.cell(row=start + 1, column=1 + j, value=h)
        c.font = Font(name=F, size=8, bold=True, color=WHITE)
        c.fill = hdr_fill; c.border = box
        c.alignment = topl if j == 0 else topc
    for n, it in enumerate(items):
        r = start + 2 + n
        c0 = db.cell(row=r, column=1, value=it); c0.font = body_font; c0.border = box
        c1 = db.cell(row=r, column=2,
                     value=f'=COUNTIFS(\'TO-DO\'!{key_col}:{key_col},A{r},\'TO-DO\'!K:K,"<>Evaso")')
        c2 = db.cell(row=r, column=3,
                     value=f'=COUNTIFS(\'TO-DO\'!{key_col}:{key_col},A{r},\'TO-DO\'!H:H,"ALTA",\'TO-DO\'!K:K,"<>Evaso")')
        for c in (c1, c2):
            c.font = body_font; c.border = box
            c.alignment = Alignment(horizontal="center")
        if n % 2 == 1:
            for k in range(1, 4):
                db.cell(row=r, column=k).fill = zebra_fill
    return start + 2 + len(items)

AMBITI = ["FIRE", "DOORS", "CLADDINGS", "BOQ / ITEM", "LIGHTING", "STONES",
          "BUDGET", "LOGISTIC", "BREEAM", "SUPPLIERS"]
DEST = ["BL DESIGN - Carol", "BL DESIGN - Fabrizia", "CARLO", "ALART", "HAUTE",
        "BERGAMASCHI", "DGA", "BASALT", "EFLA - Gudrun", "BL - Hartmann",
        "PEDRETTI", "JAVERK"]
end1 = block(10, "PER AMBITO", AMBITI, "B")
block(end1 + 2, "PER DESTINATARIO", DEST, "D")

# =================================================================== LEGENDA
lg = wb.create_sheet("LEGENDA")
lg["A1"] = "MOUNTAIN RETREAT  ·  FIT-OUT & CUSTOM INTERIORS"; lg["A1"].font = eyebrow
lg["A2"] = "Legenda e regole d'uso"; lg["A2"].font = h1_font
lg.merge_cells("A1:B1"); lg.merge_cells("A2:B2")
lg.row_dimensions[2].height = 24
lg.column_dimensions["A"].width = 30
lg.column_dimensions["B"].width = 104

RULES = [
 ("REGOLA", "COSA SIGNIFICA"),
 ("Fonte di verita'",
  "Questo file e' il registro. La mail e' solo il mezzo di trasporto: se una disposizione non e' qui, non esiste."),
 ("Quando si scrive",
  "Prima di preparare qualsiasi comunicazione. Si registra il cambio, poi si scrive la mail, mai il contrario."),
 ("Data e canale",
  "Obbligatori su ogni riga: servono a ricostruire quando e come una disposizione e' stata data."),
 ("Destinatario",
  "La colonna OWNER / DESTINATARIO dice CHI deve agire, non chi ha segnalato. Una riga senza destinatario non e' un'azione."),
 ("Ambito",
  "Rispecchia le sottocartelle della casella MOUNTAIN RETREAT, cosi' il tracker e l'archivio mail restano allineati."),
 ("GG APERTO",
  "Calcolato con TODAY(): si aggiorna da solo. Oltre 180 giorni la cella si colora."),
 ("Valori ipotizzati",
  "Ogni costo, data o quantita' stimata va evidenziato finche' non e' confermato."),
 ("Un file, colonna OWNER",
  "Niente file separati per interlocutore: le azioni cambiano proprietario. Le viste per persona si ottengono filtrando."),
 ("Doppio controllo",
  "Un cambio e' chiuso solo se TRACCIATO IN BOQ = SI, COMUNICATO A e' valorizzato e le azioni che genera esistono nel TO-DO."),
 ("Solleciti",
  "Prima di mandare una nuova richiesta a un owner, filtrare il TO-DO su quell'owner con STATO diverso da Evaso."),
 ("Aggancio alla BOQ",
  "SHEET NUMBER usa lo stesso codice del foglio CUSTOM di RA-MR-PROJECT TRACKER.xlsx (es. 5_19_01_48)."),
 ("", ""),
 ("DESTINATARI AMMESSI",
  "BL DESIGN - Carol · BL DESIGN - Fabrizia · CARLO · ALART · HAUTE · BERGAMASCHI · DGA · APIR · PEDRETTI · "
  "FORMA LIGHTING · BASALT · EFLA - Gudrun · EFLA - Sigurdur · JAVERK · BL - Hartmann · BL - Nonni · BL - Siggi · "
  "BL - Lalli · CONSULTO - Larus"),
 ("STATI TO-DO", "Aperto · In corso · Sollecitato · Bloccato · Evaso"),
 ("PRIORITA", "ALTA · MEDIA · BASSA — la riga ALTA si colora di rosso in automatico"),
 ("", ""),
 ("MANUTENZIONE",
  "Ogni azione, decisione o appunto che emerge da email o riunioni va registrato qui PRIMA che altrove. "
  "Il registro docs/REGISTRO-PROGETTI.md e il PDF dei topic aperti sono derivati di questo file."),
]
for n, (a, b) in enumerate(RULES):
    r = 5 + n
    ca = lg.cell(row=r, column=1, value=a)
    cb = lg.cell(row=r, column=2, value=b)
    if n == 0:
        for c in (ca, cb):
            c.font, c.fill, c.border = hdr_font, hdr_fill, box
            c.alignment = topl
        lg.row_dimensions[r].height = 22
    else:
        ca.font = sub_font; cb.font = body_font
        ca.alignment = topl; cb.alignment = top
        if a in ("DESTINATARI AMMESSI", "STATI TO-DO", "PRIORITA", "MANUTENZIONE"):
            ca.fill = grey_fill; cb.fill = grey_fill
        lg.row_dimensions[r].height = 30 if len(b) > 110 else 22
        for c in (ca, cb):
            c.border = box

for s in wb.worksheets:
    s.sheet_view.showGridLines = False

OUT = "/home/user/potential/docs/RA-MR-ACTION-TRACKER_2026-07-25.xlsx"
wb.save(OUT)
print("saved:", OUT)
print("TO-DO:", len(TODO), "| CHANGE LOG:", len(CHANGES))
