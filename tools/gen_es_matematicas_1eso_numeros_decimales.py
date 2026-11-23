# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º de ESO: Números decimales (Sentido numérico)
Órdenes de unidades, comparar y ordenar, aproximar (redondeo y truncamiento), operaciones, paso de fracción a decimal (exacto y periódico), problemas.
Errores: creer que 2,15 > 2,3 porque 15 > 3, colocar mal la coma al multiplicar, olvidar mover la coma del divisor.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, d, fq, num, unit, L, Kids, eur, table

R = random.Random(47005)
K = Kids(R)


def dec(n, k):
    return d(F(n, 10 ** k))


def s_valor():
    t = R.choice(["cifra", "lectura", "orden", "mayor", "entre"])
    if t == "cifra":
        n = R.randint(1000, 99999)
        k = 3
        s = dec(n, k)
        pos = R.choice([1, 2, 3])
        dig = str(n)[-k:][pos - 1]
        nm = {1: "décimas", 2: "centésimas", 3: "milésimas"}[pos]
        others = [v for v in ("décimas", "centésimas", "milésimas", "unidades") if v != nm]
        if str(n)[-k:].count(dig) > 1 or dig == str(n)[-k - 1]:
            return None
        return M("En el número %s, ¿qué orden de unidades ocupa la cifra %s?" % (s, dig), nm, others, "Después de la coma van décimas, centésimas y milésimas: <b>%s</b>." % nm)
    if t == "lectura":
        e, c = R.randint(1, 40), R.randint(1, 99)
        ok = "%d unidades y %d centésimas" % (e, c)
        return M("¿Cómo se lee %s?" % dec(e * 100 + c, 2), ok, ["%d unidades y %d décimas" % (e, c), "%d unidades y %d milésimas" % (e, c), "%d centésimas" % (e * 100 + c)] if c >= 10 else
                 ["%d unidades y %d décimas" % (e, c), "%d unidades y %d milésimas" % (e, c), "%d centésimas" % (e * 100 + c)], "Hay dos cifras decimales: centésimas. <b>%s</b>." % ok)
    if t in ("orden", "mayor"):
        e = R.randint(0, 9)
        xs = [F(e * 1000 + R.randint(0, 999), 1000)]
        xs.append(F(e * 10 + R.randint(0, 9), 10))
        xs.append(F(e * 100 + R.randint(0, 99), 100))
        xs.append(F((e + R.choice([0, 1])) * 100 + R.randint(0, 99), 100))
        if len(set(xs)) < 4:
            return None
        if t == "mayor":
            ok = max(xs)
            return M("¿Cuál es el mayor: %s?" % "; ".join(d(x) for x in xs), d(ok), [d(x) for x in xs if x != ok], "Comparamos cifra a cifra desde la izquierda: <b>%s</b>." % d(ok))
        ok = " &lt; ".join(d(x) for x in sorted(xs))
        w1 = " &lt; ".join(d(x) for x in sorted(xs, key=lambda x: len(d(x))))
        w2 = " &lt; ".join(d(x) for x in sorted(xs, reverse=True))
        w3 = " &lt; ".join(d(x) for x in sorted(xs, key=lambda x: int(d(x).split(",")[1]) if "," in d(x) else 0))
        so = sorted(xs)
        w4 = " &lt; ".join(d(x) for x in [so[0], so[2], so[1], so[3]])
        w5 = " &lt; ".join(d(x) for x in [so[1], so[0], so[2], so[3]])
        return M("Ordena de menor a mayor: %s" % "; ".join(d(x) for x in xs), ok, [w1, w2, w3, w4, w5], "Igualamos el número de decimales y comparamos: <b>%s</b>." % ok)
    a = R.randint(10, 98)
    lo, hi = F(a, 10), F(a + 1, 10)
    ok = lo + F(R.randint(1, 9), 100)
    return M("¿Qué número está entre %s y %s?" % (d(lo), d(hi)), d(ok), [d(hi + F(R.randint(1, 9), 100)), d(lo - F(R.randint(1, 9), 100)), d(F(a, 100))], "%s &lt; <b>%s</b> &lt; %s." % (d(lo), d(ok), d(hi)))


