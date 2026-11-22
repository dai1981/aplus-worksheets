# -*- coding: utf-8 -*-
"""
France Maths CE1 : Les tables de multiplication
  python3 tools/gen_fr_maths_ce1_tables_de_multiplication.py
Tables de 2, 3, 4, 5 et 10, puis jusqu’à 10 ; facteur manquant ; double ; problèmes (fonctions du générateur CE2 avec un autre tirage).
Erreurs : 4 × 7 = 11 (additionner), réciter la table sans s’arrêter au bon nombre, oublier que 6 × 4 = 4 × 6.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, FOIS
import gen_fr_maths_ce2_tables_de_multiplication as TM

R = random.Random(53119)
K = Kids(R)
TM.R = R
TM.K = K


def s1():
    return TM.fact([2, 5, 10])


def s2():
    return TM.fact([3, 4])


def s3():
    return TM.fact([2, 3, 4, 5, 6, 7, 8, 9])


def s4_double():
    a = R.randint(2, 10)
    if R.random() < 0.5:
        return mcq("Je sais que 2 %s %d = %d. Combien font 4 %s %d ?" % (FOIS, a, 2 * a, FOIS, a), str(4 * a), [str(2 * a + 2), str(4 + a), str(2 * a + a)],
                   "4, c’est le double de 2 : 4 %s %d = double de %d = <b>%d</b>." % (FOIS, a, 2 * a, 4 * a))
    return mcq("Je sais que 5 %s %d = %d. Combien font 10 %s %d ?" % (FOIS, a, 5 * a, FOIS, a), str(10 * a), [str(5 * a + 5), str(10 + a), str(5 * a + a)],
               "10, c’est le double de 5 : 10 %s %d = <b>%d</b>." % (FOIS, a, 10 * a))


def build():
    seen = set()
    sets = [("Tables de 2, 5 et 10", mix(R, seen, [(s1, 20)])), ("Tables de 3 et 4", mix(R, seen, [(s2, 20)])),
            ("Le facteur manquant", mix(R, seen, [(TM.s3_manq, 20)])), ("Toutes les tables, doubles", mix(R, seen, [(s3, 12), (s4_double, 4), (TM.s4_comm, 4)])),
            ("Problèmes", mix(R, seen, [(TM.s5_prob, 20)]))]
    body = lesson(["La table de 2, ce sont les <b>doubles</b> ; celle de 5 finit par 0 ou 5 ; celle de 10 finit par 0.",
                   "4 × 7, c’est le double de 2 × 7 : 2 × 7 = 14, donc 4 × 7 = 28.",
                   "Si tu connais 3 × 8, tu connais 8 × 3 : c’est le même résultat."],
                  [example("4 × 6", ["2 × 6 = 12", "double de 12"], "24")],
                  [["Additionner : 4 × 7 = 11", "4 × 7 = 7 + 7 + 7 + 7 = 28."],
                   ["Se tromper en récitant la table", "On peut repartir d’un résultat connu : 5 × 6 = 30, donc 6 × 6 = 36."],
                   ["Oublier que 6 × 4 = 4 × 6", "L’ordre ne change pas le résultat."]])
    faq = [("Quelles tables apprendre en premier ?", "Les tables de 2, 5 et 10, puis celles de 3 et 4."),
           ("Comment retrouver un résultat oublié ?", "On part d’un résultat connu et on ajoute ou on enlève un groupe.")]
    unit(1, R, "tables-de-multiplication", "N",
         "Connaître les tables de multiplication (de 2, 3, 4, 5 et 10, puis jusqu’à 10) et les utiliser pour calculer ; trouver un facteur manquant ; résoudre des problèmes multiplicatifs",
         "Les tables de multiplication", "Tables de multiplication",
         "Fiches de maths CE1 sur les tables de multiplication : tables de 2, 3, 4, 5 et 10, facteur manquant, doubles et problèmes. 100 exercices corrigés.",
         "2 × 7 = 14 → 4 × 7 = 28", "Le double aide à calculer.", body, faq, sets, 19)


if __name__ == "__main__":
    build()
