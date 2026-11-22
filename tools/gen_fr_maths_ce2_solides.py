# -*- coding: utf-8 -*-
"""
France Maths CE2 : Les solides (Espace et géométrie)
  python3 tools/gen_fr_maths_ce2_solides.py
Reconnaître cube, pavé droit, pyramide, boule, cylindre, cône ; faces, arêtes, sommets ; formes des faces ;
patrons du cube ; solides dans la vie courante.
Erreurs : confondre cube et pavé, arêtes et sommets, compter seulement les faces visibles, patron avec deux faces superposées.
"""
import random
import gen_de_mathe_k3_koerper_und_figuren as DE
from fr_common import mcq, lesson, example, make_unit, mix, solide_svg, table

R = random.Random(51016)
DE.R = R

NOM = {"cube": "un cube", "pave": "un pavé droit", "boule": "une boule", "cylindre": "un cylindre", "cone": "un cône", "pyramide": "une pyramide"}
SAF = {"un cube": (6, 12, 8), "un pavé droit": (6, 12, 8), "une pyramide à base carrée": (5, 8, 5), "une pyramide à base triangulaire": (4, 6, 4)}


def s1():
    k = R.choice(list(NOM))
    col = R.choice(["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0", "#e8e0a8"])
    ans = NOM[k]
    conf = {"cube": "un pavé droit", "pave": "un cube", "boule": "un disque", "cylindre": "un cône", "cone": "une pyramide", "pyramide": "un cône"}[k]
    w = [conf] + [n for n in NOM.values() if n not in (ans, conf)]
    why = {"cube": "Ses 6 faces sont des carrés identiques.", "pave": "Il a 6 faces rectangulaires ; elles ne sont pas toutes pareilles.",
           "boule": "Elle est toute ronde, sans face plane.", "cylindre": "Il a deux disques identiques et une surface courbe.",
           "cone": "Il a un disque et une pointe.", "pyramide": "Ses faces sont des triangles qui se rejoignent en une pointe."}[k]
    return mcq("<div class='qfig'>%s</div>Comment s’appelle ce solide ?%s" % (solide_svg(k, R.choice([28, 32, 36]), col), ""), ans, w,
               "%s C’est <b>%s</b>." % (why, ans))


def s2():
    n = R.choice(list(SAF))
    i = R.randint(0, 2)
    word = ["faces", "arêtes", "sommets"][i]
    v = SAF[n][i]
    others = [x for x in SAF[n] if x != v] + [v + 2, v - 2, 4]
    return mcq("Combien %s a %s ?" % (("d’" if word[0] in "aeiouéè" else "de ") + word, n), v, [x for x in others if x != v and x > 0],
               "%s a %d faces, %d arêtes et %d sommets. On demande les %s : <b>%d</b>." % (n[0].upper() + n[1:], SAF[n][0], SAF[n][1], SAF[n][2], word, v))


QUIZ = [("Quel solide n’a ni face plane, ni arête, ni sommet ?", "une boule", ["un cube", "un cylindre", "un cône"]),
        ("Quel solide a deux faces en forme de disque ?", "un cylindre", ["un cône", "une boule", "un pavé droit"]),
        ("Quel solide a une pointe et un disque ?", "un cône", ["une pyramide", "un cylindre", "une boule"]),
        ("Quel solide a 6 faces carrées identiques ?", "un cube", ["un pavé droit", "une pyramide", "un cylindre"]),
        ("Quel solide a 6 faces rectangulaires, pas toutes identiques ?", "un pavé droit", ["un cube", "une pyramide", "un cône"]),
        ("Quel solide peut rouler dans toutes les directions ?", "une boule", ["un cylindre", "un cône", "un cube"]),
        ("Quel solide a des faces triangulaires qui se rejoignent en un sommet ?", "une pyramide", ["un cône", "un cube", "un cylindre"]),
        ("Quel solide peut rouler et aussi tenir debout, sans pointe ?", "un cylindre", ["une boule", "un cône", "un cube"])]


def s3_quiz():
    q, a, w = R.choice(QUIZ)
    return mcq(q, a, w, "Réponse : <b>%s</b>." % a)


