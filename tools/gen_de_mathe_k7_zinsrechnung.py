# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Zinsrechnung（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k7_zinsrechnung.py
Kapital, Zinssatz, Zinsen (Z = K · p %), Jahreszinsen, Monatszinsen (· m/12), Tageszinsen (Bankjahr 360 Tage), Kapital oder Zinssatz berechnen, Zinseszins über wenige Jahre, Kredite.
Fehler: Monatszinsen wie Jahreszinsen gerechnet, durch 365 statt 360 Tage, Zinseszins mit einfachen Zinsen gerechnet.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table
from de_k6 import dz
from de_k7 import mcq, eur, pz, P

R = random.Random(49705)
KIDS = Kids(R)
G = ":"


def kap():
    return R.choice([200, 400, 500, 600, 800, 1000, 1200, 1500, 2000, 2400, 2500, 3000, 4000, 5000, 6000, 8000, 10000])


def satz():
    return Fr(R.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 60]), 10)


def jahr():
    k, p = kap(), satz()
    z = k * p / 100
    return mcq("Ein Kapital von %s wird zu %s verzinst. Wie viel Zinsen gibt es nach einem Jahr?" % (eur(k), pz(p)), eur(z), [eur(k + z), eur(k * p / 10), eur(z / 12)],
               "Z = K %s p%s = %s %s %s = <b>%s</b>." % (MAL, P, eur(k), MAL, dz(p / 100), eur(z)))


def monat():
    k, p = kap(), satz()
    m = R.choice([2, 3, 4, 6, 8, 9])
    z = k * p / 100 * Fr(m, 12)
    if (z * 100).denominator != 1:
        return None
    return mcq("%s werden zu %s für %d Monate angelegt. Wie viel Zinsen gibt es?" % (eur(k), pz(p), m), eur(z), [eur(k * p / 100), eur(k * p / 100 * m), eur(k * p / 100 / m) if m != 12 else None],
               "Jahreszinsen: %s. Für %d Monate: %s %s %s = <b>%s</b>." % (eur(k * p / 100), m, eur(k * p / 100), MAL, "%d/12" % m, eur(z)))


def tage():
    k = R.choice([3600, 7200, 1800, 3000, 6000, 9000, 12000])
    p = R.choice([2, 3, 4, 5, 6])
    t = R.choice([30, 45, 60, 90, 120, 180, 240])
    z = Fr(k * p, 100) * Fr(t, 360)
    if (z * 100).denominator != 1:
        return None
    return mcq("Ein Kredit von %s läuft %d Tage zu %d%s. Wie viel Zinsen fallen an? (Bankjahr: 360 Tage)" % (eur(k), t, p, P), eur(z), [eur(Fr(k * p, 100) * Fr(t, 365)), eur(Fr(k * p, 100)), eur(Fr(k * p, 100) * Fr(t, 30))],
                   "Z = K %s p%s %s t/360 = %s %s %s %s %d/360 = <b>%s</b>." % (MAL, P, MAL, eur(k), MAL, dz(Fr(p, 100)), MAL, t, eur(z)))


def rueck():
    kind = R.choice(["K", "p"])
    k, p = kap(), satz()
    z = k * p / 100
    if kind == "K":
        return mcq("Bei einem Zinssatz von %s bekommt man nach einem Jahr %s Zinsen. Wie groß war das Kapital?" % (pz(p), eur(z)), eur(k), [eur(z * p / 100), eur(z * 100), eur(z + z * p / 100)],
                   "K = Z %s p%s = %s %s %s = <b>%s</b>." % (G, P, eur(z), G, dz(p / 100), eur(k)))
    return mcq("Für %s gibt es nach einem Jahr %s Zinsen. Wie hoch ist der Zinssatz?" % (eur(k), eur(z)), pz(p), [pz(z), pz(p * 10), pz(p / 10)],
               "p%s = Z %s K = %s %s %s = %s = <b>%s</b>." % (P, G, eur(z), G, eur(k), dz(p / 100), pz(p)))


