# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Misure di lunghezza, peso e capacità (Misure)
  python3 tools/gen_it_matematica_c4_misure.py
Il sistema metrico decimale: multipli e sottomultipli di metro, litro e grammo (anche quintale e tonnellata),
equivalenze anche con i numeri decimali, scegliere l’unità, confrontare misure, righello, problemi.
Errori: spostare la virgola dalla parte sbagliata, contare male i passi, confrontare i numeri senza guardare le unità.
"""
import random
from it_common import lesson, make_unit, mix, table, Kids
import gen_it_matematica_c5_misure_ed_equivalenze as MS5
import gen_it_matematica_c3_misure_di_lunghezza as L3
import gen_it_matematica_c3_peso_e_capacita as P3

R = random.Random(70411)
G = "classe-quarta"


def s5():
    it = MS5.s5()
    if it and "²" in it["q"]:
        return None
    return it


def main():
    for m in (MS5, L3, P3):
        m.R = R
        m.K = Kids(R)
    seen = set()
    sets = [
        ("Le unità di misura", mix(R, seen, [(L3.s1_quale, 6), (P3.s1_peso, 7), (P3.s1_cap, 7)])),
        ("Equivalenze di lunghezza", mix(R, seen, [(MS5.s1, 20)])),
        ("Equivalenze di peso e capacità", mix(R, seen, [(MS5.s2, 20)])),
        ("Confrontare e misurare", mix(R, seen, [(MS5.s3_confronta, 14), (L3.s4_righello, 6)])),
        ("Problemi", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Le unità di misura di lunghezza (m), capacità (l) e peso (g) hanno <b>multipli</b> (da, h, k) e <b>sottomultipli</b> (d, c, m): ogni unità è 10 volte quella alla sua destra.",
         "Per passare a un’unità <b>più piccola</b> moltiplichi (la virgola va a destra); per passare a una <b>più grande</b> dividi (la virgola va a sinistra).",
         "Conta i passi tra le due unità: ogni passo è un posto. Se mancano cifre aggiungi zeri.",
         "Per i pesi grandi si usano anche il quintale (1 q = 100 kg) e la tonnellata (1 t = 1000 kg)."],
        [("3,5 m = … cm", ["da m a cm: 2 passi verso unità più piccole", "la virgola va a destra di 2 posti"], "350 cm")],
        [["Dividere quando si passa a un’unità più piccola", "Unità più piccola → numero più grande."],
         ["Contare male i passi (m → mm sono 3)", "Scrivi la tabella delle unità e conta le caselle."],
         ["Confrontare 80 cm e 2 m guardando solo 80 e 2", "Trasforma nella stessa unità: 2 m = 200 cm."]],
        table(["k", "h", "da", "unità", "d", "c", "m"], [["km", "hm", "dam", "m", "dm", "cm", "mm"], ["kl", "hl", "dal", "l", "dl", "cl", "ml"], ["kg", "hg", "dag", "g", "dg", "cg", "mg"]]))
    faq = [("Che cosa vuol dire «equivalenza»?", "Scrivere la stessa misura con un’altra unità: 1,2 kg = 1200 g è la stessa quantità."),
           ("Perché il kilolitro si usa poco?", "Per grandi quantità di liquido si usano di solito gli ettolitri (hl) o i metri cubi; per i pesi grandi il quintale e la tonnellata.")]
    make_unit(R, "misure", "M",
              "Conoscere le principali unità di misura per lunghezze, capacità e pesi del sistema metrico decimale ed effettuare misure e stime; passare da un’unità di misura a un’altra",
              "Misure di lunghezza, peso e capacità: le equivalenze", "Misure ed equivalenze",
              "Schede di matematica per la classe quarta sulle misure: metro, litro e grammo con multipli e sottomultipli, quintale e tonnellata, equivalenze con i decimali, confronti e problemi. 100 esercizi con soluzioni.",
              "Unità più piccola: la virgola va a destra.", "Unità più grande: la virgola va a sinistra.",
              body, faq, sets, 11, grade=G)


if __name__ == "__main__":
    main()
