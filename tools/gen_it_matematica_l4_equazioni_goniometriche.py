# -*- coding: utf-8 -*-
"""
Italia Matematica quarta liceo: Equazioni e disequazioni goniometriche (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l4_equazioni_goniometriche.py
Equazioni elementari sen x = a, cos x = a, tg x = a (soluzioni generali con 2kπ e kπ), soluzioni in [0; 2π[,
equazioni impossibili (|a| > 1), equazioni riconducibili a elementari (sen 2x, sen x = cos x), di secondo grado in sen x o cos x,
disequazioni elementari in [0; 2π[.
Errori: dimenticare la seconda famiglia di soluzioni del seno, periodo π per seno e coseno, sen x = 2 risolvibile.
"""
import math
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, FR, pif

R = random.Random(72406)
G = "quarta-liceo"
R3, R2 = "√3", "√2"
VAL = {"sen": [(Fr(0), "0"), (Fr(1, 6), FR(1, 2)), (Fr(1, 4), FR(R2, 2)), (Fr(1, 3), FR(R3, 2)), (Fr(1, 2), "1")],
       "cos": [(Fr(1, 2), "0"), (Fr(1, 3), FR(1, 2)), (Fr(1, 4), FR(R2, 2)), (Fr(1, 6), FR(R3, 2)), (Fr(0), "1")],
       "tg": [(Fr(0), "0"), (Fr(1, 6), FR(R3, 3)), (Fr(1, 4), "1"), (Fr(1, 3), R3)]}


def kp(t, per):
    return "%s + %s" % (pif(t), "2kπ" if per == 2 else "kπ") if t else ("2kπ" if per == 2 else "kπ")


def sol_gen(fn, a0, neg):
    """soluzioni generali di fn x = ±valore con angolo di riferimento a0 (in π)"""
    if fn == "sen":
        t1 = -a0 if neg else a0
        t2 = 1 + a0 if neg else 1 - a0
        if t1 % 2 == t2 % 2:
            return [kp(t1 % 2 if t1 >= 0 else t1, 2)]
        return [kp(t1, 2), kp(t2, 2)]
    if fn == "cos":
        t = 1 - a0 if neg else a0
        if t == 0:
            return [kp(0, 2)]
        if t == 1:
            return [kp(1, 2)]
        return ["±%s + 2kπ" % pif(t)]
    return [kp(-a0 if neg else a0, 1)]


def s1_elem():
    fn = R.choice(["sen", "cos", "tg"])
    a0, val = R.choice(VAL[fn][1:])
    neg = R.random() < 0.4
    v = ("−" + val) if neg else val
    sols = sol_gen(fn, a0, neg)
    ans = " ∨ ".join("x = %s" % s for s in sols)
    # distrattori
    w = []
    if fn == "sen":
        w.append("x = %s" % kp(-a0 if neg else a0, 2))
        w.append("x = %s" % kp(-a0 if neg else a0, 1))
        w.append(" ∨ ".join("x = %s" % s for s in sol_gen("cos", a0, neg)))
    elif fn == "cos":
        w.append("x = %s" % kp(1 - a0 if neg else a0, 2))
        w.append(" ∨ ".join("x = %s" % s for s in sol_gen("sen", a0, neg)))
        if (1 - a0 if neg else a0) != 0:
            w.append("x = ±%s + kπ" % pif(1 - a0 if neg else a0))
    else:
        w.append("x = %s" % kp(-a0 if neg else a0, 2))
        w.append("x = %s" % kp(a0 if neg else -a0, 1))
        w.append("x = %s" % kp(Fr(1, 2) - a0, 1))
    ALT = {FR(1, 2): ("2", "1"), FR(R2, 2): ("2", R2), FR(R3, 2): ("2", R3), FR(R3, 3): ("3", R3), "1": ("", "1"), R3: ("", R3)}
    if R.random() < 0.5 and val in ALT:
        c, r = ALT[val]
        eq = "%s%s x %s %s = 0" % (c, fn, "+" if neg else "−", r)
    else:
        eq = "%s x = %s" % (fn, v)
    w += ["x = %s" % kp(Fr(1, 2) - a0 if fn != "tg" else a0 + Fr(1, 2), 2), "x = %s" % kp(a0 + 1, 2 if fn != "tg" else 1)]
    return M("Risolvi: %s" % eq, ans, [x for x in W(*w) if x != ans],
             "L’angolo di riferimento è %s. %s: <b>%s</b>." % (pif(a0), {"sen": "Il seno ha due soluzioni in un giro (x e π − x), periodo 2π", "cos": "Il coseno ha soluzioni opposte (±x), periodo 2π", "tg": "La tangente ha periodo π"}[fn], ans))