def zinseszins():
    k = R.choice([1000, 2000, 5000, 10000, 500])
    p = R.choice([2, 3, 4, 5, 10])
    n = R.choice([2, 3])
    v = k * Fr(100 + p, 100) ** n
    einfach = k + k * Fr(p, 100) * n
    return mcq("%s werden %d Jahre zu %d%s angelegt. Die Zinsen werden jedes Jahr mitverzinst. Wie hoch ist das Guthaben nach %d Jahren?" % (eur(k), n, p, P, n), eur(v), [eur(einfach), eur(k * Fr(100 + p, 100)), eur(v + k * Fr(p, 100))],
               "K %s %s%s = %s %s %s<sup>%d</sup> = <b>%s</b>. (Einfache Zinsen wären nur %s.)" % (MAL, dz(Fr(100 + p, 100)), "<sup>%d</sup>" % n, eur(k), MAL, dz(Fr(100 + p, 100)), n, eur(v), eur(einfach)))


def sache():
    p_, er = KIDS.next()
    kind = R.choice(["spar", "kredit", "vergleich", "dispo", "ziel"])
    if kind == "spar":
        k = R.choice([300, 500, 800, 1000, 1500])
        p = R.choice([Fr(15, 10), Fr(2), Fr(25, 10), Fr(3)])
        z = k * p / 100
        return mcq("%s legt %s auf ein Sparkonto mit %s Zinsen. Wie viel Geld ist nach einem Jahr auf dem Konto?" % (p_, eur(k), pz(p)), eur(k + z), [eur(z), eur(k + p), eur(k + z * 10)],
                   "Zinsen: %s. Guthaben: %s + %s = <b>%s</b>." % (eur(z), eur(k), eur(z), eur(k + z)))
    if kind == "kredit":
        k = R.choice([2000, 3000, 4000, 6000])
        p = R.choice([5, 6, 8, 9])
        z = Fr(k * p, 100)
        return mcq("Für ein Auto wird ein Kredit von %s für ein Jahr zu %d%s aufgenommen. Wie viel muss man insgesamt zurückzahlen?" % (eur(k), p, P), eur(k + z), [eur(z), eur(k), eur(k + p)],
                   "Zinsen: %s. Rückzahlung: <b>%s</b>." % (eur(z), eur(k + z)))
    if kind == "vergleich":
        k = R.choice([1000, 2000, 5000])
        p1, p2 = Fr(R.choice([15, 20, 25]), 10), Fr(R.choice([30, 35, 40]), 10)
        g = R.choice([0, 10, 20, 30])
        z1, z2 = k * p1 / 100, k * p2 / 100 - g
        if z1 == z2:
            return None
        best = "Bank A" if z1 > z2 else "Bank B"
        return mcq("Bank A zahlt %s Zinsen. Bank B zahlt %s Zinsen, verlangt aber %d € Kontogebühr im Jahr. Bei welcher Bank bekommt man für %s mehr?" % (pz(p1), pz(p2), g, eur(k)), best, ["Bank B" if best == "Bank A" else "Bank A", "Bei beiden gleich viel.", "immer bei der Bank mit dem höheren Zinssatz"],
                   "A: %s. B: %s − %d € = %s. <b>%s</b>." % (eur(z1), eur(k * p2 / 100), g, eur(z2), best))
    if kind == "dispo":
        k = R.choice([300, 600, 900, 1200])
        p = R.choice([9, 10, 12])
        m = R.choice([1, 2, 3])
        z = Fr(k * p, 100) * Fr(m, 12)
        return mcq("Ein Konto ist %d Monat%s lang mit %s im Minus. Der Dispozins beträgt %d%s im Jahr. Wie viel Zinsen kostet das?" % (m, "e" if m > 1 else "", eur(k), p, P), eur(z), [eur(Fr(k * p, 100)), eur(Fr(k * p, 100) * m), eur(z * 10)],
                   "%s %s %s %s %d/12 = <b>%s</b>." % (eur(k), MAL, dz(Fr(p, 100)), MAL, m, eur(z)))
    p = R.choice([2, 4, 5])
    z = R.choice([40, 50, 60, 100, 120])
    return mcq("%s möchte im Jahr %s Zinsen bekommen. Die Bank zahlt %d%s. Wie viel Geld muss %s anlegen?" % (p_, eur(z), p, P, er), eur(Fr(z * 100, p)), [eur(Fr(z * p, 100)), eur(z * p), eur(Fr(z * 10, p))],
               "K = %s %s %s = <b>%s</b>." % (eur(z), G, dz(Fr(p, 100)), eur(Fr(z * 100, p))))


