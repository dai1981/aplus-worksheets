# -*- coding: utf-8 -*-
"""
France Maths CE1 : Les fractions (inférieures ou égales à 1)
  python3 tools/gen_fr_maths_ce1_fractions.py
Lire et écrire une fraction, 3/8 = 1/8 + 1/8 + 1/8, égale à 1/2 ou à 1, comparer (même dénominateur, même numérateur),
additionner et soustraire avec le même dénominateur, compléter à 1 (fonctions des générateurs CE2 avec un autre tirage).
Erreurs : inverser numérateur et dénominateur, croire que 1/8 &gt; 1/4 car 8 &gt; 4, additionner les dénominateurs.
"""
import random
import re
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, fr
import gen_fr_maths_ce2_fractions as FR
import gen_fr_maths_ce2_additionner_et_soustraire_des_fractions as FA

R = random.Random(53120)
K = Kids(R)
FR.R = FA.R = R
FR.K = FA.K = K


def le1(mk):
    def f():
        it = mk()
        if not it:
            return None
        t = it["q"] + " " + it["c"][0] + " " + it["e"]
        if "2 unités" in t:
            return None
        for n, d in re.findall(r"<span class='fn'>(\d+)</span><span class='fd'>(\d+)</span>", t):
            if int(n) > int(d):
                return None
        return it
    f.__name__ = mk.__name__
    return f


def unite():
    d = R.choice([3, 4, 5, 6, 8, 10])
    k = R.randint(2, d - 1)
    return mcq("Complète : %s = %s" % (fr(k, d), " + ".join([fr(1, d)] * 2) + " + …" if k > 2 else fr(1, d) + " + …"),
               " + ".join([fr(1, d)] * (k - 2)) if k > 2 else fr(1, d), [" + ".join([fr(1, d)] * (k - 1)), fr(k, d), fr(1, k)] if k > 2 else [fr(2, d), fr(1, 2 * d), fr(d, d)],
               "%s, c’est %d fois %s : %s." % (fr(k, d), k, fr(1, d), " + ".join([fr(1, d)] * k)))


def build():
    seen = set()
    sets = [("Lire et écrire une fraction", mix(R, seen, [(le1(FR.s1_figure), 14), (le1(FR.s1_mot), 6)])),
            ("Des parts d’unité", mix(R, seen, [(unite, 8), (le1(FR.s4_demi), 6), (le1(FR.s4_un), 6)])),
            ("Comparer des fractions", mix(R, seen, [(le1(FR.s3_meme_den), 10), (le1(FR.s3_meme_num), 10)])),
            ("Additionner, soustraire, compléter à 1", mix(R, seen, [(le1(FA.s1_add), 7), (le1(FA.s1_sub), 6), (le1(FA.s3_compl), 7)])),
            ("Problèmes", mix(R, seen, [(le1(FA.s5_prob), 8), (le1(FR.s5_pizza), 6), (le1(FR.s5_qte), 6)]))]
    body = lesson(["Une fraction dit en combien de <b>parts égales</b> on partage (le dénominateur, en bas) et combien on en prend (le numérateur, en haut).",
                   "3/8 = 1/8 + 1/8 + 1/8. Quand le numérateur est égal au dénominateur, la fraction vaut 1 : 8/8 = 1.",
                   "Avec le même dénominateur, on compare ou on additionne les numérateurs : 2/5 + 1/5 = 3/5."],
                  [example("%s + %s" % (fr(2, 6), fr(3, 6)), ["2 sixièmes + 3 sixièmes"], fr(5, 6))],
                  [["Inverser les deux nombres", "Le nombre de parts du partage est en bas."],
                   ["Croire que %s &gt; %s car 8 &gt; 4" % (fr(1, 8), fr(1, 4)), "Plus on partage, plus les parts sont petites."],
                   ["Additionner les dénominateurs : %s + %s = %s" % (fr(1, 5), fr(2, 5), fr(3, 10)), "Les parts restent des cinquièmes : %s." % fr(3, 5)]])
    faq = [("Que veut dire le dénominateur ?", "C’est le nombre de parts égales dans l’unité."),
           ("Quand une fraction vaut-elle 1 ?", "Quand on prend toutes les parts : numérateur = dénominateur.")]
    unit(1, R, "fractions", "N",
         "Comprendre et utiliser des fractions inférieures ou égales à 1 (numérateur, dénominateur) ; décomposer une fraction en fractions unitaires ; comparer des fractions de même dénominateur ou de même numérateur ; additionner et soustraire des fractions de même dénominateur",
         "Les fractions", "Fractions",
         "Fiches de maths CE1 sur les fractions : lire et écrire une fraction, parts d’unité, comparer, additionner, soustraire, compléter à 1 et problèmes. 100 exercices corrigés.",
         "3/8 = 1/8 + 1/8 + 1/8", "Dénominateur : le nombre de parts égales.", body, faq, sets, 20)


if __name__ == "__main__":
    build()
