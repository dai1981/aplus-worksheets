# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 10: Exponentielles Wachstum und Zerfall（Leitidee Funktionaler Zusammenhang, Sek I）
  python3 tools/gen_de_mathe_k10_exponentielles_wachstum_und_zerfall.py
Prozentuales Wachstum über mehrere Schritte, Zinseszins K = K₀ · (1 + p/100)ⁿ, Abnahme (Wertverlust, Medikamente), Halbwertszeit,
Verdopplungszeit, Rückrechnen auf den Anfangswert, Vergleich mit linearem Wachstum.
Fehler: Zinsen n-mal vom Anfangskapital (einfache Zinsen), Prozente addiert (3 · 10 % = 30 %), bei Abnahme mit 1 + p gerechnet, Halbwertszeit linear gedacht.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num
from de_k6 import dz
from de_k10 import mcq, zr
from de_k7 import eur

R = random.Random(50002)


def eu(v):
    return eur(Fr(v).limit_denominator(10 ** 9))


WACHS = [("Eine Stadt hat %s Einwohner. Die Zahl wächst jedes Jahr um %d %%. Wie viele Einwohner sind es nach %d Jahren (gerundet)?", "Jahre"),
         ("In einer Probe sind %s Bakterien. Ihre Zahl wächst jede Stunde um %d %%. Wie viele sind es nach %d Stunden (gerundet)?", "Stunden"),
         ("Ein Kanal hat %s Follower. Die Zahl wächst jeden Monat um %d %%. Wie viele Follower sind es nach %d Monaten (gerundet)?", "Monate"),
         ("Auf einem Teich wachsen %s Seerosen. Ihre Zahl wächst jede Woche um %d %%. Wie viele sind es nach %d Wochen (gerundet)?", "Wochen")]


def wachstum():
    a = R.choice([200, 500, 1000, 2000, 5000, 800, 1500])
    p = R.choice([2, 3, 4, 5, 8, 10, 12, 15, 20])
    n = R.randint(2, 8)
    t = R.choice(WACHS)
    v = a * (1 + p / 100) ** n
    return mcq(t[0] % (num(a), p, n), "etwa %s" % num(round(v)),
               ["etwa %s" % num(round(a * (1 + p * n / 100))), "etwa %s" % num(round(a * (1 + p / 100) ** (n - 1))), "etwa %s" % num(round(a * (1 + p / 100) ** (n + 1))),
                "etwa %s" % num(round(a * (p / 100) * n))],
               "Faktor q = %s, also %s %s %s<sup>%d</sup> ≈ <b>%s</b>. Die Prozente nicht einfach addieren (%d %s %d %% = %d %%)." % (dz(Fr(100 + p, 100)), num(a), MAL, dz(Fr(100 + p, 100)), n, num(round(v)), n, MAL, p, n * p))


def zinseszins():
    K = R.choice([1000, 2000, 2500, 5000, 10000, 1500, 800])
    p = R.choice([Fr(1), Fr(3, 2), Fr(2), Fr(5, 2), Fr(3), Fr(4), Fr(5)])
    n = R.randint(2, 10)
    kind = R.choice(["end", "end", "zinsen", "einfach"])
    q = 1 + float(p) / 100
    v = K * q ** n
    if kind == "end":
        return mcq("%s werden zu %s %% Zinseszins angelegt. Wie hoch ist das Guthaben nach %d Jahren?" % (eu(K), dz(p), n), eu(v),
                   [eu(K * (1 + float(p) * n / 100)), eu(K * q ** (n + 1)), eu(K * q ** (n - 1))],
                   "K = %s %s %s<sup>%d</sup> ≈ <b>%s</b>." % (eu(K), MAL, dz(1 + p / 100), n, eu(v)))
    if kind == "zinsen":
        return mcq("%s werden %d Jahre lang zu %s %% Zinseszins angelegt. Wie viele Zinsen bringt das insgesamt?" % (eu(K), n, dz(p)), eu(v - K),
                   [eu(v), eu(K * float(p) * n / 100), eu(K * float(p) / 100)], "Endkapital %s minus Anfangskapital: <b>%s</b>." % (eu(v), eu(v - K)))
    s = K * (1 + float(p) * n / 100)
    return mcq("Wie viel Euro mehr bringt Zinseszins gegenüber einfachen Zinsen bei %s, %s %% und %d Jahren?" % (eu(K), dz(p), n), eu(v - s),
               [eu(v - K), eu(s - K), eu(0)], "Zinseszins: %s, einfache Zinsen: %s. Unterschied <b>%s</b>." % (eu(v), eu(s), eu(v - s)))


