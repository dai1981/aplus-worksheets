# -*- coding: utf-8 -*-
"""
Italia Matematica prima liceo: Relazioni e funzioni (Relazioni e funzioni)
  python3 tools/gen_it_matematica_l1_funzioni.py
Relazioni e funzioni, immagine e controimmagine, dominio (polinomi, frazioni, radici quadrate), zeri, funzioni lineari
y = mx + q e grafico, proporzionalità diretta e inversa, funzione valore assoluto, composizione.
Errori: un elemento con due immagini, f(−2) senza parentesi, dominio di 1/(x − 3) con x ≠ −3, confondere y = k/x e y = kx.
"""
import random
from fractions import Fraction as Fr
from it_liceo import M, L, unit, mix, table, W, fq, nz, P, show, par, poly, kosy, relabel

R = random.Random(72109)
G = "prima-liceo"
BLUE = "#1f6fd1"


def pairs(ps):
    return "{" + ", ".join("(%s; %s)" % (fq(a), fq(b)) for a, b in ps) + "}"


def s1_rel():
    xs = R.sample(range(-3, 6), 4)
    ok = R.random() < 0.5
    ps = [(x, R.randint(-4, 6)) for x in xs]
    if not ok:
        i = R.randrange(4)
        ps.append((xs[i], ps[i][1] + R.choice([1, 2, -1])))
    else:
        if R.random() < 0.5:
            ps.append((R.choice([x for x in range(-3, 7) if x not in xs]), ps[0][1]))
    R.shuffle(ps)
    ans = "sì" if ok else "no"
    return M("La relazione %s è una funzione (ogni primo elemento ha una sola immagine)?" % pairs(ps), ans,
             ["no" if ok else "sì", "sì, ma solo se è iniettiva", "non si può stabilire"],
             "È una funzione se nessun primo elemento compare con due immagini diverse%s: <b>%s</b>." % (" (due x diverse possono avere la stessa y)" if ok else "", ans))


def s1_val():
    a, b, c = nz(R, -3, 3), R.randint(-6, 6), R.randint(-9, 9)
    x = nz(R, -4, 4)
    f = poly([a, b, c])
    v = a * x * x + b * x + c
    w = [a * (-x * x) + b * x + c if x < 0 else -a * x * x + b * x + c, a * x * x - b * x + c, a * 2 * x + b * x + c]
    return M("Data f(x) = %s, calcola f(%s)." % (f, fq(x)), fq(v), [fq(t) for t in w if t != v] + [fq(-v)],
             "Sostituisco x = %s tra parentesi: %s = <b>%s</b>." % (fq(x), show(P([(a, {})])) + " · " + par(x) + "² " + ("+ " if b >= 0 else "− ") + "%d · %s " % (abs(b), par(x)) + ("+ " if c >= 0 else "− ") + str(abs(c)), fq(v)))


def s1_contro():
    m, q = nz(R, -5, 5), R.randint(-9, 9)
    x = nz(R, -6, 6)
    y = m * x + q
    w = [m * y + q, Fr(y + q, m), -x]
    return M("Data f(x) = %s, per quale x si ha f(x) = %s?" % (poly([m, q]), fq(y)), "x = %s" % fq(x), ["x = %s" % fq(t) for t in w if t != x],
             "Risolvo %s = %s: <b>x = %s</b> (è la controimmagine di %s)." % (poly([m, q]), fq(y), fq(x), fq(y)))


