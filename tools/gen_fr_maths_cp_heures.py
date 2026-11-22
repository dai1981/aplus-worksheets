# -*- coding: utf-8 -*-
"""
France Maths CP : Lire l’heure (heures entières, moments de la journée, jours) ; CE1 (build(1)) : Heures et durées
  python3 tools/gen_fr_maths_cp_heures.py
CE1 : heures, demi-heures et quarts d’heure, matin et après-midi, 1 h = 60 min, durées (exercices du générateur CE2 avec un autre tirage).
Erreurs : inverser petite et grande aiguille, lire 12 h quand la grande aiguille est sur le 12, confondre hier et demain.
"""
import random
from fr_c2 import pl, mcq, num, lesson, example, unit, mix, Kids, GN, horloge, hm, dur
import gen_fr_maths_ce2_heures_et_durees as HD

R = K = None
L = 0


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(53013 + 100 * lv)
    K = Kids(R)
    HD.R = R
    HD.K = K


def H(h):
    return "%d h" % h


def s1():
    h = R.randint(1, 12)
    q = R.choice(["Quelle heure est-il ?", "Quelle heure indique l’horloge ?"])
    return mcq("<div class='qfig'>%s</div>%s" % (horloge(h, 0), q), H(h), [H(12) if h != 12 else H(6), H(h % 12 + 1), H(h - 1 if h > 1 else 11)],
               "La grande aiguille est sur le 12 : c’est une heure pile. La petite aiguille est sur le %d : il est <b>%d h</b>." % (h, h))


def s2():
    h = R.randint(1, 12)
    k = R.choice(["petite", "apres", "avant"])
    if k == "petite":
        return mcq("Il est %d h. Sur quel nombre est la petite aiguille ?" % h, "sur le %d" % h, ["sur le 12" if h != 12 else "sur le 6", "sur le %d" % (h % 12 + 1), "sur le %d" % (h - 1 if h > 1 else 11)],
                   "À %d h, la petite aiguille montre l’heure : <b>sur le %d</b> ; la grande est sur le 12." % (h, h))
    if k == "apres":
        d = R.randint(1, 3)
        v = (h + d - 1) % 12 + 1
        return mcq("<div class='qfig'>%s</div>Quelle heure sera-t-il dans %s ?" % (horloge(h, 0), pl(d, "heure")), H(v), [H((h - d - 1) % 12 + 1), H(h), H(v % 12 + 1)],
                   "%d h + %s = <b>%d h</b>." % (h, pl(d, "heure"), v))
    d = R.randint(1, 3)
    v = (h - d - 1) % 12 + 1
    return mcq("<div class='qfig'>%s</div>Quelle heure était-il il y a %s ?" % (horloge(h, 0), pl(d, "heure")), H(v), [H((h + d - 1) % 12 + 1), H(h), H(v - 1 if v > 1 else 12)],
               "On recule de %s : il était <b>%d h</b>." % (pl(d, "heure"), v))


MOMENTS = [("On prend le petit-déjeuner", "le matin"), ("On se réveille", "le matin"), ("On va à l’école", "le matin"), ("On déjeune à la cantine", "le midi"),
           ("On goûte après l’école", "l’après-midi"), ("On dîne", "le soir"), ("On regarde les étoiles", "la nuit"), ("On dort dans son lit", "la nuit"),
           ("Le soleil se lève", "le matin"), ("Le soleil se couche", "le soir"), ("On se brosse les dents avant de dormir", "le soir"), ("On fait la sieste après le repas de midi", "l’après-midi")]
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def s3():
    if R.random() < 0.5:
        a, m = R.choice(MOMENTS)
        return mcq("%s… À quel moment de la journée ?" % a, m, [x for x in ["le matin", "le midi", "l’après-midi", "le soir", "la nuit"] if x != m][:3] if m != "le matin" else ["le soir", "la nuit", "l’après-midi"],
                   "%s <b>%s</b>." % (a, m))
    seq = [("se réveiller", 0), ("prendre le petit-déjeuner", 1), ("aller à l’école", 2), ("déjeuner", 3), ("goûter", 4), ("dîner", 5), ("se coucher", 6)]
    xs = sorted(R.sample(seq, 4), key=lambda t: t[1])
    first = R.random() < 0.5
    ans = xs[0][0] if first else xs[-1][0]
    sh = list(xs)
    R.shuffle(sh)
    return mcq("Dans la journée, que fait-on en %s : %s ?" % ("premier" if first else "dernier", ", ".join(t[0] for t in sh)), ans, [t[0] for t in xs if t[0] != ans],
               "L’ordre de la journée : %s. En %s : <b>%s</b>." % (", ".join(t[0] for t in xs), "premier" if first else "dernier", ans))


