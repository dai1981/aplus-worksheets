# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 10: Sinussatz und Kosinussatz（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k10_sinussatz_und_kosinussatz.py
Allgemeine Dreiecke: Sinussatz a : sin α = b : sin β = c : sin γ (Seiten und Winkel), Kosinussatz c² = a² + b² − 2ab · cos γ
(SWS und SSS), Flächeninhalt A = ½ · a · b · sin γ, Wahl des passenden Satzes, Sachaufgaben (Vermessung, Grundstück, Navigation).
Fehler: Seite und Gegenwinkel falsch zugeordnet, −2ab cos γ vergessen (Pythagoras im nicht rechtwinkligen Dreieck), Winkelsumme vergessen, sin⁻¹ mit falschem Wert.
"""
import random, math
from de_common import lesson, example, make_unit, mix, MAL, num, wrap, line, text, INK, RED, BLUE, FILL
from de_k10 import mcq, zr

R = random.Random(50009)
M = "−"
D = math.radians


def dreieck(c, al, b, lab, label="Dreieck ABC"):
    """A=(0,0), B=(c,0), C bei Winkel al und Länge b. lab: {'a':.., 'b':.., 'c':.., 'A':.., 'B':.., 'C':..} (Winkeltexte)"""
    pts = [(0.0, 0.0), (c, 0.0), (b * math.cos(D(al)), b * math.sin(D(al)))]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    W, H = 360, 240
    sc = min((W - 90) / (max(xs) - min(xs)), (H - 80) / (max(ys) - min(ys) or 1))
    ox = 45 - min(xs) * sc + ((W - 90) - (max(xs) - min(xs)) * sc) / 2
    oy = H - 40
    P = [(ox + x * sc, oy - y * sc) for x, y in pts]
    s = ["<polygon points='%s' fill='%s' stroke='%s' stroke-width='2.6'/>" % (" ".join("%.1f,%.1f" % p for p in P), FILL, INK)]
    cx = sum(p[0] for p in P) / 3
    cy = sum(p[1] for p in P) / 3
    names = ["A", "B", "C"]
    for i, (x, y) in enumerate(P):
        dx, dy = x - cx, y - cy
        n = math.hypot(dx, dy) or 1
        s.append(text(x + dx / n * 18, y + dy / n * 18 + 6, names[i], 17, weight=700))
        if lab.get(names[i]):
            s.append(text(x - dx / n * 34, y - dy / n * 34 + 6, lab[names[i]], 15, col=RED, weight=700))
    for nm, (i, j) in (("c", (0, 1)), ("a", (1, 2)), ("b", (0, 2))):
        if lab.get(nm):
            mx, my = (P[i][0] + P[j][0]) / 2, (P[i][1] + P[j][1]) / 2
            dx, dy = mx - cx, my - cy
            n = math.hypot(dx, dy) or 1
            s.append(text(mx + dx / n * 20, my + dy / n * 20 + 6, lab[nm], 16, col=BLUE, weight=700))
    return wrap(W, H, "".join(s), label, lg=True)


def tri():
    """zufälliges Dreieck mit Winkeln in ganzen Grad"""
    al = R.choice(range(30, 100, 5))
    be = R.choice(range(25, 100, 5))
    ga = 180 - al - be
    if ga < 25:
        return None
    k = R.choice([4, 5, 6, 8, 10, 12])
    a, b, c = (k * math.sin(D(x)) / math.sin(D(ga)) * 1.0 for x in (al, be, ga))
    if max(a, b, c) > 15 or min(a, b, c) < 2.5:
        return None
    return al, be, ga, a, b, c


def cm(v):
    return "%s cm" % zr(v, 1)


def sinus_seite():
    t = tri()
    if not t:
        return None
    al, be, ga, a, b, c = t
    a = round(a, 1)
    b_ = a * math.sin(D(be)) / math.sin(D(al))
    pic = dreieck(c, al, b_, {"a": "a = %s" % cm(a), "b": "b = ?", "A": "%d°" % al, "B": "%d°" % be}, "Dreieck mit a, α und β")
    return mcq(pic + "Gegeben: a = %s, α = %d°, β = %d°. Berechne b mit dem Sinussatz (auf eine Nachkommastelle)." % (cm(a), al, be), "b ≈ %s" % cm(b_),
               ["b ≈ %s" % cm(a * math.sin(D(al)) / math.sin(D(be))), "b ≈ %s" % cm(a * be / al), "b ≈ %s" % cm(a * math.sin(D(be)) / math.sin(D(ga)))],
               "b = a %s sin β : sin α = %s %s sin %d° : sin %d° ≈ <b>%s</b>." % (MAL, zr(a, 1), MAL, be, al, cm(b_)))


def sinus_winkel():
    t = tri()
    if not t:
        return None
    al, be, ga, a, b, c = t
    if al >= 90:
        return None
    a, b = round(a, 1), round(b, 1)
    sb = b * math.sin(D(al)) / a
    if sb >= 1:
        return None
    be2 = math.degrees(math.asin(sb))
    if b > a:
        return None
    kind = R.choice(["b", "b", "g"])
    pic = dreieck(c, al, b, {"a": "a = %s" % cm(a), "b": "b = %s" % cm(b), "A": "%d°" % al, "B": "β = ?"}, "Dreieck mit a, b und α")
    if kind == "b":
        return mcq(pic + "Gegeben: a = %s, b = %s, α = %d°. Berechne β (auf eine Nachkommastelle)." % (cm(a), cm(b), al), "β ≈ %s°" % zr(be2, 1),
                   ["β ≈ %s°" % zr(math.degrees(math.asin(min(a * math.sin(D(al)) / b, 1))) if a * math.sin(D(al)) / b < 1 else 180 - al - be2 - 5, 1), "β ≈ %s°" % zr(al * b / a, 1), "β ≈ %s°" % zr(180 - al - be2, 1)],
                   "sin β = b %s sin α : a = %s %s sin %d° : %s ≈ %s ⇒ <b>β ≈ %s°</b>." % (MAL, zr(b, 1), MAL, al, zr(a, 1), zr(sb, 4), zr(be2, 1)))
    g2 = 180 - al - be2
    return mcq(pic + "Gegeben: a = %s, b = %s, α = %d°. Wie groß ist γ (auf eine Nachkommastelle)?" % (cm(a), cm(b), al), "γ ≈ %s°" % zr(g2, 1),
               ["γ ≈ %s°" % zr(be2, 1), "γ ≈ %s°" % zr(180 - be2, 1), "γ ≈ %s°" % zr(180 - al, 1)],
               "Erst β ≈ %s° mit dem Sinussatz, dann γ = 180° − %d° − %s° ≈ <b>%s°</b>." % (zr(be2, 1), al, zr(be2, 1), zr(g2, 1)))


def kos_seite():
    a = R.choice([4, 5, 6, 7, 8, 9, 10, 12])
    b = R.choice([3, 5, 6, 7, 8, 11])
    ga = R.choice([v for v in range(35, 150, 5) if v != 90])
    c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(D(ga)))
    al = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
    pic = dreieck(c, al, b, {"a": "a = %d cm" % a, "b": "b = %d cm" % b, "c": "c = ?", "C": "%d°" % ga}, "Dreieck mit a, b und γ")
    return mcq(pic + "Gegeben: a = %d cm, b = %d cm, γ = %d°. Berechne c mit dem Kosinussatz (auf eine Nachkommastelle)." % (a, b, ga), "c ≈ %s" % cm(c),
               ["c ≈ %s" % cm(math.sqrt(a * a + b * b)), "c ≈ %s" % cm(math.sqrt(abs(a * a + b * b + 2 * a * b * math.cos(D(ga))))), "c ≈ %s" % cm(a * a + b * b - 2 * a * b * math.cos(D(ga)))],
               "c² = %d² + %d² − 2 %s %d %s %d %s cos %d° ≈ %s ⇒ <b>c ≈ %s</b>." % (a, b, MAL, a, MAL, b, MAL, ga, zr(c * c, 2), cm(c)))


def kos_winkel():
    kind = R.choice(["w", "w", "w", "f", "f", "wahl"])
    if kind == "wahl":
        cs = [("drei Seiten", "Kosinussatz"), ("zwei Seiten und den eingeschlossenen Winkel", "Kosinussatz"), ("eine Seite und zwei Winkel", "Sinussatz"),
              ("zwei Seiten und den Gegenwinkel einer dieser Seiten", "Sinussatz")]
        g, ans = R.choice(cs)
        return mcq("Von einem Dreieck kennt man %s. Mit welchem Satz beginnt man am besten?" % g, "mit dem %s" % ans,
                   ["mit dem %s" % ("Sinussatz" if ans == "Kosinussatz" else "Kosinussatz"), "mit dem Satz des Pythagoras", "mit dem Strahlensatz"],
                   "%s: <b>%s</b>. Pythagoras gilt nur im rechtwinkligen Dreieck." % ("Kein Winkel mit Gegenseite bekannt" if ans == "Kosinussatz" else "Ein Paar aus Seite und Gegenwinkel ist bekannt", ans))
    if kind == "f":
        a = R.choice([4, 5, 6, 7, 8, 10, 12])
        b = R.choice([3, 5, 6, 9, 11])
        ga = R.choice([v for v in range(30, 160, 10) if v != 90])
        A = 0.5 * a * b * math.sin(D(ga))
        c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(D(ga)))
        al = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
        pic = dreieck(c, al, b, {"a": "a = %d cm" % a, "b": "b = %d cm" % b, "C": "%d°" % ga}, "Dreieck mit a, b und γ")
        return mcq(pic + "Berechne den Flächeninhalt des Dreiecks (auf eine Nachkommastelle).", "A ≈ %s cm²" % zr(A, 1),
                   ["A ≈ %s cm²" % zr(a * b * math.sin(D(ga)), 1), "A ≈ %s cm²" % zr(0.5 * a * b, 1), "A ≈ %s cm²" % zr(abs(0.5 * a * b * math.cos(D(ga))), 1)],
                   "A = ½ %s %d %s %d %s sin %d° ≈ <b>%s cm²</b>." % (MAL, a, MAL, b, MAL, ga, zr(A, 1)))
    a, b, c = sorted(R.sample([4, 5, 6, 7, 8, 9, 10, 11, 12], 3))
    if a + b <= c:
        return None
    t = R.choice(["g", "a"])
    if t == "g":
        g = math.degrees(math.acos((a * a + b * b - c * c) / (2 * a * b)))
        al = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
        pic = dreieck(c, al, b, {"a": "a = %d cm" % a, "b": "b = %d cm" % b, "c": "c = %d cm" % c, "C": "γ = ?"}, "Dreieck mit drei Seiten")
        return mcq(pic + "Berechne den größten Winkel γ (auf eine Nachkommastelle).", "γ ≈ %s°" % zr(g, 1),
                   ["γ ≈ %s°" % zr(180 - g, 1), "γ ≈ %s°" % zr(math.degrees(math.acos(max(-1, min(1, (a * a + b * b - c * c) / (a * b))))), 1), "γ ≈ %s°" % zr(180 * c / (a + b + c), 1)],
                   "cos γ = (a² + b² − c²) : (2ab) = (%d + %d − %d) : %d ≈ %s ⇒ <b>γ ≈ %s°</b>." % (a * a, b * b, c * c, 2 * a * b, zr((a * a + b * b - c * c) / (2 * a * b), 4), zr(g, 1)))
    al = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
    pic = dreieck(c, al, b, {"a": "a = %d cm" % a, "b": "b = %d cm" % b, "c": "c = %d cm" % c, "A": "α = ?"}, "Dreieck mit drei Seiten")
    return mcq(pic + "Berechne den Winkel α (auf eine Nachkommastelle).", "α ≈ %s°" % zr(al, 1),
               ["α ≈ %s°" % zr(math.degrees(math.acos((a * a + b * b - c * c) / (2 * a * b))), 1), "α ≈ %s°" % zr(180 - al, 1), "α ≈ %s°" % zr(180 * a / (a + b + c), 1)],
               "cos α = (b² + c² − a²) : (2bc) = (%d + %d − %d) : %d ≈ %s ⇒ <b>α ≈ %s°</b>." % (b * b, c * c, a * a, 2 * b * c, zr((b * b + c * c - a * a) / (2 * b * c), 4), zr(al, 1)))


def sach():
    kind = R.choice(["see", "see", "turm", "schiff", "grund", "wander"])
    if kind == "see":
        a = R.choice([120, 150, 200, 240, 300, 350])
        b = R.choice([180, 210, 250, 280, 320])
        g = R.choice([50, 60, 70, 75, 80, 100, 110, 120])
        c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(D(g)))
        return mcq("Um die Breite eines Sees zu bestimmen, misst man von einem Punkt C aus die Entfernungen zu den Uferpunkten A und B: %d m und %d m. Der Winkel bei C beträgt %d°. Wie weit sind A und B voneinander entfernt (auf ganze Meter)?" % (b, a, g),
                   "≈ %s m" % num(round(c)), ["≈ %s m" % num(round(math.sqrt(a * a + b * b))), "≈ %s m" % num(round(a + b - g)), "≈ %s m" % num(round(math.sqrt(a * a + b * b + 2 * a * b * math.cos(D(g)))))],
                   "Kosinussatz: c² = %d² + %d² − 2 %s %d %s %d %s cos %d° ⇒ <b>c ≈ %s m</b>." % (a, b, MAL, a, MAL, b, MAL, g, num(round(c))))
    if kind == "turm":
        d = R.choice([30, 40, 50, 60, 80])
        a1 = R.choice([25, 30, 35])
        a2 = R.choice([45, 50, 55, 60])
        h = d * math.sin(D(a1)) * math.sin(D(a2)) / math.sin(D(a2 - a1))
        return mcq("Von zwei Punkten, die %d m auseinander auf einer Linie zum Turm liegen, sieht man die Turmspitze unter %d° und %d°. Wie hoch ist der Turm (auf eine Nachkommastelle)?" % (d, a1, a2),
                   "≈ %s m" % zr(h, 1), ["≈ %s m" % zr(d * math.tan(D(a1)), 1), "≈ %s m" % zr(d * math.tan(D(a2)), 1), "≈ %s m" % zr(d * math.sin(D(a1)) / math.sin(D(a2 - a1)), 1)],
                   "Im Dreieck mit dem Winkel %d° an der Spitze: Sinussatz für die Strecke zur Spitze s = %d %s sin %d° : sin %d° ≈ %s m, dann h = s %s sin %d° ≈ <b>%s m</b>." % (
                       a2 - a1, d, MAL, a1, a2 - a1, zr(d * math.sin(D(a1)) / math.sin(D(a2 - a1)), 1), MAL, a2, zr(h, 1)))
    if kind == "schiff":
        v1 = R.choice([10, 12, 15, 18])
        v2 = R.choice([8, 14, 16, 20])
        g = R.choice([40, 60, 75, 120, 135])
        t = R.choice([1, 2, 3])
        a, b = v1 * t, v2 * t
        c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(D(g)))
        return mcq("Zwei Schiffe fahren gleichzeitig vom selben Hafen ab, mit %d km/h und %d km/h. Ihre Kurse bilden einen Winkel von %d°. Wie weit sind sie nach %d %s voneinander entfernt (auf eine Nachkommastelle)?" % (v1, v2, g, t, "Stunde" if t == 1 else "Stunden"),
                   "≈ %s km" % zr(c, 1), ["≈ %s km" % zr(math.sqrt(a * a + b * b), 1), "≈ %s km" % zr(abs(a - b) + g / 10, 1), "≈ %s km" % zr(math.sqrt(a * a + b * b + 2 * a * b * math.cos(D(g))), 1)],
                   "Seiten %d km und %d km, Winkel %d°: Kosinussatz ⇒ <b>≈ %s km</b>." % (a, b, g, zr(c, 1)))
    if kind == "grund":
        a = R.choice([20, 25, 30, 35, 40])
        b = R.choice([18, 24, 28, 32, 45])
        g = R.choice([50, 65, 70, 80, 100, 110, 120])
        A = 0.5 * a * b * math.sin(D(g))
        return mcq("Ein dreieckiges Grundstück hat zwei Seiten von %d m und %d m, die einen Winkel von %d° einschließen. Wie groß ist es (auf ganze m²)?" % (a, b, g),
                   "≈ %s m²" % num(round(A)), ["≈ %s m²" % num(round(a * b * math.sin(D(g)))), "≈ %s m²" % num(round(0.5 * a * b)), "≈ %s m²" % num(round(abs(0.5 * a * b * math.cos(D(g)))))],
                   "A = ½ %s %d %s %d %s sin %d° ≈ <b>%s m²</b>." % (MAL, a, MAL, b, MAL, g, num(round(A))))
    a = R.choice([3, 4, 5, 6])
    b = R.choice([2, 3, 5, 7])
    k = R.choice([30, 40, 50, 60, 70])
    g = 180 - k
    c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(D(g)))
    return mcq("Eine Wanderin geht %d km geradeaus, biegt dann um %d° ab und geht noch %d km. Wie weit ist sie vom Start entfernt (auf eine Nachkommastelle)?" % (a, k, b), "≈ %s km" % zr(c, 1),
               ["≈ %s km" % zr(math.sqrt(a * a + b * b - 2 * a * b * math.cos(D(k))), 1), "≈ %s km" % zr(a + b, 1), "≈ %s km" % zr(math.sqrt(a * a + b * b), 1)],
               "Der Innenwinkel im Dreieck ist 180° − %d° = %d°: c² = %d² + %d² − 2 %s %d %s %d %s cos %d° ⇒ <b>≈ %s km</b>." % (k, g, a, b, MAL, a, MAL, b, MAL, g, zr(c, 1)))


def main():
    seen = set()
    sets = [
        ("Sinussatz: Seiten", mix(R, seen, [(sinus_seite, 20)])),
        ("Sinussatz: Winkel", mix(R, seen, [(sinus_winkel, 20)])),
        ("Kosinussatz: Seiten", mix(R, seen, [(kos_seite, 20)])),
        ("Winkel, Flächeninhalt, Satz wählen", mix(R, seen, [(kos_winkel, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sach, 20)])),
    ]
    body = lesson(
        ["In jedem Dreieck liegt die Seite a gegenüber dem Winkel α, b gegenüber β und c gegenüber γ.",
         "<b>Sinussatz</b>: a : sin α = b : sin β = c : sin γ. Man braucht ein Paar aus Seite und Gegenwinkel.",
         "<b>Kosinussatz</b>: c² = a² + b² − 2ab %s cos γ. Er hilft bei zwei Seiten mit eingeschlossenem Winkel (SWS) und bei drei Seiten (SSS). Für γ = 90° wird er zum Satz des Pythagoras." % MAL,
         "Flächeninhalt: A = ½ %s a %s b %s sin γ." % (MAL, MAL, MAL)],
        [example("a = 7 cm, b = 5 cm, γ = 60°", ["c² = 49 + 25 − 2 %s 7 %s 5 %s 0,5 = 39" % (MAL, MAL, MAL)], "c ≈ 6,2 cm"),
         example("a = 8 cm, α = 50°, β = 70°", ["b = 8 %s sin 70° : sin 50°" % MAL], "b ≈ 9,8 cm")],
        [["c² = a² + b² (ohne rechten Winkel)", "c² = a² + b² − 2ab %s cos γ" % MAL],
         ["a : sin β", "a gehört zu α (Gegenwinkel)"],
         ["Winkelsumme vergessen", "γ = 180° − α − β"]])
    faq = [
        {"q": "Wann benutze ich den Sinussatz?", "a": "Wenn eine Seite und ihr Gegenwinkel bekannt sind, dazu noch eine weitere Seite oder ein weiterer Winkel."},
        {"q": "Wann benutze ich den Kosinussatz?", "a": "Bei zwei Seiten mit dem eingeschlossenen Winkel oder bei drei bekannten Seiten."},
        {"q": "Wie hängt der Kosinussatz mit dem Satz des Pythagoras zusammen?", "a": "Für γ = 90° ist cos γ = 0, dann bleibt c² = a² + b²."},
        {"q": "Wie berechne ich den Flächeninhalt ohne Höhe?", "a": "A = ½ · a · b · sin γ mit zwei Seiten und dem eingeschlossenen Winkel."},
    ]
    make_unit(R, "sinussatz-und-kosinussatz", "R",
              "Die Schülerinnen und Schüler berechnen Seiten, Winkel und Flächeninhalte in allgemeinen Dreiecken mit dem Sinussatz und dem Kosinussatz und wenden sie in Sachzusammenhängen an (Zusammenfassung).",
              "Sinussatz und Kosinussatz",
              "Sinussatz und Kosinussatz Klasse 10 – allgemeine Dreiecke berechnen, Arbeitsblätter mit Lösungen",
              "Sinus- und Kosinussatz",
              "Sinussatz und Kosinussatz für Klasse 10: Seiten und Winkel in allgemeinen Dreiecken, Flächeninhalt mit dem Sinus und Sachaufgaben aus der Vermessung. 100 Aufgaben mit Lösungen, kostenlos.",
              "a : sin α = b : sin β = c : sin γ",
              "Kosinussatz: c² = a² + b² − 2ab · cos γ",
              body, faq, sets, 9, grade="klasse-10")


if __name__ == "__main__":
    main()