def abnahme():
    kind = R.choice(["auto", "medi", "rueck", "proz"])
    if kind == "auto":
        a = R.choice([15000, 20000, 25000, 30000, 40000])
        p = R.choice([10, 12, 15, 20])
        n = R.randint(2, 6)
        v = a * (1 - p / 100) ** n
        return mcq("Ein Auto kostet neu %s €. Es verliert jedes Jahr %d %% seines Wertes. Wie viel ist es nach %d Jahren wert (auf ganze Euro)?" % (num(a), p, n), "%s €" % num(round(v)),
                   ["%s €" % num(round(a * (1 - p * n / 100))), "%s €" % num(round(a * (1 + p / 100) ** n)), "%s €" % num(round(a * (1 - p / 100) ** (n - 1)))],
                   "%s %s %s<sup>%d</sup> ≈ <b>%s €</b>." % (num(a), MAL, dz(Fr(100 - p, 100)), n, num(round(v))))
    if kind == "medi":
        a = R.choice([200, 400, 500, 800, 1000])
        p = R.choice([10, 20, 25, 30, 40])
        n = R.randint(2, 6)
        v = a * (1 - p / 100) ** n
        lin = a * (1 - p * n / 100)
        return mcq("Im Blut sind %d mg eines Medikaments. Pro Stunde werden %d %% abgebaut. Wie viel ist nach %d Stunden noch vorhanden (auf eine Nachkommastelle)?" % (a, p, n), "%s mg" % zr(v),
                   (["%s mg" % zr(lin)] if lin > 0 else []) + ["%s mg" % zr(a * (1 - p / 100) ** (n - 1)), "%s mg" % zr(a * (1 - p / 100) ** (n + 1)), "%s mg" % zr(a * (1 + p / 100) ** n)],
                   "%d %s %s<sup>%d</sup> ≈ <b>%s mg</b>." % (a, MAL, dz(Fr(100 - p, 100)), n, zr(v)))
    if kind == "rueck":
        q = Fr(R.choice([110, 120, 125, 150, 200]), 100)
        n = R.choice([2, 3])
        a = R.choice([100, 200, 400, 800, 1600])
        v = a * q ** n
        if v.denominator != 1:
            return None
        g = lambda x: num(int(x)) if Fr(x).denominator == 1 else zr(float(x), 1)
        return mcq("Eine Größe wächst pro Jahr mit dem Faktor %s. Nach %d %s beträgt sie %s. Wie groß war sie am Anfang?" % (dz(q), n, "Jahr" if n == 1 else "Jahren", num(int(v))), num(a),
                   [g(v / q ** (n - 1)) if n > 1 else g(v - a * (q - 1) * 2), g(v / q ** (n + 1)), g(v / (1 + (q - 1) * n)), g(v / (q * n))],
                   "Zurückrechnen: %s %s %s<sup>%d</sup> = <b>%s</b>." % (num(int(v)), ":", dz(q), n, num(a)))
    p = R.choice([10, 20, 50])
    n = R.choice([2, 3])
    tot = 1 - (1 - p / 100) ** n
    return mcq("Ein Wert nimmt %d-mal hintereinander um %d %% ab. Um wie viel Prozent hat er insgesamt abgenommen?" % (n, p), "%s %%" % zr(tot * 100, 1).replace(",0", ""),
               ["%d %%" % (p * n), "%d %%" % p, "%s %%" % zr((1 - p / 100) ** n * 100, 1).replace(",0", "")],
               "Restfaktor %s<sup>%d</sup> = %s. Abnahme 1 − %s = <b>%s %%</b>, nicht %d %%." % (dz(Fr(100 - p, 100)), n, zr((1 - p / 100) ** n, 3), zr((1 - p / 100) ** n, 3), zr(tot * 100, 1).replace(",0", ""), p * n))


