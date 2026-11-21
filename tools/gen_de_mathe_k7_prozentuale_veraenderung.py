# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 7: Prozentuale Veränderung – Rabatt, Aufschlag und Mehrwertsteuer（Leitidee Zahl und Operation, Sek I）
  python3 tools/gen_de_mathe_k7_prozentuale_veraenderung.py
Vermehrter und verminderter Grundwert (Wachstumsfaktor 1 + p %, 1 − p %), Rabatt, Skonto, Preiserhöhung, Mehrwertsteuer 19 % und 7 %, ursprünglichen Preis zurückrechnen, prozentuale Änderung bestimmen.
Fehler: nach einer Erhöhung um 20 % den alten Preis mit −20 % zurückgerechnet, Rabatt vom neuen statt vom alten Preis, Änderung auf den neuen Wert bezogen.
"""
import random
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, Kids, MAL, table
from de_k6 import dz
from de_k7 import mcq, eur, pz, P

R = random.Random(49704)
KIDS = Kids(R)
G = ":"
DINGE = [("Eine Jacke", 40, 160), ("Ein Fahrrad", 200, 900), ("Ein Paar Turnschuhe", 50, 150), ("Ein Handy", 150, 600), ("Ein Rucksack", 25, 90), ("Eine Konzertkarte", 30, 90)]


def faktor():
    p = R.choice([3, 5, 8, 10, 12, 15, 20, 25, 30, 40, 2.5, 7.5, 19, 7])
    p = Fr(p).limit_denominator(10)
    up = R.random() < 0.5
    f = 1 + p / 100 if up else 1 - p / 100
    return mcq("Welcher Faktor gehört zu einer %s um %s?" % ("Erhöhung" if up else "Senkung", pz(p)), dz(f), [dz(1 - p / 100 if up else 1 + p / 100), dz(p / 100), dz(p) if p != f else dz(f * 10)],
               "%s: 100%s %s %s = %s%s, also Faktor <b>%s</b>." % ("Erhöhung" if up else "Senkung", P, "+" if up else "−", pz(p), dz(f * 100), P, dz(f)))


def neu():
    d, lo, hi = R.choice(DINGE)
    pr = R.randint(lo, hi)
    p = R.choice([5, 10, 15, 20, 25, 30, 40, 50])
    up = R.random() < 0.4
    v = pr * (Fr(100 + p, 100) if up else Fr(100 - p, 100))
    if (v * 100).denominator != 1:
        return None
    if up:
        q = "%s kostet %d €. Der Preis steigt um %d%s. Wie hoch ist der Preis jetzt?" % (d, pr, p, P)
    else:
        q = "%s kostet %d €. Es gibt %d%s Rabatt. Wie hoch ist der Preis jetzt?" % (d, pr, p, P)
    ab = Fr(pr * p, 100)
    return mcq(q, eur(v), [eur(ab), eur(pr - ab if up else pr + ab), eur(pr - p if not up else pr + p)],
               "%d € %s %s = <b>%s</b>." % (pr, MAL, dz(Fr(100 + p, 100) if up else Fr(100 - p, 100)), eur(v)))


def zurueck():
    d, lo, hi = R.choice(DINGE)
    alt = R.randint(lo // 5, hi // 5) * 5
    p = R.choice([10, 20, 25, 30, 40, 50])
    up = R.random() < 0.5
    f = Fr(100 + p, 100) if up else Fr(100 - p, 100)
    v = alt * f
    if (v * 100).denominator != 1:
        return None
    falsch = v * (Fr(100 - p, 100) if up else Fr(100 + p, 100))
    q = ("Nach einer Preiserhöhung um %d%s kostet %s %s. Wie hoch war der Preis vorher?" % (p, P, (d[0].lower() + d[1:]), eur(v))) if up else ("Mit %d%s Rabatt kostet %s noch %s. Wie hoch war der ursprüngliche Preis?" % (p, P, d[0].lower() + d[1:], eur(v)))
    return mcq(q, eur(alt), [eur(falsch), eur(v - Fr(v * p, 100) if up else v + Fr(v * p, 100)) if eur(v - Fr(v * p, 100) if up else v + Fr(v * p, 100)) != eur(falsch) else eur(alt + 5), eur(v * f)],
               "Neuer Preis = alter Preis %s %s. Also %s %s %s = <b>%s</b>. (Nicht mit %d%s vom neuen Preis rechnen!)" % (MAL, dz(f), eur(v), G, dz(f), eur(alt), p, P))


def aenderung():
    a = R.choice([20, 40, 50, 80, 120, 150, 200, 250, 400])
    p = R.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75])
    up = R.random() < 0.5
    b = Fr(a * (100 + p if up else 100 - p), 100)
    if b.denominator != 1:
        return None
    th = R.choice(["Ein Preis", "Die Zahl der Mitglieder", "Die Besucherzahl"])
    u = " €" if th == "Ein Preis" else ""
    d = abs(b - a)
    wrong = pz(Fr(d * 100, b)) if (Fr(d * 100, b) * 10).denominator in (1, 2, 5, 10) else pz(p + 5)
    return mcq("%s ändert sich von %d%s auf %s%s. Um wie viel Prozent ist %s gestiegen oder gesunken?" % (th, a, u, dz(b), u, "er" if th == "Ein Preis" else "sie"), "um %s %s" % (pz(p), "gestiegen" if up else "gesunken"),
               ["um %s %s" % (pz(p), "gesunken" if up else "gestiegen"), "um %s %s" % (wrong if wrong != pz(p) else pz(p * 2), "gestiegen" if up else "gesunken"), "um %s %s" % (dz(d) + P, "gestiegen" if up else "gesunken") if d != p else "um %s %s" % (pz(p + 10), "gestiegen" if up else "gesunken")],
               "Änderung: %s. Auf den alten Wert beziehen: %s %s %d = %s = <b>%s</b>." % (dz(d), dz(d), G, a, dz(Fr(d, a)), pz(p)))


def mwst():
    kind = R.choice(["netto", "brutto", "sieben"])
    if kind == "netto":
        n = R.choice([20, 50, 80, 100, 150, 200, 300, 400, 500])
        return mcq("Ein Gerät kostet ohne Mehrwertsteuer %d €. Wie viel kostet es mit 19%s Mehrwertsteuer?" % (n, P), eur(Fr(n * 119, 100)), [eur(Fr(n * 19, 100)), eur(n + 19), eur(Fr(n * 81, 100))],
                   "%d € %s 1,19 = <b>%s</b>." % (n, MAL, eur(Fr(n * 119, 100))))
    if kind == "brutto":
        n = R.choice([100, 200, 300, 400, 500, 1000])
        b = Fr(n * 119, 100)
        return mcq("Ein Preis mit 19%s Mehrwertsteuer ist %s. Wie hoch ist der Preis ohne Mehrwertsteuer?" % (P, eur(b)), eur(n), [eur(b * Fr(81, 100)), eur(b - 19), eur(b / Fr(19, 100))],
                   "%s %s 1,19 = <b>%s</b>. (Nicht 19%s vom Endpreis abziehen.)" % (eur(b), G, eur(n), P))
    n = R.choice([2, 3, 4, 5, 10, 20, 30])
    return mcq("Lebensmittel haben 7%s Mehrwertsteuer. Ein Einkauf kostet ohne Steuer %d €. Wie viel kostet er mit Steuer?" % (P, n), eur(Fr(n * 107, 100)), [eur(Fr(n * 119, 100)), eur(Fr(n * 7, 100)), eur(n + 7)],
               "%d € %s 1,07 = <b>%s</b>." % (n, MAL, eur(Fr(n * 107, 100))))


def sache():
    p_, er = KIDS.next()
    kind = R.choice(["skonto", "zweimal", "abo", "vergleich", "lohn"])
    if kind == "skonto":
        r = R.choice([200, 400, 500, 800, 1200])
        s = R.choice([2, 3])
        return mcq("Eine Rechnung über %d € wird innerhalb von 10 Tagen bezahlt. Dafür gibt es %d%s Skonto. Wie viel wird überwiesen?" % (r, s, P), eur(Fr(r * (100 - s), 100)), [eur(Fr(r * s, 100)), eur(r - s), eur(Fr(r * (100 + s), 100))],
                   "%d € %s %s = <b>%s</b>." % (r, MAL, dz(Fr(100 - s, 100)), eur(Fr(r * (100 - s), 100))))
    if kind == "zweimal":
        pr = R.choice([100, 200, 400, 500])
        p = R.choice([10, 20, 25])
        v = pr * Fr(100 + p, 100) * Fr(100 - p, 100)
        return mcq("Ein Preis von %d € steigt um %d%s und sinkt danach wieder um %d%s. Wie hoch ist der Preis jetzt?" % (pr, p, P, p, P),
                   eur(v), [eur(pr), eur(pr * Fr(100 + p, 100)), eur(pr + Fr(pr * p * p, 10000))],
                   "%d € %s %s %s %s = <b>%s</b>. Die Senkung bezieht sich auf den höheren Preis." % (pr, MAL, dz(Fr(100 + p, 100)), MAL, dz(Fr(100 - p, 100)), eur(v)))
    if kind == "abo":
        m = R.choice([8, 10, 12, 15])
        p = R.choice([10, 20, 25])
        j = 12 * m * Fr(100 - p, 100)
        return mcq("Ein Abo kostet %d € im Monat. Wer für ein Jahr im Voraus zahlt, bekommt %d%s Rabatt. Wie viel kostet das Jahr dann?" % (m, p, P), eur(j), [eur(12 * m), eur(12 * m - p), eur(Fr(12 * m * p, 100))],
                   "12 %s %d € = %d €. %d € %s %s = <b>%s</b>." % (MAL, m, 12 * m, 12 * m, MAL, dz(Fr(100 - p, 100)), eur(j)))
    if kind == "vergleich":
        pr = R.choice([60, 80, 100, 120])
        p1 = R.choice([20, 25, 30])
        s2 = R.choice([15, 20, 25, 30, 35])
        a1 = pr * Fr(100 - p1, 100)
        a2 = pr - s2
        if a1 == a2:
            return None
        best = "Angebot A" if a1 < a2 else "Angebot B"
        return mcq("Ein Spiel kostet %d €. Angebot A: %d%s Rabatt. Angebot B: %d € billiger. Welches Angebot ist günstiger?" % (pr, p1, P, s2), best, ["Angebot B" if best == "Angebot A" else "Angebot A", "Beide gleich.", "Das kann man nicht sagen."],
                   "A: %s, B: %s. <b>%s</b>." % (eur(a1), eur(a2), best))
    l = R.choice([10, 12, 13, 14, 15])
    p = R.choice([2, 3, 4, 5])
    v = l * Fr(100 + p, 100)
    return mcq("%s verdient beim Ferienjob %d € pro Stunde. Der Lohn steigt um %d%s. Wie viel verdient %s jetzt pro Stunde?" % (p_, l, p, P, er), eur(v), [eur(l + p), eur(Fr(l * p, 100)), eur(l * Fr(100 - p, 100))],
                   "%d € %s %s = <b>%s</b>." % (l, MAL, dz(Fr(100 + p, 100)), eur(v)))


def main():
    seen = set()
    sets = [
        ("Wachstumsfaktor", mix(R, seen, [(faktor, 20)])),
        ("Neuer Preis", mix(R, seen, [(neu, 20)])),
        ("Mehrwertsteuer", mix(R, seen, [(mwst, 12), (neu, 8)])),
        ("Zurückrechnen und Änderung bestimmen", mix(R, seen, [(zurueck, 12), (aenderung, 8)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Bei einer <b>Erhöhung</b> um p %% ist der neue Wert (100 + p) %% des alten: neuer Wert = alter Wert %s (1 + p %%)." % MAL,
         "Bei einer <b>Senkung</b> (Rabatt) ist der neue Wert (100 − p) %%: neuer Wert = alter Wert %s (1 − p %%)." % MAL,
         "Den <b>alten Wert</b> bekommt man zurück, indem man durch den Faktor teilt – nicht, indem man p % abzieht.",
         "Die <b>prozentuale Änderung</b> bezieht sich immer auf den alten Wert: Änderung %s alter Wert." % G,
         "In Deutschland gilt meist 19 % Mehrwertsteuer, für Lebensmittel 7 %."],
        [example("80 € mit 15 % Rabatt", ["80 %s 0,85" % MAL], "68 €"),
         example("Nach +20 % kostet es 72 €. Alter Preis?", ["72 %s 1,2" % G], "60 €")],
        [["Nach +20 % auf 72 €: 72 − 20 % = 57,60 €", "Durch 1,2 teilen: 60 €"],
         ["+10 % und dann −10 % ergibt den alten Preis", "100 %s 1,1 %s 0,9 = 99" % (MAL, MAL)],
         ["Von 80 auf 100: 20 % (auf 100 bezogen)", "Auf den alten Wert 80 beziehen: 25 %"]])
    faq = [
        {"q": "Wie berechne ich einen Preis nach Rabatt?", "a": "Mit dem Faktor 1 − p %. 25 % Rabatt auf 60 €: 60 · 0,75 = 45 €."},
        {"q": "Wie finde ich den ursprünglichen Preis?", "a": "Den neuen Preis durch den Faktor teilen. Nach 20 % Rabatt kostet etwas 48 €: 48 : 0,8 = 60 €."},
        {"q": "Warum ist +10 % und −10 % nicht wieder der alte Preis?", "a": "Weil sich die 10 % beim zweiten Mal auf den höheren Preis beziehen. Am Ende sind es 99 % des alten Preises."},
        {"q": "Wie hoch ist die Mehrwertsteuer in Deutschland?", "a": "Der normale Satz ist 19 %, für Lebensmittel und Bücher gilt meist 7 %."},
    ]
    make_unit(R, "prozentuale-veraenderung", "Z",
              "Die Schülerinnen und Schüler berechnen vermehrte und verminderte Grundwerte mit Wachstumsfaktoren, rechnen Rabatte, Preiserhöhungen und Mehrwertsteuer und bestimmen prozentuale Änderungen (Zusammenfassung).",
              "Prozentuale Veränderung: Rabatt, Aufschlag, Mehrwertsteuer",
              "Prozentuale Veränderung Klasse 7 – Rabatt und Mehrwertsteuer, Arbeitsblätter",
              "Rabatt & Mehrwertsteuer",
              "Prozentuale Veränderung für Klasse 7: Wachstumsfaktor, Rabatt, Preiserhöhung, Mehrwertsteuer und zurückrechnen. 100 Aufgaben mit Lösungen, kostenlos.",
              "Neuer Wert = alter Wert · (1 ± p %).",
              "Zurückrechnen: durch den Faktor teilen.",
              body, faq, sets, 4, grade="klasse-7")


if __name__ == "__main__":
    main()
