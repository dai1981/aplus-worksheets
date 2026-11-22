# -*- coding: utf-8 -*-
"""
France Maths 6e : Solides et patrons
  python3 tools/gen_fr_maths_6e_solides_et_patrons.py
Reconnaître cube, pavé droit, prisme, pyramide, cylindre, cône, boule ; faces, arêtes, sommets ; patrons du cube ; assemblages de cubes.
(fonctions du générateur CE2 « solides » avec un autre tirage, et des questions propres à la 6e)
Erreurs : confondre arête et face, croire que tout assemblage de 6 carrés est un patron du cube, oublier les cubes cachés.
"""
import random
from fr_c4 import *
import gen_fr_maths_ce2_solides as SO

R = random.Random(60119)
K = Kids(R)
SO.R = R
SO.DE.R = R

PRISM = [("un prisme droit à base triangulaire", 5, 9, 6), ("un prisme droit à base pentagonale", 7, 15, 10), ("un prisme droit à base hexagonale", 8, 18, 12),
         ("une pyramide à base pentagonale", 6, 10, 6), ("une pyramide à base hexagonale", 7, 12, 7)]


def s_prisme():
    n, f, a, s = R.choice(PRISM)
    i = R.randint(0, 2)
    word = ["faces", "arêtes", "sommets"][i]
    v = [f, a, s][i]
    return M("Combien %s a %s ?" % (("d’" if word[0] in "aeiou" else "de ") + word, n), str(v), [str(x) for x in (f, a, s, v + 1, v - 1) if x != v][:3],
             "%s a %d faces, %d arêtes et %d sommets. Réponse : <b>%d</b>." % (n[0].upper() + n[1:], f, a, s, v))


def s_patron_pave():
    L_, l_, h_ = R.sample(range(2, 9), 3)
    k = R.choice(["nb", "rect"])
    if k == "nb":
        return M("Combien de faces faut-il dessiner sur le patron d’un pavé droit ?", "6", ["4", "8", "12"], "Un pavé droit a 6 faces : son patron a <b>6 rectangles</b>.") if R.random() < 0.3 else \
            M("Un pavé droit mesure %d cm × %d cm × %d cm. Combien de faces de %d cm × %d cm a-t-il ?" % (L_, l_, h_, L_, l_), "2", ["1", "4", "6"],
              "Les faces opposées sont identiques : il y a <b>2</b> faces de %d cm × %d cm." % (L_, l_))
    return M("Un cube a une arête de %d cm. Quelle est l’aire totale de son patron ?" % l_, "%d cm²" % (6 * l_ * l_), ["%d cm²" % (l_ * l_), "%d cm²" % (4 * l_ * l_), "%d cm³" % (l_ ** 3)],
             "6 faces carrées de %d cm² : 6 × %d = <b>%d cm²</b>." % (l_ * l_, l_ * l_, 6 * l_ * l_))


def main():
    seen = set()
    sets = [("Reconnaître les solides", mix(R, seen, [(SO.s1, 20)])), ("Faces, arêtes et sommets", mix(R, seen, [(SO.s2, 8), (s_prisme, 8), (SO.s3_quiz, 4)])),
            ("Les faces des solides", mix(R, seen, [(SO.s3_faces, 7), (SO.s3_count, 7), (s_patron_pave, 6)])), ("Les patrons du cube", mix(R, seen, [(SO.s4, 20)])),
            ("Assemblages de cubes", mix(R, seen, [(SO.s5_plan, 12), (SO.s3_haut, 8)]))]
    body = L(["Un solide a des <b>faces</b> (surfaces planes), des <b>arêtes</b> (segments où deux faces se touchent) et des <b>sommets</b>.",
              "Cube : 6 faces carrées, 12 arêtes, 8 sommets. Prisme droit : deux bases identiques et des faces rectangulaires. Pyramide : une base et des faces triangulaires.",
              "Un <b>patron</b> est une figure plane qu’on peut plier pour fabriquer le solide, sans que deux faces se superposent."],
             [("Prisme à base triangulaire", ["2 bases + 3 faces latérales", "3 × 3 = 9 arêtes", "2 × 3 = 6 sommets"], "5 faces, 9 arêtes, 6 sommets")],
             [["Confondre arête et face", "La face est une surface ; l’arête est un segment."],
              ["Croire que 6 carrés collés forment toujours un patron de cube", "Il faut vérifier en pliant qu’aucune face ne se superpose."],
              ["Oublier les cubes cachés dans un assemblage", "Un nombre sur le plan indique combien de cubes sont empilés, même ceux qu’on ne voit pas."]])
    faq = [("Combien y a-t-il de patrons différents du cube ?", "Il y en a 11."),
           ("Qu’est-ce qu’un prisme droit ?", "Un solide qui a deux bases identiques et parallèles, reliées par des faces rectangulaires.")]
    unit("6e", R, "solides-et-patrons", "E",
         "Reconnaître, nommer et décrire des solides (cube, pavé droit, prisme droit, pyramide, cylindre, cône, boule) ; utiliser le vocabulaire face, arête, sommet ; reconnaître et construire des patrons du cube et du pavé ; dénombrer des assemblages de cubes",
         "Solides et patrons", "Solides et patrons",
         "Fiches de maths 6e sur les solides : reconnaître les solides, faces, arêtes, sommets, patrons du cube et assemblages de cubes. 100 exercices corrigés.",
         "Cube : 6 faces, 12 arêtes, 8 sommets.", "Un patron se plie sans que deux faces se superposent.", body, faq, sets, 19)


if __name__ == "__main__":
    main()
