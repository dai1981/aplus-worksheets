# -*- coding: utf-8 -*-
"""
France Maths 6e : Nombres entiers et décimaux（programme 2025 du cycle 3）
  python3 tools/gen_fr_maths_6e_nombres_entiers_et_decimaux.py
Grands nombres, valeur des chiffres, fractions décimales, écriture décimale, droite graduée.
Erreurs : confondre chiffre et nombre de dizaines, 3,7 = 3/7, 0,25 = 25 dixièmes, oublier les zéros (7 dixièmes = 0,07).
"""
import random
from fr_c4 import *

R = random.Random(60101)
K = Kids(R)
RANG = ["unités", "dizaines", "centaines", "unités de mille", "dizaines de mille", "centaines de mille", "millions", "dizaines de millions", "centaines de millions"]
RD = ["dixièmes", "centièmes", "millièmes"]


def s1():
    n = R.randint(10 ** 5, 10 ** 9 - 1)
    s = str(n)
    i = R.randrange(min(len(s), 9))
    dig = int(s[len(s) - 1 - i])
    if R.random() < 0.6:
        return M("Dans %s, quel est le chiffre des %s ?" % (num(n), RANG[i]), str(dig),
                 [s[len(s) - 2 - i] if len(s) - 2 - i >= 0 else "0", s[len(s) - i] if i else s[-2], str((dig + 1) % 10)],
                 "On compte les rangs depuis la droite : le chiffre des %s est <b>%d</b>." % (RANG[i], dig))
    if i < 1:
        return None
    v = n // 10 ** i
    return M("Combien y a-t-il %s en tout dans %s ?" % (de_n(RANG[i]), num(n)), num(v), [str(dig), num(v * 10), num(v + 1)],
             "%s = %s %s et %s : le nombre %s est <b>%s</b>." % (num(n), num(v), RANG[i], num(n % 10 ** i), de_n(RANG[i]), num(v)))