def s4():
    i = R.randrange(7)
    k = R.choice(["apres", "avant", "demain", "hier"])
    d = 1 if k in ("apres", "demain") else -1
    v = JOURS[(i + d) % 7]
    q = {"apres": "Quel jour vient juste après %s ?", "avant": "Quel jour vient juste avant %s ?", "demain": "Aujourd’hui, c’est %s. Quel jour serons-nous demain ?",
         "hier": "Aujourd’hui, c’est %s. Quel jour étions-nous hier ?"}[k] % JOURS[i]
    return mcq(q, v, [JOURS[(i - d) % 7], JOURS[(i + 2 * d) % 7], JOURS[i]], "Lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche : <b>%s</b>." % v)


def s5():
    p = K.next()
    k = R.choice(["dure", "fin", "debut", "semaine"])
    if k == "dure":
        a = R.randint(1, 4)
        b = a + R.randint(1, 4)
        ev = R.choice(["La fête", "La promenade", "Le pique-nique", "Le match"])
        return mcq("%s commence à %d h et finit à %d h. Combien d’heures dure-t-%s ?" % (ev, a, b, "elle" if ev.startswith("La") else "il"), pl(b - a, "heure"), [pl(a + b, "heure"), pl(b, "heure"), pl(b - a + 1, "heure")],
                   "De %d h à %d h : %d − %d = <b>%s</b>." % (a, b, b, a, pl(b - a, "heure")))
    if k == "fin":
        a, d = R.randint(1, 8), R.randint(1, 3)
        return mcq("%s part au parc à %d h. %s y reste %s. À quelle heure rentre-t-%s ?" % (p[0], a, p[1].capitalize(), pl(d, "heure"), p[1]), H(a + d), [H(a - d) if a > d else H(a + d + 1), H(d), H(a + d + 1)],
                   "%d h + %s = <b>%d h</b>." % (a, pl(d, "heure"), a + d))
    if k == "debut":
        b, d = R.randint(4, 11), R.randint(1, 3)
        return mcq("Le spectacle finit à %d h. Il a duré %s. À quelle heure a-t-il commencé ?" % (b, pl(d, "heure")), H(b - d), [H(b + d), H(d), H(b - d + 1)],
                   "On recule de %s : <b>%d h</b>." % (pl(d, "heure"), b - d))
    i = R.randrange(7)
    n = R.randint(2, 4)
    return mcq("Aujourd’hui, c’est %s. L’anniversaire de %s est dans %d jours. Quel jour sera-t-il ?" % (JOURS[i], p[0], n), JOURS[(i + n) % 7], [JOURS[(i + n - 1) % 7], JOURS[(i + n + 1) % 7], JOURS[(i - n) % 7]],
               "On avance de %d jours : <b>%s</b>." % (n, JOURS[(i + n) % 7]))


