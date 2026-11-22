# -*- coding: utf-8 -*-
"""
France Maths CE2 : Heures et durées (Grandeurs et mesures)
  python3 tools/gen_fr_maths_ce2_heures_et_durees.py
Lire l’heure sur une horloge à aiguilles, heures du matin et de l’après-midi, « et quart, et demie, moins le quart »,
relations entre unités (h, min, s, jour, semaine), calculer une durée, une heure de fin ou de début.
Erreurs : inverser les aiguilles, lire 8 h 45 pour « 8 h moins le quart », compter 100 min dans une heure.
"""
import random
from fr_common import mcq, lesson, example, make_unit, mix, Kids, horloge, hm, dur

R = random.Random(51014)
K = Kids(R)


def s1():
    h = R.randint(1, 12)
    m = R.choice([0, 15, 30, 45, 5, 10, 20, 25, 35, 40, 50, 55])
    if R.random() < 0.4:
        m = R.choice([0, 15, 30, 45])
    swap_h, swap_m = (m // 5 if m else 12), (h % 12) * 5
    wr = [hm(swap_h, swap_m) if (swap_h, swap_m) != (h, m) else None, hm(h % 12 + 1, m), hm(h - 1 if h > 1 else 12, m), hm(h, (m + 30) % 60) if m != 30 else hm(h, 0)]
    return mcq("<div class='qfig'>%s</div>Quelle heure est-il le matin ?" % horloge(h, m), hm(h, m), [w for w in wr if w and w != hm(h, m)],
               "La petite aiguille indique les heures, la grande les minutes (chaque chiffre vaut 5 min). Il est <b>%s</b>." % hm(h, m))


WORDS = ["une", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze"]


def heures_w(h):
    return "midi" if h == 12 else WORDS[h - 1] + (" heure" if h == 1 else " heures")


def s2_mots():
    h = R.randint(2, 11)
    k = R.choice(["quart", "demie", "moins", "moins"])
    if k == "quart":
        return mcq("Il est %s et quart du matin. Comment l’écrit-on ?" % heures_w(h), hm(h, 15), [hm(h, 25), hm(h, 45), hm(h - 1, 45)],
                   "Et quart = 15 minutes après l’heure : <b>%s</b>." % hm(h, 15))
    if k == "demie":
        return mcq("Il est %s et demie du matin. Comment l’écrit-on ?" % heures_w(h), hm(h, 30), [hm(h, 50), hm(h - 1, 30), hm(h, 15)],
                   "Et demie = 30 minutes après l’heure : <b>%s</b>." % hm(h, 30))
    return mcq("Il est %s moins le quart du matin. Comment l’écrit-on ?" % heures_w(h), hm(h - 1, 45), [hm(h, 45), hm(h, 15), hm(h - 1, 15)],
               "Moins le quart = 15 minutes avant %s : <b>%s</b>." % (hm(h, 0), hm(h - 1, 45)))


APM = ["Le cours de judo commence", "La sortie au parc a lieu", "Le goûter est servi", "La bibliothèque ouvre"]
SOIR = ["Le dîner est servi", "Le spectacle commence", "Le match de handball commence", "Le train arrive"]


def s2_apm():
    h = R.randint(1, 10)
    m = R.choice([0, 0, 15, 30, 45, 20, 40])
    ev, lab = (R.choice(APM), "de l’après-midi") if h <= 5 else (R.choice(SOIR), "du soir")
    return mcq("%s à %s %s. Comment l’écrit-on avec les heures de 0 à 24 ?" % (ev, hm(h, m), lab), hm(h + 12, m), [hm(h + 10, m), hm(h, m), hm(h + 2, m)],
               "L’après-midi et le soir, on ajoute 12 : %d + 12 = %d. Il est <b>%s</b>." % (h, h + 12, hm(h + 12, m)))


def s3():
    k = R.choice(["h_min", "hm_min", "min_hm", "demi", "quart", "jour", "sem", "min_s"])
    if k == "h_min":
        a = R.randint(2, 5)
        return mcq("Combien de minutes y a-t-il dans %d heures ?" % a, "%d min" % (a * 60), ["%d min" % (a * 100), "%d min" % (a * 10), "%d min" % (a * 60 + 60)],
                   "1 h = 60 min, donc %d h = %d %s 60 = <b>%d min</b>." % (a, a, "×", a * 60))
    if k == "hm_min":
        a, b = R.randint(1, 3), R.choice([5, 10, 15, 20, 25, 30, 40, 45, 50])
        return mcq("Complète : %s = … min" % dur(a * 60 + b), "%d min" % (a * 60 + b), ["%d min" % (a * 100 + b), "%d min" % (a + b), "%d min" % (a * 10 + b)],
                   "%d h = %d min ; %d + %d = <b>%d min</b>." % (a, a * 60, a * 60, b, a * 60 + b))
    if k == "min_hm":
        n = R.choice([70, 75, 80, 90, 100, 110, 125, 135, 150, 165])
        return mcq("Complète : %d min = … h … min" % n, dur(n), ["%d h %d min" % (n // 100, n % 100) if n >= 100 and 0 < n % 100 < 60 else dur(n + 10), "%d h %d min" % (n // 60 + 1, n % 60) if n % 60 else "%d h" % (n // 60 + 1), "%d h" % (n // 60) if n % 60 else dur(n - 5)],
                   "60 min = 1 h. %d min = %d min + %d min = <b>%s</b>." % (n, (n // 60) * 60, n % 60, dur(n)))
    if k == "demi":
        a = R.randint(1, 4)
        return mcq("Combien de minutes dure %s et demie ?" % ("une heure" if a == 1 else "%d heures" % a), "%d min" % (a * 60 + 30), ["%d min" % (a * 60 + 50), "%d min" % (a * 100 + 50), "%d min" % (a * 60 + 15)],
                   "Une demi-heure = 30 min. %d %s 60 + 30 = <b>%d min</b>." % (a, "×", a * 60 + 30))
    if k == "quart":
        n = R.choice([1, 3])
        return mcq("Combien de minutes dure %s d’heure ?" % ("un quart" if n == 1 else "trois quarts"), "%d min" % (15 * n), ["%d min" % (25 * n), "%d min" % (4 * n), "%d min" % (15 * n + 15)],
                   "Une heure = 60 min ; un quart d’heure = 60 ÷ 4 = 15 min%s. Réponse : <b>%d min</b>." % ("" if n == 1 else " ; 3 %s 15 = 45" % "×", 15 * n))
    if k == "jour":
        a = R.randint(2, 4)
        return mcq("Combien d’heures y a-t-il dans %d jours ?" % a, "%d h" % (a * 24), ["%d h" % (a * 12), "%d h" % (a * 60), "%d h" % (a * 24 + 24)],
                   "1 jour = 24 h, donc %d %s 24 = <b>%d h</b>." % (a, "×", a * 24))
    if k == "sem":
        a = R.randint(2, 6)
        return mcq("Combien de jours y a-t-il dans %d semaines ?" % a, "%d jours" % (a * 7), ["%d jours" % (a * 5), "%d jours" % (a * 10), "%d jours" % (a + 7)],
                   "1 semaine = 7 jours : %d %s 7 = <b>%d jours</b>." % (a, "×", a * 7))
    a = R.randint(2, 5)
    return mcq("Combien de secondes y a-t-il dans %d minutes ?" % a, "%d s" % (a * 60), ["%d s" % (a * 100), "%d s" % (a * 10), "%d s" % (a * 60 + 60)],
               "1 min = 60 s, donc %d %s 60 = <b>%d s</b>." % (a, "×", a * 60))


def ecart(h1, m1, h2, m2):
    return (h2 * 60 + m2) - (h1 * 60 + m1)


def s4():
    h1 = R.randint(7, 16)
    m1 = R.choice([0, 10, 15, 20, 30, 40, 45])
    d = R.choice([20, 25, 35, 40, 45, 50, 75, 80, 90, 105, 110, 135, 150])
    t = h1 * 60 + m1 + d
    h2, m2 = divmod(t, 60)
    wr = [dur(d + 40) if (m2 < m1) else dur(d + 10), dur(abs((h2 - h1) * 100 + m2 - m1)) if (h2 - h1) * 100 + m2 - m1 > 0 else None, dur(d - 5), dur(d + 60)]
    return mcq("Un film commence à %s et se termine à %s. Combien de temps dure-t-il ?" % (hm(h1, m1), hm(h2, m2)) if d >= 75 else
               "La séance de piscine commence à %s et finit à %s. Combien de temps dure-t-elle ?" % (hm(h1, m1), hm(h2, m2)), dur(d), [w for w in wr if w and w != dur(d)],
               "De %s à %s, il s’écoule <b>%s</b>. On peut compter d’abord jusqu’à l’heure pile, puis le reste." % (hm(h1, m1), hm(h2, m2), dur(d)))


def s5():
    p = K.next()
    k = R.choice(["fin", "debut", "cuisson", "trajet", "cal"])
    if k in ("fin", "cuisson"):
        h1, m1 = R.randint(8, 17), R.choice([0, 5, 15, 20, 30, 35, 45, 50])
        d = R.choice([25, 35, 40, 45, 50, 55, 70, 85, 95])
        h2, m2 = divmod(h1 * 60 + m1 + d, 60)
        q = ("%s commence ses devoirs à %s. %s travaille pendant %s. À quelle heure finit-%s ?" % (p[0], hm(h1, m1), p[1].capitalize(), dur(d), p[1]) if k == "fin" else
             "Un gâteau entre dans le four à %s. Il cuit pendant %s. À quelle heure faut-il le sortir ?" % (hm(h1, m1), dur(d)))
        bad = hm(h2 - 1, m2) if h2 > h1 else hm(h2, (m2 + 20) % 60)
        return mcq(q, hm(h2, m2), [bad, hm(h2 + 1, m2), hm(h2, (m2 + 10) % 60)],
                   "%s + %s = <b>%s</b>." % (hm(h1, m1), dur(d), hm(h2, m2)))
    if k == "debut":
        h2, m2 = R.randint(10, 18), R.choice([0, 10, 15, 30, 45])
        d = R.choice([30, 45, 50, 75, 90, 105, 120])
        h1, m1 = divmod(h2 * 60 + m2 - d, 60)
        return mcq("Le match se termine à %s. Il a duré %s. À quelle heure a-t-il commencé ?" % (hm(h2, m2), dur(d)), hm(h1, m1), [hm(*divmod(h2 * 60 + m2 + d, 60)), hm(h1 + 1, m1), hm(h1, (m1 + 30) % 60)],
                   "On recule de %s : %s − %s = <b>%s</b>." % (dur(d), hm(h2, m2), dur(d), hm(h1, m1)))
    if k == "trajet":
        a, b = R.choice([15, 20, 25, 30, 35]), R.choice([10, 15, 20, 25, 40, 45])
        return mcq("%s marche %d min jusqu’à la gare, puis prend le train pendant %d min. Combien de temps dure le trajet ?" % (p[0], a, b), dur(a + b), [dur(a + b + 40) if a + b >= 60 else dur(a + b + 10), "%d h %d min" % (1, a + b) if a + b < 60 else dur(a + b - 10), dur(abs(a - b)) if a != b else dur(a + b + 5)],
                   "%d + %d = %d min = <b>%s</b>." % (a, b, a + b, dur(a + b)))
    d = R.randint(1, 20)
    n = R.randint(3, 10)
    mois = R.choice(["mars", "mai", "juin", "octobre"])
    return mcq("Nous sommes le %d %s. Les vacances commencent dans %d jours. Quelle sera la date ?" % (d, mois, n), "le %d %s" % (d + n, mois), ["le %d %s" % (d + n - 1, mois), "le %d %s" % (d + n + 1, mois), "le %d %s" % (n, mois) if n != d + n else "le %d %s" % (d, mois)],
                   "%d + %d = %d : <b>le %d %s</b>." % (d, n, d + n, d + n, mois))


def main():
    seen = set()
    sets = [
        ("Lire l’heure", mix(R, seen, [(s1, 20)])),
        ("Et quart, et demie, moins le quart, l’après-midi", mix(R, seen, [(s2_mots, 10), (s2_apm, 10)])),
        ("Heures, minutes, secondes, jours", mix(R, seen, [(s3, 20)])),
        ("Calculer une durée", mix(R, seen, [(s4, 20)])),
        ("Problèmes", mix(R, seen, [(s5, 20)])),
    ]
    body = lesson(
        ["Sur une horloge, la <b>petite aiguille</b> montre les heures et la <b>grande aiguille</b> les minutes. Entre deux chiffres, il y a 5 minutes.",
         "Après midi, on compte les heures jusqu’à 24 : 3 h de l’après-midi = 15 h.",
         "<b>1 h = 60 min</b>, 1 min = 60 s, une demi-heure = 30 min, un quart d’heure = 15 min, 1 jour = 24 h.",
         "Pour calculer une durée, on avance jusqu’à l’heure pile, puis on ajoute le reste."],
        [example("De 9 h 40 à 11 h 15", ["9 h 40 → 10 h : 20 min", "10 h → 11 h : 1 h", "11 h → 11 h 15 : 15 min"], "1 h 35 min"),
         example("Huit heures moins le quart", ["15 min avant 8 h"], "7 h 45")],
        [["Inverser les aiguilles", "La petite aiguille donne l’heure, la grande les minutes."],
         ["Lire 8 h 45 pour « 8 heures moins le quart »", "Moins le quart : c’est avant 8 h, donc 7 h 45."],
         ["Calculer comme avec 100 : de 9 h 40 à 11 h 15 = 1 h 75 min", "Une heure a 60 minutes : 1 h 35 min."]])
    faq = [("Pourquoi écrit-on 15 h au lieu de 3 h ?", "Pour ne pas confondre 3 h du matin et 3 h de l’après-midi, on compte les heures de 0 h à 24 h."),
           ("Comment calculer une durée facilement ?", "On fait des bonds sur une ligne du temps : jusqu’à l’heure pile, puis des heures, puis les minutes qui restent.")]
    make_unit(R, "heures-et-durees", "G",
              "Lire l’heure sur une horloge à aiguilles ; utiliser les unités h, min, s, jour, semaine et leurs relations ; calculer une durée, un horaire de début ou de fin (résumé du programme 2024 du cycle 2).",
              "Heures et durées", "Heures et durées CE2 : fiches et exercices avec corrigé", "Heures et durées",
              "Fiches de maths CE2 sur l’heure et les durées : lire l’heure, et quart, moins le quart, l’après-midi, h, min, s, calculer une durée et problèmes. 100 exercices corrigés.",
              "1 h = 60 min.", "Pour une durée, on avance jusqu’à l’heure pile, puis on ajoute le reste.",
              body, faq, sets, 14)


if __name__ == "__main__":
    main()