def s2_dom():
    a = nz(R, -9, 9)
    k = R.choice(["fraz", "rad", "poly", "fraz2", "rad2"])
    if k == "fraz":
        f = "<span class='fr'><span class='fn'>%d</span><span class='fd'>%s</span></span>" % (R.randint(1, 9), poly([1, -a]))
        ans, w = "x ≠ %s" % fq(a), ["x ≠ %s" % fq(-a), "ℝ", "x &gt; %s" % fq(a)]
        e = "Il denominatore non deve essere 0: x − %s ≠ 0 → <b>x ≠ %s</b>." % (par(a), fq(a)) if False else "Il denominatore non deve essere 0: %s ≠ 0 → <b>x ≠ %s</b>." % (poly([1, -a]), fq(a))
    elif k == "rad":
        f = "√(%s)" % poly([1, -a])
        ans, w = "x ≥ %s" % fq(a), ["x &gt; %s" % fq(a), "x ≥ %s" % fq(-a), "x ≠ %s" % fq(a)]
        e = "Sotto la radice quadrata ci vuole un numero non negativo: %s ≥ 0 → <b>x ≥ %s</b>." % (poly([1, -a]), fq(a))
    elif k == "rad2":
        c = R.choice([2, 3, 4])
        b = c * R.randint(-4, 4)
        f = "√(%s)" % poly([-c, b])
        z = Fr(b, c)
        ans, w = "x ≤ %s" % fq(z), ["x ≥ %s" % fq(z), "x ≤ %s" % fq(-z) if z else "x ≥ 1", "x &lt; %s" % fq(z)]
        e = "%s ≥ 0 → %s ≥ %s → dividendo per −%d il verso cambia: <b>x ≤ %s</b>." % (poly([-c, b]), show(P([(-c, {"x": 1})])), fq(-b), c, fq(z))
    elif k == "fraz2":
        b = R.randint(1, 6)
        f = "<span class='fr'><span class='fn'>x</span><span class='fd'>%s</span></span>" % poly([1, 0, -b * b])
        ans, w = "x ≠ −%d ∧ x ≠ %d" % (b, b), ["x ≠ %d" % b, "x ≠ %d" % (b * b), "ℝ"]
        e = "x² − %d ≠ 0 → x ≠ ±%d: <b>x ≠ −%d ∧ x ≠ %d</b>." % (b * b, b, b, b)
    else:
        f = poly([nz(R, -3, 3), R.randint(-5, 5), a])
        ans, w = "ℝ (tutti i numeri reali)", ["x ≠ 0", "x ≥ 0", "x ≠ %s" % fq(a)]
        e = "Un polinomio si calcola per ogni x: il dominio è <b>ℝ</b>."
    return M("Qual è il dominio della funzione y = %s?" % f, ans, w, e)


def s2_zero():
    m = nz(R, -6, 6)
    z = Fr(R.randint(-8, 8), R.choice([1, 1, 1, 2, 3]))
    q = -m * z
    if q.denominator != 1 or z == 0:
        return None
    w = [-z, Fr(q), Fr(m, q) if q else Fr(1), z + 1]
    return M("Qual è lo zero della funzione f(x) = %s?" % poly([m, q]), "x = %s" % fq(z), ["x = %s" % fq(t) for t in w if t != z],
             "Lo zero è dove f(x) = 0: %s = 0 → <b>x = %s</b> (il grafico taglia l’asse x lì)." % (poly([m, q]), fq(z)))