FACES = [("Quelle est la forme des faces d’un cube ?", "des carrés", ["des rectangles", "des triangles", "des disques"]),
         ("Quelle est la forme des faces d’un pavé droit ?", "des rectangles", ["des triangles", "des disques", "des losanges"]),
         ("Quelle est la forme de la base d’un cône ?", "un disque", ["un carré", "un triangle", "un rectangle"]),
         ("Quelle est la forme des faces latérales d’une pyramide ?", "des triangles", ["des carrés", "des disques", "des rectangles"]),
         ("Si on trace le contour de la base d’un cylindre, quelle figure obtient-on ?", "un cercle", ["un carré", "un triangle", "un rectangle"]),
         ("Si on trace le contour d’une face d’un cube, quelle figure obtient-on ?", "un carré", ["un cercle", "un triangle", "un losange"]),
         ("Si on trace le contour de la base d’une pyramide à base carrée, quelle figure obtient-on ?", "un carré", ["un triangle", "un cercle", "un pentagone"])]


def s3_faces():
    q, a, w = R.choice(FACES)
    return mcq(q, a, w, "Réponse : <b>%s</b>." % a)


def s4():
    it = DE.wuerfelnetz()
    if not it:
        return None
    q = it["q"].replace("aria-label='vier Netze A bis D'", "aria-label='quatre patrons A à D'")
    good = "Welches Netz kann man zu einem Würfel falten?" in q
    q = q.replace("Welches Netz kann man zu einem Würfel falten?", "Quel patron permet de fabriquer un cube ?")
    q = q.replace("Drei Netze ergeben einen Würfel. Welches Netz ergibt <b>keinen</b> Würfel?", "Trois patrons permettent de fabriquer un cube. Lequel ne le permet <b>pas</b> ?")
    k = it["c"][0]
    e = ("Avec le patron %s, en pliant, chacune des 6 faces se place à un endroit différent du cube." % k if good else
         "Avec le patron %s, deux faces se superposent en pliant et il manque une face." % k)
    return mcq(q, k, it["c"][1:], e)


VIE = [("un ballon de football", "une boule"), ("une orange", "une boule"), ("une boîte de conserve", "un cylindre"), ("une bougie", "un cylindre"),
       ("une boîte à chaussures", "un pavé droit"), ("une brique", "un pavé droit"), ("un dé à jouer", "un cube"), ("un morceau de sucre", "un cube"),
       ("un cornet de glace", "un cône"), ("un chapeau de fête", "un cône"), ("un plot de chantier", "un cône"), ("une brique de lait", "un pavé droit"),
       ("une bille", "une boule"), ("un rouleau d’essuie-tout", "un cylindre"), ("la pyramide du Louvre", "une pyramide"), ("un tube de colle", "un cylindre")]


COUNT = [("Combien de faces triangulaires a une pyramide à base carrée ?", 4, [5, 3, 8]),
         ("Combien de faces carrées a un cube ?", 6, [4, 8, 12]),
         ("Combien de disques a un cylindre ?", 2, [1, 3, 0]),
         ("Combien de disques a un cône ?", 1, [2, 0, 3]),
         ("Combien d’arêtes partent d’un sommet du cube ?", 3, [4, 2, 6]),
         ("Un pavé droit a 2 faces carrées. Combien de faces ne sont pas carrées ?", 4, [6, 2, 8]),
         ("Combien de faces triangulaires a une pyramide à base triangulaire ?", 4, [3, 5, 6])]


def s3_count():
    q, a, w = R.choice(COUNT)
    return mcq(q, a, w, "Réponse : <b>%d</b>." % a)


def tr(it, pairs):
    if not it:
        return None
    for a, b in pairs:
        it["q"], it["e"] = it["q"].replace(a, b), it["e"].replace(a, b)
        it["c"] = [c.replace(a, b) for c in it["c"]]
    return mcq(it["q"], it["c"][0], it["c"][1:], it["e"])


def s3_haut():
    return tr(DE.bauplan_hoch(), [("Bauplan eines Würfelgebäudes: Wie hoch ist der höchste Turm?", "Plan d’une construction en cubes vue du dessus : combien de cubes a la plus haute tour ?"),
                                  ("Die größte Zahl im Bauplan ist", "Le plus grand nombre du plan est"), ("Der höchste Turm ist", "La plus haute tour a"),
                                  (" Würfel</b> hoch.", " cubes</b>."), (" Würfel", " cubes")])


