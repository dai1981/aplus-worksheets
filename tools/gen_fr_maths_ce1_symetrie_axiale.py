# -*- coding: utf-8 -*-
"""
France Maths CE1 : La symétrie axiale
  python3 tools/gen_fr_maths_ce1_symetrie_axiale.py
Figures symétriques ou non, lettres symétriques, compléter par symétrie sur quadrillage (axe vertical ou horizontal),
symétrique d’un point, axes de symétrie (fonctions du générateur CE2 avec un autre tirage).
Erreurs : glisser la figure au lieu de la retourner, compter les carreaux à partir du mauvais bord, oublier qu’un carré a 4 axes.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids
import gen_fr_maths_ce2_symetrie_axiale as SY

R = random.Random(53121)
SY.R = R
SY.DE.R = R


def build():
    seen = set()
    sets = [("Figure symétrique ou non ?", mix(R, seen, [(SY.s1, 20)])), ("Les lettres symétriques", mix(R, seen, [(SY.s2, 20)])),
            ("Compléter par symétrie", mix(R, seen, [(SY.s3, 20)])), ("Le symétrique d’un point", mix(R, seen, [(SY.s4, 20)])),
            ("Les axes de symétrie", mix(R, seen, [(SY.s5, 20)]))]
    body = lesson(["Une figure est <b>symétrique</b> si, en la pliant le long d’une droite (l’<b>axe</b>), les deux moitiés se superposent.",
                   "Sur un quadrillage, le point symétrique est à la même distance de l’axe, de l’autre côté.",
                   "L’axe peut être vertical ou horizontal."],
                  [example("Un point à 3 carreaux à gauche de l’axe", ["même distance de l’autre côté"], "3 carreaux à droite")],
                  [["Glisser la figure au lieu de la retourner", "Le symétrique est comme dans un miroir."],
                   ["Compter les carreaux depuis le bord de la feuille", "On compte depuis l’axe."],
                   ["Oublier des axes", "Un carré a 4 axes de symétrie, un rectangle en a 2."]])
    faq = [("Comment vérifier qu’une figure est symétrique ?", "On la plie le long de l’axe : les deux parties doivent se superposer exactement."),
           ("Une figure peut-elle avoir plusieurs axes ?", "Oui : le carré en a 4, le rectangle 2, le cercle une infinité.")]
    unit(1, R, "symetrie-axiale", "E",
         "Reconnaître si une figure possède un axe de symétrie (par pliage, avec un quadrillage) ; compléter une figure par symétrie axiale sur quadrillage, avec un axe vertical ou horizontal",
         "La symétrie axiale", "Symétrie axiale",
         "Fiches de maths CE1 sur la symétrie axiale : figures symétriques, lettres, compléter par symétrie, symétrique d’un point et axes. 100 exercices corrigés.",
         "On plie le long de l’axe : les deux moitiés se superposent.", "Même distance de l’axe, de l’autre côté.", body, faq, sets, 21)


if __name__ == "__main__":
    build()
