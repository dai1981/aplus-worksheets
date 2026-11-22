# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: La frazione di un numero (Numeri)
  python3 tools/gen_it_matematica_c4_frazione_di_un_numero.py
Calcolare la frazione di un numero (: denominatore × numeratore), dalla parte all’intero, frazione complementare,
addizioni e sottrazioni di frazioni con lo stesso denominatore, problemi.
Errori: moltiplicare per il denominatore e dividere per il numeratore, sommare anche i denominatori.
"""
import random
from it_common import Kids, lesson, make_unit, mix, table, DIV, FOIS
import gen_it_matematica_c5_operazioni_con_le_frazioni as O5

R = random.Random(70407)
G = "classe-quarta"


def main():
    O5.R = R
    O5.K = Kids(R)
    F = O5.F
    seen = set()
    sets = [
        ("Frazione di un numero", mix(R, seen, [(O5.s1_di, 20)])),
        ("Unità frazionaria e frazione", mix(R, seen, [(O5.s1_di, 10), (O5.s3_complementare, 10)])),
        ("Dalla parte all’intero", mix(R, seen, [(O5.s2_inverso, 20)])),
        ("Addizioni e sottrazioni", mix(R, seen, [(O5.s3_somma, 20)])),
        ("Problemi", mix(R, seen, [(O5.s5, 20)])),
    ]
    body = lesson(
        ["Per calcolare la frazione di un numero <b>dividi per il denominatore</b> (trovi l’unità frazionaria) e <b>moltiplica per il numeratore</b>.",
         "Esempio: %s di 20 → 20 %s 4 = 5 (cioè %s), 5 %s 3 = 15." % (F(3, 4), DIV, F(1, 4), FOIS),
         "Dalla parte all’intero: se %s sono 15, allora %s è 15 %s 3 = 5 e l’intero (%s) è 5 %s 4 = 20." % (F(3, 4), F(1, 4), DIV, F(4, 4), FOIS),
         "La frazione <b>complementare</b> è quella che manca per arrivare all’intero: %s e %s." % (F(3, 4), F(1, 4)),
         "Con lo stesso denominatore si sommano (o sottraggono) solo i <b>numeratori</b>: %s + %s = %s." % (F(2, 7), F(3, 7), F(5, 7))],
        [("%s di 35 €" % F(2, 5), ["35 %s 5 = 7" % DIV, "7 %s 2 = 14" % FOIS], "14 €")],
        [["Fare 35 %s 2 %s 5" % (DIV, FOIS), "Prima dividi per il denominatore, poi moltiplica per il numeratore."],
         ["Sommare anche i denominatori: %s + %s = %s" % (F(2, 7), F(3, 7), F(5, 14)), "Il denominatore resta uguale: %s." % F(5, 7)],
         ["Fermarsi all’unità frazionaria", "Se il numeratore non è 1, devi ancora moltiplicare."]],
        table(["Domanda", "Operazione"], [["%s di 24" % F(3, 8), "24 %s 8 %s 3 = 9" % (DIV, FOIS)], ["%s di un numero è 9: il numero?" % F(3, 8), "9 %s 3 %s 8 = 24" % (DIV, FOIS)]]))
    faq = [("Perché si divide per il denominatore?", "Perché il denominatore dice in quante parti uguali si divide l’intero: 20 diviso in 4 parti dà 5 per parte."),
           ("Come controllo il risultato?", "La frazione propria di un numero è sempre più piccola del numero: 3/4 di 20 deve essere meno di 20.")]
    make_unit(R, "frazione-di-un-numero", "N",
              "Calcolare la frazione di una quantità; individuare l’intero conoscendo una sua parte frazionaria; addizionare e sottrarre frazioni con lo stesso denominatore",
              "La frazione di un numero e la frazione complementare", "Frazione di un numero",
              "Schede di matematica per la classe quarta sulla frazione di un numero: dividere per il denominatore e moltiplicare per il numeratore, dalla parte all’intero, frazione complementare, addizioni di frazioni e problemi. 100 esercizi con soluzioni.",
              "Dividi per il denominatore, moltiplica per il numeratore.", "Dalla parte all’intero fai il contrario.",
              body, faq, sets, 7, grade=G)


if __name__ == "__main__":
    main()