def in02(fn, a0, neg):
    out = []
    for k in range(0, 24):
        t = Fr(k, 12)
        v = {"sen": math.sin, "cos": math.cos, "tg": math.tan}[fn](float(t) * math.pi)
        tv = {"sen": math.sin, "cos": math.cos, "tg": math.tan}[fn](float(a0) * math.pi) * (-1 if neg else 1)
        if fn == "tg" and (k % 12 == 6):
            continue
        if abs(v - tv) < 1e-9:
            out.append(t)
    return out


def s2_int():
    fn = R.choice(["sen", "cos", "tg"])
    a0, val = R.choice(VAL[fn])
    neg = R.random() < 0.4 and val != "0"
    sols = in02(fn, a0, neg)
    ans = "; ".join(pif(t) for t in sols)
    v = ("−" + val) if neg else val
    alt = in02("cos" if fn == "sen" else "sen", a0, neg)
    w = ["; ".join(pif(t) for t in alt) if alt and alt != sols else pif(sols[0] + Fr(1, 2) if sols else 1), pif(sols[0]) if len(sols) > 1 else "; ".join(pif(t) for t in sorted(set(sols + [(sols[0] + Fr(1, 2)) % 2]))) , "; ".join(pif(t) for t in sorted((t + 1) % 2 for t in sols)) if sorted((t + 1) % 2 for t in sols) != sols else pif(Fr(1, 2))]
    ALT = {FR(1, 2): ("2", "1"), FR(R2, 2): ("2", R2), FR(R3, 2): ("2", R3), FR(R3, 3): ("3", R3), "1": ("", "1"), R3: ("", R3), "0": ("", "0")}
    if R.random() < 0.5 and val in ALT and val != "0":
        c, r = ALT[val]
        eq = "%s%s x %s %s = 0" % (c, fn, "+" if neg else "−", r)
    else:
        eq = "%s x = %s" % (fn, v)
    return M("Trova le soluzioni di %s nell’intervallo [0; 2π[." % eq, ans, [x for x in W(*w) if x != ans],
             "Sulla circonferenza goniometrica i punti con %s uguale a %s sono: <b>%s</b>." % (fn, v, ans))


def s2_imp():
    fn = R.choice(["sen", "cos"])
    v = R.choice(["2", "−3", FR(3, 2), "−" + FR(5, 4), "√5", "π"])
    return M("Quante soluzioni ha l’equazione %s x = %s?" % (fn, v), "nessuna", ["infinite", "due in ogni giro", "una sola"],
             "%s x è sempre compreso tra −1 e 1, e %s è fuori da questo intervallo: <b>nessuna</b> soluzione." % (fn, v))


def s3_ricond():
    k = R.choice(["dop", "sc", "sen2"])
    if k == "sc":
        ans = "x = π/4 + kπ"
        return M("Risolvi: sen x = cos x", ans, ["x = π/4 + 2kπ", "x = ±π/4 + 2kπ", "x = kπ"],
                 "cos x = 0 non dà soluzioni; divido per cos x: tg x = 1 → <b>x = π/4 + kπ</b>.")
    if k == "sen2":
        n = R.choice([2, 3, 4])
        ans = "x = kπ/%d" % n
        return M("Risolvi: sen %dx = 0" % n, ans, ["x = kπ", "x = 2kπ", "x = %dkπ" % n],
                 "sen t = 0 per t = kπ: %dx = kπ → <b>x = kπ/%d</b>." % (n, n))
    n = R.choice([2, 3])
    fn = R.choice(["sen", "cos"])
    a0, val = R.choice(VAL[fn][1:4])
    sols = sol_gen(fn, a0, False)
    ans = " ∨ ".join("x = %s" % s.replace("2kπ", "kπ" if n == 2 else "2kπ/3").replace(pif(a0) if a0 else "§", pif(a0 / n) if a0 else "§").replace(pif(1 - a0) if fn == "sen" else "§", pif((1 - a0) / n) if fn == "sen" else "§") for s in sols)
    # ricalcolo pulito
    parts = []
    per = Fr(2, n)
    per_t = "kπ" if per == 1 else ("2kπ/3" if n == 3 else "kπ")
    if fn == "sen":
        parts = ["x = %s + %s" % (pif(a0 / n), per_t), "x = %s + %s" % (pif((1 - a0) / n), per_t)]
    else:
        parts = ["x = ±%s + %s" % (pif(a0 / n), per_t)]
    ans = " ∨ ".join(parts)
    w = [" ∨ ".join(p.replace(per_t, "2kπ") for p in parts), " ∨ ".join(p.replace(pif(a0 / n), pif(a0)) for p in parts), " ∨ ".join(p.replace(per_t, "kπ/%d" % n) for p in parts) if per_t != "kπ/%d" % n else "x = kπ"]
    return M("Risolvi: %s %dx = %s" % (fn, n, val), ans, [x for x in W(*w) if x != ans],
             "Pongo t = %dx e risolvo %s t = %s, poi divido per %d (anche il periodo): <b>%s</b>." % (n, fn, val, n, ans))


