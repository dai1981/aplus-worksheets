# -*- coding: utf-8 -*-
"""
Deutschland Mathe Klasse 9: Kugel und zusammengesetzte Körper（Leitidee Größen und Messen, Sek I）
  python3 tools/gen_de_mathe_k9_kugel.py
Volumen V = 4/3 · π · r³, Oberfläche O = 4 · π · r², Halbkugel, Radius aus Volumen oder Oberfläche, zusammengesetzte Körper
(Zylinder mit Halbkugel, Kegel mit Halbkugel), Sachaufgaben (Bälle, Kugeln im Würfel, Erde, Seifenblase).
Fehler: r² statt r³, Durchmesser statt Radius, Halbkugel ohne Grundkreis, beim Verdoppeln des Radius nur doppeltes Volumen.
"""
import random, math
from fractions import Fraction as Fr
from de_common import lesson, example, make_unit, mix, MAL, num
from de_k6 import dz
from de_k9 import mcq, zr

R = random.Random(49913)
G = ":"
PI = math.pi


def L(v, u, k=1):
    return "%s %s" % (zr(v, k), u)


def volumen():
    kind = R.choice(["r", "r", "d", "halb"])
    r = R.randint(2, 15) if R.random() < 0.8 else Fr(R.randint(5, 45), 10)
    rf = float(r)
    V = 4 / 3 * PI * rf ** 3
    if kind == "halb":
        return mcq("Berechne das Volumen einer Halbkugel mit r = %s cm (auf eine Nachkommastelle)." % dz(r), L(V / 2, "cm³"),
                   [L(V, "cm³"), L(2 / 3 * PI * rf ** 2, "cm³"), L(V / 4, "cm³")], "V = ½ %s 4/3 %s π %s r³ = 2/3 %s π %s %s³ ≈ <b>%s</b>." % (MAL, MAL, MAL, MAL, MAL, dz(r), L(V / 2, "cm³")))
    if kind == "d":
        return mcq("Eine Kugel hat den Durchmesser %s cm. Berechne ihr Volumen (auf eine Nachkommastelle)." % dz(2 * Fr(r)), L(V, "cm³"),
                   [L(4 / 3 * PI * (2 * rf) ** 3, "cm³"), L(4 / 3 * PI * rf ** 2, "cm³"), L(4 * PI * rf ** 2, "cm³")], "r = %s cm. V = 4/3 %s π %s %s³ ≈ <b>%s</b>." % (dz(r), MAL, MAL, dz(r), L(V, "cm³")))
    return mcq("Berechne das Volumen einer Kugel mit r = %s cm (auf eine Nachkommastelle)." % dz(r), L(V, "cm³"),
               [L(4 / 3 * PI * rf ** 2, "cm³"), L(4 * PI * rf ** 2, "cm³"), L(PI * rf ** 3, "cm³")], "V = 4/3 %s π %s r³ = 4/3 %s π %s %s ≈ <b>%s</b>." % (MAL, MAL, MAL, MAL, num(int(rf ** 3)) if rf == int(rf) else zr(rf ** 3, 3), L(V, "cm³")))


