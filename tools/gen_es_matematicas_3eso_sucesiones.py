# -*- coding: utf-8 -*-
"""
España Matemáticas 3.º de ESO: Sucesiones y progresiones (Sentido algebraico)
Término general y recurrente, progresiones aritméticas (d, aₙ, suma) y geométricas (r, aₙ, suma de n términos), problemas.
Errores: usar n en lugar de n − 1 en aₙ = a₁ + (n − 1)d, confundir diferencia y razón, sumar sin multiplicar por n/2.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, num, sg, fq, unit, L, E, MINUS, eur, Kids

R = random.Random(49003)
K = Kids(R)


def a(n):
    return "a<sub>%s</sub>" % n


def lst(xs):
    return "; ".join(sg(x) if isinstance(x, int) else fq(x) for x in xs) + "; …"


def s_general():
    t = R.choice(["lin", "cuad", "sig", "frac"])
    n = R.randint(3, 15)
    if t == "lin":
        p, q = R.randint(-6, 9), R.randint(-9, 9)
        if p in (0, 1):
            return None
        f = E((p, "n"), (q, ""))
        v = p * n + q
        return M("Si %s = %s, ¿cuánto vale %s?" % (a("n"), f, a(n)), sg(v), [sg(p * (n - 1) + q), sg(p + q + n), sg(p * n - q) if q else sg(v + p)], "%s = %s · %d %s %d = <b>%s</b>." % (a(n), sg(p), n, "+" if q >= 0 else MINUS, abs(q), sg(v)))
    if t == "cuad":
        q = R.randint(-5, 5)
        v = n * n + q
        return M("Si %s = n² %s, ¿cuánto vale %s?" % (a("n"), ("+ %d" % q) if q > 0 else ("%s %d" % (MINUS, -q)) if q else "", a(n)), sg(v), [sg(2 * n + q), sg((n - 1) ** 2 + q), sg(n * n - q) if q else sg(v + 1)], "%s = %d² %s = <b>%s</b>." % (a(n), n, ("+ %d" % q) if q > 0 else ("%s %d" % (MINUS, -q)) if q else "", sg(v)))
    if t == "sig":
        k = R.randint(2, 9)
        v = (-1) ** n * k * n
        return M("Si %s = (%s1)ⁿ · %dn, ¿cuánto vale %s?" % (a("n"), MINUS, k, a(n)), sg(v), [sg(-v), sg(k * n * n), sg((-1) ** (n + 1) * k * (n + 1))], "(%s1)<sup>%d</sup> = %s: %s = <b>%s</b>." % (MINUS, n, sg((-1) ** n), a(n), sg(v)))
    p = R.randint(1, 5)
    v = F(n, n + p)
    return M("Si %s = n / (n + %d), ¿cuánto vale %s?" % (a("n"), p, a(n)), fq(v), [fq(F(n + p, n)), fq(F(n + 1, n + p + 1)), fq(F(n, p))], "%s = %d / %d = <b>%s</b>." % (a(n), n, n + p, fq(v)))


def s_patron():
    t = R.choice(["ar", "geo", "cuad", "fib"])
    if t == "ar":
        a1, dd = R.randint(-20, 30), R.choice([-7, -5, -4, -3, -2, 2, 3, 4, 5, 6, 8, 9, 11])
        xs = [a1 + i * dd for i in range(5)]
        k = R.choice(["sig", "gen"])
        if k == "sig":
            return M("¿Cuál es el siguiente término? %s" % lst(xs[:4]), sg(xs[4]), [sg(xs[4] + dd), sg(xs[3] - dd), sg(xs[3] * 2 - xs[0])], "Se suma %s cada vez: <b>%s</b>." % (sg(dd), sg(xs[4])))
        ok = E((dd, "n"), (a1 - dd, ""))
        return M("¿Cuál es el término general de %s?" % lst(xs[:4]), "%s = %s" % (a("n"), ok), ["%s = %s" % (a("n"), E((dd, "n"), (a1, ""))), "%s = %s" % (a("n"), E((a1, "n"), (dd, ""))), "%s = %s" % (a("n"), E((a1 - dd, "n"), (dd, "")))],
                 "Diferencia %s y %s = %s: %s = %s + (n − 1) · %s = <b>%s</b>." % (sg(dd), a(1), sg(a1), a("n"), sg(a1), sg(dd), ok))
    if t == "geo":
        a1, r = R.choice([1, 2, 3, 4, 5, -2, -3]), R.choice([2, 3, -2, 4, 5])
        xs = [a1 * r ** i for i in range(5)]
        return M("¿Cuál es el siguiente término? %s" % lst(xs[:4]), sg(xs[4]), [sg(xs[3] + (xs[3] - xs[2])), sg(xs[3] * (r + 1)), sg(-xs[4])], "Se multiplica por %s cada vez: <b>%s</b>." % (sg(r), sg(xs[4])))
    if t == "cuad":
        q = R.randint(-3, 6)
        xs = [i * i + q for i in range(1, 6)]
        return M("¿Cuál es el siguiente término? %s" % lst(xs[:4]), sg(xs[4]), [sg(xs[3] + (xs[3] - xs[2])), sg(xs[3] + 2 * (xs[3] - xs[2])), sg(xs[4] + 1)], "Las diferencias son 3, 5, 7, … (impares): la siguiente es 9. <b>%s</b>." % sg(xs[4]))
    x1, x2 = R.randint(1, 9), R.randint(1, 9)
    xs = [x1, x2]
    while len(xs) < 6:
        xs.append(xs[-1] + xs[-2])
    return M("Cada término es la suma de los dos anteriores: %s ¿Cuál es el siguiente?" % lst(xs[:5]), num(xs[5]), [num(xs[4] + (xs[4] - xs[3])), num(xs[4] * 2), num(xs[5] + xs[0])], "%d + %d = <b>%d</b>." % (xs[3], xs[4], xs[5]))


def s_aritmetica():
    t = R.choice(["an", "an", "d", "n", "a1"])
    a1, dd = R.randint(-15, 25), R.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
    n = R.randint(8, 60)
    an = a1 + (n - 1) * dd
    if t == "an":
        return M("En una progresión aritmética, %s = %s y d = %s. ¿Cuánto vale %s?" % (a(1), sg(a1), sg(dd), a(n)), sg(an), [sg(a1 + n * dd), sg(a1 * n + dd) if a1 else sg(an + dd * 2), sg(n * dd)], "%s = %s + (%d − 1) · %s = <b>%s</b>." % (a(n), sg(a1), n, "(%s)" % sg(dd) if dd < 0 else sg(dd), sg(an)))
    if t == "d":
        m = R.randint(3, 9)
        am = a1 + (m - 1) * dd
        return M("En una progresión aritmética, %s = %s y %s = %s. ¿Cuál es la diferencia d?" % (a(1), sg(a1), a(m), sg(am)), sg(dd), [sg(F(am - a1, m)) if (am - a1) % m == 0 else fq(F(am - a1, m)), sg(am - a1), sg(-dd)], "(%s − %s) / %d = <b>%s</b>." % (sg(am), "(%s)" % sg(a1) if a1 < 0 else sg(a1), m - 1, sg(dd)))
    if t == "n":
        return M("En la progresión %s ¿qué lugar ocupa el término %s?" % (lst([a1 + i * dd for i in range(4)]), sg(an)), "el %d.º" % n, ["el %d.º" % (n - 1), "el %d.º" % (n + 1), "el %d.º" % ((an - a1) // abs(dd) if dd else 1) if abs((an - a1) // abs(dd)) not in (n, n - 1, n + 1) else "el %d.º" % (n + 2)],
                 "%s = %s + (n − 1) · %s → n − 1 = %d → <b>n = %d</b>." % (sg(an), sg(a1), sg(dd), n - 1, n))
    m = R.randint(4, 12)
    am = a1 + (m - 1) * dd
    return M("En una progresión aritmética, %s = %s y d = %s. ¿Cuánto vale %s?" % (a(m), sg(am), sg(dd), a(1)), sg(a1), [sg(am - m * dd), sg(am + (m - 1) * dd), sg(am - dd)], "%s = %s − (%d − 1) · %s = <b>%s</b>." % (a(1), sg(am), m, "(%s)" % sg(dd) if dd < 0 else sg(dd), sg(a1)))


def s_suma():
    t = R.choice(["ar", "ar", "nat", "geo", "geo"])
    if t == "nat":
        n = R.choice([10, 20, 30, 40, 50, 60, 80, 100, 150, 200])
        s = n * (n + 1) // 2
        return M("¿Cuánto suman los números naturales del 1 al %d?" % n, num(s), [num(n * n // 2), num(n * (n - 1) // 2), num(n * (n + 1))], "S = (1 + %d) · %d / 2 = <b>%s</b>." % (n, n, num(s)))
    if t == "ar":
        a1, dd = R.randint(-10, 20), R.choice([-3, -2, 2, 3, 4, 5, 6])
        n = R.randint(6, 30)
        an = a1 + (n - 1) * dd
        s = (a1 + an) * n // 2 if (a1 + an) * n % 2 == 0 else None
        if s is None:
            return None
        return M("Calcula la suma de los %d primeros términos de la progresión aritmética %s" % (n, lst([a1 + i * dd for i in range(4)])), sg(s), [sg((a1 + an) * n), sg((a1 + an + dd) * n // 2) if (a1 + an + dd) * n % 2 == 0 else sg(s + an), sg(an * n)],
                 "%s = %s; S = (%s + %s) · %d / 2 = <b>%s</b>." % (a(n), sg(an), sg(a1), "(%s)" % sg(an) if an < 0 else sg(an), n, sg(s)))
    a1, r = R.choice([1, 2, 3, 4, 5]), R.choice([2, 3, -2])
    n = R.randint(4, 8 if abs(r) == 2 else 6)
    s = a1 * (r ** n - 1) // (r - 1)
    return M("Calcula la suma de los %d primeros términos de la progresión geométrica %s" % (n, lst([a1 * r ** i for i in range(4)])), sg(s), [sg(a1 * r ** n), sg(a1 * (r ** (n + 1) - 1) // (r - 1)), sg(a1 * (r ** (n - 1) - 1) // (r - 1))],
             "S = %s · (%s<sup>%d</sup> − 1) / (%s − 1) = <b>%s</b>." % (sg(a1), "(%s)" % sg(r) if r < 0 else sg(r), n, sg(r), sg(s)))


def s_geometrica():
    t = R.choice(["an", "an", "r", "tipo", "frac"])
    a1, r = R.choice([1, 2, 3, 5, -1, -2, -3]), R.choice([2, 3, -2, -3, 4, 5, 10])
    n = R.randint(3, 7 if abs(r) <= 3 else 5)
    an = a1 * r ** (n - 1)
    if t == "an":
        return M("En una progresión geométrica, %s = %s y r = %s. ¿Cuánto vale %s?" % (a(1), sg(a1), sg(r), a(n)), sg(an), [sg(a1 * r ** n), sg(a1 + (n - 1) * r), sg(a1 * r * (n - 1)) if a1 * r * (n - 1) != an else sg(-an)],
                 "%s = %s · %s<sup>%d</sup> = <b>%s</b>." % (a(n), sg(a1), "(%s)" % sg(r) if r < 0 else sg(r), n - 1, sg(an)))
    if t == "r":
        xs = [a1 * r ** i for i in range(4)]
        return M("¿Cuál es la razón de la progresión geométrica %s" % lst(xs), sg(r), [sg(xs[1] - xs[0]), sg(-r), fq(F(1, r))], "%s : %s = <b>%s</b>." % (sg(xs[1]), "(%s)" % sg(xs[0]) if xs[0] < 0 else sg(xs[0]), sg(r)))
    if t == "frac":
        a1 = R.choice([64, 81, 128, 243, 160, 96])
        r = F(1, 2) if a1 % 3 else F(1, 3)
        xs = [a1 * r ** i for i in range(4)]
        if any(x.denominator > 1 for x in xs):
            return None
        return M("¿Cuál es el siguiente término de %s" % lst([int(x) for x in xs]), fq(xs[3] * r), [fq(xs[3] - (xs[2] - xs[3])), fq(xs[3] * r * r), fq(xs[3] / r)], "Se multiplica por %s: <b>%s</b>." % (fq(r), fq(xs[3] * r)))
    kind = R.choice(["ar", "geo", "ninguna"])
    if kind == "ar":
        b, dd = R.randint(1, 20), R.randint(2, 9)
        xs = [b + i * dd for i in range(4)]
    elif kind == "geo":
        b, rr = R.randint(1, 6), R.choice([2, 3, 5])
        xs = [b * rr ** i for i in range(4)]
    else:
        b = R.randint(1, 6)
        xs = [i * i + b for i in range(1, 5)]
    ok = {"ar": "aritmética", "geo": "geométrica", "ninguna": "ni aritmética ni geométrica"}[kind]
    return M("¿Qué tipo de sucesión es %s" % lst(xs), ok, [o for o in ["aritmética", "geométrica", "ni aritmética ni geométrica", "aritmética y geométrica"] if o != ok],
             "Diferencias: %s. Cocientes: %s. <b>%s</b>." % (", ".join(sg(xs[i + 1] - xs[i]) for i in range(3)), ", ".join(fq(F(xs[i + 1], xs[i])) for i in range(3)), ok))


def s_problema():
    t = R.choice(["ahorro", "asientos", "bacterias", "rebote", "escalera", "sueldo"])
    p, _ = K.next()
    if t == "ahorro":
        a1, dd, n = R.choice([1, 2, 5]), R.choice([1, 2, 3]), R.randint(10, 30)
        an = a1 + (n - 1) * dd
        s = (a1 + an) * n // 2 if (a1 + an) * n % 2 == 0 else None
        if s is None:
            return None
        return M("%s ahorra %d € la primera semana y cada semana %d € más que la anterior. ¿Cuánto habrá ahorrado en total en %d semanas?" % (p, a1, dd, n), "%s €" % num(s), ["%s €" % num(an), "%s €" % num(an * n), "%s €" % num(a1 * n + dd * n)], "Última semana: %d €. S = (%d + %d) · %d / 2 = <b>%s €</b>." % (an, a1, an, n, num(s)))
    if t == "asientos":
        a1, dd, n = R.randint(12, 25), R.choice([2, 3, 4]), R.randint(10, 25)
        an = a1 + (n - 1) * dd
        return M("Un teatro tiene %d butacas en la primera fila y cada fila tiene %d más que la anterior. ¿Cuántas butacas hay en la fila %d?" % (a1, dd, n), num(an), [num(a1 + n * dd), num(a1 * n), num((a1 + an) * n // 2)], "%s = %d + (%d − 1) · %d = <b>%d</b>." % (a(n), a1, n, dd, an))
    if t == "bacterias":
        b, h = R.choice([100, 200, 500, 50, 300]), R.randint(3, 8)
        return M("Un cultivo tiene %d bacterias y se duplica cada hora. ¿Cuántas habrá dentro de %d horas?" % (b, h), num(b * 2 ** h), [num(b * 2 * h), num(b * 2 ** (h - 1)), num(b + 2 ** h)], "%d · 2<sup>%d</sup> = <b>%s</b>." % (b, h, num(b * 2 ** h)))
    if t == "rebote":
        h0 = R.choice([128, 256, 162, 243, 64, 400, 200])
        r = F(1, 2) if h0 % 3 else F(1, 3)
        if h0 in (400, 200):
            r = F(1, 2)
        k = R.randint(2, 4)
        v = h0 * r ** k
        if v.denominator > 1:
            return None
        return M("Una pelota cae desde %d cm y en cada bote sube %s de la altura anterior. ¿A qué altura sube en el bote %d.º?" % (h0, "la mitad" if r == F(1, 2) else "un tercio", k), "%s cm" % fq(v), ["%s cm" % fq(h0 * r ** (k - 1)), "%s cm" % fq(h0 * r ** (k + 1)), "%s cm" % fq(h0 - k * h0 * r) if h0 - k * h0 * r > 0 else "%s cm" % fq(v * 3)],
                 "%d · (%s)<sup>%d</sup> = <b>%s cm</b>." % (h0, fq(r), k, fq(v)))
    if t == "escalera":
        n = R.randint(5, 20)
        return M("Con palillos se forman cuadrados en fila: 1 cuadrado usa 4 palillos, 2 cuadrados 7, 3 cuadrados 10… ¿Cuántos palillos hacen falta para %d cuadrados?" % n, num(3 * n + 1), [num(4 * n), num(3 * n), num(3 * n + 4)], "%s = 3n + 1 = <b>%d</b>." % (a("n"), 3 * n + 1))
    s0, pc, y = R.choice([1000, 1200, 1500, 2000]), R.choice([2, 3, 5, 10]), R.randint(2, 4)
    r = 1 + F(pc, 100)
    v = s0 * r ** y
    try:
        from es_eso import d
        sv = d(v)
    except ValueError:
        return None
    return M("Un sueldo de %s € sube un %d %% cada año. ¿Cuánto será dentro de %d años?" % (num(s0), pc, y), "%s €" % sv, ["%s €" % num(s0 + s0 * pc * y // 100), "%s €" % d(s0 * r ** (y - 1)), "%s €" % d(s0 * r ** (y + 1))], "Geométrica de razón %s: %s · %s<sup>%d</sup> = <b>%s €</b>." % (d(r), num(s0), d(r), y, sv))


seen = set()
sets = [("Término general", mix(R, seen, [(s_general, 12), (s_patron, 8)])), ("Progresiones aritméticas", mix(R, seen, [(s_aritmetica, 20)])),
        ("Progresiones geométricas", mix(R, seen, [(s_geometrica, 20)])), ("Suma de términos", mix(R, seen, [(s_suma, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
think = ["Una <b>sucesión</b> es una lista ordenada de números: a₁, a₂, a₃… El <b>término general</b> aₙ da cualquier término a partir de n.",
         "<b>Aritmética</b>: se suma siempre la misma diferencia d. aₙ = a₁ + (n − 1) · d. Suma: Sₙ = (a₁ + aₙ) · n / 2.",
         "<b>Geométrica</b>: se multiplica siempre por la misma razón r. aₙ = a₁ · rⁿ⁻¹. Suma: Sₙ = a₁ · (rⁿ − 1) / (r − 1)."]
ex = [("3; 7; 11; 15; … ¿a₂₀?", ["d = 4", "a₂₀ = 3 + 19 · 4"], "79"), ("2; 6; 18; … ¿a₆?", ["r = 3", "a₆ = 2 · 3⁵"], "486")]
mist = [["Usar n en vez de n − 1", "a₂₀ = a₁ + 19d, no 20d."], ["Confundir d y r", "d se resta; r se divide."], ["Olvidar dividir entre 2 en la suma", "Sₙ = (a₁ + aₙ) · n / 2."]]
body = L(think, ex, mist)
faq = [("¿Cómo sé si una progresión es aritmética o geométrica?", "Resta términos seguidos: si la diferencia es constante, es aritmética. Divide: si el cociente es constante, es geométrica."),
       ("¿De dónde sale la fórmula de la suma?", "Sumando el primero con el último, el segundo con el penúltimo… siempre da lo mismo, y hay n/2 parejas.")]
unit(3, R, "sucesiones-y-progresiones", "A", "Sucesiones: término general y recurrente; progresiones aritméticas y geométricas: término general y suma de n términos; problemas",
     "Sucesiones y progresiones", "Sucesiones", "Fichas de matemáticas de 3.º de ESO: término general, progresiones aritméticas y geométricas, suma de términos y problemas. 100 ejercicios con soluciones.",
     "aₙ = a₁ + (n − 1) · d", "Geométrica: aₙ = a₁ · rⁿ⁻¹.", body, faq, sets, 3)