def s3_retta():
    m, q = Fr(nz(R, -3, 3)), Fr(R.randint(-3, 3))
    if R.random() < 0.3:
        m = Fr(R.choice([1, -1, 1, 3]), 2)
    x1 = R.choice([-2, 0, 2])
    x2 = x1 + R.choice([2, 4]) if m.denominator == 2 else x1 + R.randint(1, 3)
    y1, y2 = m * x1 + q, m * x2 + q
    if not (-5 <= y1 <= 5 and -5 <= y2 <= 5 and -5 <= x2 <= 5):
        return None
    fig = relabel(kosy([(m, q, BLUE, "")], [(x1, y1, "A"), (x2, y2, "B")], -5, 5, 22), "retta nel piano cartesiano")
    k = R.choice(["m", "q", "eq"])
    if k == "m":
        return M("%sQual è il coefficiente angolare m della retta passante per A(%s; %s) e B(%s; %s)?" % (fig, fq(x1), fq(y1), fq(x2), fq(y2)), "m = %s" % fq(m),
                 ["m = %s" % fq(t) for t in uniq([1 / m if m else None, -m, Fr(x2 - x1) / (y2 - y1) if y2 != y1 else None, q if q != m else m + 1]) if t is not None and t != m],
                 "m = (y<sub>B</sub> − y<sub>A</sub>)/(x<sub>B</sub> − x<sub>A</sub>) = (%s)/(%s) = <b>%s</b>." % (fq(y2 - y1), fq(x2 - x1), fq(m)))
    if k == "q":
        return M("%sLa retta passa per A(%s; %s) e B(%s; %s). In quale punto taglia l’asse y (ordinata all’origine q)?" % (fig, fq(x1), fq(y1), fq(x2), fq(y2)), "q = %s" % fq(q),
                 ["q = %s" % fq(t) for t in uniq([m, -q if q else Fr(1), y1 if y1 != q else y2, -m]) if t != q],
                 "Con m = %s: q = y<sub>A</sub> − m · x<sub>A</sub> = <b>%s</b>." % (fq(m), fq(q)))
    ans = "y = %s" % poly([m, q]) if q else "y = %s" % show(P([(m, {"x": 1})]))
    eq = lambda mm, qq: "y = %s" % (poly([mm, qq]) if qq else show(P([(mm, {"x": 1})])))
    return M("%sQual è l’equazione della retta passante per A(%s; %s) e B(%s; %s)?" % (fig, fq(x1), fq(y1), fq(x2), fq(y2)), ans,
             [eq(a, b) for a, b in uniq([(-m, q), (m, -q) if q else (m, 1), (1 / m, q), (q, m) if q else (m, 2)]) if eq(a, b) != ans],
             "m = %s e q = %s: <b>%s</b>." % (fq(m), fq(q), ans))


def uniq(xs):
    out = []
    for x in xs:
        if x is not None and x not in out:
            out.append(x)
    return out