def s_aprox():
    n = R.randint(1000, 99999)
    x = F(n, 1000)
    k = R.choice([0, 1, 2])
    nm = {0: "las unidades", 1: "las décimas", 2: "las centésimas"}[k]
    q = 10 ** (3 - k)
    t = R.choice(["red", "red", "trunc"])
    if t == "red":
        r = (n + q // 2) // q * q
        tr = n // q * q
        if r == tr:
            return None
        return M("Redondea %s a %s." % (d(x), nm), d(F(r, 1000)) if k else num(r // 1000), [d(F(tr, 1000)) if k else num(tr // 1000), d(F(r + q, 1000)) if k else num(r // 1000 + 1), d(F(n // 10 * 10, 1000))],
                 "La cifra siguiente es %s: %s. Resultado: <b>%s</b>." % (str(n)[-(3 - k)], "5 o más, subimos" if int(str(n)[-(3 - k)]) >= 5 else "menos de 5, se queda", d(F(r, 1000)) if k else num(r // 1000)))
    tr = n // q * q
    r = (n + q // 2) // q * q
    if r == tr:
        return None
    return M("Trunca %s a %s." % (d(x), nm), d(F(tr, 1000)) if k else num(tr // 1000), [d(F(r, 1000)) if k else num(r // 1000), d(x), d(F(tr + q, 1000)) if tr + q != r else d(F(tr - q, 1000))],
             "Truncar es cortar sin mirar la cifra siguiente: <b>%s</b>." % (d(F(tr, 1000)) if k else num(tr // 1000)))


def s_ops():
    t = R.choice(["+", "-", "x", "x", ":", ":10"])
    a = F(R.randint(100, 9999), 100)
    b = F(R.randint(10, 999), 10 ** R.choice([1, 2]))
    if t == "+":
        r = a + b
        wrong = F(int(d(a).replace(",", "")) + int(d(b).replace(",", "")), 100) if len(d(a).split(",")[1]) != len(d(b).split(",")[1]) else r + F(1, 10)
        return M("Calcula: %s + %s" % (d(a), d(b)), d(r), [d(wrong), d(r + 1), d(r - F(1, 10))], "Colocamos las comas una debajo de otra: <b>%s</b>." % d(r))
    if t == "-":
        if a < b:
            a, b = b, a
        r = a - b
        return M("Calcula: %s − %s" % (d(a), d(b)), d(r), [d(r + F(1, 10)), d(a + b), d(r - 1) if r > 1 else d(r + 1)], "Comas alineadas y restamos: <b>%s</b>." % d(r))
    if t == "x":
        a = F(R.randint(11, 999), 10 ** R.choice([1, 2]))
        b = F(R.randint(2, 99), 10 ** R.choice([0, 1]))
        r = a * b
        return M("Calcula: %s · %s" % (d(a), d(b)), d(r), [d(r * 10), d(r / 10), d(r + F(1, 10))], "Multiplicamos sin comas y ponemos tantos decimales como tienen entre los dos factores: <b>%s</b>." % d(r))
    if t == ":10":
        a = F(R.randint(11, 9999), 100)
        p = R.choice([10, 100, 1000])
        op = R.choice(["·", ":"])
        r = a * p if op == "·" else a / p
        return M("Calcula: %s %s %s" % (d(a), op, num(p)), d(r), [d(a / p) if op == "·" else d(a * p), d(r * 10), d(r / 10)], "La coma se mueve %d lugar%s a la %s: <b>%s</b>." % (len(str(p)) - 1, "" if p == 10 else "es", "derecha" if op == "·" else "izquierda", d(r)))
    b = F(R.randint(2, 25), 10 ** R.choice([1, 1, 2]))
    q = F(R.randint(2, 99), 10)
    a = b * q
    return M("Calcula: %s : %s" % (d(a), d(b)), d(q), [d(q / 10), d(q * 10), d(q + 1)], "Movemos la coma del divisor (y la del dividendo) hasta que el divisor sea entero: <b>%s</b>." % d(q))


def s_frac():
    t = R.choice(["fd", "fd", "df", "per"])
    if t == "fd":
        dd = R.choice([2, 4, 5, 8, 10, 20, 25])
        n = R.randint(1, 3 * dd)
        f = F(n, dd)
        if f.denominator == 1:
            return None
        return M("Escribe %s como número decimal." % fq(f), d(f), [d(F(f.numerator, 10)) if f.numerator < 100 else d(f * 10), d(f * 10), d(f + F(1, 10))], "%d : %d = <b>%s</b>." % (f.numerator, f.denominator, d(f)))
    if t == "df":
        n = R.randint(1, 999)
        k = R.choice([1, 2, 3])
        f = F(n, 10 ** k)
        if n % 10 == 0:
            return None
        return M("Escribe %s como fracción irreducible." % d(f), fq(f), [fq(F(n, 10 ** (k + 1))), fq(F(n, 10 ** k + 1)) if k == 1 else fq(F(n, 10 ** (k - 1))), fq(F(10 ** k, n)) if n < 10 ** k else fq(f + 1)],
                 "%s = %d/%d, y simplificamos: <b>%s</b>." % (d(f), n, 10 ** k, fq(f)))
    dd = R.choice([3, 6, 7, 9, 11, 12])
    n = R.randint(1, dd - 1)
    f = F(n, dd)
    if f.denominator in (2, 4, 5):
        return None
    ok = "periódico"
    return M("Al dividir %d : %d, ¿qué tipo de número decimal sale?" % (f.numerator, f.denominator), ok, ["exacto", "entero", "no se puede dividir"],
             "El denominador simplificado (%d) tiene factores distintos de 2 y 5: el decimal es <b>periódico</b>." % f.denominator)


def s_problema():
    p = K.next()[0]
    t = R.choice(["compra", "kilos", "reparto", "gasolina", "media"])
    if t == "compra":
        a, b = R.randint(120, 990), R.randint(120, 990)
        pay = 2000 if a + b < 2000 else 5000
        return M("%s compra un cuaderno de %s y un bolígrafo de %s. Paga con %s. ¿Cuánto le devuelven?" % (p, eur(a), eur(b), eur(pay)), eur(pay - a - b), [eur(pay - a + b), eur(a + b), eur(pay - a - b + 100)],
                 "%s − %s = <b>%s</b>." % (eur(pay), eur(a + b), eur(pay - a - b)))
    if t == "kilos":
        kg = F(R.randint(5, 40), 10)
        pr = R.randint(120, 480)
        tot = kg * pr
        if tot.denominator != 1:
            return None
        return M("Las manzanas cuestan %s el kilo. ¿Cuánto cuestan %s kg?" % (eur(pr), d(kg)), eur(int(tot)), [eur(int(tot) * 10), eur(pr + int(kg * 100)), eur(int(tot) + 10)], "%s · %s = <b>%s</b>." % (d(kg), d(F(pr, 100)), eur(int(tot))))
    if t == "reparto":
        n = R.randint(3, 8)
        each = R.randint(150, 1500)
        tot = each * n
        return M("%d amigos pagan a partes iguales una cena de %s. ¿Cuánto paga cada uno?" % (n, eur(tot)), eur(each), [eur(each * 10), eur(tot - n * 100), eur(each + 5)], "%s : %d = <b>%s</b>." % (eur(tot), n, eur(each)))
    if t == "gasolina":
        L_ = R.randint(20, 55)
        pr = F(R.randint(140, 190), 100)
        tot = L_ * pr
        return M("Un litro de gasolina cuesta %s €. ¿Cuánto cuestan %d litros?" % (d(pr), L_), "%s €" % d(tot), ["%s €" % d(tot / 10), "%s €" % d(tot + 1), "%s €" % d(L_ + pr)], "%d · %s = <b>%s €</b>." % (L_, d(pr), d(tot)))
    xs = [F(R.randint(50, 100), 10) for _ in range(4)]
    m = sum(xs) / 4
    if (m * 100).denominator != 1:
        return None
    return M("%s ha sacado estas notas: %s. ¿Cuál es su nota media?" % (p, "; ".join(d(x) for x in xs)), d(m), [d(sum(xs)), d(m + F(1, 10)), d(sum(xs) / 3)], "Sumamos y dividimos entre 4: %s : 4 = <b>%s</b>." % (d(sum(xs)), d(m)))


seen = set()
sets = [("Órdenes de unidades y comparar", mix(R, seen, [(s_valor, 20)])), ("Redondear y truncar", mix(R, seen, [(s_aprox, 20)])), ("Operaciones con decimales", mix(R, seen, [(s_ops, 20)])),
        ("Fracciones y decimales", mix(R, seen, [(s_frac, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
body = L(["Después de la coma van las <b>décimas</b>, las <b>centésimas</b> y las <b>milésimas</b>.",
          "Para comparar, iguala el número de cifras decimales: 2,30 &gt; 2,15.",
          "Al multiplicar, el resultado lleva tantos decimales como los dos factores juntos. Al dividir, convierte el divisor en un número entero moviendo las dos comas.",
          "Una fracción da un decimal <b>exacto</b> si su denominador (simplificado) solo tiene los factores 2 y 5; si no, da un decimal <b>periódico</b>."],
         [("2,4 · 0,35", ["24 · 35 = 840", "1 + 2 = 3 decimales"], "0,840 = 0,84"), ("7,56 : 0,6", ["75,6 : 6"], "12,6")],
         [["Creer que 2,15 &gt; 2,3", "Iguala: 2,15 &lt; 2,30."], ["Colocar mal la coma al multiplicar", "Cuenta los decimales de los dos factores."], ["No mover la coma del dividendo", "Si mueves la del divisor, mueve también la del dividendo."]],
         table(["Fracción", "1/2", "1/4", "3/4", "1/5", "1/8"], [["Decimal", "0,5", "0,25", "0,75", "0,2", "0,125"]]))
faq = [("¿Qué diferencia hay entre redondear y truncar?", "Truncar es cortar las cifras sin más. Redondear mira la cifra siguiente: si es 5 o más, sube una unidad."),
       ("¿Cuándo una fracción da un decimal periódico?", "Cuando su denominador, ya simplificado, tiene algún factor primo distinto de 2 y de 5, como 1/3 = 0,333…")]
unit(1, R, "numeros-decimales", "N", "Números decimales: órdenes de unidades, comparación, aproximación por redondeo y truncamiento; operaciones; relación entre fracciones y decimales",
     "Números decimales", "Números decimales",
     "Fichas de matemáticas de 1.º de ESO: décimas, centésimas y milésimas, ordenar, redondear, operar con decimales, fracciones y problemas. 100 ejercicios con soluciones.",
     "Iguala los decimales para comparar", "2,30 es mayor que 2,15.", body, faq, sets, 5)