def main():
    seen = set()
    sets = [
        ("Jahreszinsen", mix(R, seen, [(jahr, 20)])),
        ("Monats- und Tageszinsen", mix(R, seen, [(monat, 12), (tage, 8)])),
        ("Kapital und Zinssatz berechnen", mix(R, seen, [(rueck, 20)])),
        ("Zinseszins", mix(R, seen, [(zinseszins, 14), (monat, 6)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Zinsrechnung ist Prozentrechnung: Das <b>Kapital</b> K ist der Grundwert, der <b>Zinssatz</b> p % der Prozentsatz, die <b>Zinsen</b> Z der Prozentwert.",
         "Jahreszinsen: Z = K %s p %%. Für m Monate: Z = K %s p %% %s m/12. Für t Tage (Bankjahr 360 Tage): Z = K %s p %% %s t/360." % (MAL, MAL, MAL, MAL, MAL),
         "Werden die Zinsen mitverzinst (<b>Zinseszins</b>), multipliziert man jedes Jahr mit dem Zinsfaktor: K %s (1 + p %%)<sup>n</sup>." % MAL],
        [example("2000 € zu 3 % für 4 Monate", ["Jahr: 60 €", "60 € %s 4/12" % MAL], "20 €"),
         example("1000 € zu 5 %, 2 Jahre mit Zinseszins", ["1000 %s 1,05 %s 1,05" % (MAL, MAL)], "1102,50 €")],
        [["4 Monate: 2000 %s 0,03 = 60 €" % MAL, "Nur 4/12 eines Jahres: 20 €"],
         ["90 Tage: durch 365", "In der Schule meist mit dem Bankjahr: 360 Tage"],
         ["2 Jahre Zinseszins = 2 %s Jahreszinsen" % MAL, "Im 2. Jahr gibt es auch Zinsen auf die Zinsen"]])
    faq = [
        {"q": "Wie berechnet man Zinsen?", "a": "Zinsen = Kapital · Zinssatz. 1500 € zu 2 %: 1500 · 0,02 = 30 € im Jahr."},
        {"q": "Wie berechnet man Zinsen für einige Monate?", "a": "Jahreszinsen mal Anzahl der Monate durch 12."},
        {"q": "Was ist Zinseszins?", "a": "Die Zinsen werden dem Kapital zugeschlagen und im nächsten Jahr mitverzinst. Das Guthaben wächst jedes Jahr mit dem Faktor 1 + p %."},
        {"q": "Was ist das Bankjahr?", "a": "Für Tageszinsen rechnet man oft mit 360 Tagen im Jahr und 30 Tagen im Monat."},
    ]
    make_unit(R, "zinsrechnung", "Z",
              "Die Schülerinnen und Schüler berechnen Zinsen, Kapital und Zinssatz, Monats- und Tageszinsen sowie Zinseszinsen über wenige Jahre und vergleichen Angebote (Zusammenfassung).",
              "Zinsrechnung",
              "Zinsrechnung Klasse 7 – Zinsen, Kapital, Zinssatz, Arbeitsblätter",
              "Zinsrechnung",
              "Zinsrechnung für Klasse 7: Jahres-, Monats- und Tageszinsen, Kapital und Zinssatz berechnen, Zinseszins und Kredite. 100 Aufgaben mit Lösungen, kostenlos.",
              "Zinsen = Kapital · Zinssatz.",
              "Für Monate: mal m/12. Für Tage: mal t/360.",
              body, faq, sets, 5, grade="klasse-7")


if __name__ == "__main__":
    main()