def oberflaeche():
    kind = R.choice(["r", "r", "d", "halb"])
    r = R.randint(2, 20)
    O = 4 * PI * r * r
    if kind == "halb":
        return mcq("Wie groß ist die Oberfläche einer massiven Halbkugel mit r = %d cm (gewölbte Fläche und Grundkreis, auf eine Nachkommastelle)?" % r, L(3 * PI * r * r, "cm²"),
                   [L(2 * PI * r * r, "cm²"), L(O, "cm²"), L(PI * r * r, "cm²")], "Halbe Kugelfläche 2πr² plus Grundkreis πr² = 3 %s π %s %d² ≈ <b>%s</b>." % (MAL, MAL, r, L(3 * PI * r * r, "cm²")))
    if kind == "d":
        return mcq("Eine Kugel hat den Durchmesser %d cm. Berechne ihre Oberfläche (auf eine Nachkommastelle)." % (2 * r), L(O, "cm²"), [L(4 * PI * 4 * r * r, "cm²"), L(PI * r * r, "cm²"), L(4 / 3 * PI * r ** 3, "cm²")],
                   "r = %d cm. O = 4 %s π %s %d² ≈ <b>%s</b>." % (r, MAL, MAL, r, L(O, "cm²")))
    return mcq("Berechne die Oberfläche einer Kugel mit r = %d cm (auf eine Nachkommastelle)." % r, L(O, "cm²"), [L(PI * r * r, "cm²"), L(4 * PI * r, "cm²"), L(4 / 3 * PI * r ** 3, "cm²")],
               "O = 4 %s π %s r² = 4 %s π %s %d ≈ <b>%s</b>." % (MAL, MAL, MAL, MAL, r * r, L(O, "cm²")))


def rueck():
    r = R.randint(2, 12)
    kind = R.choice(["V", "O", "faktor", "faktor"])
    if kind == "V":
        V = round(4 / 3 * PI * r ** 3, 1)
        return mcq("Eine Kugel hat das Volumen %s cm³. Wie groß ist ihr Radius (gerundet)?" % zr(V), "etwa %d cm" % r, ["etwa %s cm" % zr(math.sqrt(V / (4 / 3 * PI))), "etwa %s cm" % zr(V / (4 / 3 * PI) / 10), "etwa %d cm" % (2 * r)],
                   "r³ = V %s (4/3 %s π) ≈ %d ⇒ r = ∛%d = <b>%d cm</b>." % (G, MAL, r ** 3, r ** 3, r))
    if kind == "O":
        O = round(4 * PI * r * r, 1)
        return mcq("Eine Kugel hat die Oberfläche %s cm². Wie groß ist ihr Radius (gerundet)?" % zr(O), "etwa %d cm" % r, ["etwa %s cm" % zr(O / (4 * PI)), "etwa %s cm" % zr(math.sqrt(O / PI)), "etwa %s cm" % zr((O / (4 / 3 * PI)) ** (1 / 3))],
                   "r² = O %s (4π) ≈ %d ⇒ <b>r = %d cm</b>." % (G, r * r, r))
    k = R.choice([2, 3, Fr(1, 2), 10])
    what = R.choice(["Volumen", "Oberfläche"])
    f = Fr(k) ** (3 if what == "Volumen" else 2)
    P_ = "Es" if what == "Volumen" else "Sie"
    return mcq("Der Radius einer Kugel wird %s. Wie verändert sich %s?" % ({2: "verdoppelt", 3: "verdreifacht", Fr(1, 2): "halbiert", 10: "verzehnfacht"}[k], "das Volumen" if what == "Volumen" else "die Oberfläche"),
               ("%s wird mit %s multipliziert." % (P_, dz(f))),
               ["%s wird mit %s multipliziert." % (P_, dz(Fr(k))), "%s wird mit %s multipliziert." % (P_, dz(Fr(k) ** (2 if what == "Volumen" else 3))), "%s bleibt gleich." % P_],
               "%s hängt von r%s ab: %s%s = <b>%s</b>." % (what, "³" if what == "Volumen" else "²", dz(Fr(k)), "³" if what == "Volumen" else "²", dz(f)))