def s2():
    k = R.randint(1, 3)
    n = R.randint(1, 10 ** (k + 1) - 1)
    if n % 10 == 0:
        return None
    v = Fr(n, 10 ** k)
    den = 10 ** k
    if R.random() < 0.5:
        return M("Quelle est l’écriture décimale de %s ?" % fr(num(n), num(den)), d(v), [d(Fr(n, 10 ** (k + 1))), d(Fr(n, 10 ** (k - 1))) if k > 1 else d(n), "%s,%s" % (n, den) if False else d(v + Fr(1, den))],
                 "%s = %s %s, donc <b>%s</b>." % (fr(num(n), num(den)), num(n), RD[k - 1], d(v)))
    return M("%s = …" % d(v), "%s" % fr(num(n), num(den)), [fr(num(n), num(den * 10)), fr(num(n), num(den // 10)) if den > 10 else fr(num(n), "100"), fr(num(den), num(n))],
             "Le dernier chiffre est au rang des %s : %s = <b>%s</b>." % (RD[k - 1], d(v), fr(num(n), num(den))))


def s3():
    ip = R.randint(0, 999)
    ds = [R.randint(0, 9) for _ in range(3)]
    if ds[2] == 0:
        ds[2] = R.randint(1, 9)
    v = Fr(ip * 1000 + ds[0] * 100 + ds[1] * 10 + ds[2], 1000)
    i = R.randrange(3)
    if R.random() < 0.5:
        return M("Dans %s, quel est le chiffre des %s ?" % (d(v), RD[i]), str(ds[i]), [str(ds[(i + 1) % 3]), str(ip % 10), str((ds[i] + 1) % 10)],
                 "Après la virgule : dixièmes, centièmes, millièmes. Le chiffre des %s est <b>%d</b>." % (RD[i], ds[i]))
    a, b, c = R.randint(1, 9), R.randint(0, 9), R.randint(1, 9)
    v = Fr(a * 100 + b * 10 + c, 100)
    return M("Quel nombre s’écrit %s, %s et %s ?" % (pl(a, "unité"), pl(b, "dixième"), pl(c, "centième")), d(v), [d(Fr(a * 100 + c * 10 + b, 100)) if b != c else d(v + 1), "%d,%d%d0" % (a, c, b) if False else d(Fr(a * 1000 + b * 10 + c, 1000)), d(v + Fr(1, 10))],
             "%d + %s + %s = <b>%s</b>." % (a, fr(b, 10), fr(c, 100), d(v)))


def s4():
    step = R.choice([Fr(1, 10), Fr(1, 100), Fr(1, 10)])
    lo = Fr(R.randint(0, 30), 10) if step == Fr(1, 10) else Fr(R.randint(100, 300), 100)
    if step == Fr(1, 10):
        lo = Fr(int(lo))
    else:
        lo = Fr(int(lo * 10), 10)
    k = R.randint(1, 9)
    if k == 5:
        k = 7
    v = lo + k * step
    sc = 10 if step == Fr(1, 10) else 100
    from fr_c3 import droite_dec
    svg = droite_dec(int(lo * sc), int((lo + 10 * step) * sc), 1, [(int(v * sc), "A")], k=1 if sc == 10 else 2, every=5)
    return M("<div class='qfig'>%s</div>Quel nombre est repéré par la lettre A ?" % svg, d(v), [d(v + step), d(lo + k * step * 10) if lo + k * step * 10 < 100 else d(v - step), d(lo + Fr(k, 100) if sc == 10 else lo + Fr(k, 1000))],
             "Entre %s et %s, il y a 10 graduations : chacune vaut %s. A = <b>%s</b>." % (d(lo), d(lo + 10 * step), d(step), d(v)))


def s5():
    p = K.next()
    k = R.choice(["pop", "dist", "prix", "lettres"])
    if k == "pop":
        n = R.randint(1, 60) * 10 ** 6 + R.randint(0, 999) * 1000
        return M("Une ville compte %s habitants. Combien de milliers d’habitants cela fait-il (en tout) ?" % num(n), num(n // 1000), [num(n // 10 ** 6), num(n // 100), num(n // 1000 % 1000)],
                 "1 millier = 1 000. %s = %s milliers : <b>%s</b>." % (num(n), num(n // 1000), num(n // 1000)))
    if k == "dist":
        a = R.randint(20, 140)
        b = R.randint(10, 99)
        v = Fr(a * 100 + b, 100)
        return M("%s mesure la longueur d’un terrain de sport : %d m et %d cm. Quelle est cette longueur en mètres ?" % (p[0], a, b), "%s m" % d(v), ["%s m" % d(Fr(a * 10 + b, 10)) if b < 10 else "%d,%d m" % (a, b // 10), "%s m" % d(Fr(a * 1000 + b, 1000)), "%s m" % num(a + b)],
                 "1 cm = 0,01 m : %d cm = %s m. Donc <b>%s m</b>." % (b, d(Fr(b, 100)), d(v)))
    if k == "prix":
        e, c = R.randint(2, 99), R.randint(1, 9)
        v = Fr(e * 100 + c, 100)
        return M("Un article coûte %d euros et %s. Comment l’écrire en euros ?" % (e, pl(c, "centime")), "%s €" % d(v), ["%d,%d €" % (e, c), "%s €" % d(Fr(e * 1000 + c, 1000)), "%d,%d0 €" % (e, c)],
                 "%s = 0,0%d € : <b>%s €</b>." % (pl(c, "centime"), c, d(v)))
    n = R.randint(1, 999) * 1000 + R.randint(1, 999)
    from fr_c3 import lettres_big
    return M("Comment s’écrit « %s » en chiffres ?" % lettres_big(n), num(n), [num(n // 1000 * 100 + n % 1000) if n % 1000 < 100 else num(n + 1000), num(n // 1000 * 10000 + n % 1000), num(n + 1)],
             "« %s » : <b>%s</b>." % (lettres_big(n), num(n)))


def main():
    seen = set()
    sets = [("Les grands nombres", mix(R, seen, [(s1, 20)])), ("Fractions décimales", mix(R, seen, [(s2, 20)])),
            ("Valeur des chiffres d’un décimal", mix(R, seen, [(s3, 20)])), ("Droite graduée", mix(R, seen, [(s4, 20)])), ("Problèmes", mix(R, seen, [(s5, 20)]))]
    body = L(["Chaque chiffre a une valeur selon son <b>rang</b> : unités, dizaines, centaines, unités de mille… Après la virgule : dixièmes, centièmes, millièmes.",
              "Une <b>fraction décimale</b> a pour dénominateur 10, 100, 1 000… : 37/100 = 0,37.",
              "Le <b>chiffre</b> des dizaines de 4 583 est 8 ; le <b>nombre</b> de dizaines est 458."],
             [("Écris 7/100 en écriture décimale", ["7 centièmes", "le 7 est au rang des centièmes"], "0,07")],
             [["Écrire 7/100 = 0,7", "0,7 = 7 dixièmes ; 7 centièmes = 0,07."],
              ["Croire que 3,7 = 3/7", "3,7 = 3 + 7/10 = 37/10."],
              ["Confondre chiffre et nombre de dizaines", "Le nombre de dizaines compte toutes les dizaines du nombre."]])
    faq = [("Que veut dire la virgule ?", "Elle sépare la partie entière de la partie décimale : à droite, ce sont des dixièmes, des centièmes…"),
           ("Comment lire 0,25 ?", "« zéro virgule vingt-cinq » ou « 25 centièmes ».")]
    unit("6e", R, "nombres-entiers-et-decimaux", "N",
         "Connaître les nombres entiers jusqu’au milliard ; comprendre et utiliser les fractions décimales et l’écriture à virgule ; connaître la valeur des chiffres selon leur rang ; repérer des nombres sur une droite graduée",
         "Nombres entiers et décimaux", "Nombres entiers et décimaux",
         "Fiches de maths 6e sur les nombres entiers et décimaux : grands nombres, fractions décimales, valeur des chiffres, droite graduée et problèmes. 100 exercices corrigés.",
         "Après la virgule : dixièmes, centièmes, millièmes.", "37/100 = 0,37", body, faq, sets, 1)


if __name__ == "__main__":
    main()
