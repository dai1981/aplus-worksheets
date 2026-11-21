# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Pyramide und Kegel（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k9_pyramide_und_kegel.py
Volumen V = ⅓ · G · h (Pyramide) und V = ⅓ · π · r² · h (Kegel), Oberfläche der quadratischen Pyramide (G + 4 Dreiecke),
Mantel und Oberfläche des Kegels (M = π · r · s), Höhe aus dem Volumen, Sachaufgaben (Zelt, Eistüte, Dach, Sandhaufen).
Fehler: Faktor ⅓ vergessen, Körperhöhe statt Seitenhöhe für die Dreiecke, Mantel π · r · h statt π · r · s, Durchmesser statt Radius.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num, wrap, line, text, INK, RED, GREEN, FILL
from de_k6 import dz
from de_k9 import mcq, zr

R = random.Random(49912)
G = ":"
PI = math.pi


def L(v, u, k=1):
    return "%s %s" % (zr(v, k), u)


def pyr_svg(a, h):
    s = ["<polygon points='40,160 180,160 240,120 100,120' fill='%s' stroke='%s' stroke-width='2'/>" % (FILL, GREEN),
         "<polygon points='40,160 180,160 140,20' fill='#e6f2ea' stroke='%s' stroke-width='2.4'/>" % GREEN,
         "<polygon points='180,160 240,120 140,20' fill='#d9ecdf' stroke='%s' stroke-width='2.4'/>" % GREEN,
         line(140, 20, 140, 140, RED, 2, " stroke-dasharray='5 4'") + line(140, 80, 252, 80, RED, 1, " stroke-dasharray='2 3'") + text(256, 86, h, 17, col=RED, anchor="start"),
         text(110, 186, a, 17, col=RED)]
    return wrap(350, 200, "".join(s), "quadratische Pyramide", lg=True)


def kegel_svg(r, h):
    s = ["<path d='M40 160 A80 20 0 0 0 200 160 L120 20 Z' fill='%s' stroke='%s' stroke-width='2.4'/>" % (FILL, GREEN),
         "<path d='M40 160 A80 20 0 0 1 200 160' fill='none' stroke='%s' stroke-width='1.5' stroke-dasharray='5 4'/>" % GREEN,
         line(120, 20, 120, 160, RED, 2, " stroke-dasharray='5 4'") + text(226, 80, h, 17, col=RED, anchor="start"),
         line(122, 78, 222, 78, RED, 1, " stroke-dasharray='2 3'"),
         line(120, 160, 200, 160, RED, 2.4) + text(160, 205, r, 17, col=RED)]
    return wrap(330, 215, "".join(s), "Kegel", lg=True)