def zusammen():
    kind = R.choice(["silo", "eis", "kapsel", "hohl", "wuerfel"])
    if kind == "silo":
        r, h = R.randint(2, 6), R.randint(5, 15)
        V = PI * r * r * h + 2 / 3 * PI * r ** 3
        return mcq("Ein Silo besteht aus einem Zylinder (r = %d m, h = %d m) mit einer Halbkugel als Dach. Wie groß ist sein Volumen (auf eine Nachkommastelle)?" % (r, h), L(V, "m³"),
                   [L(PI * r * r * h + 4 / 3 * PI * r ** 3, "m³"), L(PI * r * r * h, "m³"), L(PI * r * r * h + 2 * PI * r * r, "m³")],
                   "Zylinder π %s %d² %s %d ≈ %s, Halbkugel 2/3 %s π %s %d³ ≈ %s. Zusammen <b>%s</b>." % (MAL, r, MAL, h, zr(PI * r * r * h), MAL, MAL, r, zr(2 / 3 * PI * r ** 3), L(V, "m³")))
    if kind == "eis":
        r, h = R.choice([(3, 10), (Fr(5, 2), 12), (3, 12), (2, 9)])
        rf = float(r)
        V = PI * rf * rf * h / 3 + 2 / 3 * PI * rf ** 3
        return mcq("Eine Eistüte (Kegel, r = %s cm, h = %d cm) ist bis zum Rand gefüllt, oben liegt eine Halbkugel Eis. Wie viel Eis ist es (auf ganze cm³)?" % (dz(r), h), "etwa %d cm³" % round(V),
                   ["etwa %d cm³" % round(PI * rf * rf * h / 3 + 4 / 3 * PI * rf ** 3), "etwa %d cm³" % round(PI * rf * rf * h + 2 / 3 * PI * rf ** 3), "etwa %d cm³" % round(PI * rf * rf * h / 3)],
                   "Kegel ⅓ %s π %s %s² %s %d + Halbkugel 2/3 %s π %s %s³ ≈ <b>%d cm³</b>." % (MAL, MAL, dz(r), MAL, h, MAL, MAL, dz(r), round(V)))
    if kind == "kapsel":
        r, h = R.randint(1, 4), R.randint(4, 12)
        V = PI * r * r * h + 4 / 3 * PI * r ** 3
        return mcq("Eine Kapsel besteht aus einem Zylinder (r = %d cm, h = %d cm) mit je einer Halbkugel an beiden Enden. Berechne ihr Volumen (auf eine Nachkommastelle)." % (r, h), L(V, "cm³"),
                   [L(PI * r * r * h + 2 / 3 * PI * r ** 3, "cm³"), L(PI * r * r * h + 8 / 3 * PI * r ** 3, "cm³"), L(PI * r * r * (h + 2 * r), "cm³")],
                   "Zwei Halbkugeln ergeben eine ganze Kugel: π r² h + 4/3 π r³ ≈ <b>%s</b>." % L(V, "cm³"))
    if kind == "hohl":
        ra, ri = R.choice([(5, 4), (10, 9), (6, 5), (12, 10), (8, 7)])
        V = 4 / 3 * PI * (ra ** 3 - ri ** 3)
        return mcq("Eine Hohlkugel hat außen den Radius %d cm und innen %d cm. Wie groß ist das Materialvolumen (auf eine Nachkommastelle)?" % (ra, ri), L(V, "cm³"),
                   [L(4 / 3 * PI * (ra - ri) ** 3, "cm³"), L(4 / 3 * PI * ra ** 3, "cm³"), L(4 * PI * (ra * ra - ri * ri), "cm³")], "V = 4/3 %s π %s (%d − %d) ≈ <b>%s</b>." % (MAL, MAL, ra ** 3, ri ** 3, L(V, "cm³")))
    a = R.choice([4, 6, 8, 10, 12])
    r = a / 2
    return mcq("Eine Kugel passt genau in einen Würfel mit der Kantenlänge %d cm. Wie viel Prozent des Würfels füllt sie aus (auf ganze Prozent)?" % a, "etwa 52 %",
               ["etwa 79 %", "etwa 67 %", "etwa 100 %"], "V<sub>Kugel</sub> = 4/3 %s π %s %s³ ≈ %s cm³, V<sub>Würfel</sub> = %d cm³. Anteil π : 6 ≈ <b>52 %%</b>." % (MAL, MAL, zr(r) if r != int(r) else int(r), zr(4 / 3 * PI * r ** 3), a ** 3)) if R.random() < 0.3 else None


