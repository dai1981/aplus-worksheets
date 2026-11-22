# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Compravendita e peso lordo, netto, tara (Misure)
  python3 tools/gen_it_matematica_c4_compravendita.py
Spesa, ricavo, guadagno e perdita; costo unitario e costo totale; peso lordo, netto e tara; problemi in più passaggi.
Errori: confondere ricavo e guadagno, togliere la tara dal netto, dividere invece di moltiplicare per il costo totale.
"""
import random
from it_common import lesson, make_unit, mix, table, Kids
import gen_it_matematica_c5_compravendita as CV5

R = random.Random(70412)
G = "classe-quarta"


def main():
    CV5.R = R
    CV5.K = Kids(R)
    seen = set()
    sets = [
        ("Costo unitario e costo totale", mix(R, seen, [(CV5.s2_unitario, 12), (CV5.s2_kg, 8)])),
        ("Spesa, ricavo, guadagno, perdita", mix(R, seen, [(CV5.s1_gp, 20)])),
        ("Peso lordo, netto e tara", mix(R, seen, [(CV5.s3_lnt, 20)])),
        ("Problemi in più passaggi", mix(R, seen, [(CV5.s4_passi, 20)])),
        ("Problemi della vita di tutti i giorni", mix(R, seen, [(CV5.s5, 20)])),
    ]
    body = lesson(
        ["<b>Costo totale</b> = costo unitario × quantità. <b>Costo unitario</b> = costo totale : quantità.",
         "Chi vende: <b>spesa</b> (quanto ha pagato la merce), <b>ricavo</b> (quanto incassa), <b>guadagno</b> = ricavo − spesa; se il ricavo è minore c’è una <b>perdita</b>.",
         "<b>Peso lordo</b> = merce + contenitore; <b>tara</b> = contenitore; <b>peso netto</b> = lordo − tara."],
        [("Un fruttivendolo compra 20 cassette a 8 € e le rivende a 12 €.", ["spesa: 20 × 8 = 160 €", "ricavo: 20 × 12 = 240 €", "guadagno: 240 − 160 = 80 €"], "80 €")],
        [["Confondere ricavo e guadagno", "Il guadagno è solo la parte in più: ricavo − spesa."],
         ["Calcolare il prezzo sul peso lordo", "Si paga la merce: usa il peso netto."],
         ["Moltiplicare invece di dividere", "Se conosci il totale e cerchi il prezzo di uno, dividi."]],
        table(["Formula", ""], [["guadagno", "ricavo − spesa"], ["ricavo", "spesa + guadagno"], ["spesa", "ricavo − guadagno"], ["peso netto", "lordo − tara"], ["peso lordo", "netto + tara"]]))
    faq = [("Che cos’è la tara?", "Il peso del contenitore: cassetta, sacco, barattolo. Non si paga come merce."),
           ("Si può guadagnare se il ricavo è uguale alla spesa?", "No: in quel caso non c’è né guadagno né perdita, si va «in pari».")]
    make_unit(R, "compravendita", "M",
              "Risolvere problemi di compravendita (spesa, ricavo, guadagno, perdita) e con peso lordo, peso netto e tara, utilizzando le misure di valore e di peso",
              "Compravendita e peso lordo, netto, tara", "Compravendita",
              "Schede di matematica per la classe quarta sulla compravendita: costo unitario e totale, spesa, ricavo, guadagno e perdita, peso lordo, netto e tara, problemi in più passaggi. 100 esercizi con soluzioni.",
              "Guadagno = ricavo − spesa.", "Peso netto = peso lordo − tara.",
              body, faq, sets, 12, grade=G)


if __name__ == "__main__":
    main()
