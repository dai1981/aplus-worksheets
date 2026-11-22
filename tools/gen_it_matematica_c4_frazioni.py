# -*- coding: utf-8 -*-
"""
Italia Matematica classe quarta: Le frazioni (Numeri)
  python3 tools/gen_it_matematica_c4_frazioni.py
Unità frazionaria e frazione, numeratore e denominatore, frazioni proprie, improprie e apparenti,
frazioni equivalenti, confrontare e ordinare frazioni, frazioni sulla retta, problemi.
Errori: pensare che 1/8 sia più grande di 1/4, confondere numeratore e denominatore, credere che 4/4 sia impropria.
"""
import random
from it_common import Kids, lesson, make_unit, mix, table
import gen_it_matematica_c3_frazioni as F3
import gen_it_matematica_c5_frazioni as F5

R = random.Random(70406)
G = "classe-quarta"


def main():
    for m in (F3, F5):
        m.R = R
    F3.K = Kids(R)
    seen = set()
    sets = [
        ("Leggere e scrivere le frazioni", mix(R, seen, [(F3.s1_figura, 8), (F3.s2_parola, 6), (F3.s2_termini, 6)])),
        ("Proprie, improprie, apparenti", mix(R, seen, [(F5.s1_tipo, 14), (F5.s1_misto, 6)])),
        ("Frazioni equivalenti", mix(R, seen, [(F5.s2_equivalenti, 10), (F5.s2_mancante, 10)])),
        ("Confrontare e ordinare", mix(R, seen, [(F3.s3_confronta, 6), (F5.s3_confronta, 6), (F5.s3_ordina, 4), (F5.s4_retta, 4)])),
        ("Problemi", mix(R, seen, [(F5.s5, 12), (F3.s5_problema, 8)])),
    ]
    F = F5.F
    body = lesson(
        ["Una figura divisa in parti <b>uguali</b>: ogni parte è un’<b>unità frazionaria</b> (%s, %s, %s …)." % (F(1, 2), F(1, 4), F(1, 8)),
         "Nella frazione %s il <b>denominatore</b> (4) dice in quante parti uguali è diviso l’intero, il <b>numeratore</b> (3) quante parti prendi." % F(3, 4),
         "Frazione <b>propria</b>: numeratore minore del denominatore (meno di un intero). <b>Impropria</b>: numeratore maggiore (più di un intero). <b>Apparente</b>: il numeratore è multiplo del denominatore (%s = 2 interi)." % F(8, 4),
         "Frazioni <b>equivalenti</b> indicano la stessa parte: moltiplica (o dividi) numeratore e denominatore per lo stesso numero: %s = %s." % (F(1, 2), F(3, 6))],
        [("Confronta %s e %s" % (F(2, 3), F(3, 4)), ["%s = %s" % (F(2, 3), F(8, 12)), "%s = %s" % (F(3, 4), F(9, 12)), "%s &lt; %s" % (F(8, 12), F(9, 12))], "%s &lt; %s" % (F(2, 3), F(3, 4)))],
        [["Pensare che %s sia più grande di %s perché 8 &gt; 4" % (F(1, 8), F(1, 4)), "Più parti = parti più piccole."],
         ["Confondere numeratore e denominatore", "Il denominatore sta sotto e dice in quante parti dividi."],
         ["Chiamare impropria %s" % F(4, 4), "%s = 1 intero: è apparente." % F(4, 4)]],
        table(["Tipo", "Esempio", "Rispetto all’intero"], [["propria", F(3, 5), "meno di 1"], ["impropria", F(7, 5), "più di 1"], ["apparente", F(10, 5), "interi esatti (2)"]]))
    faq = [("Come si confrontano due frazioni con lo stesso denominatore?", "È maggiore quella con il numeratore più grande: 5/8 > 3/8."),
           ("E con lo stesso numeratore?", "È maggiore quella con il denominatore più piccolo: 3/4 > 3/8, perché i quarti sono più grandi degli ottavi.")]
    make_unit(R, "frazioni", "N",
              "Operare con le frazioni e riconoscere frazioni equivalenti; confrontare e ordinare frazioni; rappresentarle sulla retta",
              "Le frazioni: proprie, improprie ed equivalenti", "Frazioni",
              "Schede di matematica per la classe quarta sulle frazioni: numeratore e denominatore, frazioni proprie, improprie e apparenti, equivalenti, confronto, ordine e retta, problemi. 100 esercizi con soluzioni.",
              "Il denominatore divide, il numeratore prende.", "Frazioni equivalenti indicano la stessa parte dell’intero.",
              body, faq, sets, 6, grade=G)


if __name__ == "__main__":
    main()