def sache():
    kind = R.choice(["ball", "erde", "blase", "kugeln", "leder", "metall"])
    if kind == "ball":
        d = R.choice([22, 24, 21, 70])
        r = d / 2
        nm = "Fußball" if d in (22, 21) else ("Basketball" if d == 24 else "Gymnastikball")
        return mcq("Ein %s hat etwa %d cm Durchmesser. Wie viel Liter Luft enthält er (auf eine Nachkommastelle)?" % (nm, d), "%s l" % zr(4 / 3 * PI * r ** 3 / 1000),
                   ["%s l" % zr(4 / 3 * PI * d ** 3 / 1000), "%s l" % zr(4 * PI * r * r / 1000), "%s l" % zr(4 / 3 * PI * r ** 3 / 100)], "V = 4/3 %s π %s %s³ ≈ %s cm³ ≈ <b>%s l</b>." % (MAL, MAL, zr(r) if r != int(r) else int(r), num(round(4 / 3 * PI * r ** 3)), zr(4 / 3 * PI * r ** 3 / 1000)))
    if kind == "erde":
        r = 6370
        return mcq("Die Erde ist ungefähr eine Kugel mit dem Radius 6370 km. Wie groß ist ihre Oberfläche ungefähr?", "etwa 510 Millionen km²",
                   ["etwa 127 Millionen km²", "etwa 1 Billion km²", "etwa 80 000 km²"], "O = 4 %s π %s 6370² ≈ 509 900 000 km² ≈ <b>510 Millionen km²</b>." % (MAL, MAL))
    if kind == "blase":
        d = R.choice([4, 6, 8, 10, 20])
        return mcq("Eine Seifenblase hat %d cm Durchmesser. Wie groß ist ihre Oberfläche (auf eine Nachkommastelle)?" % d, L(4 * PI * (d / 2) ** 2, "cm²"),
                   [L(4 * PI * d * d, "cm²"), L(PI * (d / 2) ** 2, "cm²"), L(4 / 3 * PI * (d / 2) ** 3, "cm²")], "r = %d cm. O = 4 %s π %s %d² ≈ <b>%s</b>." % (d // 2, MAL, MAL, d // 2, L(4 * PI * (d / 2) ** 2, "cm²")))
    if kind == "kugeln":
        r, R2 = R.choice([(1, 2), (1, 3), (2, 4), (1, 4), (1, 5)])
        n = (R2 // r) ** 3
        return mcq("Aus einer Metallkugel mit r = %d cm werden kleine Kugeln mit r = %d cm gegossen. Wie viele kleine Kugeln entstehen?" % (R2, r), str(n), [str(R2 // r), str((R2 // r) ** 2), str(n * 2)],
                   "Volumen wächst mit r³: (%d : %d)³ = <b>%d</b>." % (R2, r, n))
    if kind == "leder":
        r = R.choice([10, 11, 12])
        return mcq("Wie viel Leder braucht man ungefähr für einen Ball mit r = %d cm (ohne Verschnitt, auf ganze cm²)?" % r, "etwa %s cm²" % num(round(4 * PI * r * r)),
                   ["etwa %s cm²" % num(round(4 / 3 * PI * r ** 3)), "etwa %s cm²" % num(round(PI * r * r)), "etwa %s cm²" % num(round(2 * PI * r * r))], "O = 4 %s π %s %d² ≈ <b>%s cm²</b>." % (MAL, MAL, r, num(round(4 * PI * r * r))))
    r = R.choice([1, 2, 3])
    rho = R.choice([(Fr(79, 10), "Stahl"), (Fr(113, 10), "Blei"), (Fr(27, 10), "Aluminium")])
    V = 4 / 3 * PI * r ** 3
    m = V * float(rho[0])
    return mcq("Eine Kugel aus %s (1 cm³ wiegt %s g) hat den Radius %d cm. Wie schwer ist sie (auf ganze g)?" % (rho[1], dz(rho[0]), r), "etwa %d g" % round(m),
               ["etwa %d g" % round(V), "etwa %d g" % round(4 * PI * r * r * float(rho[0])), "etwa %d g" % round(m / 2)], "V ≈ %s cm³, mal %s g ≈ <b>%d g</b>." % (zr(V), dz(rho[0]), round(m)))


def main():
    seen = set()
    sets = [
        ("Volumen der Kugel", mix(R, seen, [(volumen, 20)])),
        ("Oberfläche der Kugel", mix(R, seen, [(oberflaeche, 20)])),
        ("Radius und Veränderungen", mix(R, seen, [(rueck, 20)])),
        ("Zusammengesetzte Körper", mix(R, seen, [(zusammen, 20)])),
        ("Sachaufgaben", mix(R, seen, [(sache, 20)])),
    ]
    body = lesson(
        ["<b>Volumen</b> der Kugel: V = 4/3 %s π %s r³." % (MAL, MAL),
         "<b>Oberfläche</b> der Kugel: O = 4 %s π %s r² (so groß wie vier Kreise mit demselben Radius)." % (MAL, MAL),
         "Ist der Durchmesser gegeben, zuerst halbieren. Verdoppelt man r, wird O 4-mal und V 8-mal so groß.",
         "Zusammengesetzte Körper: in Teilkörper zerlegen, Volumen addieren. Bei Oberflächen nur die außen liegenden Flächen zählen."],
        [example("r = 3 cm", ["V = 4/3 %s π %s 27 ≈ 113,1 cm³" % (MAL, MAL), "O = 4 %s π %s 9 ≈ 113,1 cm²" % (MAL, MAL)], "V ≈ 113,1 cm³, O ≈ 113,1 cm²"),
         example("Halbkugel r = 6 cm", ["V = 2/3 %s π %s 216" % (MAL, MAL)], "≈ 452,4 cm³")],
        [["V = 4/3 %s π %s r²" % (MAL, MAL), "Beim Volumen r³"],
         ["d = 10 cm: V = 4/3 %s π %s 10³" % (MAL, MAL), "Erst r = 5 cm bilden"],
         ["r verdoppelt ⇒ V verdoppelt", "V wird 2³ = 8-mal so groß"]])
    faq = [
        {"q": "Wie berechne ich das Volumen einer Kugel?", "a": "V = 4/3 · π · r³."},
        {"q": "Wie berechne ich die Oberfläche einer Kugel?", "a": "O = 4 · π · r²."},
        {"q": "Wie finde ich den Radius aus dem Volumen?", "a": "r³ = V : (4/3 · π) ausrechnen und dann die dritte Wurzel ziehen."},
        {"q": "Was passiert, wenn der Radius doppelt so groß wird?", "a": "Die Oberfläche wird 4-mal, das Volumen 8-mal so groß."},
    ]
    make_unit(R, "kugel", "G",
              "Die Schülerinnen und Schüler berechnen Volumen und Oberfläche von Kugeln und Halbkugeln, bestimmen Radien, beschreiben Veränderungen bei Streckung und berechnen zusammengesetzte Körper (Zusammenfassung).",
              "Kugel: Volumen und Oberfläche",
              "Kugel Volumen und Oberfläche Klasse 9 – zusammengesetzte Körper, Arbeitsblätter",
              "Kugel",
              "Kugel für Klasse 9: Volumen V = 4/3 · π · r³, Oberfläche O = 4 · π · r², Halbkugel, Radius bestimmen, zusammengesetzte Körper und Sachaufgaben. 100 Aufgaben mit Lösungen, kostenlos.",
              "V = 4/3 · π · r³",
              "O = 4 · π · r²",
              body, faq, sets, 13, grade="klasse-9")


if __name__ == "__main__":
    main()