def s3_prop():
    k = R.choice([2, 3, 4, 5, 6, 12])
    t = R.choice(["dir", "inv", "nessuna"])
    xs = sorted(R.sample([1, 2, 3, 4, 6, 8], 4))
    if t == "dir":
        ys = [k * x for x in xs]
        ans, e = "direttamente proporzionali (y = %dx)" % k, "Il rapporto y/x è costante (%d): <b>direttamente proporzionali</b>." % k
    elif t == "inv":
        k = R.choice([24, 48, 12, 72])
        xs = sorted(R.sample([x for x in (1, 2, 3, 4, 6, 8, 12) if k % x == 0], 4))
        ys = [k // x for x in xs]
        ans, e = "inversamente proporzionali (y = %d/x)" % k, "Il prodotto x · y è costante (%d): <b>inversamente proporzionali</b>." % k
    else:
        q = R.randint(1, 5)
        ys = [k * x + q for x in xs]
        ans, e = "né direttamente né inversamente proporzionali", "Né y/x né x · y sono costanti (y = %dx + %d è lineare ma non proporzionale): <b>nessuna delle due</b>." % (k, q)
    tab = table(["x"] + [str(x) for x in xs], [["y"] + [str(y) for y in ys]])
    opts = ["direttamente proporzionali (y = %dx)" % k if t != "dir" else "inversamente proporzionali (y = %d/x)" % (k * xs[0] * xs[0]),
            "inversamente proporzionali (y = %d/x)" % k if t != "inv" else "direttamente proporzionali (y = %dx)" % (ys[0] // xs[0] if ys[0] % xs[0] == 0 else 2),
            "né direttamente né inversamente proporzionali"]
    return M("Come sono le grandezze x e y della tabella?%s" % tab, ans, [o for o in opts if o != ans] + ["sempre proporzionali"], e)


def s4_abs():
    a, b = nz(R, -5, 5), R.randint(-4, 4)
    x = nz(R, -6, 6)
    v = abs(x - a) + b
    f = "|%s|%s" % (poly([1, -a]), (" + %d" % b if b > 0 else " − %d" % -b) if b else "")
    w = [x - a + b, abs(x + a) + b, -abs(x - a) + b, abs(x) - a + b, abs(x - a) - b, abs(x) + abs(a) + b]
    return M("Data f(x) = %s, calcola f(%s)." % (f, fq(x)), fq(v), [fq(t) for t in uniq(w) if t != v],
             "|%s − %s| = |%s| = %s, quindi f(%s) = <b>%s</b>." % (fq(x), par(a), fq(x - a), fq(abs(x - a)), fq(x), fq(v)))


def s4_comp():
    a, b = nz(R, -4, 4), R.randint(-5, 5)
    c = R.randint(-3, 3)
    x = nz(R, -3, 3)
    f = lambda t: a * t + b
    g = lambda t: t * t + c
    k = R.choice(["fg", "gf"])
    if k == "fg":
        v = f(g(x))
        w = [g(f(x)), f(x) * g(x), f(x) + g(x)]
        e = "Prima g(%s) = %s, poi f(%s) = <b>%s</b>." % (fq(x), fq(g(x)), fq(g(x)), fq(v))
        q = "f(g(%s))" % fq(x)
    else:
        v = g(f(x))
        w = [f(g(x)), f(x) * g(x), f(x) + g(x)]
        e = "Prima f(%s) = %s, poi g(%s) = <b>%s</b>." % (fq(x), fq(f(x)), fq(f(x)), fq(v))
        q = "g(f(%s))" % fq(x)
    return M("Date f(x) = %s e g(x) = %s, calcola %s." % (poly([a, b]), poly([1, 0, c]), q), fq(v), [fq(t) for t in uniq(w) if t != v] + [fq(v + 1)], e)


def s5_probl():
    k = R.choice(["taxi", "tel", "vasca", "molla"])
    if k == "taxi":
        q0, m = R.choice([3, 4, 5]), R.choice([Fr(3, 2), Fr(6, 5), Fr(2), Fr(5, 4)])
        km = R.randint(4, 20)
        v = q0 + m * km
        q = "Un taxi costa %d € alla partenza più %s € al km. Scrivi la funzione del costo y in base ai km x e calcola il costo di %d km." % (q0, fq(m).replace("<span class='fr'><span class='fn'>", "").replace("</span><span class='fd'>", "/").replace("</span></span>", "") if m.denominator != 1 else fq(m), km)
        q = q.replace("3/2", "1,50").replace("6/5", "1,20").replace("5/4", "1,25")
        from it_liceo import dk
        ans = "y = %sx + %d; %s €" % ({Fr(3, 2): "1,5", Fr(6, 5): "1,2", Fr(2): "2", Fr(5, 4): "1,25"}[m], q0, dk(v, 2))
        w = ["y = %dx + %s; %s €" % (q0, {Fr(3, 2): "1,5", Fr(6, 5): "1,2", Fr(2): "2", Fr(5, 4): "1,25"}[m], dk(q0 * km + m, 2)), "y = %sx; %s €" % ({Fr(3, 2): "1,5", Fr(6, 5): "1,2", Fr(2): "2", Fr(5, 4): "1,25"}[m], dk(m * km, 2)), "y = %sx + %d; %s €" % ({Fr(3, 2): "1,5", Fr(6, 5): "1,2", Fr(2): "2", Fr(5, 4): "1,25"}[m], q0, dk(v + m, 2))]
        return M(q, ans, w, "Parte fissa q = %d, coefficiente angolare m = costo al km: %s, e per x = %d il costo è <b>%s €</b>." % (q0, ans.split(";")[0], km, dk(v, 2)))
    if k == "vasca":
        h0 = R.choice([40, 60, 80, 100, 120])
        r = R.choice([2, 4, 5, 8, 10])
        t = h0 // r
        q = "Una vasca contiene %d litri e si svuota di %d litri al minuto. Dopo quanti minuti è vuota? (y = %d − %dx)" % (h0, r, h0, r)
        return M(q, "%d minuti" % t, ["%d minuti" % v for v in (h0 * r if h0 * r < 1000 else h0 + r, h0 - r, t + 1)], "Lo zero della funzione: %d − %dx = 0 → <b>x = %d</b> minuti." % (h0, r, t))
    if k == "tel":
        a, ma = R.choice([(10, 0), (5, Fr(1, 10)), (0, Fr(1, 5))]), None
        return None
    L0 = R.choice([10, 12, 15, 20])
    kk = R.choice([2, 3, 4, 5])
    p = R.randint(2, 8)
    v = L0 + kk * p
    q = "Una molla è lunga %d cm e si allunga di %d cm per ogni kg appeso. Quanto è lunga con %d kg? (y = %dx + %d)" % (L0, kk, p, kk, L0)
    return M(q, "%d cm" % v, ["%d cm" % x for x in (kk * p, L0 * p + kk, v + kk)], "y = %d · %d + %d = <b>%d cm</b>." % (kk, p, L0, v))


def main():
    seen = set()
    sets = [
        ("Relazioni e funzioni, immagini", mix(R, seen, [(s1_rel, 6), (s1_val, 8), (s1_contro, 6)])),
        ("Dominio e zeri", mix(R, seen, [(s2_dom, 12), (s2_zero, 8)])),
        ("Funzioni lineari e grafico", mix(R, seen, [(s3_retta, 20)])),
        ("Proporzionalità, valore assoluto, composizione", mix(R, seen, [(s3_prop, 8), (s4_abs, 6), (s4_comp, 6)])),
        ("Problemi con le funzioni", mix(R, seen, [(s5_probl, 12), (s4_comp, 4), (s1_contro, 4)])),
    ]
    body = L(["Una <b>funzione</b> f da A a B associa a <b>ogni</b> elemento x di A <b>uno e un solo</b> elemento y = f(x) di B, la sua <b>immagine</b>. Il <b>dominio</b> è l’insieme degli x per cui f(x) si può calcolare.",
              "Per il dominio: un polinomio va bene per ogni x; un denominatore non deve essere 0; sotto una radice quadrata ci vuole un numero ≥ 0.",
              "Gli <b>zeri</b> sono gli x con f(x) = 0. La funzione <b>lineare</b> y = mx + q ha per grafico una retta: m è il coefficiente angolare, q l’ordinata all’origine.",
              "<b>Proporzionalità diretta</b>: y = kx (y/x costante). <b>Inversa</b>: y = k/x (x · y costante). La <b>composta</b> f(g(x)) si calcola da dentro a fuori."],
             [("Dominio di y = √(x − 4)", ["x − 4 ≥ 0"], "x ≥ 4"),
              ("f(x) = 2x − 1, g(x) = x² + 1: calcola f(g(2)).", ["g(2) = 5", "f(5) = 9"], "9")],
             [["f(−3) con x² = −9", "Si sostituisce tra parentesi: (−3)² = 9."],
              ["Dominio di 1/(x − 3): x ≠ −3", "Si esclude il valore che annulla il denominatore: x ≠ 3."],
              ["f(g(x)) = g(f(x))", "La composizione in generale non è commutativa: conta l’ordine."]])
    faq = [("Qual è la differenza tra relazione e funzione?", "Una relazione è un qualsiasi insieme di coppie. È una funzione se ogni primo elemento ha una sola immagine: lo stesso x non può comparire con due y diverse."),
           ("Come si trova il dominio di una funzione?", "Si guardano le operazioni che non si possono sempre fare: dividere per 0 e fare la radice quadrata di un numero negativo. Si escludono i valori di x che le causano.")]
    unit(G, R, "funzioni", "F",
         "Il concetto di funzione; dominio, immagine, zeri; funzioni lineari, proporzionalità diretta e inversa, funzione valore assoluto; composizione",
         "Relazioni e funzioni", "Funzioni",
         "Schede di matematica per la prima liceo sulle funzioni: relazioni e funzioni, immagine e controimmagine, dominio e zeri, funzioni lineari e grafico, proporzionalità diretta e inversa, valore assoluto, composizione. 100 esercizi con soluzioni.",
         "A ogni x una sola immagine f(x).", "Dominio: niente denominatori nulli e niente radici quadrate di numeri negativi.",
         body, faq, sets, 9)


if __name__ == "__main__":
    main()
