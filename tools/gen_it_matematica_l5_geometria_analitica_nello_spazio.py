# -*- coding: utf-8 -*-
"""
Italia Matematica quinta liceo: Geometria analitica nello spazio (Geometria)
  python3 tools/gen_it_matematica_l5_geometria_analitica_nello_spazio.py
Coordinate nello spazio: distanza tra due punti, punto medio, vettori e prodotto scalare (perpendicolarità e parallelismo),
equazione del piano (vettore normale, per un punto), piani paralleli e perpendicolari, distanza punto-piano,
retta in forma parametrica, superficie sferica (centro e raggio).
Errori: distanza senza la terza coordinata, normale del piano letta dal termine noto, centro della sfera senza il segno meno.
"""
import math
import random
import it_liceo
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P, show, simp_root

R = random.Random(72501)
_M = M


def M(q, a, w, e):
    return _M(q, a, w, e.replace("+ −", "− "))
G = "quinta-liceo"


def pt(p, n=""):
    return "%s(%s)" % (n, "; ".join(fq(x) for x in p))


def vec(p):
    return "(%s)" % "; ".join(fq(x) for x in p)


def rt(n):
    k, m = simp_root(int(n))
    return str(k) if m == 1 else ("" if k == 1 else str(k)) + "√" + str(m)


def plane(a, b, c, dd):
    return "%s = 0" % show(P([(a, {"x": 1}), (b, {"y": 1}), (c, {"z": 1}), (dd, {})]))


def s1_dist():
    A = [R.randint(-5, 5) for _ in range(3)]
    dv = R.choice([(1, 2, 2), (2, 3, 6), (1, 4, 8), (2, 6, 9), (4, 4, 7), (2, 1, 2)]) if R.random() < 0.6 else (R.randint(-4, 4), R.randint(-4, 4), R.randint(-4, 4))
    dv = [x * R.choice([1, -1]) for x in dv]
    B = [a + b for a, b in zip(A, dv)]
    n = sum(x * x for x in dv)
    if n == 0:
        return None
    k = R.choice(["d", "m"])
    if k == "d":
        v = rt(n)
        return M("Calcola la distanza tra %s e %s." % (pt(A, "A"), pt(B, "B")), v, [x for x in W(rt(dv[0] ** 2 + dv[1] ** 2) if dv[0] ** 2 + dv[1] ** 2 else "0", str(sum(abs(x) for x in dv)), str(n), rt(n + 1)) if x != v],
                 "AB = √[(Δx)² + (Δy)² + (Δz)²] = √(%s) = <b>%s</b>." % (" + ".join(str(x * x) for x in dv), v))
    Mm = [Fr(a + b, 2) for a, b in zip(A, B)]
    return M("Trova il punto medio di AB con %s e %s." % (pt(A, "A"), pt(B, "B")), pt(Mm, "M"), [pt([Fr(b - a, 2) for a, b in zip(A, B)], "M"), pt([a + b for a, b in zip(A, B)], "M"), pt([Mm[0], Mm[1], -Mm[2]] if Mm[2] else [Mm[0], Mm[1], 1], "M")],
             "Media delle coordinate: <b>%s</b>." % pt(Mm, "M"))


def s2_scal():
    u = [nz(R, -4, 4) for _ in range(3)]
    v = [R.randint(-4, 4) for _ in range(3)]
    k = R.choice(["prod", "perp"])
    s = sum(a * b for a, b in zip(u, v))
    if k == "prod":
        return M("Calcola il prodotto scalare dei vettori u = %s e v = %s." % (vec(u), vec(v)), fq(s), [fq(x) for x in W(sum(abs(a * b) for a, b in zip(u, v)), -s if s else 1, u[0] * v[0] + u[1] * v[1], s + 1) if x != s],
                     "u · v = u<sub>x</sub>v<sub>x</sub> + u<sub>y</sub>v<sub>y</sub> + u<sub>z</sub>v<sub>z</sub> = %s = <b>%s</b>." % (" + ".join("(%s)" % fq(a * b) if a * b < 0 else fq(a * b) for a, b in zip(u, v)), fq(s)))
    # k tale che u ⟂ (v0, v1, k)
    if u[2] == 0:
        return None
    kk = Fr(-(u[0] * v[0] + u[1] * v[1]), u[2])
    return M("Per quale valore di k i vettori u = %s e v = (%s; %s; k) sono perpendicolari?" % (vec(u), fq(v[0]), fq(v[1])), "k = %s" % fq(kk), ["k = %s" % fq(x) for x in W(-kk if kk else 1, Fr(u[2], -(u[0] * v[0] + u[1] * v[1])) if (u[0] * v[0] + u[1] * v[1]) else 2, kk + 1, kk - 1, -(u[0] * v[0] + u[1] * v[1])) if x != kk],
             "Perpendicolari se u · v = 0: %s + %s · k = 0 → <b>k = %s</b>." % (fq(u[0] * v[0] + u[1] * v[1]), fq(u[2]), fq(kk)))


