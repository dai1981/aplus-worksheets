# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Frazioni decimali e numeri decimali (Numeri)
  python3 tools/gen_it_matematica_c4_numeri_decimali.py
Frazioni decimali (decimi, centesimi, millesimi) e numeri decimali, parte intera e parte decimale, tabella
da u , d c m, valore delle cifre, decimali equivalenti, confrontare, ordinare, arrotondare, retta, problemi.
Errori: pensare che 0,25 sia più grande di 0,3, scrivere 7/100 come 0,7, confondere decimi e centesimi.
"""
import random
from it_common import lesson, make_unit, mix, table, fr
import gen_it_matematica_c5_numeri_decimali as N5

R = random.Random(70408)
G = "classe-quarta"


def main():
    N5.R = R
    seen = set()
    sets = [
        ("Frazioni decimali e numeri decimali", mix(R, seen, [(N5.s1_frazione, 12), (N5.s1_tabella, 8)])),
        ("Valore delle cifre", mix(R, seen, [(N5.s2_valore, 12), (N5.s2_equivalenti, 8)])),
        ("Confrontare e ordinare", mix(R, seen, [(N5.s3_confronta, 14), (N5.s3_ordina, 6)])),
        ("Arrotondare e retta", mix(R, seen, [(N5.s4_arrotonda, 10), (N5.s4_retta, 10)])),
        ("Problemi", mix(R, seen, [(N5.s5, 20)])),
    ]
    body = lesson(
        ["Le <b>frazioni decimali</b> hanno denominatore 10, 100, 1000: %s = 0,1 (un decimo), %s = 0,01 (un centesimo), %s = 0,001 (un millesimo)." % (fr(1, 10), fr(1, 100), fr(1, 1000)),
         "Nel numero decimale la <b>virgola</b> separa la parte intera (a sinistra) dalla parte decimale (a destra): d, c, m.",
         "Dopo la virgola ci sono tante cifre quanti sono gli zeri del denominatore: %s = 0,07 (non 0,7)." % fr(7, 100),
         "Per confrontare: prima la parte intera, poi i decimi, poi i centesimi… 0,3 = 0,30 è maggiore di 0,25."],
        [("Confronta 2,45 e 2,5", ["parte intera uguale: 2", "decimi: 4 e 5", "5 decimi sono di più"], "2,45 &lt; 2,5")],
        [["Pensare che 0,25 &gt; 0,3 perché 25 &gt; 3", "Confronta prima i decimi: 2 &lt; 3."],
         ["Scrivere %s = 0,7" % fr(7, 100), "Centesimi: due cifre dopo la virgola, 0,07."],
         ["Confondere decimi e centesimi", "Il primo posto dopo la virgola è il decimo, il secondo il centesimo."]],
        table(["da", "u", ",", "d", "c", "m"], [["1", "4", ",", "0", "7", "5"]]))
    faq = [("Perché 0,5 e 0,50 sono uguali?", "Perché 5 decimi sono 50 centesimi: lo zero in fondo alla parte decimale non cambia il valore."),
           ("Dove si usano i numeri decimali?", "Nei prezzi (2,35 €), nelle misure (1,5 m; 0,75 l) e nei tempi delle gare (12,48 secondi).")]
    make_unit(R, "numeri-decimali", "N",
              "Conoscere le frazioni decimali e i numeri decimali fino ai millesimi; leggere, scrivere, confrontare numeri decimali e rappresentarli sulla retta",
              "Frazioni decimali e numeri decimali", "Numeri decimali",
              "Schede di matematica per la classe quarta su frazioni decimali e numeri decimali: decimi, centesimi, millesimi, valore delle cifre, confronto, ordine, arrotondamento, retta e problemi. 100 esercizi con soluzioni.",
              "Dopo la virgola: decimi, centesimi, millesimi.", "0,3 = 0,30: confronta posto per posto.",
              body, faq, sets, 8, grade=G)


if __name__ == "__main__":
    main()
