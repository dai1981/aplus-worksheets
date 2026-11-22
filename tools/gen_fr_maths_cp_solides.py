# -*- coding: utf-8 -*-
"""
France Maths CP (CE1 : build(1)) : Les solides
  python3 tools/gen_fr_maths_cp_solides.py
CP : cube, pavé droit, boule, cylindre, cône ; rouler ou glisser ; faces ; tours de cubes. CE1 : + pyramide ; faces, arêtes, sommets ;
constructions de cubes (exercices du générateur CE2 avec un autre tirage).
Erreurs : confondre cube et pavé, appeler « rond » une boule et un disque, croire qu’un cylindre n’a pas de face plane.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, pic, solide_svg
import k_pics as KP
import gen_fr_maths_ce2_solides as SO

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53015 + 100 * lv)
    K = Kids(R)
    SO.R = R
    SO.DE.R = R


NOM0 = {"cube": "un cube", "pave": "un pavé droit", "boule": "une boule", "cylindre": "un cylindre", "cone": "un cône"}
COLS = ["#cfe6d6", "#f6d6a8", "#c9dcf2", "#f2c6d0", "#e8e0a8"]
WHY = {"cube": "Toutes ses faces sont des carrés pareils.", "pave": "Il ressemble à une boîte : ses faces sont des rectangles.",
       "boule": "Elle est toute ronde.", "cylindre": "Il a deux disques et il peut rouler.", "cone": "Il a un disque et une pointe."}


def s1():
    k = R.choice(list(NOM0))
    ans = NOM0[k]
    conf = {"cube": "un pavé droit", "pave": "un cube", "boule": "un disque", "cylindre": "un cône", "cone": "un cylindre"}[k]
    w = [conf] + [n for n in NOM0.values() if n not in (ans, conf)]
    q = R.choice(["Comment s’appelle ce solide ?", "Quel est le nom de ce solide ?"])
    return mcq("<div class='qfig'>%s</div>%s" % (solide_svg(k, R.choice([28, 32, 36]), R.choice(COLS)), q), ans, w, "%s C’est <b>%s</b>." % (WHY[k], ans))


ROULE = {"cube": "non", "pave": "non", "boule": "oui", "cylindre": "oui", "cone": "oui"}


def s2():
    k = R.choice(list(NOM0))
    if R.random() < 0.5:
        a = ROULE[k]
        return mcq("<div class='qfig'>%s</div>Ce solide peut-il rouler ?" % solide_svg(k, 32, R.choice(COLS)), a, ["non" if a == "oui" else "oui", "seulement s’il est petit", "on ne peut pas savoir"],
                   "%s %s" % (WHY[k], "Il a une partie courbe : il <b>peut rouler</b>." if a == "oui" else "Il n’a que des faces plates : il <b>ne peut pas rouler</b>, il glisse."))
    Q = [("Quel solide roule dans toutes les directions ?", "une boule", ["un cube", "un pavé droit", "un cylindre"]),
         ("Quel solide n’a que des faces carrées ?", "un cube", ["un pavé droit", "une boule", "un cône"]),
         ("Quel solide a une pointe ?", "un cône", ["un cylindre", "une boule", "un cube"]),
         ("Quel solide ressemble à une boîte à chaussures ?", "un pavé droit", ["un cube", "un cylindre", "une boule"]),
         ("Quel solide a deux disques et peut rouler tout droit ?", "un cylindre", ["un cône", "une boule", "un cube"]),
         ("Lequel de ces solides ne peut pas rouler ?", "un cube", ["une boule", "un cylindre", "un cône"]),
         ("Quel solide n’a aucune face plate ?", "une boule", ["un cylindre", "un cône", "un cube"]),
         ("On peut empiler facilement des…", "cubes", ["boules", "cônes", "boules de neige"])]
    q, a, w = R.choice(Q)
    return mcq(q, a, w, "Réponse : <b>%s</b>." % a)


VIE0 = [(t, a) for t, a in SO.VIE if a != "une pyramide"] + [("un dé à coudre", "un cylindre"), ("une boule de pétanque", "une boule"), ("une gomme rectangulaire", "un pavé droit"),
                                                            ("un cube de glace", "un cube"), ("un entonnoir retourné", "un cône"), ("une pomme", "une boule"),
                                                            ("une boîte de mouchoirs", "un pavé droit"), ("une pile", "un cylindre"), ("un livre fermé", "un pavé droit")]


def s3():
    thing, ans = R.choice(VIE0)
    pool = ["une boule", "un cylindre", "un pavé droit", "un cube", "un cône"] + (["une pyramide"] if L else [])
    w = [x for x in pool if x != ans]
    R.shuffle(w)
    de = ("d’" if thing.startswith("un") else "de ") + thing
    return mcq("Quelle est la forme %s ?" % de, ans, w, "La forme %s est <b>%s</b>." % (de, ans))


FACES0 = [("Quelle est la forme des faces d’un cube ?", "des carrés", ["des triangles", "des disques", "des ronds"]),
          ("Combien de faces a un cube ?", "6", ["4", "8", "12"]), ("Combien de faces a un pavé droit ?", "6", ["4", "8", "2"]),
          ("Quelle est la forme des deux faces plates d’un cylindre ?", "des disques", ["des carrés", "des triangles", "des rectangles"]),
          ("Combien de faces plates a un cône ?", "1", ["2", "0", "3"]), ("Combien de faces plates a une boule ?", "0", ["1", "2", "6"]),
          ("Combien de faces plates a un cylindre ?", "2", ["1", "0", "3"]),
          ("Si on pose un cube sur une feuille et qu’on fait le tour d’une face, quelle figure obtient-on ?", "un carré", ["un disque", "un triangle", "un rectangle long"]),
          ("Si on fait le tour de la base d’un cône, quelle figure obtient-on ?", "un disque", ["un carré", "un triangle", "un rectangle"]),
          ("Quelle est la forme des faces d’un pavé droit ?", "des rectangles", ["des disques", "des triangles", "des ronds"])]


def s4():
    if R.random() < 0.5:
        q, a, w = R.choice(FACES0)
        return mcq(q, a, w, "Réponse : <b>%s</b>." % a)
    n = R.randint(2, 4)
    hs = R.sample(range(1, 8), n)
    i = max(range(n), key=lambda j: hs[j])
    svg = pic(KP.towers_svg(hs), "%d tours de cubes A à %s" % (n, "ABCD"[n - 1]), lg=True)
    if R.random() < 0.5:
        return mcq("<div class='qfig'>%s</div>Quelle tour est la plus haute ?" % svg, "la tour %s" % "ABCD"[i], ["la tour %s" % "ABCD"[j] for j in range(n) if j != i] + ["elles ont la même hauteur"],
                   "La tour %s a %d cubes : c’est <b>la plus haute</b>." % ("ABCD"[i], hs[i]))
    t = sum(hs)
    return mcq("<div class='qfig'>%s</div>Combien de cubes faut-il pour construire toutes ces tours ?" % svg, str(t), [str(t + 1), str(t - 1), str(max(hs) * n) if max(hs) * n != t else str(t + 2)],
               "%s = <b>%d</b> cubes." % (" + ".join(map(str, hs)), t))


def s5():
    p = K.next()
    k = R.choice(["tour", "deux", "pile", "manque"])
    if k == "tour":
        a, b = R.randint(3, 9), R.randint(2, 6)
        return mcq("%s construit une tour de %d cubes. %s ajoute %d cubes. Combien de cubes a la tour ?" % (p[0], a, p[1].capitalize(), b), str(a + b), [str(a - b) if a > b else str(a + b + 1), str(a + b - 1), str(b)],
                   "%d + %d = <b>%d</b> cubes." % (a, b, a + b))
    if k == "deux":
        a, b = R.randint(4, 10), R.randint(2, 8)
        if a == b:
            return None
        return mcq("Une tour a %d cubes, une autre en a %d. Combien de cubes de plus a la plus haute ?" % (a, b), str(abs(a - b)), [str(a + b), str(max(a, b)), str(abs(a - b) + 1)],
                   "%d − %d = <b>%d</b>." % (max(a, b), min(a, b), abs(a - b)))
    if k == "pile":
        n, h = R.randint(2, 4), R.randint(2, 5)
        return mcq("%s fait %d tours de %d cubes chacune. Combien de cubes utilise-t-%s ?" % (p[0], n, h, p[1]), str(n * h), [str(n + h), str(n * h + 1), str(h)],
                   "%s = <b>%d</b> cubes." % (" + ".join([str(h)] * n), n * h))
    a, b = R.randint(2, 6), R.randint(7, 12)
    return mcq("La tour de %s a %d cubes. %s veut une tour de %d cubes. Combien de cubes doit-%s ajouter ?" % (p[0], a, p[1].capitalize(), b, p[1]), str(b - a), [str(a + b), str(b), str(b - a + 1)],
               "%d + … = %d : il faut <b>%d</b> cubes." % (a, b, b - a))


def build(lv):
    setup(lv)
    seen = set()
    if lv == 0:
        sets = [("Reconnaître les solides", mix(R, seen, [(s1, 20)])), ("Rouler ou glisser", mix(R, seen, [(s2, 20)])),
                ("Les solides autour de nous", mix(R, seen, [(s3, 20)])), ("Faces et tours de cubes", mix(R, seen, [(s4, 20)])),
                ("Problèmes", mix(R, seen, [(s5, 20)]))]
        th = ["Le <b>cube</b> a 6 faces carrées. Le <b>pavé droit</b> ressemble à une boîte.",
              "La <b>boule</b> est toute ronde. Le <b>cylindre</b> a deux disques. Le <b>cône</b> a un disque et une pointe.",
              "Une <b>face</b> est une partie plate d’un solide. Les solides qui ont une partie courbe peuvent rouler."]
        ex = example("Une boîte de conserve", ["deux disques", "elle roule"], "un cylindre")
        faq = [("Quelle est la différence entre un disque et une boule ?", "Le disque est plat (une figure) ; la boule est un solide qu’on peut tenir dans la main."),
               ("Quels solides peuvent rouler ?", "La boule, le cylindre et le cône.")]
        std = "Reconnaître et nommer le cube, le pavé droit, la boule, le cylindre et le cône ; utiliser le mot face ; reproduire des assemblages de cubes"
        meta = "Fiches de maths CP sur les solides : cube, pavé droit, boule, cylindre, cône, rouler ou glisser, faces et tours de cubes. 100 exercices corrigés."
    else:
        sets = [("Reconnaître les solides", mix(R, seen, [(SO.s1, 20)])), ("Faces, arêtes et sommets", mix(R, seen, [(SO.s2, 12), (SO.s3_quiz, 8)])),
                ("Les faces des solides", mix(R, seen, [(SO.s3_faces, 7), (SO.s3_count, 7), (SO.s3_haut, 6)])), ("Les solides autour de nous", mix(R, seen, [(s3, 20)])),
                ("Constructions de cubes", mix(R, seen, [(SO.s5_plan, 12), (s4, 8)]))]
        th = ["Un solide a des <b>faces</b> (parties plates), des <b>arêtes</b> (où deux faces se touchent) et des <b>sommets</b> (les pointes).",
              "Le cube a 6 faces carrées, 12 arêtes et 8 sommets. La <b>pyramide</b> a des faces triangulaires qui se rejoignent en un sommet.",
              "La boule, le cylindre et le cône ont une surface courbe : ils peuvent rouler."]
        ex = example("Un dé à jouer", ["6 faces carrées pareilles"], "un cube")
        faq = [("Qu’est-ce qu’une arête ?", "C’est un segment où deux faces d’un solide se rencontrent."),
               ("Quelle est la différence entre un cube et un pavé droit ?", "Les 6 faces du cube sont des carrés pareils ; celles du pavé sont des rectangles.")]
        std = "Reconnaître et nommer le cube, le pavé droit, la pyramide, la boule, le cylindre et le cône ; utiliser les mots face, arête et sommet ; décrire des assemblages de cubes"
        meta = "Fiches de maths CE1 sur les solides : cube, pavé, pyramide, boule, cylindre, cône, faces, arêtes, sommets et constructions de cubes. 100 exercices corrigés."
    mist = [["Confondre cube et pavé droit", "Le cube a toutes ses faces carrées et pareilles."],
            ["Dire « rond » pour une boule et un disque", "La boule est un solide, le disque est une figure plate."],
            ["Croire qu’un cylindre n’a pas de face plate", "Il a 2 faces plates : les deux disques."]]
    unit(lv, R, "solides", "E", std, "Les solides", "Solides", meta, "Un solide se tient dans la main.", "Le cube a 6 faces carrées.", lesson(th, [ex], mist), faq, sets, 15)


if __name__ == "__main__":
    build(0)