def s4_quad():
    k = R.choice([1, 2, 3])
    if k == 1:
        q, ans = "2 sen²x − sen x − 1 = 0", "x = π/2 + 2kπ ∨ x = −π/6 + 2kπ ∨ x = 7π/6 + 2kπ"
        e = "sen x = t: 2t² − t − 1 = 0 → t = 1 ∨ t = −1/2."
        w = ["x = π/2 + 2kπ", "x = π/2 + 2kπ ∨ x = π/6 + 2kπ ∨ x = 5π/6 + 2kπ", "x = −π/6 + 2kπ ∨ x = 7π/6 + 2kπ"]
    elif k == 2:
        q, ans = "2 cos²x − 1 = 0", "x = π/4 + kπ/2"
        e = "cos²x = 1/2 → cos x = ±√2/2: gli angoli π/4, 3π/4, 5π/4, 7π/4 distano π/2."
        w = ["x = ±π/4 + 2kπ", "x = π/4 + kπ", "x = π/4 + 2kπ"]
    else:
        q, ans = "sen²x − sen x = 0", "x = kπ ∨ x = π/2 + 2kπ"
        e = "sen x (sen x − 1) = 0 → sen x = 0 ∨ sen x = 1."
        w = ["x = kπ", "x = π/2 + 2kπ", "x = 2kπ ∨ x = π/2 + 2kπ"]
    return M("Risolvi: %s" % q, ans, w, "%s <b>%s</b>." % (e, ans))


DIS = [("sen x &gt; 1/2", "π/6 &lt; x &lt; 5π/6", ["0 ≤ x &lt; π/6 ∨ 5π/6 &lt; x &lt; 2π", "π/6 &lt; x &lt; π/3", "π/3 &lt; x &lt; 2π/3"]),
       ("cos x ≤ 0", "π/2 ≤ x ≤ 3π/2", ["0 ≤ x ≤ π/2 ∨ 3π/2 ≤ x &lt; 2π", "π ≤ x &lt; 2π", "0 ≤ x ≤ π"]),
       ("sen x &lt; 0", "π &lt; x &lt; 2π", ["0 &lt; x &lt; π", "π/2 &lt; x &lt; 3π/2", "3π/2 &lt; x &lt; 2π"]),
       ("cos x &gt; 1/2", "0 ≤ x &lt; π/3 ∨ 5π/3 &lt; x &lt; 2π", ["π/3 &lt; x &lt; 5π/3", "0 ≤ x &lt; π/6 ∨ 11π/6 &lt; x &lt; 2π", "π/6 &lt; x &lt; 5π/6"]),
       ("tg x ≥ 1", "π/4 ≤ x &lt; π/2 ∨ 5π/4 ≤ x &lt; 3π/2", ["π/4 ≤ x &lt; π/2", "π/4 ≤ x ≤ 5π/4", "0 ≤ x ≤ π/4 ∨ π ≤ x ≤ 5π/4"]),
       ("sen x ≥ −1/2", "0 ≤ x ≤ 7π/6 ∨ 11π/6 ≤ x &lt; 2π", ["7π/6 ≤ x ≤ 11π/6", "0 ≤ x ≤ 5π/6", "π/6 ≤ x ≤ 5π/6"]),
       ("cos x &lt; −√2/2", "3π/4 &lt; x &lt; 5π/4", ["π/4 &lt; x &lt; 7π/4", "0 ≤ x &lt; 3π/4 ∨ 5π/4 &lt; x &lt; 2π", "5π/4 &lt; x &lt; 7π/4"]),
       ("2 sen x − √3 ≥ 0", "π/3 ≤ x ≤ 2π/3", ["π/6 ≤ x ≤ 5π/6", "0 ≤ x ≤ π/3", "π/3 ≤ x ≤ 5π/3"]),
       ("tg x &lt; 0", "π/2 &lt; x &lt; π ∨ 3π/2 &lt; x &lt; 2π", ["0 &lt; x &lt; π/2 ∨ π &lt; x &lt; 3π/2", "π &lt; x &lt; 2π", "π/2 &lt; x &lt; 3π/2"]),
       ("cos x ≥ √3/2", "0 ≤ x ≤ π/6 ∨ 11π/6 ≤ x &lt; 2π", ["π/6 ≤ x ≤ 11π/6", "0 ≤ x ≤ π/3", "π/6 ≤ x ≤ 5π/6"])]


