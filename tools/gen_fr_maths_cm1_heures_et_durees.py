# -*- coding: utf-8 -*-
"""
France Maths CM1 (CM2 : build(2)) : Heures et durées (Grandeurs et mesures)
  python3 tools/gen_fr_maths_cm1_heures_et_durees.py
Lire l’heure sur une horloge à aiguilles, heures de 0 à 24, relations h/min (CM2 : et secondes), calculer une durée,
un horaire de début ou de fin, problèmes en une ou plusieurs étapes. Réutilise les fonctions du CE2 (autres tirages).
Erreurs : compter 100 minutes dans une heure, 1 h 30 = 1,30 h, oublier de passer l’heure pile.
"""
import random
from fr_c3 import mcq, num, lesson, example, unit, mix, Kids, GN, FOIS, DIV, hm, dur
import gen_fr_maths_ce2_heures_et_durees as CE

R = K = None
L = 1


def setup(lv):
    global R, K, L
    L = lv
    R = random.Random(52120 + 100 * lv)
    K = Kids(R)
    CE.R = R
    CE.K = K


def re(it):
    return mcq(it["q"], it["c"][0], it["c"][1:], it["e"]) if it else None


def s1():
    return re(CE.s1() if R.random() < 0.6 else CE.s2_apm())


def sec():
    k = R.choice(["m_s", "ms_s", "s_ms", "cmp"])
    if k == "m_s":
        a = R.randint(2, 9)
        return mcq("Complète : %d min = … s" % a, "%d s" % (a * 60), ["%d s" % (a * 100), "%d s" % (a * 10), "%d s" % (a * 60 + 60)], "1 min = 60 s : %d %s 60 = <b>%d s</b>." % (a, FOIS, a * 60))
    if k == "ms_s":
        a, b = R.randint(1, 5), R.randint(5, 55)
        return mcq("Complète : %d min %d s = … s" % (a, b), "%d s" % (a * 60 + b), ["%d s" % (a * 100 + b), "%d s" % (a + b), "%d s" % (a * 10 + b)], "%d %s 60 + %d = <b>%d s</b>." % (a, FOIS, b, a * 60 + b))
    if k == "s_ms":
        n = R.randint(65, 290)
        if n % 60 == 0:
            return None
        return mcq("Complète : %d s = … min … s" % n, "%d min %d s" % (n // 60, n % 60), ["%d min %d s" % (n // 100, n % 100) if n >= 100 else "%d min %d s" % (n // 10, n % 10), "%d min %d s" % (n // 60 + 1, n % 60), "%d min" % (n // 60)],
                   "60 s = 1 min. %d = %d %s 60 + %d : <b>%d min %d s</b>." % (n, n // 60, FOIS, n % 60, n // 60, n % 60))
    a, b = R.randint(61, 200), R.randint(1, 3)
    c = R.randint(0, 59)
    x = b * 60 + c
    if x == a:
        return None
    big = "%d s" % a if a > x else "%d min %d s" % (b, c)
    return mcq("Quelle durée est la plus longue : %d s ou %d min %d s ?" % (a, b, c), big, ["%d min %d s" % (b, c) if big == "%d s" % a else "%d s" % a, "elles sont égales", "on ne peut pas comparer"],
               "%d min %d s = %d s. Réponse : <b>%s</b>." % (b, c, x, big))


def s2():
    return sec() if L == 2 and R.random() < 0.5 else re(CE.s3())


def s3():
    h1 = R.randint(6, 19)
    m1 = R.choice([0, 5, 10, 15, 20, 25, 35, 40, 45, 50, 55])
    d = R.choice([35, 50, 75, 95, 105, 125, 140, 155, 185, 200, 215, 250])
    h2, m2 = divmod(h1 * 60 + m1 + d, 60)
    if h2 > 23:
        return None
    w = [dur(d + 40) if m2 < m1 else dur(d + 10), dur((h2 - h1) * 60 + abs(m2 - m1)) if m2 < m1 else dur(d - 5), dur(d + 60), dur(d - 10)]
    return mcq("Un trajet commence à %s et se termine à %s. Combien de temps dure-t-il ?" % (hm(h1, m1), hm(h2, m2)), dur(d), [x for x in w if x != dur(d)],
               "On avance jusqu’à l’heure pile, puis on compte les heures et les minutes : de %s à %s, il s’écoule <b>%s</b>." % (hm(h1, m1), hm(h2, m2), dur(d)))


def s4():
    if L == 2 and R.random() < 0.5:
        p = K.next()
        k = R.choice(["course", "chrono"])
        if k == "course":
            a, b = R.randint(52, 75), R.randint(45, 70)
            return mcq("%s court le 400 m en %d s, puis encore en %d s. Quelle est la durée totale ?" % (p[0], a, b), "%d min %d s" % ((a + b) // 60, (a + b) % 60),
                       ["%d s" % (a + b - 60), "%d min %d s" % ((a + b) // 100, (a + b) % 100), "%d min %d s" % ((a + b) // 60 + 1, (a + b) % 60)],
                       "%d + %d = %d s = <b>%d min %d s</b>." % (a, b, a + b, (a + b) // 60, (a + b) % 60))
        m, s = R.randint(1, 4), R.randint(10, 50)
        t = m * 60 + s
        r = R.randint(15, 45)
        if s + r < 60 or s + r == 60:
            return None
        return mcq("Un chronomètre affiche %d min %d s. On ajoute %d s. Que va-t-il afficher ?" % (m, s, r), "%d min %d s" % ((t + r) // 60, (t + r) % 60) if (t + r) % 60 else "%d min" % ((t + r) // 60),
                   ["%d min %d s" % (m, s + r), "%d min %d s" % (m + 1, s + r), "%d min %d s" % ((t + r) // 60 + 1, (t + r) % 60)],
                   "%d s + %d s = %d s = 1 min %d s : <b>%s</b>." % (s, r, s + r, s + r - 60, "%d min %d s" % ((t + r) // 60, (t + r) % 60)) if s + r >= 60 else "%d s + %d s = %d s : <b>%d min %d s</b>." % (s, r, s + r, m, s + r))
    return re(CE.s5())


def s5():
    p = K.next()
    k = R.choice(["seances", "film2", "train", "ecole"])
    if k == "seances":
        n, d, pause = R.randint(3, 5), R.choice([30, 40, 45, 50]), R.choice([10, 15])
        t = n * d + (n - 1) * pause
        h1, m1 = R.randint(8, 14), R.choice([0, 15, 30])
        h2, m2 = divmod(h1 * 60 + m1 + t, 60)
        return mcq("Un club fait %d séances de %d min, avec %d min de pause entre deux séances. Il commence à %s. À quelle heure finit-il ?" % (n, d, pause, hm(h1, m1)), hm(h2, m2),
                   [hm(*divmod(h1 * 60 + m1 + n * d, 60)), hm(*divmod(h1 * 60 + m1 + n * (d + pause), 60)), hm(h2 + 1, m2)],
                   "%d %s %d + %d %s %d = %d min = %s ; %s + %s = <b>%s</b>." % (n, FOIS, d, n - 1, FOIS, pause, t, dur(t), hm(h1, m1), dur(t), hm(h2, m2)))
    if k == "film2":
        a, b = R.choice([95, 105, 110, 125]), R.choice([85, 90, 100])
        return mcq("%s regarde deux films de %s et %s. Combien de temps en tout ?" % (p[0], dur(a), dur(b)), dur(a + b), [dur(a + b - 40), "%d h %d min" % (a // 60 + b // 60, a % 60 + b % 60) if a % 60 + b % 60 >= 60 else dur(a + b + 60), dur(a + b + 10)],
                   "%s + %s = %d min = <b>%s</b>." % (dur(a), dur(b), a + b, dur(a + b)))
    if k == "train":
        h1, m1 = R.randint(6, 16), R.randint(1, 11) * 5
        d = R.randint(95, 290)
        h2, m2 = divmod(h1 * 60 + m1 + d, 60)
        if m2 % 5:
            return None
        return mcq("Un train part à %s et arrive %s plus tard. À quelle heure arrive-t-il ?" % (hm(h1, m1), dur(d)), hm(h2, m2), [hm(h1 + d // 60, m1 + d % 60) if m1 + d % 60 < 100 and m1 + d % 60 >= 60 else hm(h2 + 1, m2), hm(h2, (m2 + 10) % 60), hm(h2 - 1, m2)],
                   "%s + %s = <b>%s</b>." % (hm(h1, m1), dur(d), hm(h2, m2)))
    a, b = R.choice([(8, 30), (8, 45), (9, 0)]), R.choice([(16, 30), (16, 15), (16, 45)])
    lunch = R.choice([90, 105, 120])
    t = (b[0] * 60 + b[1]) - (a[0] * 60 + a[1]) - lunch
    return mcq("L’école commence à %s et finit à %s, avec une pause de midi de %s. Combien de temps les élèves sont-ils en classe ?" % (hm(*a), hm(*b), dur(lunch)), dur(t),
               [dur(t + lunch), dur(t - 10), dur(t + 40)], "De %s à %s : %s ; %s − %s = <b>%s</b>." % (hm(*a), hm(*b), dur(t + lunch), dur(t + lunch), dur(lunch), dur(t)))


def build(lv):
    setup(lv)
    seen = set()
    sets = [
        ("Lire l’heure", mix(R, seen, [(s1, 20)])),
        ("Heures, minutes" + ("" if lv == 1 else " et secondes"), mix(R, seen, [(s2, 20)])),
        ("Calculer une durée", mix(R, seen, [(s3, 20)])),
        ("Heure de début ou de fin" if lv == 1 else "Secondes et chronomètre", mix(R, seen, [(s4, 20)])),
        ("Problèmes en plusieurs étapes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["<b>1 h = 60 min</b>" + (" ; <b>1 min = 60 s</b>" if lv == 2 else "") + " ; 1 jour = 24 h. Après midi, on compte jusqu’à 24 h : 3 h de l’après-midi = 15 h.",
         "Pour calculer une durée, on avance jusqu’à l’<b>heure pile</b>, puis on ajoute les heures et les minutes.",
         "Quand on additionne des durées, 60 min font 1 h : 1 h 45 min + 30 min = 2 h 15 min."],
        [example("De 9 h 40 à 11 h 15", ["9 h 40 → 10 h : 20 min", "10 h → 11 h 15 : 1 h 15 min"], "1 h 35 min")],
        [["Compter 100 minutes dans une heure", "1 h = 60 min : 9 h 50 + 20 min = 10 h 10."],
         ["1 h 30 min = 1,30 h", "1 h 30 min = 1 h et demie = 90 min."],
         ["Oublier l’étape de l’heure pile", "Fais des bonds sur une ligne du temps."]])
    faq = [("Comment calculer une durée facilement ?", "Avec une ligne du temps : on avance jusqu’à l’heure pile, puis d’heure en heure, puis les minutes."),
           ("Pourquoi 60 et pas 100 ?", "Les heures se comptent en base soixante : 60 secondes font une minute, 60 minutes une heure.")]
    unit(lv, R, "heures-et-durees", "G",
         "Lire l’heure sur une horloge à aiguilles ; comparer et mesurer des durées en heures et minutes%s ; résoudre des problèmes à une ou plusieurs étapes" % ("" if lv == 1 else " et secondes"),
         "Heures et durées", "Heures et durées",
         "Fiches de maths %s sur l’heure et les durées : lire l’heure, h, min%s, calculer une durée, horaires de début et de fin et problèmes. 100 exercices corrigés." % (GN(lv), "" if lv == 1 else ", s"),
         "1 h = 60 min.", "Pour une durée, j’avance jusqu’à l’heure pile.",
         body, faq, sets, 20)


if __name__ == "__main__":
    build(1)