def halbwert():
    kind = R.choice(["rest", "rest", "zeit", "verdopp", "anzahl"])
    if kind == "rest":
        T = R.choice([5, 8, 10, 12, 20, 30])
        k = R.randint(2, 5)
        m0 = R.choice([80, 160, 320, 400, 640, 1000])
        v = Fr(m0, 2 ** k)
        return mcq("Ein radioaktiver Stoff hat eine Halbwertszeit von %d Tagen. Von %d g ist nach %d Tagen wie viel übrig?" % (T, m0, k * T), "%s g" % dz(v),
                   ["%s g" % dz(Fr(m0, 2 * k)), "%s g" % dz(max(Fr(m0) - Fr(m0, 2) * k, 0)) if Fr(m0) - Fr(m0, 2) * k > 0 else "0 g", "%s g" % dz(Fr(m0, 2 ** (k + 1)))],
                   "%d Tage sind %d Halbwertszeiten: %d %s (½)<sup>%d</sup> = <b>%s g</b>." % (k * T, k, m0, MAL, k, dz(v)))
    if kind == "zeit":
        T = R.choice([3, 4, 6, 8, 25])
        k = R.randint(2, 5)
        return mcq("Von einem Stoff ist nach %d Stunden nur noch 1/%d der Anfangsmenge vorhanden. Wie groß ist die Halbwertszeit?" % (k * T, 2 ** k), "%d Stunden" % T,
                   ["%s Stunden" % zr(k * T / 2 ** k, 1), "%s Stunden" % zr(k * T / 2, 1), "%d Stunden" % (k * T // (k - 1) if k > 1 else T + 1)],
                   "1/%d = (½)<sup>%d</sup>: %d Halbwertszeiten in %d Stunden ⇒ <b>%d Stunden</b>." % (2 ** k, k, k, k * T, T))
    if kind == "verdopp":
        T = R.choice([2, 3, 4, 5, 10, 20])
        k = R.randint(2, 6)
        n0 = R.choice([100, 500, 1000, 50])
        return mcq("Eine Bakterienkultur verdoppelt sich alle %d Stunden. Am Anfang sind es %s. Wie viele sind es nach %d Stunden?" % (T, num(n0), k * T), num(n0 * 2 ** k),
                   [num(n0 * 2 * k), num(n0 * 2 ** (k * T)) if n0 * 2 ** (k * T) < 10 ** 9 else num(n0 * 2 ** (k + 1)), num(n0 + 2 ** k)],
                   "%d Stunden = %d Verdopplungen: %s %s 2<sup>%d</sup> = <b>%s</b>." % (k * T, k, num(n0), MAL, k, num(n0 * 2 ** k)))
    p = R.choice([2, 5, 7, 10, 12])
    n = math.ceil(math.log(2) / math.log(1 + p / 100))
    return mcq("Ein Guthaben wächst jährlich um %d %%. Nach wie vielen vollen Jahren hat es sich mindestens verdoppelt?" % p, "nach %d Jahren" % n,
               ["nach %d Jahren" % math.ceil(100 / p), "nach %d Jahren" % (n - 2 if n > 3 else n + 3), "nach %d Jahren" % (n + 2)],
               "1,%02d<sup>%d</sup> ≈ %s ≥ 2, aber 1,%02d<sup>%d</sup> ≈ %s &lt; 2. <b>nach %d Jahren</b>" % (p, n, zr((1 + p / 100) ** n, 2), p, n - 1, zr((1 + p / 100) ** (n - 1), 2), n))


def vergleich():
    a = R.choice([100, 200, 500, 1000])
    d = R.choice([20, 50, 100, 150])
    p = R.choice([5, 10, 15, 20])
    if a * p / 100 >= d:
        return None
    n = 1
    while a * (1 + p / 100) ** n <= a + d * n:
        n += 1
    if n < 3 or n > 30:
        return None
    return mcq("Zwei Sparpläne starten mit %s €. Plan A: jedes Jahr %d € mehr (linear). Plan B: jedes Jahr %d %% mehr (exponentiell). Ab welchem Jahr hat Plan B mehr?" % (num(a), d, p), "ab dem %d. Jahr" % n,
               ["ab dem %d. Jahr" % (n + 2), "ab dem %d. Jahr" % max(1, n - 2) if n > 2 else "ab dem %d. Jahr" % (n + 4), "Plan B hat nie mehr."],
               "Jahr %d: A %s €, B %s €. Vorher liegt A vorn. <b>ab dem %d. Jahr</b> – exponentielles Wachstum überholt lineares immer." % (n, num(a + d * n), num(round(a * (1 + p / 100) ** n)), n))


def main():
    seen = set()
    sets = [
        ("Prozentuales Wachstum", mix(R, seen, [(wachstum, 20)])),
        ("Zinseszins", mix(R, seen, [(zinseszins, 20)])),
        ("Abnahme und Zurückrechnen", mix(R, seen, [(abnahme, 20)])),
        ("Halbwertszeit und Verdopplung", mix(R, seen, [(halbwert, 20)])),
        ("Gemischte Sachaufgaben", mix(R, seen, [(vergleich, 6), (wachstum, 4), (abnahme, 5), (halbwert, 5)])),
    ]
    body = lesson(
        ["Bei <b>exponentiellem Wachstum</b> um p %% pro Schritt wird jeweils mit q = 1 + p/100 multipliziert: N(n) = N₀ %s q<sup>n</sup>." % MAL,
         "Bei <b>Abnahme</b> um p %% ist q = 1 − p/100. Zinseszins: K<sub>n</sub> = K₀ %s (1 + p/100)<sup>n</sup>." % MAL,
         "<b>Halbwertszeit</b>: In dieser Zeit halbiert sich der Bestand. Nach k Halbwertszeiten bleibt (½)<sup>k</sup> übrig. <b>Verdopplungszeit</b> entsprechend.",
         "Prozente bei mehreren Schritten nicht addieren: 2-mal +10 % ist +21 %."],
        [example("1000 € zu 3 % für 5 Jahre", ["1000 %s 1,03<sup>5</sup>" % MAL], "≈ 1159,27 €"),
         example("80 g, Halbwertszeit 5 Tage, nach 15 Tagen", ["3 Halbwertszeiten", "80 %s ⅛" % MAL], "10 g")],
        [["5 Jahre 3 %%: 1000 + 5 %s 30" % MAL, "Zinsen auf Zinsen: 1000 %s 1,03<sup>5</sup>" % MAL],
         ["−20 % ⇒ Faktor 1,2", "Faktor 0,8"],
         ["Halbwertszeit 5 Tage: nach 10 Tagen alles weg", "Nach 10 Tagen ist noch ¼ da"]])
    faq = [
        {"q": "Wie berechne ich Zinseszins?", "a": "K_n = K₀ · (1 + p/100)^n. Jedes Jahr werden die Zinsen mitverzinst."},
        {"q": "Was ist die Halbwertszeit?", "a": "Die Zeit, in der sich ein abnehmender Bestand halbiert. Nach zwei Halbwertszeiten ist noch ein Viertel übrig."},
        {"q": "Warum ergibt zweimal 10 % Zunahme nicht 20 %?", "a": "Die zweite Zunahme bezieht sich auf den schon vergrößerten Wert: 1,1 · 1,1 = 1,21, also +21 %."},
        {"q": "Wann überholt exponentielles Wachstum lineares?", "a": "Immer irgendwann – auch wenn es langsam beginnt, weil der Zuwachs selbst ständig größer wird."},
    ]
    make_unit(R, "exponentielles-wachstum-und-zerfall", "F",
              "Die Schülerinnen und Schüler modellieren Wachstums- und Abnahmeprozesse exponentiell, berechnen Zinseszins, Halbwertszeiten und Verdopplungszeiten und vergleichen exponentielles mit linearem Wachstum (Zusammenfassung).",
              "Exponentielles Wachstum und Zerfall",
              "Exponentielles Wachstum Klasse 10 – Zinseszins, Halbwertszeit, Arbeitsblätter mit Lösungen",
              "Wachstum und Zerfall",
              "Exponentielles Wachstum für Klasse 10: prozentuales Wachstum, Zinseszins, Abnahme, Halbwertszeit, Verdopplungszeit und Vergleich mit linearem Wachstum. 100 Aufgaben mit Lösungen, kostenlos.",
              "N(n) = N₀ · qⁿ",
              "Wachstum: q = 1 + p/100. Abnahme: q = 1 − p/100.",
              body, faq, sets, 2, grade="klasse-10")


if __name__ == "__main__":
    main()