def s5_dis():
    q, a, w = R.choice(DIS)
    return M("Risolvi nell’intervallo [0; 2π[: %s" % q, a, w, "Si trovano sulla circonferenza goniometrica gli angoli che rendono vera la disuguaglianza: <b>%s</b>." % a)


def main():
    seen = set()
    sets = [
        ("Equazioni elementari", mix(R, seen, [(s1_elem, 20)])),
        ("Soluzioni in un giro", mix(R, seen, [(s2_int, 14), (s2_imp, 6)])),
        ("Equazioni riconducibili", mix(R, seen, [(s3_ricond, 12), (s1_elem, 8)])),
        ("Equazioni di secondo grado e riepilogo", mix(R, seen, [(s4_quad, 3), (s2_int, 8), (s2_imp, 4), (s3_ricond, 3), (s1_elem, 2)])),
        ("Disequazioni goniometriche", mix(R, seen, [(s5_dis, 10), (s2_int, 10)])),
    ]
    body = L(["Le equazioni goniometriche hanno di solito <b>infinite soluzioni</b>, perché le funzioni sono periodiche: si trovano le soluzioni in un giro e si aggiunge il periodo (2kπ per seno e coseno, kπ per la tangente).",
              "<b>sen x = a</b> (|a| ≤ 1): x = α + 2kπ ∨ x = π − α + 2kπ. <b>cos x = a</b>: x = ±α + 2kπ. <b>tg x = a</b>: x = α + kπ (per ogni a reale).",
              "Se |a| &gt; 1, sen x = a e cos x = a sono impossibili. Le equazioni come 2 sen²x − sen x − 1 = 0 si risolvono ponendo t = sen x.",
              "Le <b>disequazioni</b> si risolvono sulla circonferenza goniometrica, cercando gli archi in cui la disuguaglianza è vera."],
             [("sen x = √3/2", ["Angolo di riferimento π/3", "x = π/3 e x = π − π/3"], "x = π/3 + 2kπ ∨ x = 2π/3 + 2kπ"),
              ("cos x &lt; 0 in [0; 2π[", ["Ascissa negativa: II e III quadrante"], "π/2 &lt; x &lt; 3π/2")],
             [["Solo x = π/6 + 2kπ per sen x = 1/2", "C’è anche x = 5π/6 + 2kπ (seno uguale in x e π − x)."],
              ["Periodo π per il coseno", "Seno e coseno hanno periodo 2π; solo la tangente ha periodo π."],
              ["Risolvere sen x = 2", "Il seno non supera 1: l’equazione è impossibile."]])
    faq = [("Perché nelle soluzioni compare k?", "k è un numero intero qualsiasi: aggiungendo un multiplo del periodo si ritorna allo stesso punto della circonferenza goniometrica."),
           ("Come si risolve sen 2x = 1/2?", "Si pone t = 2x: t = π/6 + 2kπ ∨ t = 5π/6 + 2kπ. Poi si divide tutto per 2, anche il periodo: x = π/12 + kπ ∨ x = 5π/12 + kπ.")]
    unit(G, R, "equazioni-goniometriche", "F",
         "Equazioni e disequazioni goniometriche elementari e riconducibili a elementari",
         "Equazioni e disequazioni goniometriche", "Equazioni goniometriche",
         "Schede di matematica per la quarta liceo su equazioni e disequazioni goniometriche: equazioni elementari in seno, coseno e tangente, soluzioni in [0; 2π[, equazioni impossibili, riconducibili e di secondo grado, disequazioni. 100 esercizi con soluzioni.",
         "sen x = a: x = α + 2kπ ∨ x = π − α + 2kπ", "cos x = a: x = ±α + 2kπ; tg x = a: x = α + kπ.",
         body, faq, sets, 6)


if __name__ == "__main__":
    main()