def s5_vie():
    thing, ans = R.choice(VIE)
    w = [x for x in ["une boule", "un cylindre", "un pavé droit", "un cube", "un cône", "une pyramide"] if x != ans]
    R.shuffle(w)
    de = ("d’" if thing.startswith("un") else "de ") + thing
    return mcq("Quelle est la forme %s ?" % de, ans, w, "La forme %s est <b>%s</b>." % (de, ans))


def s5_plan():
    return tr(DE.bauplan(), [("Ein Bauplan zeigt ein Würfelgebäude von oben. Die Zahl sagt, wie viele Würfel übereinander stehen. Wie viele Würfel sind es?",
                              "Ce plan montre une construction en cubes vue du dessus. Chaque nombre dit combien de cubes sont empilés. Combien de cubes y a-t-il en tout ?"),
                             ("Addiere alle Zahlen im Bauplan:", "On additionne tous les nombres du plan :")])


def main():
    seen = set()
    sets = [
        ("Reconnaître les solides", mix(R, seen, [(s1, 20)])),
        ("Faces, arêtes et sommets", mix(R, seen, [(s2, 12), (s3_quiz, 8)])),
        ("Les faces des solides", mix(R, seen, [(s3_faces, 7), (s3_count, 7), (s3_haut, 6)])),
        ("Les patrons du cube", mix(R, seen, [(s4, 20)])),
        ("Les solides autour de nous", mix(R, seen, [(s5_vie, 12), (s5_plan, 8)])),
    ]
    body = lesson(
        ["Un <b>solide</b> a des <b>faces</b> (surfaces planes), des <b>arêtes</b> (les bords où deux faces se touchent) et des <b>sommets</b> (les coins).",
         "Le <b>cube</b> a 6 faces carrées identiques. Le <b>pavé droit</b> a 6 faces rectangulaires.",
         "La boule, le cylindre et le cône ont une surface courbe : ils peuvent rouler.",
         "Un <b>patron</b> est un dessin à plier pour fabriquer un solide. Le patron d’un cube a 6 carrés."],
        [example("Le cube", ["6 faces, 12 arêtes, 8 sommets"], "comme le pavé droit"),
         example("La pyramide à base carrée", ["1 carré + 4 triangles = 5 faces", "8 arêtes, 5 sommets"], "5 faces")],
        [["Confondre cube et pavé droit", "Le cube a toutes ses faces carrées et identiques."],
         ["Confondre arêtes et sommets", "Une arête est un trait (un bord) ; un sommet est un point (un coin)."],
         ["Ne compter que les faces visibles sur le dessin", "Il y a aussi des faces cachées derrière et dessous."]],
        table(["Solide", "Faces", "Arêtes", "Sommets"], [["cube", "6", "12", "8"], ["pavé droit", "6", "12", "8"], ["pyramide à base carrée", "5", "8", "5"]]))
    faq = [("Quelle est la différence entre un carré et un cube ?", "Le carré est une figure plane (on le dessine) ; le cube est un solide (on peut le prendre en main). Les faces du cube sont des carrés."),
           ("Combien y a-t-il de patrons du cube ?", "Il existe 11 patrons différents du cube.")]
    make_unit(R, "solides", "E",
              "Reconnaître, nommer et décrire des solides usuels (cube, pavé droit, pyramide, boule, cylindre, cône) ; utiliser le vocabulaire face, arête, sommet ; reconnaître des patrons du cube (résumé du programme 2024 du cycle 2).",
              "Les solides : cube, pavé, pyramide…", "Solides CE2 : fiches et exercices avec corrigé", "Solides",
              "Fiches de maths CE2 sur les solides : cube, pavé droit, pyramide, boule, cylindre, cône, faces, arêtes, sommets et patrons du cube. 100 exercices corrigés.",
              "Un solide a des faces, des arêtes et des sommets.", "Le cube a 6 faces carrées, 12 arêtes et 8 sommets.",
              body, faq, sets, 16)


if __name__ == "__main__":
    main()
