# -*- coding: utf-8 -*-
"""
España Matemáticas 2.º de ESO: Fracciones y números decimales (Sentido numérico)
Operaciones combinadas con fracciones, potencias de fracciones, decimales exactos y periódicos, fracción generatriz, aproximación y error.
Errores: no respetar la jerarquía, escribir la generatriz de un periódico mixto como la de uno puro, confundir error absoluto y relativo.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, fq, d, num, unit, L, Kids, nz, sup, par

R = random.Random(48001)
K = Kids(R)


def rf(hi=9, neg=False):
    import math
    while True:
        b = R.randint(2, hi)
        a = R.randint(1, 2 * b)
        if math.gcd(a, b) == 1 and a != b:
            return F(-a if neg and R.random() < 0.4 else a, b)


def per(f):
    """decimal periódico de una fracción: «0,1<span class='ov'>6</span>»"""
    f = F(f)
    s = "−" if f < 0 else ""
    f = abs(f)
    ip = f.numerator // f.denominator
    r = f.numerator % f.denominator
    digs, seen = [], {}
    while r and r not in seen:
        seen[r] = len(digs)
        r *= 10
        digs.append(str(r // f.denominator))
        r %= f.denominator
    if not r:
        return s + num(ip) + ("," + "".join(digs) if digs else "")
    k = seen[r]
    return s + num(ip) + "," + "".join(digs[:k]) + "<span class='ov'>" + "".join(digs[k:]) + "</span>"


def s_comb():
    a, b, c = rf(), rf(), rf()
    t = R.choice(["a+b·c", "(a+b)·c", "a−b:c", "a·b−c", "a:(b+c)"])
    if t == "a+b·c":
        q, r, w = "%s + %s · %s" % (fq(a), fq(b), fq(c)), a + b * c, (a + b) * c
    elif t == "(a+b)·c":
        q, r, w = "(%s + %s) · %s" % (fq(a), fq(b), fq(c)), (a + b) * c, a + b * c
    elif t == "a−b:c":
        q, r, w = "%s − %s : %s" % (fq(a), fq(b), fq(c)), a - b / c, (a - b) / c
    elif t == "a·b−c":
        q, r, w = "%s · %s − %s" % (fq(a), fq(b), fq(c)), a * b - c, a * (b - c)
    else:
        q, r, w = "%s : (%s + %s)" % (fq(a), fq(b), fq(c)), a / (b + c), a / b + c
    if r.denominator > 60 or abs(r.numerator) > 200:
        return None
    return M("Calcula y simplifica: %s" % q, fq(r), [fq(w), fq(-r), fq(r + 1)], "Primero paréntesis, después multiplicaciones y divisiones, y al final sumas y restas: <b>%s</b>." % fq(r))


def s_pot():
    f = rf(6)
    n = R.choice([2, 3, -1, -2, 0])
    t = R.choice(["pot", "pot", "neg", "prod"])
    if t == "prod":
        m, k = R.randint(2, 5), R.randint(2, 5)
        b = R.randint(2, 6)
        ok = "%d%s" % (b, sup(m - k)) if m != k else "1"
        return M("Escribe como una potencia: %d%s : %d%s" % (b, sup(m), b, sup(k)), ok, ["%d%s" % (b, sup(m + k)), "%d%s" % (b, sup(m * k)), "%d%s" % (b, sup(k - m)) if k != m else "%d" % b], "Se restan los exponentes: <b>%s</b>." % ok)
    if t == "neg":
        b = R.randint(2, 6)
        e = R.randint(1, 3)
        r = F(1, b ** e)
        return M("Calcula: %d%s" % (b, sup(-e)), fq(r), [sg_(-b ** e), fq(F(-1, b ** e)), fq(F(b, e)) if F(b, e) != r else fq(r * 2)], "Exponente negativo: 1 / %d%s = <b>%s</b>." % (b, sup(e), fq(r)))
    if n == 0:
        return M("Calcula: (%s)⁰" % fq(f), "1", ["0", fq(f), "no existe"], "Todo número distinto de 0 elevado a 0 da <b>1</b>.")
    r = f ** n
    return M("Calcula: (%s)%s" % (fq(f), sup(n)), fq(r), [fq(F(f.numerator * n, f.denominator)) if n > 0 else fq(-f), fq(F(f.numerator ** abs(n), f.denominator)) if F(f.numerator ** abs(n), f.denominator) != r else fq(r + 1), fq(1 / r) if 1 / r != r else fq(r * 2)],
             "Se elevan numerador y denominador%s: <b>%s</b>." % (" (el exponente negativo invierte la fracción)" if n < 0 else "", fq(r)))


def sg_(x):
    from es_eso import sg
    return sg(x)


def s_tipo():
    t = R.choice(["tipo", "escribe", "escribe", "clasifica"])
    if t == "tipo":
        dd = R.choice([2, 4, 5, 8, 20, 3, 9, 11, 6, 12, 15, 30])
        n = R.randint(1, dd - 1)
        f = F(n, dd)
        den = f.denominator
        m = den
        for p in (2, 5):
            while m % p == 0:
                m //= p
        ok = "exacto" if m == 1 else ("periódico puro" if den % 2 and den % 5 else "periódico mixto")
        return M("¿Qué tipo de decimal da la fracción %s?" % fq(f), ok, [x for x in ("exacto", "periódico puro", "periódico mixto", "entero") if x != ok], "%s = %s: <b>%s</b>." % (fq(f), per(f), ok))
    if t == "escribe":
        f = F(R.randint(1, 20), R.choice([3, 6, 9, 11, 12, 7]))
        if f.denominator in (1, 2, 4, 5):
            return None
        return M("Escribe %s como número decimal." % fq(f), per(f), [per(f + F(1, 10)), per(f * 10) if f * 10 != f else per(f + 1), d(F(int(f * 100), 100))], "Dividimos %d : %d: <b>%s</b>." % (f.numerator, f.denominator, per(f)))
    q, a, w = R.choice([("En 2,3<span class='ov'>45</span>, ¿cuál es el periodo?", "45", ["3", "345", "2"]), ("En 0,8<span class='ov'>3</span>, ¿cuál es el anteperiodo?", "8", ["3", "0", "83"]),
                        ("¿Qué número es periódico puro?", "4,<span class='ov'>27</span>", ["4,2<span class='ov'>7</span>", "4,27", "4,270"]), ("¿Qué número es periódico mixto?", "1,5<span class='ov'>3</span>", ["1,<span class='ov'>53</span>", "1,53", "15,3"]),
                        ("¿Los números decimales periódicos son racionales?", "sí: se pueden escribir como fracción", ["no, nunca", "solo los puros", "solo los mixtos"]),
                        ("¿Es √2 = 1,41421… un número racional?", "no: su desarrollo decimal es infinito y no periódico", ["sí, es decimal", "sí, porque es periódico", "solo con calculadora"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_generatriz():
    t = R.choice(["exacto", "puro", "puro", "mixto", "mixto"])
    if t == "exacto":
        n = R.randint(11, 999)
        k = R.choice([1, 2, 3])
        f = F(n, 10 ** k)
        if n % 10 == 0:
            return None
        return M("Calcula la fracción generatriz de %s." % d(f), fq(f), [fq(F(n, 10 ** k * 9 // 9 * 9)) if f != F(n, 9) else fq(f + 1), fq(F(n, 10 ** (k + 1))), fq(F(n, 99)) if F(n, 99) != f else fq(f * 2)], "%s = %d/%d, simplificada: <b>%s</b>." % (d(f), n, 10 ** k, fq(f)))
    if t == "puro":
        ip = R.randint(0, 5)
        L_ = R.choice([1, 2])
        p = R.randint(1, 10 ** L_ - 2)
        if L_ == 2 and p < 10:
            p += 10
        f = ip + F(p, 10 ** L_ - 1)
        if f.denominator in (1,):
            return None
        whole = int(str(ip) + str(p).rjust(L_, "0"))
        wrong = F(whole, 10 ** L_)
        return M("Calcula la fracción generatriz de %s." % per(f), fq(f), [fq(wrong), fq(F(whole - ip, 10 ** L_)) if F(whole - ip, 10 ** L_) != wrong else fq(f + 1), fq(F(whole, 10 ** L_ - 1))] if F(whole, 10 ** L_ - 1) != f else [fq(wrong), fq(f + 1), fq(F(whole - ip, 10 ** L_))],
                 "(número sin coma − parte entera) / %s: (%d − %d)/%d = <b>%s</b>." % ("9" if L_ == 1 else "99", whole, ip, 10 ** L_ - 1, fq(f)))
    ip = R.randint(0, 3)
    a = R.randint(1, 9)
    p = R.randint(0, 9)
    if p == a:
        return None
    f = ip + F(a, 10) + F(p, 90)
    whole = int("%d%d%d" % (ip, a, p))
    base = int("%d%d" % (ip, a))
    return M("Calcula la fracción generatriz de %s." % per(f), fq(f), [fq(F(whole - base, 99)), fq(F(whole - ip, 90)), fq(F(whole, 90)) if F(whole, 90) != f else fq(f + 1)],
             "(%d − %d)/90 = %d/90 = <b>%s</b>." % (whole, base, whole - base, fq(f)))


def s_error():
    t = R.choice(["redondeo", "ea", "er", "trunc"])
    x = F(R.randint(10000, 99999), 1000)
    if t in ("redondeo", "trunc"):
        k = R.choice([1, 2])
        q = 10 ** (3 - k)
        n = int(x * 1000)
        rd = F((n + q // 2) // q * q, 1000)
        tr = F(n // q * q, 1000)
        if rd == tr:
            return None
        ok = rd if t == "redondeo" else tr
        return M("%s %s a las %s." % ("Redondea" if t == "redondeo" else "Trunca", d(x), "décimas" if k == 1 else "centésimas"), d(ok), [d(tr if t == "redondeo" else rd), d(x), d(ok + F(1, 10 ** k))],
                 "<b>%s</b>." % d(ok))
    real = F(R.randint(1000, 9999), 1000)
    ap = F((int(real * 1000) + 50) // 100 * 100, 1000)
    ea = abs(real - ap)
    if t == "ea":
        return M("Aproximamos %s por %s. ¿Cuál es el error absoluto?" % (d(real), d(ap)), d(ea), [d(ea * 10), d(real + ap), d(ea + F(1, 100))], "Ea = |valor real − aproximación| = <b>%s</b>." % d(ea))
    er = ea / real
    if not ea:
        return None
    import math
    v = int(math.floor(float(er) * 10000 + 0.5))
    ok = d(F(v, 10000))
    return M("Aproximamos %s por %s. ¿Cuál es el error relativo (redondeado a diezmilésimas)?" % (d(real), d(ap)), ok, [d(ea), d(F(int(math.floor(float(ea / ap) * 10000 + 0.5)) + 1, 10000)), d(F(v * 10, 10000))],
             "Er = Ea / valor real = %s / %s ≈ <b>%s</b>." % (d(ea), d(real), ok))


seen = set()
sets = [("Operaciones combinadas con fracciones", mix(R, seen, [(s_comb, 20)])), ("Potencias de fracciones", mix(R, seen, [(s_pot, 20)])), ("Decimales exactos y periódicos", mix(R, seen, [(s_tipo, 20)])),
        ("Fracción generatriz", mix(R, seen, [(s_generatriz, 20)])), ("Aproximación y error", mix(R, seen, [(s_error, 20)]))]
body = L(["En las operaciones combinadas: paréntesis, potencias, multiplicaciones y divisiones, y al final sumas y restas.",
          "Una fracción da un decimal <b>exacto</b> si su denominador solo tiene los factores 2 y 5; si no, da un decimal <b>periódico</b> (puro o mixto).",
          "Fracción generatriz: periódico puro 2,<span class='ov'>3</span> = (23 − 2)/9 = 21/9 = 7/3; periódico mixto 1,2<span class='ov'>5</span> = (125 − 12)/90 = 113/90.",
          "Error absoluto: |valor real − aproximación|. Error relativo: error absoluto / valor real."],
         [("0,<span class='ov'>45</span>", ["(45 − 0)/99", "45/99"], "5/11"), ("(2/3)⁻²", ["(3/2)²"], "9/4")],
         [["No respetar la jerarquía", "1/2 + 1/3 · 3 = 1/2 + 1 = 3/2."], ["Usar 9 en un periódico mixto", "Un 9 por cada cifra del periodo y un 0 por cada cifra del anteperiodo."], ["Pensar que el exponente negativo da un número negativo", "2⁻³ = 1/8."]])
faq = [("¿Qué es la fracción generatriz?", "La fracción irreducible que da un número decimal exacto o periódico al dividir el numerador entre el denominador."),
       ("¿Qué diferencia hay entre periódico puro y mixto?", "En el puro el periodo empieza justo después de la coma (0,333…); en el mixto hay cifras que no se repiten antes (0,1666…).")]
unit(2, R, "fracciones-y-decimales", "N", "Números racionales: operaciones combinadas con fracciones; potencias de exponente entero; decimales exactos y periódicos; fracción generatriz; aproximaciones y errores",
     "Fracciones, decimales y fracción generatriz", "Fracciones y decimales",
     "Fichas de matemáticas de 2.º de ESO: operaciones combinadas con fracciones, potencias, decimales periódicos, fracción generatriz y errores. 100 ejercicios con soluciones.",
     "Todo periódico es una fracción", "Generatriz: un 9 por cada cifra del periodo.", body, faq, sets, 1)
