#!/usr/bin/env python3
"""Topic aperti Mountain Retreat — PDF leggero, font base-14 non incorporati."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)

RED   = colors.HexColor("#C71617")
GREY  = colors.HexColor("#D9D9D9")
INK   = colors.HexColor("#000000")
INK2  = colors.HexColor("#3B3535")
MUT   = colors.HexColor("#6E6664")
HAIR  = colors.HexColor("#E2DEDD")
ZEB   = colors.HexColor("#F7F6F6")
MID   = colors.HexColor("#9A9A9A")

H, B = "Helvetica-Bold", "Helvetica"

def S(n, **k): return ParagraphStyle(n, **k)

st_eyebrow = S("e", fontName=H, fontSize=7,  textColor=RED,  leading=9,  spaceAfter=6,
               trackingAmount=1.2)
st_h1      = S("h1", fontName=H, fontSize=21, textColor=INK, leading=23, spaceAfter=3)
st_sub     = S("s", fontName=B, fontSize=9.5, textColor=MUT, leading=12)
st_meta    = S("m", fontName=B, fontSize=7.2, textColor=MUT, leading=9.5)
st_h2      = S("h2", fontName=H, fontSize=8.4, textColor=INK, leading=10, trackingAmount=1)
st_cnt     = S("c", fontName=H, fontSize=7,  textColor=MUT, leading=10, alignment=TA_RIGHT)
st_ttl     = S("t", fontName=H, fontSize=8.4, textColor=INK, leading=10.5)
st_ttlA    = S("ta", fontName=H, fontSize=8.4, textColor=RED, leading=10.5)
st_dsc     = S("d", fontName=B, fontSize=7.8, textColor=INK2, leading=9.8, spaceBefore=1.5)
st_own     = S("o", fontName=B, fontSize=7.2, textColor=MUT, leading=9)
st_date    = S("dt", fontName=B, fontSize=7.2, textColor=MUT, leading=9, alignment=TA_RIGHT)
st_dateS   = S("dts", fontName=H, fontSize=7.2, textColor=RED, leading=9, alignment=TA_RIGHT)
st_note    = S("n", fontName=B, fontSize=7.6, textColor=INK2, leading=10)
st_nlab    = S("nl", fontName=H, fontSize=6.8, textColor=RED, leading=9, spaceAfter=2,
               trackingAmount=1)
st_leg     = S("lg", fontName=B, fontSize=6.8, textColor=MUT, leading=9)

PW, PH = A4
LM = RM = 14*mm
CW = PW - LM - RM

doc = BaseDocTemplate("/home/user/potential/docs/MR-Topic-Aperti_2026-07-25.pdf",
                      pagesize=A4, leftMargin=LM, rightMargin=RM,
                      topMargin=15*mm, bottomMargin=16*mm,
                      title="Mountain Retreat — Topic aperti",
                      author="Potential", subject="Riepilogo dei punti non chiusi")

def deco(canv, d):
    canv.saveState()
    canv.setFillColor(RED)
    canv.rect(LM, PH - 13*mm, CW, 1.1*mm, stroke=0, fill=1)          # filetto rosso in testa
    canv.setFillColor(MUT); canv.setFont(B, 6.6)
    canv.drawString(LM, 10*mm, "Mountain Retreat — Topic aperti  ·  25.07.2026  ·  documento interno")
    canv.drawRightString(PW - RM, 10*mm, "EVERY SPACE. DELIVERED.")
    canv.setStrokeColor(HAIR); canv.setLineWidth(.4)
    canv.line(LM, 12.5*mm, PW - RM, 12.5*mm)
    canv.setFillColor(MID); canv.setFont(B, 6.6)
    canv.drawCentredString(PW/2, 10*mm, str(d.page))
    canv.restoreState()

doc.addPageTemplates([PageTemplate(id="p",
    frames=[Frame(LM, 16*mm, CW, PH - 15*mm - 16*mm, id="f",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)],
    onPage=deco)])

flow = []

# ------------------------------------------------------------- testata
flow.append(Paragraph("MOUNTAIN RETREAT&nbsp;&nbsp;·&nbsp;&nbsp;FIT-OUT &amp; CUSTOM INTERIORS", st_eyebrow))
flow.append(Paragraph("Topic aperti", st_h1))
flow.append(Paragraph("Riepilogo dei punti non chiusi, per area di progetto", st_sub))
flow.append(Spacer(1, 9))

meta = Table([[Paragraph("Aggiornato al <b>25.07.2026</b>", st_meta),
               Paragraph("Fonte <b>archivio email MOUNTAIN RETREAT</b> — 12 cartelle, 311 messaggi", st_meta),
               Paragraph("Periodo <b>gen 2024 – lug 2026</b>", st_meta)]],
              colWidths=[CW*.22, CW*.52, CW*.26])
meta.setStyle(TableStyle([("LINEABOVE",(0,0),(-1,0),.4,HAIR),
                          ("TOPPADDING",(0,0),(-1,-1),6),
                          ("BOTTOMPADDING",(0,0),(-1,-1),0),
                          ("LEFTPADDING",(0,0),(-1,-1),0),
                          ("VALIGN",(0,0),(-1,-1),"TOP")]))
flow.append(meta)
flow.append(Spacer(1, 12))

# ------------------------------------------------------------- cruscotto
def kpi(num, lab, lead=False):
    fg = colors.white if lead else INK
    t = Table([[Paragraph(f'<font size="18">{num}</font>',
                          S("k", fontName=H, fontSize=18, textColor=fg, leading=19))],
               [Paragraph(lab, S("kl", fontName=H, fontSize=6.2,
                                 textColor=colors.white if lead else INK2, leading=8,
                                 trackingAmount=.9))]],
              colWidths=[CW/4 - 3])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), RED if lead else GREY),
                           ("LEFTPADDING",(0,0),(-1,-1),8),
                           ("RIGHTPADDING",(0,0),(-1,-1),8),
                           ("TOPPADDING",(0,0),(0,0),8),
                           ("BOTTOMPADDING",(0,0),(0,0),1),
                           ("TOPPADDING",(0,1),(0,1),0),
                           ("BOTTOMPADDING",(0,1),(0,1),8)]))
    return t

dash = Table([[kpi("37","TOPIC APERTI",True), kpi("15","PRIORITÀ ALTA"),
               kpi("9","FERMI DA &gt; 6 MESI"), kpi("10","AREE COINVOLTE")]],
             colWidths=[CW/4]*4)
dash.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
                          ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
                          ("VALIGN",(0,0),(-1,-1),"TOP")]))
flow.append(dash)
flow.append(Spacer(1, 11))

# ------------------------------------------------------------- nota
nota = Table([[Paragraph("TRE SCADENZE CHE STRINGONO", st_nlab)],
              [Paragraph("<b>DGA chiude 10–21.08</b> (ultime spedizioni 04.08) e "
                         "<b>Forma Lighting 10–14.08</b>: quanto serve per la mock-up room va "
                         "movimentato prima. La <b>soletta della bike room</b> va decisa ora, perché "
                         "condiziona un'opera strutturale. L'<b>RFI 198</b> blocca l'inizio della "
                         "piastrellatura in cantiere.", st_note)]],
             colWidths=[CW])
nota.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#FAFAFA")),
                          ("LINEBEFORE",(0,0),(0,-1),2.2,RED),
                          ("LEFTPADDING",(0,0),(-1,-1),9),("RIGHTPADDING",(0,0),(-1,-1),9),
                          ("TOPPADDING",(0,0),(0,0),7),("BOTTOMPADDING",(0,0),(0,0),0),
                          ("TOPPADDING",(0,1),(0,1),0),("BOTTOMPADDING",(0,1),(0,1),7)]))
flow.append(nota)
flow.append(Spacer(1, 9))

leg = Table([[Paragraph("Alta", st_leg), Paragraph("Media", st_leg), Paragraph("Bassa", st_leg),
              Paragraph("La data indica da quando il punto è aperto — "
                        '<font color="#C71617"><b>in rosso</b></font> se fermo da oltre sei mesi',
                        S("lr", fontName=B, fontSize=6.8, textColor=MUT, leading=9, alignment=TA_RIGHT))]],
            colWidths=[26, 30, 30, CW-86])
leg.setStyle(TableStyle([
    ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),0),
    ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("RIGHTPADDING",(3,0),(3,0),0),("LEFTPADDING",(3,0),(3,0),0),
]))
flow.append(leg)
# pallini della legenda disegnati come piccoli riquadri colorati
class Dots(Table):
    pass
dots = Table([[""]], colWidths=[CW], rowHeights=[0])
flow.append(Spacer(1, 10))

# ------------------------------------------------------------- sezioni
def section(title, rows):
    """rows: (prio, titolo, descrizione, owner, data, stale)"""
    hdr = Table([[Paragraph(title.upper(), st_h2),
                  Paragraph(f"{len(rows)} punti", st_cnt)]], colWidths=[CW*.72, CW*.28])
    hdr.setStyle(TableStyle([("LINEBELOW",(0,0),(-1,-1),1.2,INK),
                             ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
                             ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),4),
                             ("VALIGN",(0,0),(-1,-1),"BOTTOM")]))
    data, style = [], [
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("RIGHTPADDING",(3,0),(3,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
    ]
    for i,(prio,t,d,own,dt,stale) in enumerate(rows):
        cell = [Paragraph(t, st_ttlA if prio=="A" else st_ttl)]
        if d: cell.append(Paragraph(d, st_dsc))
        data.append(["", cell, Paragraph(own, st_own),
                     Paragraph(dt, st_dateS if stale else st_date)])
        col = RED if prio=="A" else (MID if prio=="M" else GREY)
        # quadratino di priorità, al posto di un glifo non presente nei font base-14
        style += [("BACKGROUND",(0,i),(0,i), col),
                  ("VALIGN",(0,i),(0,i),"TOP")]
        if i < len(rows)-1:
            style.append(("LINEBELOW",(0,i),(-1,i),.4,HAIR))
    tbl = Table(data, colWidths=[5, CW-5-92-52, 92, 52])
    tbl.setStyle(TableStyle(style))
    return KeepTogether([hdr, tbl, Spacer(1, 11)])

A,M,Bp = "A","M","B"
SEC = [
 ("Fire — reazione al fuoco", [
  (A,"Protega Novatherm 1FR — verifica di fattibilità",
   "Prodotto suggerito da EFLA per raggiungere B,s1-d0 sui cielini, che non hanno deroga. Nessuna risposta dopo la mail del 6 febbraio.",
   "Carlo · EFLA","06.02.26",True),
  (A,"Assessment B,s2-d0 per le pareti",
   "Grazie agli sprinkler EFLA apre al declassamento del cladding a parete, ma la valutazione non è mai stata formalizzata.",
   "EFLA","06.02.26",True),
  (M,"Linee guida porte islandesi → Bergamaschi",
   "PDF tradotto in inglese ricevuto da Hartmann, da inoltrare. Chiarito che la norma sulla Danimarca non si applica a Bergamaschi.",
   "Carlo · Carol","22.05.26",False),
  (M,"Il pavimento Haute soddisfa Cfl-s1?",
   "Domanda posta da Perla a BLD; nessuna risposta conclusiva in archivio.",
   "Fabrizia · Carol","14.11.24",True),
  (M,"Contraddizione sul sistema di aggancio",
   "Basalt: il requisito non si applica se il sistema è chiuso e non raggiungibile dal fuoco. EFLA: i telai di supporto sono soggetti a B,s1-d0. Mai riconciliate.",
   "Carlo · EFLA","19.11.24",True),
  (Bp,"Categorie CGF e CGS della bachelite HPL",
   "Da chiarire con il referente islandese; sopra i 6 mm la classe è comunque raggiunta.",
   "Carol","23.10.24",True)]),
 ("Doors", [
  (A,"Secondo fornitore porte — offerta alternativa",
   "L'ultima offerta Bergamaschi vale ~840.000 €. Il board ha chiesto conto della singola offerta; Javerk può procurarne un'altra. Si resta liberi di cambiare fino alla firma.",
   "Hartmann · Carol","18.03.26",False),
  (M,"Test Xeno — ingiallimento UV",
   "Hartmann lo vuole fare. Da procurare le offerte e decidere se il costo entra nel pacchetto mock-up room.",
   "Carol","18.03.26",False),
  (M,"Campione pavimento ignifugo — due classi",
   "Servono scale e aree comuni con classi diverse; la classe è cambiata dopo il campione precedente. Da rivedere entrambi.",
   "Carol · Haute","18.03.26",False),
  (M,"Porte esterne SPA con contrappeso",
   "Da chiarire con Bergamaschi come realizzarle: peso al posto del chiudiporta tradizionale.",
   "Bergamaschi","14.10.25",True),
  (M,"Porte d'ingresso principali SPA e Hotel",
   "Modalità realizzativa mai definita.","Bergamaschi","14.10.25",True),
  (M,"Codici errati e porte aggiunte nelle liste",
   "Alcune porte sono state aggiunte dopo la quotazione, altre riportano codici sbagliati. Serve un controllo incrociato.",
   "Fabrizia · Carlo","14.10.25",True)]),
 ("Claddings &amp; Portals", [
  (A,"RFI 198 — disegno 5-19-XX-04 mai pubblicato",
   "Il contractor lo attende per la finitura del vano porta camera/vanity. Serve lo spessore materiali per fissare il foro <b>prima della piastrellatura</b>.",
   "BLD · Basalt","21.05.26",False),
  (A,"Spessore cladding: modello 20 mm vs doga reale 16 mm",
   "Impatta ceiling plans e dettagli porte. Sollevato da Basalt, mai chiuso formalmente.",
   "Basalt · Carlo","19.11.24",True),
  (A,"Rischio imbarcamento delle doghe da 16 mm",
   "Una doga da 900 mm in Basalt risulta già visibilmente imbarcata. Chiesto se la posa proposta lo prevenga: nessuna risposta tecnica.",
   "Haute · Alart","19.11.24",True),
  (M,"Trattamento dei claddings in zone umide",
   "Domanda di Perla: differisce da quello dei corridoi o è identico a meno del fire rating?",
   "Carlo · Haute","19.11.24",True)]),
 ("BOQ &amp; item", [
  (A,"5_19_01_51 — locker SPA, scelta fra due opzioni",
   "144 pezzi: 1.445 €/pz (HPL-ARPA, facce Fenix full colour) contro 660 €/pz (MDF hydro, box laminato). Differenza ~113.000 €.",
   "Carol · Hartmann","—",False),
  (A,"5_19_XX_94 — specchio bagno, modifiche dimensionali",
   "39 pezzi per 17.394 €. Disegno da aggiornare e quotazione da riverificare.",
   "Fabrizia","17.07.26",False),
  (M,"5_19_XX_12 — sofa sideboard, decisione finale",
   "Tenuto a costo per non perdere le prese elettriche; V2 emessa il 23.07 dopo il cambio di divano. Resta da decidere se sopravvive alla revisione.",
   "Carol · Fabrizia","16.07.26",False),
  (M,"Tre item senza disegno, non quotati",
   "5_19_03_43 battery shelf · 5_19_03_76 low cabinet · 5_19_03_19 fireplace. Da disegnare o da escludere formalmente.",
   "Fabrizia","04.06.26",False),
  (M,"Action Tracker ancora vuoto",
   "Il file conteneva solo le righe di esempio. Compilato il 25.07 con 37 azioni e 12 decisioni.",
   "Carlo","—",False)]),
 ("Lighting", [
  (A,"Indirizzo campione DGA e rientro delle piastre",
   "DGA ha già prodotto tutte le componenti e attende solo le piastre rivestite in pelle. <b>Chiude 10–21.08, ultime spedizioni 04.08.</b>",
   "Carlo · DGA","22.07.26",False),
  (A,"Test dello spinotto jack DGA",
   "Influisce sulla costruzione di mobile e barra. Dall'esperienza Trenitalia si danneggia spesso: va testato ora, o DGA dovrà rifare il sistema più avanti.",
   "Carlo · DGA","20.07.26",False),
  (M,"Magneti e riscontro metallico",
   "Forza dei magneti da provare sul riscontro verniciato; se la barra è in alluminio serve un riscontro in ferro, con impatto sullo sviluppo.",
   "Carlo · DGA","20.07.26",False)]),
 ("Stones", [
  (A,"Abbassamento della soletta per pietre da 50 mm",
   "Bike room e ingressi hotel: la distanza attuale non basta. EFLA chiede conferma immediata perché è un'opera strutturale.",
   "Basalt · EFLA","28.11.25",False),
  (M,"Accettazione della variabilità di spessore",
   "Il 2/5 cm non è una misura ma la variabilità dello spacco. Proposta: 2/5 pedonale e carrabile, 4/8 giganti — 7 cm non è un'opzione.",
   "Carlo · Carol","28.11.25",False),
  (M,"Ingombro totale dei pavimenti",
   "Da calcolare includendo gli inerti di sottofondo. Da chiarire anche cosa si intenda per «pezzatura normale».",
   "Carlo · Pedretti","28.11.25",False)]),
 ("Budget &amp; Logistic", [
  (A,"Stima ore-uomo fino a fine 2027",
   "Richiesta da Lárus per la cost estimation destinata alla banca. Non ancora consegnata.",
   "Carol · Carlo","15.06.26",False),
  (A,"Destinazione trasporti da correggere",
   "Il preventivo dice DAP Grindavík, che è Blue Lagoon. Per Mountain valgono <b>Árnes</b> e il porto di <b>Þorlákshöfn</b>.",
   "Carlo · Alart","25.06.26",False),
  (M,"Container in sito — quanti e per quanto tempo",
   "Non considerato nel preventivo da 8–9 K€ a container.","Carlo · Carol","25.06.26",False),
  (M,"Assicurazione trasporto",
   "Esclusa dal preventivo, in corso di quantificazione da parte di Alart.","Alart","25.06.26",False),
  (M,"Rifugio con cucina per i montatori",
   "Ipotesi per abbattere i costi di vitto: BL fornisce la materia prima, i montatori cucinano.",
   "Carlo","26.06.26",False),
  (M,"Tre porte Javerk mancanti nei conteggi",
   "Il budget porte non è chiudibile finché non rientrano.","Carol · Javerk","26.06.26",False)]),
 ("BREEAM &amp; fornitori", [
  (A,"Arredi fissi in BREEAM — conformità dei fornitori custom",
   "Da febbraio 2025 gli arredi avvitati o inchiodati all'edificio rientrano in Hea 02 e Mat 03. Il team assumeva il contrario: va verificata la conformità di tutto il custom.",
   "Carol · EFLA","03.02.25",True),
  (A,"Pelle Apir — conferma ad Alart e spedizione",
   "1 m² di spaccata 0,8 mm in strisce da 45 cm, da inviare ad Apir che esegue taglio e applicazione.",
   "Carlo · Alart","22.07.26",False),
  (M,"Schede tecniche Haute in inglese",
   "Le schede inviate erano in italiano. Perla le ha richieste due volte in inglese, con i valori VOC evidenziati. Nessun seguito.",
   "Carlo · Haute","19.02.25",True),
  (M,"Date trasferta Islanda e durata trasporto",
   "Proposta partenza ven 26 / rientro dom 28–29. Matteo chiede quanto impiega un camion dedicato: sette giorni?",
   "Carlo · Alart","06.06.26",False)]),
]

for title, rows in SEC:
    flow.append(section(title, rows))

doc.build(flow)

import os
p = "/home/user/potential/docs/MR-Topic-Aperti_2026-07-25.pdf"
print("saved:", p, os.path.getsize(p), "byte")
