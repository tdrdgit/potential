# CLAUDE.md

## Firma email — account Potential

Regola permanente: **ogni volta che si crea una email o una bozza dall'account Potential
(`carlo@potential.contractors`, connettore Gmail), aggiungere in fondo al corpo la firma
standard.**

- Firma canonica: [`potential-email-signature.html`](./potential-email-signature.html)
- Inserire il contenuto HTML del file (la tabella `zs-output-sig`) dopo il testo del messaggio,
  nel campo `htmlBody`. Fornire anche una versione testo equivalente nel campo `body`.
- Caratteristiche: Helvetica 12px, accento rosso `#C71617`, nero `#000001`, logo 155×50 via link.
- **Non** incorporare il logo come allegato (CID): l'utente vuole il logo come link esterno
  per evitare che diventi un allegato nelle risposte.
- Il connettore Gmail può solo **creare bozze**, non inviare: l'invio finale resta all'utente.

Nota nota: il `src` del logo punta a un URL esterno gimm.io che al momento potrebbe non
caricarsi; è una scelta esplicita dell'utente tenerlo così. Se serve renderlo visibile,
sostituire il `src` con un URL stabile del logo (non trasformarlo in allegato).
