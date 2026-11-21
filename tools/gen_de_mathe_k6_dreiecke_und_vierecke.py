# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 6: Dreiecke und Vierecke（Leitidee Raum und Form, Sek I）
  python3 tools/gen_de_mathe_k6_dreiecke_und_vierecke.py
Dreiecke nach Seiten und Winkeln einteilen, Winkelsumme im Dreieck (180°) und im Viereck (360°), Eigenschaften von Quadrat, Rechteck, Raute, Parallelogramm, Trapez und Drachenviereck, Haus der Vierecke.
Fehler: Winkelsumme im Dreieck 360°, gleichschenklig und gleichseitig verwechselt, jede Raute für ein Quadrat gehalten.
"""
import math
import random
from de_common import lesson, example, make_unit, mix, Kids, MAL, table, wrap, line, text, INK, RED, GREEN, FILL
from de_k6 import mcq

R = random.Random(49616)
KIDS = Kids(R)


def dreieck_svg(a, b, labs=True, zeige=(True, True, False)):
    """Dreieck mit Winkeln a (links), b (rechts); Basis 200"""
    L = 220
    A = (30, 170)
    B = (30 + L, 170)
    ta, tb = math.tan(math.radians(a)), math.tan(math.radians(b))
    x = L * tb / (ta + tb)
    y = x * ta
    C = (30 + x, 170 - y)
    sc = 1.0
    if C[1] < 20:
        sc = 150.0 / y
        C = (30 + x * sc, 170 - y * sc)
        B = (30 + L * sc, 170)
    s = ["<polygon points='%.1f,%.1f %.1f,%.1f %.1f,%.1f' fill='%s' stroke='%s' stroke-width='2.5'/>" % (A + B + C + (FILL, GREEN))]
    c = 180 - a - b
    vals = [a, b, c]
    pos = [(A[0] + 30, A[1] - 8), (B[0] - 30, B[1] - 8), (C[0], C[1] + 30)]
    for i, (v, p) in enumerate(zip(vals, pos)):
        s.append(text(p[0], p[1], ("%d°" % v) if zeige[i] else "?", 14, col=RED if not zeige[i] else INK))
    W = max(B[0], C[0]) + 30
    return wrap(W, 190, "".join(s), "Dreieck mit Winkeln")


def winkelsumme():
    kind = R.choice(["bild", "bild", "text", "viereck"])
    if kind == "viereck":
        ws = [R.randint(50, 140) for _ in range(3)]
        d = 360 - sum(ws)
        if not 30 <= d <= 170:
            return None
        return mcq("In einem Viereck sind drei Winkel %d°, %d° und %d° groß. Wie groß ist der vierte Winkel?" % tuple(ws), "%d°" % d, ["%d°" % x for x in (180 - sum(ws) % 180 if 180 - sum(ws) % 180 != d else d + 20, d + 10, 360 - ws[0] - ws[1])],
                   "Winkelsumme im Viereck: 360°. 360° − %d° − %d° − %d° = <b>%d°</b>." % (ws[0], ws[1], ws[2], d))
    a, b = R.randint(25, 95), R.randint(25, 95)
    c = 180 - a - b
    if c < 15:
        return None
    w = ["%d°" % x for x in (360 - a - b, c + 10, a + b, 90 - a if 90 - a > 0 and 90 - a != c else c - 5)]
    if kind == "bild":
        return mcq(dreieck_svg(a, b, zeige=(True, True, False)) + "Wie groß ist der fehlende Winkel?", "%d°" % c, w, "Winkelsumme im Dreieck: 180°. 180° − %d° − %d° = <b>%d°</b>." % (a, b, c))
    return mcq("In einem Dreieck sind α = %d° und β = %d°. Wie groß ist γ?" % (a, b), "%d°" % c, w, "α + β + γ = 180°. 180° − %d° − %d° = <b>%d°</b>." % (a, b, c))


def art_winkel():
    kind = R.choice(["spitz", "recht", "stumpf"])
    if kind == "spitz":
        while True:
            a, b = R.randint(40, 85), R.randint(40, 85)
            if 180 - a - b < 90 and 180 - a - b > 20:
                break
    elif kind == "recht":
        a = R.randint(25, 65)
        b = 90 if R.random() < 0.5 else 90 - a
        if b == 90:
            a = R.randint(25, 60)
    else:
        a, b = R.randint(15, 40), R.randint(15, 40)
    if 180 - a - b <= 0:
        return None
    ws = sorted([a, b, 180 - a - b])
    ans = {"spitz": "spitzwinklig", "recht": "rechtwinklig", "stumpf": "stumpfwinklig"}[kind]
    if (kind == "recht" and 90 not in ws) or (kind == "stumpf" and ws[-1] <= 90) or (kind == "spitz" and ws[-1] >= 90):
        return None
    return mcq("Ein Dreieck hat die Winkel %d°, %d° und %d°. Welche Art von Dreieck ist es?" % tuple(ws), ans, [x for x in ("spitzwinklig", "rechtwinklig", "stumpfwinklig") if x != ans] + ["gleichseitig"],
               "Der größte Winkel ist %d°: %s. <b>%s</b>." % (ws[-1], "kleiner als 90°" if ws[-1] < 90 else "genau 90°" if ws[-1] == 90 else "größer als 90°", ans[0].upper() + ans[1:]))


def art_seiten():
    kind = R.choice(["gs", "gl", "un", "winkel_gl"])
    if kind == "gs":
        a = R.randint(3, 12)
        return mcq("Ein Dreieck hat drei Seiten von je %d cm. Wie heißt es?" % a, "gleichseitig", ["gleichschenklig, aber nicht gleichseitig", "unregelmäßig", "rechtwinklig"], "Alle drei Seiten gleich lang: <b>gleichseitig</b> (jeder Winkel 60°).")
    if kind == "gl":
        a, b = R.randint(4, 12), R.randint(3, 10)
        if a == b or 2 * a <= b:
            return None
        return mcq("Ein Dreieck hat die Seiten %d cm, %d cm und %d cm. Wie heißt es?" % (a, a, b), "gleichschenklig", ["gleichseitig", "unregelmäßig", "Ein solches Dreieck gibt es nicht."], "Zwei Seiten sind gleich lang: <b>gleichschenklig</b>.")
    if kind == "un":
        a, b, c = sorted(R.sample(range(3, 14), 3))
        if a + b <= c:
            return None
        return mcq("Ein Dreieck hat die Seiten %d cm, %d cm und %d cm. Wie heißt es?" % (a, b, c), "unregelmäßig (allgemein)", ["gleichschenklig", "gleichseitig", "Ein solches Dreieck gibt es nicht."], "Alle Seiten sind verschieden lang: <b>unregelmäßig</b>.")
    b = R.randint(20, 80)
    if b * 2 >= 180:
        return None
    c = 180 - 2 * b
    return mcq("In einem gleichschenkligen Dreieck sind die beiden Basiswinkel je %d° groß. Wie groß ist der dritte Winkel?" % b, "%d°" % c, ["%d°" % x for x in (b, 180 - b, 360 - 2 * b)], "180° − 2 %s %d° = <b>%d°</b>." % (MAL, b, c))


VIERECKE = {
    "Quadrat": "4 gleich lange Seiten und 4 rechte Winkel",
    "Rechteck": "4 rechte Winkel, gegenüberliegende Seiten gleich lang",
    "Raute": "4 gleich lange Seiten, gegenüberliegende Seiten parallel",
    "Parallelogramm": "zwei Paare paralleler Seiten",
    "Trapez": "mindestens ein Paar paralleler Seiten",
    "Drachenviereck": "zwei Paare gleich langer benachbarter Seiten",
}


def viereck():
    kind = R.choice(["name", "wahr", "falsch", "diag"])
    if kind == "name":
        n = R.choice(list(VIERECKE))
        return mcq("Welches Viereck hat %s?" % VIERECKE[n].replace("zwei Paare paralleler Seiten", "zwei Paare paralleler Seiten (aber nicht unbedingt rechte Winkel oder gleiche Seiten)"), n if n != "Trapez" else "Trapez",
                   [x for x in VIERECKE if x != n], "Das ist die Eigenschaft eines <b>%s</b>." % ({"Quadrat": "Quadrats", "Rechteck": "Rechtecks", "Raute": "Raute", "Parallelogramm": "Parallelogramms", "Trapez": "Trapezes", "Drachenviereck": "Drachenvierecks"}[n]) if n != "Raute" else "Das ist die Eigenschaft einer <b>Raute</b>.")
    if kind == "wahr":
        good = R.choice(["Jedes Quadrat ist ein Rechteck.", "Jedes Quadrat ist eine Raute.", "Jedes Rechteck ist ein Parallelogramm.", "Jede Raute ist ein Parallelogramm.", "Jedes Parallelogramm ist ein Trapez.", "Jede Raute ist ein Drachenviereck."])
        bad = R.sample(["Jedes Rechteck ist ein Quadrat.", "Jede Raute ist ein Quadrat.", "Jedes Trapez ist ein Parallelogramm.", "Jedes Parallelogramm ist ein Rechteck.", "Jedes Drachenviereck ist eine Raute.", "Jedes Parallelogramm ist eine Raute."], 3)
        return mcq("Welche Aussage ist richtig? %s" % " / ".join(sorted(bad + [good])), good, bad, "<b>%s</b> Die speziellere Figur hat alle Eigenschaften der allgemeineren." % good)
    if kind == "falsch":
        bad = R.choice(["Jedes Rechteck ist ein Quadrat.", "Jede Raute ist ein Quadrat.", "Jedes Trapez ist ein Parallelogramm.", "Jedes Parallelogramm ist ein Rechteck."])
        goods = R.sample(["Jedes Quadrat ist ein Rechteck.", "Jedes Quadrat ist eine Raute.", "Jedes Rechteck ist ein Parallelogramm.", "Jede Raute ist ein Parallelogramm.", "Jedes Parallelogramm ist ein Trapez."], 3)
        return mcq("Welche Aussage ist <b>falsch</b>? %s" % " / ".join(sorted(goods + [bad])), bad, goods, "<b>%s</b> ist falsch: Es gibt Gegenbeispiele." % bad)
    D = [("In welchem Viereck sind die Diagonalen gleich lang und stehen senkrecht aufeinander?", "Quadrat", ["Raute", "Rechteck", "Trapez"]),
         ("In welchem Viereck sind die Diagonalen gleich lang, stehen aber nicht immer senkrecht aufeinander?", "Rechteck", ["Raute", "Drachenviereck", "Quadrat"]),
         ("In welchem Viereck halbieren sich die Diagonalen und stehen senkrecht aufeinander, sind aber nicht immer gleich lang?", "Raute", ["Rechteck", "Trapez", "Parallelogramm"]),
         ("Wie viele Symmetrieachsen hat ein Rechteck, das kein Quadrat ist?", "2", ["4", "1", "0"]),
         ("Wie viele Symmetrieachsen hat ein Drachenviereck (keine Raute)?", "1", ["2", "0", "4"]),
         ("Wie groß ist die Winkelsumme in jedem Viereck?", "360°", ["180°", "400°", "270°"])]
    q, a, w = R.choice(D)
    return mcq(q, a, w, "<b>%s</b>." % a)


def sache():
    p, er = KIDS.next()
    k = R.randrange(8)
    if k == 0:
        a = R.randint(20, 70)
        return mcq("Eine Leiter lehnt an einer senkrechten Wand. Sie bildet mit dem Boden einen Winkel von %d°. Welchen Winkel bildet sie mit der Wand?" % a, "%d°" % (90 - a), ["%d°" % x for x in (180 - a, 360 - a, a)],
                   "Wand, Boden und Leiter bilden ein rechtwinkliges Dreieck: 180° − 90° − %d° = <b>%d°</b>." % (a, 90 - a))
    if k == 1:
        a = R.randint(30, 70)
        return mcq("Ein Dachgiebel ist ein gleichschenkliges Dreieck. Die Dachneigung (Basiswinkel) beträgt %d°. Wie groß ist der Winkel am First (oben)?" % a, "%d°" % (180 - 2 * a), ["%d°" % x for x in (180 - a, 90 - a, 360 - 2 * a)],
                   "180° − 2 %s %d° = <b>%d°</b>." % (MAL, a, 180 - 2 * a))
    if k == 2:
        return mcq("Ein Verkehrsschild „Vorfahrt gewähren“ ist ein gleichseitiges Dreieck. Wie groß ist jeder Winkel?", "60°", ["90°", "45°", "120°"], "180° %s 3 = <b>60°</b>." % ":")
    if k == 3:
        a = R.randint(60, 120)
        return mcq("Ein Parallelogramm hat einen Winkel von %d°. Wie groß ist der benachbarte Winkel?" % a, "%d°" % (180 - a), ["%d°" % x for x in (a, 360 - a, 90 - a if a < 90 else a - 90)],
                   "Benachbarte Winkel im Parallelogramm ergeben zusammen 180°: <b>%d°</b>." % (180 - a))
    if k == 4:
        return mcq("Ein Fenster hat vier rechte Winkel und vier gleich lange Seiten. Welche Form hat es?", "Quadrat", ["Raute ohne rechte Winkel", "Trapez", "Drachenviereck"], "Vier rechte Winkel und vier gleiche Seiten: <b>Quadrat</b>.")
    if k == 5:
        a = R.randint(3, 9)
        return mcq("%s baut aus Strohhalmen ein Dreieck mit den Längen %d cm, %d cm und %d cm. Geht das?" % (p, a, a + 1, 2 * a + 3), "Nein, die zwei kurzen Seiten sind zusammen zu kurz.", ["Ja, jedes Dreieck geht.", "Ja, wenn man es rechtwinklig baut.", "Nein, weil zwei Seiten fast gleich lang sind."],
                   "%d + %d = %d &lt; %d: <b>Es geht nicht</b>. Zwei Seiten müssen zusammen länger sein als die dritte." % (a, a + 1, 2 * a + 1, 2 * a + 3))
    if k == 6:
        a = R.randint(50, 80)
        b = R.randint(100, 130)
        return mcq("Ein Drachen (Drachenviereck) hat zwei gleich große Winkel von je %d° und einen Winkel von %d°. Wie groß ist der vierte Winkel?" % (a, b), "%d°" % (360 - 2 * a - b), ["%d°" % x for x in (180 - a - b % 180, 360 - a - b, 2 * a)],
                   "360° − 2 %s %d° − %d° = <b>%d°</b>." % (MAL, a, b, 360 - 2 * a - b)) if 360 - 2 * a - b > 20 else None
    a = R.randint(40, 80)
    return mcq("Ein Trapez hat zwei parallele Seiten. Ein Winkel an der unteren Seite ist %d°. Wie groß ist der Winkel darüber an derselben Schenkelseite?" % a, "%d°" % (180 - a), ["%d°" % x for x in (a, 90 + a, 360 - a)],
               "Winkel an einem Schenkel zwischen den parallelen Seiten ergeben 180°: <b>%d°</b>." % (180 - a))


def main():
    seen = set()
    sets = [
        ("Dreiecke einteilen", mix(R, seen, [(art_winkel, 10), (art_seiten, 10)])),
        ("Winkelsummen", mix(R, seen, [(winkelsumme, 20)])),
        ("Vierecke und ihre Eigenschaften", mix(R, seen, [(viereck, 20)])),
        ("Gemischte Aufgaben", mix(R, seen, [(art_seiten, 6), (winkelsumme, 8), (art_winkel, 6)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Nach den <b>Winkeln</b>: spitzwinklig (alle unter 90°), rechtwinklig (ein 90°-Winkel), stumpfwinklig (ein Winkel über 90°).",
         "Nach den <b>Seiten</b>: gleichseitig (3 gleiche Seiten), gleichschenklig (2 gleiche Seiten), unregelmäßig.",
         "Die <b>Winkelsumme im Dreieck</b> ist 180°, im <b>Viereck</b> 360°.",
         "Haus der Vierecke: Jedes Quadrat ist ein Rechteck und eine Raute. Jedes Rechteck und jede Raute ist ein Parallelogramm. Jedes Parallelogramm ist ein Trapez."],
        [example("α = 50°, β = 70°", ["180° − 50° − 70°"], "γ = 60°"),
         example("Winkel 30°, 60°, 90°", ["ein rechter Winkel"], "rechtwinkliges Dreieck")],
        [["Winkelsumme im Dreieck 360°", "Im Dreieck 180°, im Viereck 360°"],
         ["Jedes Rechteck ist ein Quadrat", "Nur, wenn alle Seiten gleich lang sind"],
         ["Gleichschenklig heißt: alle Seiten gleich", "Gleichschenklig: zwei Seiten gleich. Gleichseitig: drei"]],
        extra=table(["Viereck", "Eigenschaften"], [[k, v] for k, v in VIERECKE.items()]))
    faq = [
        {"q": "Wie groß ist die Winkelsumme im Dreieck?", "a": "Immer 180°. Kennt man zwei Winkel, rechnet man 180° minus beide."},
        {"q": "Ist jedes Quadrat ein Rechteck?", "a": "Ja. Ein Quadrat hat vier rechte Winkel. Es ist ein besonderes Rechteck mit gleich langen Seiten."},
        {"q": "Was ist der Unterschied zwischen gleichschenklig und gleichseitig?", "a": "Gleichschenklig: zwei Seiten gleich lang. Gleichseitig: alle drei Seiten gleich lang (jeder Winkel 60°)."},
        {"q": "Was ist das Haus der Vierecke?", "a": "Eine Übersicht, die zeigt, welches Viereck ein Sonderfall eines anderen ist: Quadrat → Rechteck/Raute → Parallelogramm → Trapez."},
    ]
    make_unit(R, "dreiecke-und-vierecke", "R",
              "Die Schülerinnen und Schüler klassifizieren Dreiecke nach Seiten und Winkeln, nutzen die Winkelsumme im Dreieck und Viereck und beschreiben Vierecke über ihre Eigenschaften (Zusammenfassung).",
              "Dreiecke und Vierecke",
              "Dreiecke und Vierecke Klasse 6 – Winkelsumme, Haus der Vierecke, Arbeitsblätter",
              "Dreiecke & Vierecke",
              "Dreiecke und Vierecke für Klasse 6: Dreiecksarten, Winkelsumme, Eigenschaften der Vierecke und Haus der Vierecke. 100 Aufgaben mit Lösungen, kostenlos.",
              "Winkelsumme: Dreieck 180°, Viereck 360°.",
              "Jedes Quadrat ist ein Rechteck – aber nicht umgekehrt.",
              body, faq, sets, 16, grade="klasse-6")


if __name__ == "__main__":
    main()