def s3_piano():
    n = [nz(R, -4, 4) for _ in range(3)]
    p0 = [R.randint(-3, 3) for _ in range(3)]
    dd = -sum(a * b for a, b in zip(n, p0))
    k = R.choice(["scrivi", "app", "norm"])
    if k == "scrivi":
        ans = plane(*n, dd)
        return M("Scrivi l’equazione del piano passante per %s e perpendicolare al vettore n = %s." % (pt(p0, "P"), vec(n)), ans, [x for x in W(plane(*n, -dd) if dd else plane(*n, 1), plane(*p0, -sum(a * b for a, b in zip(n, p0))) if any(p0) else plane(1, 1, 1, 0), plane(*n, dd + 1)) if x != ans],
                     "a(x − x<sub>0</sub>) + b(y − y<sub>0</sub>) + c(z − z<sub>0</sub>) = 0 con (a; b; c) = n: <b>%s</b>." % ans)
    if k == "norm":
        return M("Qual è un vettore normale (perpendicolare) al piano %s?" % plane(*n, dd), vec(n), [vec([n[1], n[0], n[2]]) if n[0] != n[1] else vec([n[0], n[1], -n[2]]), vec([n[0], n[1], dd]) if dd != n[2] else vec([-n[0], n[1], n[2]]), vec([n[2], n[1], n[0]]) if n[0] != n[2] else vec([n[0], -n[1], n[2]])],
                     "I coefficienti di x, y, z formano un vettore normale: <b>%s</b>." % vec(n))
    q = [x + R.choice([0, 0, 1, -1]) for x in p0]
    ok = sum(a * b for a, b in zip(n, q)) + dd == 0
    return M("Il punto %s appartiene al piano %s?" % (pt(q, "Q"), plane(*n, dd)), "sì" if ok else "no", ["no" if ok else "sì", "solo se z = 0", "non si può stabilire"],
             "Sostituisco le coordinate: %s = %s, quindi <b>%s</b>." % (" + ".join("%s · %s" % (fq(a), "(%s)" % fq(b) if b < 0 else fq(b)) for a, b in zip(n, q)) + (" %s %s" % ("+" if dd >= 0 else "−", fq(abs(dd)))), fq(sum(a * b for a, b in zip(n, q)) + dd), "sì" if ok else "no"))


def s3_pos():
    n1 = [nz(R, -3, 3) for _ in range(3)]
    k = R.choice(["par", "perp", "inc"])
    if k == "par":
        m = R.choice([2, -1, 3])
        n2 = [m * x for x in n1]
        ans = "paralleli"
    elif k == "perp":
        a, b = nz(R, -3, 3), nz(R, -3, 3)
        if n1[2] == 0:
            return None
        c = Fr(-(n1[0] * a + n1[1] * b), n1[2])
        if c.denominator != 1:
            return None
        n2 = [a, b, int(c)]
        ans = "perpendicolari"
    else:
        n2 = [nz(R, -3, 3) for _ in range(3)]
        dot = sum(x * y for x, y in zip(n1, n2))
        cross = [n1[1] * n2[2] - n1[2] * n2[1], n1[2] * n2[0] - n1[0] * n2[2], n1[0] * n2[1] - n1[1] * n2[0]]
        if dot == 0 or not any(cross):
            return None
        ans = "incidenti ma non perpendicolari"
    d1, d2 = R.randint(-5, 5), R.randint(-5, 5)
    if k == "par" and d2 == m * d1:
        d2 += 1
    return M("Come sono i piani %s e %s?" % (plane(*n1, d1), plane(*n2, d2)), ans, [x for x in ["paralleli", "perpendicolari", "incidenti ma non perpendicolari", "coincidenti"] if x != ans],
             "Confronto i vettori normali %s e %s: %s → <b>%s</b>." % (vec(n1), vec(n2), "sono proporzionali" if k == "par" else "il prodotto scalare è 0" if k == "perp" else "non sono proporzionali e il prodotto scalare non è 0", ans))


