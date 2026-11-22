# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Operazioni con i numeri decimali (Numeri)
  python3 tools/gen_it_matematica_c4_operazioni_con_i_decimali.py
Addizioni e sottrazioni in colonna con i decimali (virgola sotto virgola, zeri per pareggiare), calcolo mentale,
moltiplicare e dividere per 10, 100, 1000, moltiplicare un decimale per un numero naturale, problemi con euro e misure.
Errori: incolonnare a destra senza allineare le virgole, spostare la virgola dalla parte sbagliata.
"""
import random
from it_common import lesson, make_unit, mix, table, Kids
import gen_it_matematica_c5_addizioni_e_sottrazioni_con_i_decimali as A5
import gen_it_matematica_c5_moltiplicazioni_e_divisioni_con_i_decimali as M5

R = random.Random(70409)
G = "classe-quarta"


def main():
    for m in (A5, M5):
        m.R = R
        m.K = Kids(R)
    seen = set()
    sets = [
        ("Addizioni in colonna", mix(R, seen, [(A5.s1, 12), (A5.s2, 8)])),
        ("Sottrazioni in colonna", mix(R, seen, [(A5.s3, 20)])),
        ("Calcolo mentale", mix(R, seen, [(A5.s4_mentale, 14), (A5.s4_tre, 6)])),
        ("Per e diviso 10, 100, 1000 e per un numero naturale", mix(R, seen, [(M5.s1_dieci, 12), (M5.s2_per_naturale, 8)])),
        ("Problemi", mix(R, seen, [(A5.s5, 20)])),
    ]
    body = lesson(
        ["Nelle addizioni e sottrazioni incolonna <b>virgola sotto virgola</b>: unità sotto unità, decimi sotto decimi.",
         "Se le parti decimali hanno cifre diverse, aggiungi zeri: 5 − 1,25 diventa 5,00 − 1,25.",
         "Per × 10, 100, 1000 la virgola si sposta di 1, 2, 3 posti verso <b>destra</b>; per : 10, 100, 1000 verso <b>sinistra</b>.",
         "Per moltiplicare un decimale per un numero naturale, moltiplica senza virgola e poi metti nel risultato tante cifre decimali quante ne ha il fattore."],
        [("12,5 + 3,75", ["12,50 + 3,75", "virgola sotto virgola", "16,25"], "16,25")],
        [["Incolonnare a destra 12,5 e 3,75", "Allinea le virgole, non le ultime cifre."],
         ["Per × 100 spostare la virgola a sinistra", "Moltiplicando il numero diventa più grande."],
         ["Dimenticare la virgola nel risultato", "Conta le cifre decimali dei numeri di partenza."]],
        table(["Operazione", "Virgola", "Esempio"], [["× 10", "1 posto a destra", "3,45 × 10 = 34,5"], ["× 100", "2 posti a destra", "3,45 × 100 = 345"], [": 10", "1 posto a sinistra", "3,45 : 10 = 0,345"]]))
    faq = [("Perché si aggiungono gli zeri?", "Per avere lo stesso numero di cifre dopo la virgola e non sbagliare l’incolonnamento: 5 = 5,00."),
           ("Come controllo un’operazione con i decimali?", "Con una stima: 12,5 + 3,75 è circa 13 + 4 = 17, quindi 16,25 è ragionevole.")]
    make_unit(R, "operazioni-con-i-decimali", "N",
              "Eseguire le quattro operazioni con i numeri decimali; moltiplicare e dividere per 10, 100, 1000",
              "Operazioni con i numeri decimali", "Operazioni con i decimali",
              "Schede di matematica per la classe quarta sulle operazioni con i numeri decimali: addizioni e sottrazioni in colonna, calcolo mentale, × e : 10, 100, 1000, moltiplicare per un numero naturale, problemi. 100 esercizi con soluzioni.",
              "Virgola sotto virgola.", "× 10, 100, 1000: la virgola va a destra; : va a sinistra.",
              body, faq, sets, 9, grade=G)


if __name__ == "__main__":
    main()
