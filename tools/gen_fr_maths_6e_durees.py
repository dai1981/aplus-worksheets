# -*- coding: utf-8 -*-
"""
France Maths 6e : Les durées
  python3 tools/gen_fr_maths_6e_durees.py
Conversions (s, min, h, jour, semaine, mois, année, siècle), calculer une durée, une heure de fin ou de début, durées décimales (1,5 h),
problèmes. Erreurs : 1 h = 100 min, 1,5 h = 1 h 50 min, oublier de passer par l’heure pile.
"""
import random
from fr_c4 import *
import gen_fr_maths_ce2_heures_et_durees as HD

R = random.Random(60120)
K = Kids(R)
HD.R = R
HD.K = K


def s1():
    k = R.choice(["h_min", "min_h", "min_s", "jours", "sem", "an", "siecle", "jour_h"])
    a = R.randint(2, 9)
    if k == "h_min":
        b = R.choice([5, 10, 15, 20, 25, 35, 40, 45, 50])
        return M("%s = … min" % dur(a * 60 + b), "%d min" % (a * 60 + b), ["%d min" % (a * 100 + b), "%d min" % (a + b), "%d min" % (a * 60 - b)],
                 "%d h = %d min ; %d + %d = <b>%d min</b>." % (a, a * 60, a * 60, b, a * 60 + b))
    if k == "min_h":
        n = R.choice([75, 90, 100, 110, 125, 135, 150, 170, 195, 210, 250])
        return M("%d min = …" % n, dur(n), ["%d h %d min" % (n // 100, n % 100) if 0 < n % 100 < 60 else dur(n + 10), dur(n + 60), dur(n - 10)],
                 "60 min = 1 h : %d min = %d × 60 + %d = <b>%s</b>." % (n, n // 60, n % 60, dur(n)))
    if k == "min_s":
        return M("%d min = … s" % a, "%d s" % (a * 60), ["%d s" % (a * 100), "%d s" % (a * 10), "%d s" % (a * 60 + 60)], "1 min = 60 s : %d × 60 = <b>%d s</b>." % (a, a * 60))
    if k == "jours":
        return M("Combien d’heures y a-t-il dans %d jours ?" % a, "%d h" % (a * 24), ["%d h" % (a * 12), "%d h" % (a * 60), "%d h" % (a * 24 + 24)], "1 jour = 24 h : %d × 24 = <b>%d h</b>." % (a, a * 24))
    if k == "sem":
        n = R.randint(15, 60)
        return M("%d jours, c’est combien de semaines et de jours ?" % n, "%d semaines et %s" % (n // 7, pl(n % 7, "jour")) if n % 7 else "%d semaines" % (n // 7),
                 ["%s et %s" % (pl(n // 10, "semaine"), pl(n % 10, "jour")), "%d semaines et %s" % (n // 7 + 1, pl(n % 7, "jour")), "%s et %s" % (pl(n // 5, "semaine"), pl(n % 5, "jour"))],
                 "1 semaine = 7 jours ; %d = 7 × %d + %d." % (n, n // 7, n % 7))
    if k == "an":
        y = R.choice([2023, 2024, 2025, 2026, 2027, 2028, 2030, 2032])
        bis = y % 4 == 0
        return M("Combien de jours compte l’année %d ?" % y, "366 jours" if bis else "365 jours", ["365 jours" if bis else "366 jours", "360 jours", "52 jours"],
                 "%d %s divisible par 4 : c’est une année %s, <b>%s</b>." % (y, "est" if bis else "n’est pas", "bissextile" if bis else "ordinaire", "366 jours" if bis else "365 jours"))
    if k == "siecle":
        y = R.randint(1001, 2099)
        c = (y - 1) // 100 + 1
        rom = {11: "XI", 12: "XII", 13: "XIII", 14: "XIV", 15: "XV", 16: "XVI", 17: "XVII", 18: "XVIII", 19: "XIX", 20: "XX", 21: "XXI"}
        if c not in rom:
            return None
        return M("En quel siècle est l’année %d ?" % y, "au %s<sup>e</sup> siècle" % rom[c], ["au %s<sup>e</sup> siècle" % rom.get(c - 1, "X"), "au %s<sup>e</sup> siècle" % rom.get(c + 1, "XXII"), "au %d<sup>e</sup> siècle" % (y // 100 * 10 if False else y // 10)],
                 "Le %s<sup>e</sup> siècle va de %d à %d : <b>au %s<sup>e</sup> siècle</b>." % (rom[c], (c - 1) * 100 + 1, c * 100, rom[c]))
    return M("Combien de minutes y a-t-il dans une journée ?", "1 440 min", ["2 400 min", "1 200 min", "24 min"], "24 × 60 = <b>1 440 min</b>.")


def s3():
    k = R.choice(["dec", "dec2", "frac"])
    if k == "dec":
        h = R.randint(1, 5)
        f = R.choice([Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 10), Fr(2, 10)])
        mins = int((h + f) * 60)
        return M("%s h = …" % d(h + f), dur(mins), ["%d h %d min" % (h, int(f * 100)), dur(mins + 10), "%d h %d min" % (h, int(f * 10))],
                 "%s h = %s × 60 min = %d min : <b>%s</b>." % (d(f), d(f), int(f * 60), dur(mins)))
    if k == "dec2":
        m = R.choice([15, 30, 45, 6, 12, 36, 48])
        h = R.randint(0, 3)
        v = h + Fr(m, 60)
        return M("%s = … h (écriture décimale)" % dur(h * 60 + m), "%s h" % d(v), ["%d,%d h" % (h, m), "%s h" % d(v + Fr(1, 10)), "%s h" % d(h + Fr(m, 100))],
                 "%d min = %s h (on divise par 60), donc <b>%s h</b>." % (m, d(Fr(m, 60)), d(v)))
    f, w = R.choice([(Fr(1, 4), "un quart d’heure"), (Fr(3, 4), "trois quarts d’heure"), (Fr(1, 3), "un tiers d’heure"), (Fr(1, 2), "une demi-heure"), (Fr(1, 6), "un sixième d’heure")])
    return M("Combien de minutes dure %s ?" % w, "%d min" % (f * 60), ["%d min" % (f * 100), "%d min" % (f * 60 + 5), "%d min" % (f * 10)],
             "%s × 60 = <b>%d min</b>." % (fq(f), f * 60))


def s5():
    p = K.next()
    k = R.choice(["train", "film", "age", "chrono", "ce2"])
    if k == "ce2":
        return HD.s5()
    if k == "train":
        h1, m1 = R.randint(6, 18), R.choice([5, 12, 25, 38, 47, 52])
        dd = R.randint(70, 260)
        h2, m2 = divmod(h1 * 60 + m1 + dd, 60)
        return M("Un train part à %s et arrive à %s. Combien de temps dure le trajet ?" % (hm(h1, m1), hm(h2, m2)), dur(dd), [dur(dd + 40) if m2 < m1 else dur(dd + 10), dur(abs((h2 - h1) * 100 + m2 - m1)), dur(dd - 60)],
                 "De %s à %s, puis à %s : <b>%s</b>." % (hm(h1, m1), hm(h1 + 1, 0), hm(h2, m2), dur(dd)))
    if k == "film":
        dd = R.randint(85, 170)
        h2, m2 = R.randint(20, 23), R.choice([0, 15, 30, 45, 10, 50])
        h1, m1 = divmod(h2 * 60 + m2 - dd, 60)
        return M("Un film de %s finit à %s. À quelle heure a-t-il commencé ?" % (dur(dd), hm(h2, m2)), hm(h1, m1), [hm(*divmod(h1 * 60 + m1 + 40, 60)), hm(h1 + 1, m1), hm(*divmod(h2 * 60 + m2 - dd + 20, 60))],
                 "%s − %s = <b>%s</b>." % (hm(h2, m2), dur(dd), hm(h1, m1)))
    if k == "age":
        y1 = R.randint(1950, 2014)
        y2 = R.randint(2024, 2026)
        return M("%s est né%s en %d. Quel âge aura-t-%s à son anniversaire en %d ?" % (p[0], "e" if p[1] == "elle" else "", y1, p[1], y2), "%d ans" % (y2 - y1), ["%d ans" % (y2 - y1 + 1), "%d ans" % (y2 - y1 - 1), "%d ans" % (y2 - y1 + 10)],
                 "%d − %d = <b>%d ans</b>." % (y2, y1, y2 - y1))
    a, b = R.randint(40, 99), R.randint(40, 99)
    t = a + b
    return M("%s court deux tours de piste en %d s et %d s. Quel est son temps total ?" % (p[0], a, b), "%d min %d s" % (t // 60, t % 60) if t % 60 else "%d min" % (t // 60),
             ["%d min %d s" % (t // 100, t % 100) if 0 < t % 100 < 60 else "%d min %d s" % (t // 60 + 1, t % 60), "%d s" % (t + 60), "%d min" % (t // 60 + 1)],
             "%d + %d = %d s = %d min %d s." % (a, b, t, t // 60, t % 60))


def main():
    seen = set()
    sets = [("Convertir des durées", mix(R, seen, [(s1, 20)])), ("Calculer une durée", mix(R, seen, [(HD.s4, 20)])),
            ("Durées décimales et fractions d’heure", mix(R, seen, [(s3, 20)])), ("Heure de début ou de fin", mix(R, seen, [(s5, 20)])),
            ("Problèmes", mix(R, seen, [(HD.s5, 10), (s5, 10)]))]
    body = L(["1 h = 60 min ; 1 min = 60 s ; 1 jour = 24 h ; 1 semaine = 7 jours ; 1 an = 365 jours (366 les années bissextiles) ; 1 siècle = 100 ans.",
              "Pour calculer une durée, on peut passer par l’heure pile : de 9 h 45 à 11 h 20, c’est 15 min + 1 h + 20 min.",
              "1,5 h = 1 h 30 min (0,5 h = la moitié de 60 min). 1 h 15 min = 1,25 h."],
             [("De 14 h 50 à 16 h 25", ["14 h 50 → 15 h : 10 min", "15 h → 16 h 25 : 1 h 25 min"], "1 h 35 min")],
             [["Croire que 1 h = 100 min", "Une heure, c’est 60 minutes."],
              ["Écrire 1,5 h = 1 h 50 min", "0,5 h = 30 min : 1,5 h = 1 h 30 min."],
              ["Soustraire les heures et les minutes séparément sans retenue", "On passe par l’heure pile pour éviter les erreurs."]])
    faq = [("Comment convertir des minutes en heures ?", "On cherche combien de fois 60 : 150 min = 2 × 60 + 30 = 2 h 30 min."),
           ("Qu’est-ce qu’une année bissextile ?", "Une année de 366 jours (avec un 29 février), en général tous les 4 ans.")]
    unit("6e", R, "durees", "G",
         "Connaître les unités de durée et leurs relations ; calculer des durées, des horaires de début et de fin ; utiliser des durées écrites sous forme décimale ou fractionnaire",
         "Les durées", "Durées",
         "Fiches de maths 6e sur les durées : convertir, calculer une durée, durées décimales, heure de début ou de fin et problèmes. 100 exercices corrigés.",
         "1 h = 60 min ; 1,5 h = 1 h 30 min", "On passe par l’heure pile.", body, faq, sets, 20)


if __name__ == "__main__":
    main()