# ---------------------------------------------------------------- CE1
def e1():
    h = R.randint(1, 12)
    m = R.choice([0, 15, 30, 45])
    swap = (m // 5 if m else 12, (h % 12) * 5)
    wr = [hm(*swap) if swap != (h, m) and swap[1] in (0, 15, 30, 45) else hm(h, (m + 30) % 60), hm(h % 12 + 1, m), hm(h, (m + 15) % 60)]
    return mcq("<div class='qfig'>%s</div>Quelle heure est-il le matin ?" % horloge(h, m), hm(h, m), [w for w in wr if w != hm(h, m)],
               "La petite aiguille indique les heures, la grande les minutes : 15 min sur le 3, 30 min sur le 6, 45 min sur le 9. Il est <b>%s</b>." % hm(h, m))


def e3():
    it = HD.s3()
    if it is None or "secondes" in it["q"] or "heures y a-t-il dans" in it["q"]:
        return None
    return it


def e4():
    it = HD.s4()
    return it


def build(lv):
    setup(lv)
    seen = set()
    if lv == 0:
        sets = [("Lire l’heure", mix(R, seen, [(s1, 20)])), ("Les aiguilles, avant et après", mix(R, seen, [(s2, 20)])),
                ("Les moments de la journée", mix(R, seen, [(s3, 20)])), ("Les jours de la semaine", mix(R, seen, [(s4, 20)])),
                ("Problèmes", mix(R, seen, [(s5, 20)]))]
        th = ["La <b>petite aiguille</b> montre les heures, la <b>grande aiguille</b> les minutes.",
              "Quand la grande aiguille est sur le 12, c’est une heure pile : 3 h, 7 h…",
              "Les 7 jours de la semaine : lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche."]
        ex = example("La petite aiguille est sur le 4, la grande sur le 12", ["heure pile"], "4 h")
        mist = [["Inverser les aiguilles", "La petite montre l’heure, la grande les minutes."],
                ["Lire 12 h parce que la grande aiguille est sur le 12", "C’est la petite aiguille qui dit l’heure."],
                ["Confondre hier et demain", "Hier, c’est avant aujourd’hui ; demain, c’est après."]]
        faq = [("À quoi sert la grande aiguille ?", "Elle montre les minutes. Au CP, on lit surtout les heures pile : elle est alors sur le 12."),
               ("Combien y a-t-il de jours dans une semaine ?", "7 jours.")]
        unit(lv, R, "lire-l-heure", "G",
             "Lire l’heure (heures entières) sur une horloge à aiguilles ; connaître les moments de la journée et les jours de la semaine ; résoudre des problèmes de durées en heures entières",
             "Lire l’heure", "Lire l’heure",
             "Fiches de maths CP pour lire l’heure : heures pile, petite et grande aiguille, moments de la journée, jours de la semaine et problèmes. 100 exercices corrigés.",
             "La petite aiguille montre l’heure.", "Grande aiguille sur le 12 : heure pile.", lesson(th, [ex], mist), faq, sets, 13)
        return
    sets = [("Lire l’heure", mix(R, seen, [(e1, 20)])), ("Et quart, et demie, l’après-midi", mix(R, seen, [(HD.s2_mots, 10), (HD.s2_apm, 10)])),
            ("Heures, minutes, jours", mix(R, seen, [(e3, 20)])), ("Calculer une durée", mix(R, seen, [(e4, 20)])), ("Problèmes", mix(R, seen, [(HD.s5, 20)]))]
    th = ["La petite aiguille montre les heures, la grande les minutes. Quand la grande est sur le 6, il est « et demie » (30 min).",
          "Et quart = 15 min ; moins le quart = 15 min avant l’heure. 1 h = 60 min.",
          "L’après-midi, on peut ajouter 12 : 3 h de l’après-midi = 15 h."]
    ex = example("Un film commence à 14 h 30 et dure 1 h 15 min", ["14 h 30 + 1 h = 15 h 30", "15 h 30 + 15 min = 15 h 45"], "15 h 45")
    mist = [["Inverser les aiguilles", "La petite montre l’heure, la grande les minutes."],
            ["Lire 3 h 30 en « 3 h 6 »", "La grande aiguille sur le 6 veut dire 30 minutes."],
            ["1 h = 100 min", "1 heure = 60 minutes."]]
    faq = [("Que veut dire « moins le quart » ?", "15 minutes avant l’heure : 9 h moins le quart = 8 h 45."),
           ("Combien de minutes dans une heure ?", "60 minutes.")]
    unit(lv, R, "heures-et-durees", "G",
         "Lire l’heure (heures, demi-heures, quarts d’heure) ; distinguer le matin et l’après-midi ; connaître les relations 1 h = 60 min, 1 jour = 24 h, 1 semaine = 7 jours ; calculer des durées",
         "Heures et durées", "Heures et durées",
         "Fiches de maths CE1 sur les heures et les durées : lire l’heure, et quart, et demie, matin et après-midi, minutes, calculer une durée et problèmes. 100 exercices corrigés.",
         "1 h = 60 min", "Et demie = 30 min ; et quart = 15 min.", lesson(th, [ex], mist), faq, sets, 13)


if __name__ == "__main__":
    build(0)