def s4_distp():
    n = R.choice([(1, 2, 2), (2, 1, 2), (2, 3, 6), (1, 4, 8), (4, 4, 7), (2, 6, 9)])
    n = [x * R.choice([1, -1]) for x in n]
    N = int(math.isqrt(sum(x * x for x in n)))
    p = [R.randint(-4, 4) for _ in range(3)]
    dd = R.randint(-10, 10)
    num = abs(sum(a * b for a, b in zip(n, p)) + dd)
    if num == 0:
        return None
    v = Fr(num, N)
    return M("Calcola la distanza del punto %s dal piano %s." % (pt(p, "P"), plane(*n, dd)), fq(v), [fq(x) for x in W(num, Fr(num, N * N), Fr(abs(sum(a * b for a, b in zip(n, p)) - dd), N), v + 1) if x != v],
             "d = |ax<sub>0</sub> + by<sub>0</sub> + cz<sub>0</sub> + d| / √(a² + b² + c²) = %d / %d = <b>%s</b>." % (num, N, fq(v)))


def s5_retta():
    p0 = [R.randint(-4, 4) for _ in range(3)]
    v = [nz(R, -3, 3) for _ in range(3)]
    t = nz(R, -3, 3)
    k = R.choice(["punto", "dir"])
    eqs = "<span class='sys'>%s</span>" % "<br>".join("%s = %s" % (c, show(P([(b, {"t": 1}), (a, {})]))) for c, a, b in zip("xyz", p0, v))
    if k == "punto":
        q = [a + t * b for a, b in zip(p0, v)]
        return M("Data la retta %s trova il punto che corrisponde a t = %s." % (eqs, fq(t)), pt(q, "Q"), [pt([a - t * b for a, b in zip(p0, v)], "Q"), pt([b * t for b in v], "Q"), pt([a + b for a, b in zip(p0, v)], "Q") if t != 1 else pt(p0, "Q")],
                     "Sostituisco t = %s: <b>%s</b>." % (fq(t), pt(q, "Q")))
    return M("Qual è un vettore direzione della retta %s?" % eqs, vec(v), [vec(p0) if p0 != v else vec([x + 1 for x in v]), vec([v[1], v[0], v[2]]) if v[0] != v[1] else vec([v[0], v[1], -v[2]]), vec([a + b for a, b in zip(p0, v)])],
             "I coefficienti di t danno la direzione: <b>%s</b>." % vec(v))


def s5_sfera():
    c = [R.randint(-4, 4) for _ in range(3)]
    r2 = R.choice([1, 4, 9, 16, 25, 2, 5, 3])
    dd = sum(x * x for x in c) - r2
    eq = "%s = 0" % show(P([(1, {"x": 2}), (1, {"y": 2}), (1, {"z": 2}), (-2 * c[0], {"x": 1}), (-2 * c[1], {"y": 1}), (-2 * c[2], {"z": 1}), (dd, {})]))
    k = R.choice(["C", "r"])
    if k == "C":
        return M("Qual è il centro della superficie sferica %s?" % eq, pt(c, "C"), [pt([-x for x in c], "C") if any(c) else pt([1, 0, 0], "C"), pt([2 * x for x in c], "C") if any(c) else pt([0, 1, 0], "C"), pt([c[1], c[0], c[2]], "C") if c[0] != c[1] else pt([c[0], c[1], c[2] + 1], "C")],
                     "C(−a/2; −b/2; −c/2) = <b>%s</b>." % pt(c, "C"))
    return M("Qual è il raggio della superficie sferica %s?" % eq, rt(r2), [x for x in W(str(r2) if r2 > 1 else "2", rt(abs(dd)) if dd else "0", rt(r2 + 2), rt(2 * r2)) if x != rt(r2)],
             "Centro %s; r = √(x<sub>C</sub>² + y<sub>C</sub>² + z<sub>C</sub>² − d) = √(%d − (%s)) = <b>%s</b>." % (pt(c, "C"), sum(x * x for x in c), fq(dd), rt(r2)))


