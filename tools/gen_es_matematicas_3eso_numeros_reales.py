# -*- coding: utf-8 -*-
"""
España Matemáticas ESO: números racionales e irracionales (3.º) / números reales e intervalos (4.º) (Sentido numérico)
build(lv): lv = 3 → «numeros-racionales-e-irracionales»: tipos de números, fracción → decimal (exacto, periódico puro o mixto), fracción generatriz, ordenar racionales, aproximaciones y errores;
lv = 4 → «numeros-reales-e-intervalos»: números reales, intervalos y semirrectas, unión e intersección, valor absoluto y distancias, errores.
Errores: creer que todo decimal infinito es irracional, confundir corchete y paréntesis, olvidar restar la parte no periódica en la fracción generatriz.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, d, fq, sg, num, unit, L, MINUS, recta

R = None
LV = 3
OV = "<span class='ov'>%s</span>"
INF = "+∞"
MINF = MINUS + "∞"


def dec(x):
    """Fraction → decimal (con período si lo hay)"""
    x = F(x)
    s = MINUS if x < 0 else ""
    x = abs(x)
    ip, r = divmod(x.numerator, x.denominator)
    q = x.denominator
    if r == 0:
        return s + num(ip)
    digs, pos = [], {}
    while r and r not in pos:
        pos[r] = len(digs)
        r *= 10
        digs.append(str(r // q))
        r %= q
    if not r:
        return s + num(ip) + "," + "".join(digs)
    k = pos[r]
    return s + num(ip) + "," + "".join(digs[:k]) + OV % "".join(digs[k:])


def tipo(x):
    x = F(x)
    p = abs(x)
    ip, r = divmod(p.numerator, p.denominator)
    if r == 0:
        return "decimal exacto"
    q = p.denominator
    while q % 2 == 0:
        q //= 2
    while q % 5 == 0:
        q //= 5
    if q == 1:
        return "decimal exacto"
    q2 = p.denominator
    return "periódico puro" if q2 % 2 and q2 % 5 else "periódico mixto"


def frac_nice(lo=2, hi=40):
    while True:
        b = R.randint(lo, hi)
        a = R.randint(1, 3 * b)
        x = F(a, b)
        if x.denominator > 1:
            return x


# ---------- 3.º ----------

def s_tipo_num():
    t = R.choice(["nat", "ent", "rac", "rac", "irr", "irr"])
    if t == "nat":
        k = R.randint(2, 15)
        x, ok = R.choice(["√%d" % (k * k), "%d/%d" % (k * 3, 3), num(k)]), "natural"
    elif t == "ent":
        k = R.randint(2, 30)
        x, ok = R.choice([MINUS + num(k), MINUS + "√%d" % (k * k) if k < 15 else MINUS + num(k)]), "entero (no natural)"
    elif t == "rac":
        f = frac_nice()
        x, ok = R.choice([fq(f) if R.random() < 0.5 else dec(f), dec(f), MINUS + dec(f)]), "racional (no entero)"
    else:
        n = R.choice([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 17, 18, 20])
        x = R.choice(["√%d" % n, "%d + √%d" % (R.randint(1, 9), n), "π", "2π", "π + 1", "0,1010010001…", "1,234567891011…", MINUS + "√%d" % n])
        ok = "irracional"
    opts = ["natural", "entero (no natural)", "racional (no entero)", "irracional"]
    return M("¿Cuál es el conjunto más pequeño al que pertenece el número %s?" % x, ok, [o for o in opts if o != ok],
             {"natural": "Es un número natural: <b>natural</b>.", "entero (no natural)": "Es un entero negativo: <b>entero (no natural)</b>.",
              "racional (no entero)": "Se puede escribir como fracción y no es entero: <b>racional</b>.", "irracional": "Tiene infinitas cifras decimales no periódicas: <b>irracional</b>."}[ok])


def s_cual_irr():
    n = R.choice([2, 3, 5, 6, 7, 10, 11, 13, 14, 15])
    irr = R.choice(["√%d" % n, "π", "√%d + 1" % n])
    sq = R.randint(2, 12)
    f = frac_nice()
    rac = [ "√%d" % (sq * sq), dec(f), fq(frac_nice()), "√(%d/%d)" % (R.choice([1, 4, 9]), R.choice([4, 16, 25, 49])), "%s" % dec(F(R.randint(1, 98), 99))]
    R.shuffle(rac)
    rac = list(dict.fromkeys(rac))
    if len(rac) < 3:
        return None
    return M("¿Cuál de estos números es irracional? (%s)" % "; ".join(sorted(rac[:3] + [irr])), irr, rac[:3], "Las raíces exactas, los decimales exactos y los periódicos son racionales. <b>%s</b> es irracional." % irr)


def s_frac_dec():
    t = R.choice(["exacto", "puro", "mixto"])
    while True:
        f = frac_nice(2, 30)
        if tipo(f) == ("decimal exacto" if t == "exacto" else "periódico " + t):
            break
    k = R.choice(["valor", "tipo"])
    if k == "tipo":
        ok = tipo(f)
        return M("¿Qué tipo de decimal es %s?" % fq(f), ok, [o for o in ["decimal exacto", "periódico puro", "periódico mixto", "irracional"] if o != ok],
                 "%s = %s. Denominador simplificado: %d. <b>%s</b>." % (fq(f), dec(f), f.denominator, ok))
    w = [dec(f + F(1, 10)), dec(F(f.denominator, f.numerator)) if f.numerator > 1 else dec(f * 2), dec(f * 10)]
    return M("Escribe %s en forma decimal." % fq(f), dec(f), w, "%d : %d = <b>%s</b>." % (f.numerator, f.denominator, dec(f)))


def s_generatriz():
    t = R.choice(["puro", "puro2", "mixto", "exacto"])
    if t == "puro":
        a, p = R.randint(0, 9), R.randint(1, 8)
        x = F(a) + F(p, 9)
        how = "(%d%d − %d) / 9" % (a, p, a) if a else "%d / 9" % p
        wrong = [fq(F(a * 10 + p, 10)), fq(F(a * 10 + p, 99)), fq(F(p, 10) + a), fq(F(a * 10 + p, 9)), fq(x + F(1, 9))]
    elif t == "puro2":
        a, p = R.randint(0, 5), R.randint(10, 98)
        if p % 11 == 0:
            return None
        x = F(a) + F(p, 99)
        how = "(%d%02d − %d) / 99" % (a, p, a) if a else "%d / 99" % p
        wrong = [fq(F(p, 100) + a), fq(F(p, 9) + a), fq(F(a * 100 + p, 999))]
    elif t == "mixto":
        a, b, p = R.randint(0, 5), R.randint(1, 9), R.randint(1, 9)
        if b == p:
            return None
        x = F(a) + F(b, 10) + F(p, 90)
        how = "(%d%d%d − %d%d) / 90" % (a, b, p, a, b) if a else "(%d%d − %d) / 90" % (b, p, b)
        wrong = [fq(F(a * 100 + b * 10 + p, 99)), fq(F(a * 100 + b * 10 + p - a, 90)), fq(F(a * 100 + b * 10 + p, 100))]
    else:
        n = R.choice([2, 4, 5, 8, 20, 25, 40])
        x = F(R.randint(1, 4 * n), n)
        if x.denominator == 1:
            return None
        how = "decimal exacto entre potencia de 10, simplificado"
        wrong = [fq(x * F(10, 9)), fq(x + F(1, 10)), fq(F(x.numerator, x.denominator + 1))]
    return M("¿Cuál es la fracción generatriz de %s?" % dec(x), fq(x), wrong, "%s = <b>%s</b>." % (how, fq(x)))


def s_ordenar():
    t = R.choice(["mayor", "menor", "entre"])
    xs = []
    while len(xs) < 4:
        f = F(R.randint(-30, 30), R.choice([3, 4, 6, 7, 9, 11, 12]))
        if f not in xs and f.denominator > 1:
            xs.append(f)
    sh = [R.choice([fq, dec])(x) for x in xs]
    if t == "entre":
        a, b = F(R.randint(-5, 5)), None
        b = a + 1
        f = None
        for c in xs:
            if a < c < b:
                f = c
        if f is None:
            return None
        w = [s for c, s in zip(xs, sh) if not (a < c < b)]
        if len(w) < 3:
            return None
        return M("¿Qué número está entre %s y %s? (%s)" % (sg(int(a)), sg(int(b)), "; ".join(sorted(sh))), sh[xs.index(f)], w, "%s = %s: <b>%s</b>." % (sh[xs.index(f)], dec(f), sh[xs.index(f)]))
    v = max(xs) if t == "mayor" else min(xs)
    ok = sh[xs.index(v)]
    return M("¿Cuál es el %s de estos números? (%s)" % (t, "; ".join(sorted(sh))), ok, [s for s in sh if s != ok], "Pasando a decimal: %s. El %s es <b>%s</b>." % ("; ".join(dec(x) for x in sorted(xs)), t, ok))


def s_error():
    t = R.choice(["redondeo", "trunc", "ea", "er"])
    if t in ("redondeo", "trunc"):
        x = F(R.randint(100000, 999999), 10 ** R.choice([4, 5]))
        k = R.choice([1, 2, 3])
        m = 10 ** k
        tr = F(int(x * m), m)
        rd = F(int(x * m + F(1, 2)), m)
        if tr == rd:
            return None
        lugar = {1: "décimas", 2: "centésimas", 3: "milésimas"}[k]
        if t == "redondeo":
            return M("Redondea %s a las %s." % (d(x), lugar), d(rd, k) if True else "", [d(tr), d(F(int(x * m * 10), m * 10)), d(rd + F(1, m))], "La cifra siguiente es 5 o más: subimos. <b>%s</b>." % d(rd))
        return M("Trunca %s a las %s." % (d(x), lugar), d(tr), [d(rd), d(F(int(x * m * 10), m * 10)), d(tr - F(1, m))], "Truncar es cortar sin mirar la cifra siguiente: <b>%s</b>." % d(tr))
    real = R.choice([50, 80, 100, 125, 200, 250, 400, 500, 800, 1000])
    ea = F(real, R.choice([20, 25, 40, 50, 100, 200]))
    ap = real + ea * R.choice([1, -1])
    if t == "ea":
        return M("Una medida real es %s cm y se aproxima por %s cm. ¿Cuál es el error absoluto?" % (num(real), d(ap)), "%s cm" % d(ea), ["%s cm" % d(ea / real), "%s cm" % d(ap), "%s %%" % d(ea / real * 100)], "|valor real − aproximación| = |%s − %s| = <b>%s cm</b>." % (num(real), d(ap), d(ea)))
    er = ea / real
    return M("Una medida real es %s m y se aproxima por %s m. ¿Cuál es el error relativo?" % (num(real), d(ap)), "%s (%s %%)" % (d(er), d(er * 100)), ["%s (%s %%)" % (d(ea), d(ea * 100)), "%s (%s %%)" % (d(er * 10), d(er * 1000)), "%s (%s %%)" % (d(ea / ap), d(ea / ap * 100)) if (ea / ap * 10 ** 6).denominator == 1 else "%s (%s %%)" % (d(er / 10), d(er * 10))],
             "E<sub>r</sub> = E<sub>a</sub> / valor real = %s / %s = <b>%s</b> (%s %%)." % (d(ea), num(real), d(er), d(er * 100)))


# ---------- 4.º ----------

def ivl(a, b, ca, cb):
    sa = MINF if a is None else sg(a)
    sb = INF if b is None else sg(b)
    return "%s%s, %s%s" % ("[" if ca else "(", sa, sb, "]" if cb else ")")


def ineq(a, b, ca, cb):
    if a is None:
        return "x %s %s" % ("≤" if cb else "&lt;", sg(b))
    if b is None:
        return "x %s %s" % ("≥" if ca else "&gt;", sg(a))
    return "%s %s x %s %s" % (sg(a), "≤" if ca else "&lt;", "≤" if cb else "&lt;", sg(b))


def rnd_ivl(semi=None):
    a = R.randint(-9, 6)
    b = a + R.randint(1, 8)
    ca, cb = R.random() < 0.5, R.random() < 0.5
    k = semi if semi is not None else R.choice([0, 0, 1, 2])
    if k == 1:
        return (None, b, False, cb)
    if k == 2:
        return (a, None, ca, False)
    return (a, b, ca, cb)


def s_ivl():
    I = rnd_ivl()
    a, b, ca, cb = I
    t = R.choice(["a_ivl", "a_ineq", "pertenece"])
    alt = [ivl(a, b, not ca if a is not None else ca, cb), ivl(a, b, ca, not cb if b is not None else cb), ivl(a, b, not ca if a is not None else ca, not cb if b is not None else cb), ivl(b, a, cb, ca) if a is not None and b is not None else ivl(b if b is not None else a, None if b is None else None, True, False)]
    if a is None:
        rev = [(b, None, cb, False), (b, None, not cb, False)]
    elif b is None:
        rev = [(None, a, False, ca), (None, a, False, not ca)]
    else:
        rev = []
    alt += [ivl(*x) for x in rev]
    if t == "a_ivl":
        return M("¿Qué intervalo corresponde a %s?" % ineq(*I), ivl(*I), alt, "Corchete si el extremo se incluye (≤, ≥); paréntesis si no (&lt;, &gt;) y siempre en ∞: <b>%s</b>." % ivl(*I))
    if t == "a_ineq":
        al = [ineq(a, b, not ca if a is not None else ca, cb), ineq(a, b, ca, not cb if b is not None else cb), ineq(a, b, not ca if a is not None else ca, not cb if b is not None else cb)]
        return M("¿Qué desigualdad describe el intervalo %s?" % ivl(*I), ineq(*I), al + [ineq(b, a, cb, ca) if a is not None and b is not None else None] + [ineq(*x) for x in rev], "Respuesta: <b>%s</b>." % ineq(*I))
    ext = [v for v in (a, b) if v is not None]
    cand = sorted(set(ext + [e + s for e in ext for s in (-1, 1)]))

    def inside(x):
        return (a is None or x > a or (ca and x == a)) and (b is None or x < b or (cb and x == b))
    yes = [x for x in cand if inside(x)]
    no = [x for x in cand if not inside(x)]
    if not yes or len(no) < 3:
        return None
    x = R.choice(yes)
    R.shuffle(no)
    return M("¿Qué número pertenece al intervalo %s?" % ivl(*I), sg(x), [sg(v) for v in no], "Comprueba los extremos: <b>%s</b> está dentro." % sg(x))


def s_union():
    NI, PI_ = float("-inf"), float("inf")
    while True:
        A, B = rnd_ivl(0), rnd_ivl(R.choice([0, 1, 2]))
        lo = max(A[0], B[0] if B[0] is not None else -99)
        hi = min(A[1], B[1] if B[1] is not None else 99)
        if lo < hi:
            break

    def ends(I):
        return ((NI if I[0] is None else I[0], I[2]), (PI_ if I[1] is None else I[1], I[3]))

    def comb(op):
        (la, ca), (ua, cua) = ends(A)
        (lb, cb), (ub, cub) = ends(B)
        if op == "∩":
            lo = (la, ca) if la > lb else (lb, cb) if lb > la else (la, ca and cb)
            hi = (ua, cua) if ua < ub else (ub, cub) if ub < ua else (ua, cua and cub)
        else:
            lo = (la, ca) if la < lb else (lb, cb) if lb < la else (la, ca or cb)
            hi = (ua, cua) if ua > ub else (ub, cub) if ub > ua else (ua, cua or cub)
        f = lambda v: None if v in (NI, PI_) else int(v)
        return (f(lo[0]), f(hi[0]), lo[1] and lo[0] != NI, hi[1] and hi[0] != PI_)
    op = R.choice(["∩", "∪"])
    X = comb(op)
    if X in (A, B):
        return None
    Y = comb("∪" if op == "∩" else "∩")
    w = [ivl(*Y)]
    if X[0] is not None:
        w.append(ivl(X[0], X[1], not X[2], X[3]))
    if X[1] is not None:
        w.append(ivl(X[0], X[1], X[2], not X[3]))
    if X[0] is not None and X[1] is not None:
        w.append(ivl(X[0], X[1], not X[2], not X[3]))
    w.append(ivl(*A))
    w.append(ivl(*B))
    ok = ivl(*X)
    return M("Calcula %s %s %s." % (ivl(*A), op, ivl(*B)), ok, w, "%s: <b>%s</b>." % ("La intersección son los números que están en los dos" if op == "∩" else "La unión son los números que están en alguno", ok))


def s_absoluto():
    t = R.choice(["valor", "dist", "le", "ge"])
    a = R.randint(-9, 9)
    r = R.randint(1, 7)
    if t == "valor":
        x = R.randint(-20, 20)
        y = R.randint(-20, 20)
        if x == y:
            return None
        return M("Calcula |%s − %s|." % (sg(x), par(y)), num(abs(x - y)), [sg(x - y) if x < y else MINUS + num(x - y), num(abs(x) + abs(y)) if abs(x) + abs(y) != abs(x - y) else num(abs(x - y) + 2), num(abs(abs(x) - abs(y))) if abs(abs(x) - abs(y)) != abs(x - y) else num(abs(x - y) + 1)], "|%s| = <b>%s</b>." % (sg(x - y), num(abs(x - y))))
    if t == "dist":
        b = R.randint(-15, 15)
        if b == a:
            return None
        return M("¿Cuál es la distancia entre %s y %s en la recta real?" % (sg(a), sg(b)), num(abs(a - b)), [num(abs(a + b)) if abs(a + b) != abs(a - b) else num(abs(a - b) + 1), sg(a - b) if a < b else MINUS + num(a - b), num(abs(a) + abs(b) + 1), num(2 * abs(a - b)), num(abs(a - b) - 1)], "d = |%s − %s| = <b>%s</b>." % (sg(a), par(b), num(abs(a - b))))
    xa = "x" if a == 0 else ("x − %d" % a if a > 0 else "x + %d" % -a)
    if t == "le":
        ok = ivl(a - r, a + r, True, True)
        return M("¿Qué números cumplen |%s| ≤ %d?" % (xa, r), ok, [ivl(-r, r, True, True) if a else ivl(a - r, a + r, False, False), ivl(a - r, a + r, False, False), "(%s, %s] ∪ [%s, %s)" % (MINF, sg(a - r), sg(a + r), INF), ivl(a, a + r, True, True)],
                 "Los que están a distancia ≤ %d de %s: <b>%s</b>." % (r, sg(a), ok))
    ok = "(%s, %s) ∪ (%s, %s)" % (MINF, sg(a - r), sg(a + r), INF)
    return M("¿Qué números cumplen |%s| &gt; %d?" % (xa, r), ok, [ivl(a - r, a + r, False, False), "(%s, %s] ∪ [%s, %s)" % (MINF, sg(a - r), sg(a + r), INF), "(%s, %s)" % (sg(a + r), INF)],
             "Los que están a distancia mayor que %d de %s: <b>%s</b>." % (r, sg(a), ok))


def par(x):
    return "(%s)" % sg(x) if x < 0 else sg(x)


def s_reales():
    t = R.choice(["tipo", "irr", "aprox", "orden"])
    if t == "tipo":
        return s_tipo_num()
    if t == "irr":
        return s_cual_irr()
    if t == "aprox":
        n = R.choice([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 50])
        k = int(n ** 0.5)
        return M("¿Entre qué dos enteros consecutivos está √%d?" % n, "entre %d y %d" % (k, k + 1), ["entre %d y %d" % (k - 1, k), "entre %d y %d" % (k + 1, k + 2), "entre %d y %d" % (n // 2, n // 2 + 1)],
                 "%d² = %d &lt; %d &lt; %d = %d²: <b>entre %d y %d</b>." % (k, k * k, n, (k + 1) ** 2, k + 1, k, k + 1))
    n = R.choice([2, 3, 5, 7, 10])
    import math
    v = math.sqrt(n)
    cands = [("√%d" % n, v), ("π", math.pi), (d(F(round(v * 100) + R.choice([-3, 3]), 100)), (round(v * 100) + 0) / 100), (fq(F(R.randint(10, 40), 7)), 0)]
    cands[3] = (cands[3][0], float(F(cands[3][0].count("x") or 1)))
    vals = [("√%d" % n, v), ("π", math.pi)]
    a = F(R.randint(100, 400), 100)
    b = F(R.randint(8, 30), 7)
    vals += [(d(a), float(a)), (fq(b), float(b))]
    if len(set(round(x, 4) for _, x in vals)) < 4:
        return None
    big = max(vals, key=lambda p: p[1])
    return M("¿Cuál es el mayor de estos números? (%s)" % "; ".join(sorted(s for s, _ in vals)), big[0], [s for s, _ in vals if s != big[0]],
             "Aproximando: %s. El mayor es <b>%s</b>." % ("; ".join("%s ≈ %s" % (s, d(F(round(x * 1000), 1000))) for s, x in sorted(vals, key=lambda p: p[1])), big[0]))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(49001 + (lv - 3) * 1000)
    seen = set()
    if lv == 3:
        sets = [("Tipos de números", mix(R, seen, [(s_tipo_num, 14), (s_cual_irr, 6)])), ("De fracción a decimal", mix(R, seen, [(s_frac_dec, 20)])),
                ("Fracción generatriz", mix(R, seen, [(s_generatriz, 20)])), ("Ordenar racionales", mix(R, seen, [(s_ordenar, 20)])), ("Aproximaciones y errores", mix(R, seen, [(s_error, 20)]))]
        think = ["Un número es <b>racional</b> si se puede escribir como fracción: enteros, decimales exactos y decimales periódicos.",
                 "Es <b>irracional</b> si tiene infinitas cifras decimales sin período: √2, π, √7…",
                 "Fracción generatriz de un periódico puro: (número sin coma − parte entera) / tantos 9 como cifras tiene el período. Si es mixto, se añade un 0 por cada cifra no periódica y se resta también la parte no periódica.",
                 "Error absoluto = |valor real − aproximación|. Error relativo = error absoluto / valor real."]
        ex = [("1,<span class='ov'>3</span>", ["(13 − 1) / 9 = 12/9"], "4/3"), ("0,1<span class='ov'>6</span>", ["(16 − 1) / 90 = 15/90"], "1/6")]
        mist = [["Decir que 0,<span class='ov'>3</span> es irracional", "Es periódico, luego racional: 1/3."], ["Poner un 9 por cada cifra decimal", "Solo por las cifras del período; las no periódicas ponen 0."], ["Redondear cuando piden truncar", "Truncar es cortar sin más."]]
        slug, title, short, kb, ks, sort, dom = "numeros-racionales-e-irracionales", "Números racionales e irracionales", "Racionales e irracionales", "Todo periódico es racional", "Irracional: infinitas cifras sin período.", 1, "N"
        meta = "Fichas de matemáticas de 3.º de ESO: tipos de números, decimales exactos y periódicos, fracción generatriz, ordenar racionales y errores. 100 ejercicios con soluciones."
        std = "Números racionales e irracionales: expresión decimal, fracción generatriz, comparación y ordenación; aproximaciones, redondeo, truncamiento y errores absoluto y relativo"
    else:
        sets = [("Números reales", mix(R, seen, [(s_reales, 20)])), ("Intervalos", mix(R, seen, [(s_ivl, 20)])), ("Unión e intersección", mix(R, seen, [(s_union, 20)])),
                ("Valor absoluto y distancias", mix(R, seen, [(s_absoluto, 20)])), ("Aproximaciones y errores", mix(R, seen, [(s_error, 20)]))]
        think = ["Los <b>números reales</b> son los racionales y los irracionales juntos: llenan toda la recta.",
                 "Un <b>intervalo</b> es un trozo de la recta: [a, b] incluye los extremos; (a, b) no. Con ∞ siempre se pone paréntesis.",
                 "<b>Unión</b> (∪): los que están en alguno. <b>Intersección</b> (∩): los que están en los dos.",
                 "|x − a| es la distancia entre x y a. |x − a| ≤ r son los números a distancia r o menos de a: [a − r, a + r]."]
        ex = [("−2 &lt; x ≤ 5", ["−2 no se incluye; 5 sí"], "(−2, 5]"), ("|x − 3| ≤ 2", ["distancia a 3 menor o igual que 2"], "[1, 5]")]
        mist = [["Cerrar el corchete en ∞", "∞ no es un número: siempre paréntesis."], ["Confundir unión e intersección", "∩: en los dos a la vez."], ["Olvidar el valor absoluto en una distancia", "La distancia nunca es negativa."]]
        slug, title, short, kb, ks, sort, dom = "numeros-reales-e-intervalos", "Números reales e intervalos", "Reales e intervalos", "[ ] incluye el extremo; ( ) no", "Con ∞ siempre paréntesis.", 1, "N"
        meta = "Fichas de matemáticas de 4.º de ESO: números reales, intervalos, unión e intersección, valor absoluto, distancias y errores. 100 ejercicios con soluciones."
        std = "Números reales: clasificación, representación en la recta, intervalos y semirrectas, unión e intersección, valor absoluto y distancias; aproximaciones y errores"
    body = L(think, ex, mist, recta(-3, 3, 1) if lv == 4 else "")
    faq = [("¿Un decimal infinito siempre es irracional?", "No. Si sus cifras se repiten (periódico), es racional. Solo es irracional si no hay período."),
           ("¿Por qué ∞ va con paréntesis?", "Porque no es un número que se pueda alcanzar o incluir.")]
    unit(lv, R, slug, dom, std, title, short, meta, kb, ks, body, faq, sets, sort)


if __name__ == "__main__":
    build(3)