def pyr_v():
    kind = R.choice(["quad", "quad", "bild", "recht", "dreieck"])
    h = R.randint(3, 24)
    if kind in ("quad", "bild"):
        a = R.randint(2, 15)
        V = Fr(a * a * h, 3)
        pic = pyr_svg("a = %d cm" % a, "h = %d cm" % h) if kind == "bild" else ""
        q = (pic + "Berechne das Volumen der quadratischen Pyramide.") if pic else "Eine quadratische Pyramide hat die Grundkante a = %d cm und die Höhe h = %d cm. Berechne das Volumen." % (a, h)
        if V.denominator != 1:
            q += " (Runde auf eine Nachkommastelle.)"
        return mcq(q, L(V, "cm³") if V.denominator != 1 else "%s cm³" % num(int(V)), ["%s cm³" % num(a * a * h), L(Fr(a * h, 3), "cm³") if (a * h) % 3 else "%s cm³" % num(a * h // 3), L(Fr(a * a * h, 2), "cm³") if (a * a * h) % 2 else "%s cm³" % num(a * a * h // 2)],
                   "V = ⅓ %s a² %s h = ⅓ %s %d %s %d %s <b>%s</b>." % (MAL, MAL, MAL, a * a, MAL, h, "=" if V.denominator == 1 else "≈", L(V, "cm³") if V.denominator != 1 else "%s cm³" % num(int(V))))
    if kind == "recht":
        a, b = R.randint(2, 12), R.randint(2, 12)
        V = Fr(a * b * h, 3)
        if V.denominator != 1:
            return None
        return mcq("Eine Pyramide hat eine rechteckige Grundfläche %d cm × %d cm und die Höhe %d cm. Berechne das Volumen." % (a, b, h), "%s cm³" % num(int(V)), ["%s cm³" % num(a * b * h), "%s cm³" % num(int(V) * 2), "%s cm³" % num(a * b + h)],
                   "V = ⅓ %s %d %s %d %s %d = <b>%s cm³</b>." % (MAL, a, MAL, b, MAL, h, num(int(V))))
    g, hg = R.randint(2, 12), R.randint(2, 12)
    G_ = Fr(g * hg, 2)
    V = G_ * h / 3
    if V.denominator != 1:
        return None
    return mcq("Eine dreiseitige Pyramide hat als Grundfläche ein Dreieck mit g = %d cm und h<sub>g</sub> = %d cm. Die Pyramide ist %d cm hoch. Berechne das Volumen." % (g, hg, h), "%s cm³" % num(int(V)),
               ["%s cm³" % num(int(G_ * h)) if (G_ * h).denominator == 1 else L(G_ * h, "cm³"), "%s cm³" % num(int(2 * V)), "%s cm³" % num(int(V) + g)],
               "G = %d %s %d : 2 = %s cm². V = ⅓ %s %s %s %d = <b>%s cm³</b>." % (g, MAL, hg, dz(G_), MAL, dz(G_), MAL, h, num(int(V))))


def pyr_o():
    a, hs = R.choice([(6, 5), (10, 13), (8, 5), (12, 10), (4, 6), (10, 8), (6, 9), (8, 12), (16, 10), (5, 7)])
    kind = R.choice(["o", "o", "m", "hs"])
    M = 2 * a * hs
    if kind == "m":
        return mcq("Eine quadratische Pyramide hat die Grundkante %d cm und die Seitenhöhe h<sub>s</sub> = %d cm. Wie groß ist die Mantelfläche (vier Dreiecke)?" % (a, hs), "%d cm²" % M,
                   ["%d cm²" % (4 * a * hs), "%d cm²" % (a * hs), "%d cm²" % (M + a * a)], "4 %s (%d %s %d : 2) = <b>%d cm²</b>." % (MAL, a, MAL, hs, M))
    if kind == "hs":
        h = math.sqrt(hs * hs - (a / 2) ** 2)
        if abs(h - round(h)) > 1e-9:
            return None
        return mcq("Eine quadratische Pyramide hat die Grundkante %d cm und die Höhe %d cm. Berechne die Oberfläche." % (a, round(h)), "%d cm²" % (a * a + M),
                   ["%d cm²" % (a * a + 2 * a * round(h)), "%d cm²" % M, "%d cm²" % (a * a + 4 * a * hs)],
                   "Erst die Seitenhöhe: h<sub>s</sub> = √(%d² + %d²) = %d cm. O = %d + 4 %s %d %s %d : 2 = <b>%d cm²</b>." % (round(h), a // 2, hs, a * a, MAL, a, MAL, hs, a * a + M))
    return mcq("Eine quadratische Pyramide hat die Grundkante %d cm und die Seitenhöhe h<sub>s</sub> = %d cm. Berechne die Oberfläche." % (a, hs), "%d cm²" % (a * a + M),
               ["%d cm²" % M, "%d cm²" % (a * a + 4 * a * hs), "%d cm²" % (a * a + a * hs)], "O = a² + 4 %s (a %s h<sub>s</sub> : 2) = %d + %d = <b>%d cm²</b>." % (MAL, MAL, a * a, M, a * a + M))


def kegel_v():
    r, h = R.randint(2, 12), R.randint(3, 20)
    kind = R.choice(["r", "d", "bild"])
    V = PI * r * r * h / 3
    w = [L(PI * r * r * h, "cm³"), L(PI * (2 * r) ** 2 * h / 3, "cm³"), L(PI * r * h / 3, "cm³")]
    if kind == "d":
        return mcq("Ein Kegel hat den Durchmesser %d cm und die Höhe %d cm. Berechne das Volumen (auf eine Nachkommastelle)." % (2 * r, h), L(V, "cm³"), w,
                   "r = %d cm. V = ⅓ %s π %s %d² %s %d ≈ <b>%s</b>." % (r, MAL, MAL, r, MAL, h, L(V, "cm³")))
    pic = kegel_svg("r = %d cm" % r, "h = %d cm" % h) if kind == "bild" else ""
    return mcq(pic + ("Berechne das Volumen des Kegels (auf eine Nachkommastelle)." if pic else "Ein Kegel hat r = %d cm und h = %d cm. Berechne das Volumen (auf eine Nachkommastelle)." % (r, h)), L(V, "cm³"), w,
               "V = ⅓ %s π %s r² %s h = ⅓ %s π %s %d %s %d ≈ <b>%s</b>." % (MAL, MAL, MAL, MAL, MAL, r * r, MAL, h, L(V, "cm³")))


def kegel_o():
    r, s = R.choice([(3, 5), (5, 13), (6, 10), (4, 9), (2, 7), (8, 17), (5, 8), (3, 10), (7, 25), (4, 6)])
    kind = R.choice(["m", "m", "o", "s"])
    if kind == "m":
        return mcq("Ein Kegel hat den Radius %d cm und die Mantellinie s = %d cm. Berechne die Mantelfläche (auf eine Nachkommastelle)." % (r, s), L(PI * r * s, "cm²"),
                   [L(2 * PI * r * s, "cm²"), L(PI * r * r, "cm²"), L(PI * r * s + PI * r * r, "cm²")], "M = π %s r %s s = π %s %d %s %d ≈ <b>%s</b>." % (MAL, MAL, MAL, r, MAL, s, L(PI * r * s, "cm²")))
    if kind == "o":
        return mcq("Ein Kegel hat den Radius %d cm und die Mantellinie s = %d cm. Berechne die Oberfläche (auf eine Nachkommastelle)." % (r, s), L(PI * r * r + PI * r * s, "cm²"),
                   [L(PI * r * s, "cm²"), L(2 * PI * r * r + PI * r * s, "cm²"), L(PI * r * r + 2 * PI * r * s, "cm²")],
                   "O = π r² + π r s = %s + %s ≈ <b>%s</b>." % (zr(PI * r * r), zr(PI * r * s), L(PI * r * r + PI * r * s, "cm²")))
    h = math.sqrt(s * s - r * r)
    return mcq("Ein Kegel hat den Radius %d cm und die Höhe %s cm. Wie lang ist die Mantellinie s?" % (r, zr(h, 1) if abs(h - round(h)) > 1e-9 else str(round(h))), "%d cm" % s,
               ["%s cm" % (zr(r + h)), "%s cm" % zr(math.sqrt(abs(h * h - r * r))), "%d cm" % (s + r)], "s = √(r² + h²) = <b>%d cm</b>." % s) if abs(h - round(h)) < 1e-9 else None


def sache():
    kind = R.choice(["zelt", "eis", "dach", "sand", "trichter", "pyramide"])
    if kind == "zelt":
        a, h = R.choice([(2, Fr(3, 2)), (3, 2), (Fr(5, 2), 2), (4, 3)])
        V = Fr(a) * a * h / 3
        Lz = lambda v: ("%s m³" % dz(v)) if (Fr(v) * 100).denominator == 1 else ("etwa " + L(v, "m³", 2))
        return mcq("Ein Zelt hat die Form einer quadratischen Pyramide mit der Grundkante %s m und der Höhe %s m. Wie viel Luft ist im Zelt?" % (dz(a), dz(h)), Lz(V),
                   [Lz(Fr(a) * a * h), Lz(Fr(a) * h / 3), Lz(Fr(a) * a * h / 2)], "V = ⅓ %s %s² %s %s: <b>%s</b>." % (MAL, dz(a), MAL, dz(h), Lz(V)))
    if kind == "eis":
        r, h = R.choice([(Fr(5, 2), 12), (3, 10), (2, 11), (Fr(5, 2), 10), (3, 12)])
        V = PI * float(r) ** 2 * h / 3
        return mcq("Eine Eistüte ist kegelförmig mit r = %s cm und h = %d cm. Wie viel ml passen hinein (auf ganze ml)?" % (dz(r), h), "etwa %d ml" % round(V),
                   ["etwa %d ml" % round(3 * V), "etwa %d ml" % round(PI * float(r) * h / 3), "etwa %d ml" % round(4 * V)], "V = ⅓ %s π %s %s² %s %d ≈ %s cm³ = <b>%d ml</b>." % (MAL, MAL, dz(r), MAL, h, zr(V), round(V)))
    if kind == "dach":
        a, hs = R.choice([(6, 5), (8, 5), (10, 8), (12, 10), (8, 6)])
        M = 2 * a * hs
        p = R.choice([25, 30, 35, 40])
        return mcq("Ein Turmdach ist eine quadratische Pyramide (Grundkante %d m, Seitenhöhe %d m). Die Dachdeckung kostet %d € pro m². Was kostet die Dachfläche?" % (a, hs, p), "%s €" % num(M * p),
                   ["%s €" % num((M + a * a) * p), "%s €" % num(M * p // 2), "%s €" % num(a * hs * p)], "M = 4 %s %d %s %d : 2 = %d m². %d %s %d € = <b>%s €</b>." % (MAL, a, MAL, hs, M, M, MAL, p, num(M * p)))
    if kind == "sand":
        r, h = R.choice([(2, 1), (3, Fr(3, 2)), (Fr(5, 2), 1), (4, 2)])
        V = PI * float(r) ** 2 * float(h) / 3
        return mcq("Ein Sandhaufen ist kegelförmig mit dem Radius %s m und der Höhe %s m. Wie viel m³ Sand sind das (auf eine Nachkommastelle)?" % (dz(r), dz(h)), L(V, "m³"),
                   [L(3 * V, "m³"), L(PI * float(r) * float(h) / 3, "m³"), L(PI * float(r) * float(h), "m³")], "V = ⅓ %s π %s %s² %s %s ≈ <b>%s</b>." % (MAL, MAL, dz(r), MAL, dz(h), L(V, "m³")))
    if kind == "trichter":
        r, s = R.choice([(5, 13), (3, 5), (6, 10), (8, 17)])
        return mcq("Für einen kegelförmigen Trichter (ohne Deckel) mit r = %d cm und s = %d cm braucht man Blech für den Mantel. Wie viel Blech ist das (auf eine Nachkommastelle)?" % (r, s), L(PI * r * s, "cm²"),
                   [L(PI * r * s + PI * r * r, "cm²"), L(PI * r * r, "cm²"), L(2 * PI * r * s, "cm²")], "Nur der Mantel: π %s %d %s %d ≈ <b>%s</b>." % (MAL, r, MAL, s, L(PI * r * s, "cm²")))
    a, h = R.choice([(230, 146), (215, 143), (35, 21)])
    V = a * a * h / 3
    return mcq("Eine Pyramide in Ägypten hat (vereinfacht) eine quadratische Grundfläche mit %d m Seitenlänge und ist %d m hoch. Wie groß ist ihr Volumen (gerundet)?" % (a, h), "etwa %s m³" % num(round(V, -3 if V > 10000 else 0)),
               ["etwa %s m³" % num(round(a * a * h, -3 if V > 10000 else 0)), "etwa %s m³" % num(round(a * a * h / 2, -3 if V > 10000 else 0)), "etwa %s m³" % num(round(a * h / 3, 0))],
               "V = ⅓ %s %d² %s %d ≈ <b>%s m³</b>." % (MAL, a, MAL, h, num(round(V, -3 if V > 10000 else 0))))


def main():
    seen = set()
    sets = [
        ("Volumen der Pyramide", mix(R, seen, [(pyr_v, 20)])),
        ("Oberfläche der Pyramide", mix(R, seen, [(pyr_o, 20)])),
        ("Volumen des Kegels", mix(R, seen, [(kegel_v, 20)])),
        ("Mantel und Oberfläche des Kegels", mix(R, seen, [(kegel_o, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["Pyramide und Kegel sind „Spitzkörper“. Ihr Volumen ist ein Drittel des Prismas bzw. Zylinders mit gleicher Grundfläche und Höhe: <b>V = ⅓ %s G %s h</b>." % (MAL, MAL),
         "Quadratische Pyramide: V = ⅓ %s a² %s h. Oberfläche O = a² + 4 %s (a %s h<sub>s</sub> : 2) mit der <b>Seitenhöhe</b> h<sub>s</sub>." % (MAL, MAL, MAL, MAL),
         "Kegel: V = ⅓ %s π %s r² %s h. Mantel M = π %s r %s s mit der <b>Mantellinie</b> s, Oberfläche O = π r² + π r s." % (MAL, MAL, MAL, MAL, MAL),
         "Fehlt h<sub>s</sub> oder s, hilft der Satz des Pythagoras."],
        [example("Pyramide a = 6 cm, h = 4 cm", ["V = ⅓ %s 36 %s 4" % (MAL, MAL)], "48 cm³"),
         example("Kegel r = 3 cm, s = 5 cm", ["M = π %s 3 %s 5" % (MAL, MAL)], "≈ 47,1 cm²")],
        [["V = G %s h" % MAL, "Bei Spitzkörpern ⅓ nicht vergessen"],
         ["Dreiecksfläche mit der Körperhöhe h", "Dreiecke brauchen die Seitenhöhe h<sub>s</sub>"],
         ["Kegelmantel π %s r %s h" % (MAL, MAL), "π %s r %s s (Mantellinie)" % (MAL, MAL)]])
    faq = [
        {"q": "Wie berechne ich das Volumen einer Pyramide?", "a": "V = ⅓ · G · h. Bei einer quadratischen Pyramide ist G = a²."},
        {"q": "Wie berechne ich das Volumen eines Kegels?", "a": "V = ⅓ · π · r² · h."},
        {"q": "Was ist der Unterschied zwischen Höhe und Seitenhöhe?", "a": "Die Höhe h steht senkrecht auf der Grundfläche. Die Seitenhöhe h_s ist die Höhe eines Seitendreiecks."},
        {"q": "Wie berechne ich den Mantel eines Kegels?", "a": "M = π · r · s mit der Mantellinie s = √(r² + h²)."},
    ]
    make_unit(R, "pyramide-und-kegel", "G",
              "Die Schülerinnen und Schüler berechnen Volumen und Oberfläche von Pyramiden und Kegeln, nutzen den Satz des Pythagoras für fehlende Höhen und Mantellinien und lösen Sachaufgaben (Zusammenfassung).",
              "Pyramide und Kegel",
              "Pyramide und Kegel Klasse 9 – Volumen und Oberfläche, Arbeitsblätter mit Lösungen",
              "Pyramide und Kegel",
              "Pyramide und Kegel für Klasse 9: Volumen V = ⅓ · G · h, Oberfläche der Pyramide, Mantel und Oberfläche des Kegels und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "V = ⅓ · G · h",
              "Kegel: M = π · r · s",
              body, faq, sets, 12, grade="klasse-9")


if __name__ == "__main__":
    main()