def main():
    seen = set()
    sets = [
        ("Distanza e punto medio", mix(R, seen, [(s1_dist, 20)])),
        ("Vettori e prodotto scalare", mix(R, seen, [(s2_scal, 20)])),
        ("Equazione del piano", mix(R, seen, [(s3_piano, 14), (s3_pos, 6)])),
        ("Posizioni e distanze", mix(R, seen, [(s3_pos, 8), (s4_distp, 12)])),
        ("Rette e superfici sferiche", mix(R, seen, [(s5_retta, 10), (s5_sfera, 10)])),
    ]
    body = L(["Nello spazio un punto ha tre coordinate P(x; y; z). Distanza: AB = √[(x<sub>B</sub> − x<sub>A</sub>)² + (y<sub>B</sub> − y<sub>A</sub>)² + (z<sub>B</sub> − z<sub>A</sub>)²]; punto medio: media delle coordinate.",
              "Due vettori sono <b>perpendicolari</b> se il prodotto scalare u<sub>x</sub>v<sub>x</sub> + u<sub>y</sub>v<sub>y</sub> + u<sub>z</sub>v<sub>z</sub> è 0, <b>paralleli</b> se sono proporzionali.",
              "Un <b>piano</b> ha equazione ax + by + cz + d = 0: (a; b; c) è un vettore normale. Distanza di un punto dal piano: |ax<sub>0</sub> + by<sub>0</sub> + cz<sub>0</sub> + d| / √(a² + b² + c²).",
              "Una <b>retta</b> si scrive in forma parametrica: x = x<sub>0</sub> + lt, y = y<sub>0</sub> + mt, z = z<sub>0</sub> + nt, con direzione (l; m; n). La <b>superficie sferica</b> x² + y² + z² + ax + by + cz + d = 0 ha centro (−a/2; −b/2; −c/2)."],
             [("Piano per P(1; 0; 2) con n = (2; −1; 3)", ["2(x − 1) − (y − 0) + 3(z − 2) = 0"], "2x − y + 3z − 8 = 0"),
              ("Distanza di O dal piano x + 2y + 2z − 6 = 0", ["|−6| / √9"], "2")],
             [["Distanza con due coordinate", "Nello spazio servono tutte e tre le differenze."],
              ["Normale del piano con il termine noto", "Il vettore normale è (a; b; c), senza d."],
              ["Piani paralleli con normali perpendicolari", "Piani paralleli: normali proporzionali; piani perpendicolari: prodotto scalare delle normali uguale a 0."]])
    faq = [("Come si capisce se una retta è perpendicolare a un piano?", "Se il suo vettore direzione è parallelo (proporzionale) al vettore normale del piano."),
           ("Quante equazioni servono per una retta nello spazio?", "In forma parametrica tre, con un parametro t; in forma cartesiana due, come intersezione di due piani.")]
    unit(G, R, "geometria-analitica-nello-spazio", "G",
         "Coordinate cartesiane nello spazio: vettori, equazioni di piani, rette e sfere, distanze",
         "Geometria analitica nello spazio", "Geometria analitica nello spazio",
         "Schede di matematica per la quinta liceo sulla geometria analitica nello spazio: distanza e punto medio, vettori e prodotto scalare, equazione del piano, piani paralleli e perpendicolari, distanza punto-piano, rette parametriche, superficie sferica. 100 esercizi con soluzioni.",
         "Piano: ax + by + cz + d = 0, normale (a; b; c)", "Vettori perpendicolari: prodotto scalare nullo.",
         body, faq, sets, 1)


if __name__ == "__main__":
    main()
