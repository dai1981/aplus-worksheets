# -*- coding: utf-8 -*-
"""
España Matemáticas ESO: Potencias, notación científica, radicales y logaritmos (Sentido numérico)
build(lv): lv = 2 → «potencias-y-notacion-cientifica»: exponente entero, propiedades, notación científica, raíces cuadradas y cúbicas;
lv = 3 → «potencias-y-radicales»: propiedades con exponente negativo, notación científica y operaciones, simplificar, sumar y multiplicar radicales;
lv = 4 → «radicales-y-logaritmos»: potencias de exponente fraccionario, racionalizar, logaritmos y sus propiedades.
Errores: 2⁻³ = −8, mover la coma hacia el lado equivocado, sumar radicales no semejantes (√2 + √3 = √5), log(a + b) = log a + log b.
"""
import math
import random
from fractions import Fraction as F
from es_eso import M, mix, fq, d, num, sg, sup, raiz, rq, unit, L, Kids, nz

R = None
LV = 2


def pw(b, e):
    return ("(%s)" % fq(b) if (F(b) < 0 or F(b).denominator != 1) else fq(b)) + sup(e)


def sci(m, e):
    """m: Fraction con 1 ≤ m < 10"""
    return "%s · 10%s" % (d(m), sup(e) if e != 1 else "")


def s_prop():
    b = R.randint(2, 7)
    m, n = nz(R, -6, 6), nz(R, -6, 6)
    t = R.choice(["prod", "coc", "pot", "val", "mix"])
    if t == "prod":
        return M("Escribe como una sola potencia: %s · %s" % (pw(b, m), pw(b, n)), pw(b, m + n) if m + n else "1", [pw(b, m * n), pw(b, m - n) if m != n else pw(b, 2 * m + 1), pw(b * b, m + n)], "Se suman los exponentes: %s + %s = %s: <b>%s</b>." % (sg(m), "(%s)" % sg(n) if n < 0 else sg(n), sg(m + n), pw(b, m + n) if m + n else "1"))
    if t == "coc":
        if m == n:
            return None
        return M("Escribe como una sola potencia: %s : %s" % (pw(b, m), pw(b, n)), pw(b, m - n), [pw(b, m + n) if m + n != m - n else pw(b, m * n), pw(b, n - m), pw(1, m - n)], "Se restan los exponentes: %s − %s = %s: <b>%s</b>." % (sg(m), "(%s)" % sg(n) if n < 0 else sg(n), sg(m - n), pw(b, m - n)))
    if t == "pot":
        if m * n == m + n or m == 1:
            return None
        return M("Escribe como una sola potencia: (%s)%s" % (pw(b, m), sup(n)), pw(b, m * n), [pw(b, m + n), pw(b, abs(m * n)) if m * n < 0 else pw(b, -m * n), pw(b, m ** 2)] if m ** 2 != m * n else [pw(b, m + n), pw(b, -m * n), pw(b, m * n + 1)], "Se multiplican los exponentes: <b>%s</b>." % pw(b, m * n))
    if t == "val":
        e = R.randint(1, 4)
        f = F(R.randint(1, 5), R.randint(2, 6))
        if f.denominator == 1 or f == 1:
            return None
        r = f ** (-e)
        return M("Calcula: %s" % pw(f, -e), fq(r), [fq(-(f ** e)), fq(f ** e), fq(F(-e) * f)], "El exponente negativo invierte la base: (%s)%s = <b>%s</b>." % (fq(1 / f), sup(e), fq(r)))
    a = R.randint(2, 3)
    x, y = R.randint(2, 5), R.randint(1, 4)
    r = x * a - y
    if r == 0:
        return None
    return M("Simplifica: (%d%s)%s : %d%s" % (b, sup(x), sup(a), b, sup(y)), pw(b, r), [pw(b, x + a - y), pw(b, x * a + y), pw(b, x * (a - y)) if x * (a - y) != r else pw(b, r + 1)], "(%d%s)%s = %d%s; %d − %d = %d: <b>%s</b>." % (b, sup(x), sup(a), b, sup(x * a), x * a, y, r, pw(b, r)))


def s_cient():
    t = R.choice(["escribe_g", "escribe_p", "decimal", "orden", "prod", "coc"] if LV >= 3 else ["escribe_g", "escribe_p", "decimal", "orden", "escribe_g"])
    m = F(R.randint(11, 99), 10)
    if t == "escribe_g":
        e = R.randint(4, 11)
        n = m * 10 ** e
        return M("Escribe %s en notación científica." % num(int(n)), sci(m, e), [sci(m, e - 1), sci(m * 10, e - 1).replace(",0 ", " "), sci(m, -e)], "Movemos la coma %d lugares a la izquierda: <b>%s</b>." % (e, sci(m, e)))
    if t == "escribe_p":
        e = R.randint(3, 8)
        n = m / 10 ** e
        return M("Escribe %s en notación científica." % d(n), sci(m, -e), [sci(m, e), sci(m, -e + 1), sci(m, -e - 1)], "Movemos la coma %d lugares a la derecha: exponente negativo, <b>%s</b>." % (e, sci(m, -e)))
    if t == "decimal":
        e = R.choice([-5, -4, -3, 3, 4, 5, 6])
        n = m * F(10) ** e
        ok = num(int(n)) if n.denominator == 1 else d(n)
        w = [num(int(m * 10 ** (abs(e) + 1))) if e > 0 else d(m / 10 ** (abs(e) + 1)), num(int(m * 10 ** (abs(e) - 1))) if e > 0 else d(m / 10 ** (abs(e) - 1)), d(m / 10 ** abs(e)) if e > 0 else num(int(m * 10 ** abs(e)))]
        return M("Escribe %s como número decimal." % sci(m, e), ok, w, "Movemos la coma %d lugares a la %s: <b>%s</b>." % (abs(e), "derecha" if e > 0 else "izquierda", ok))
    if t == "orden":
        xs = [(F(R.randint(11, 99), 10), R.randint(-6, 8)) for _ in range(3)]
        if len(set(v[1] for v in xs)) < 3:
            return None
        big = max(xs, key=lambda v: v[0] * F(10) ** v[1])
        return M("¿Cuál es el mayor: %s?" % "; ".join(sci(*v) for v in xs), sci(*big), [sci(*v) for v in xs if v != big] + [sci(F(99, 10), big[1] - 1)], "Manda el exponente: <b>%s</b>." % sci(*big))
    a, ea = F(R.randint(11, 49), 10), R.randint(-5, 9)
    b, eb = F(R.randint(11, 49), 10), R.randint(-5, 9)
    if t == "prod":
        p, e = a * b, ea + eb
        if p >= 10:
            p, e = p / 10, e + 1
        return M("Calcula y escribe en notación científica: (%s) · (%s)" % (sci(a, ea), sci(b, eb)), sci(p, e), [sci(p, ea * eb) if ea * eb != e else sci(p, e + 2), sci(a + b if a + b < 10 else (a + b) / 10, e), sci(p, e - 1)],
                 "Multiplicamos %s · %s y sumamos exponentes: <b>%s</b>." % (d(a), d(b), sci(p, e)))
    q, e = a / b, ea - eb
    if q < 1:
        q, e = q * 10, e - 1
    if (q * 1000).denominator != 1:
        return None
    return M("Calcula y escribe en notación científica: (%s) : (%s)" % (sci(a, ea), sci(b, eb)), sci(q, e), [sci(q, ea + eb) if ea + eb != e else sci(q, e + 2), sci(q, e + 1), sci(q, eb - ea) if eb - ea != e else sci(q, e - 1)],
             "Dividimos %s : %s y restamos exponentes: <b>%s</b>." % (d(a), d(b), sci(q, e)))


def s_raices():
    t = R.choice(["cuad", "cubo", "frac", "neg", "entre"])
    if t == "cuad":
        r = R.randint(11, 40)
        return M("Calcula: √%s" % num(r * r), num(r), [num(r * r // 2), sg(-r) + " solo", num(r + 1)], "%d² = %s. Las raíces cuadradas son <b>%d</b> y −%d." % (r, num(r * r), r, r))
    if t == "cubo":
        r = nz(R, -10, 10)
        return M("Calcula: ∛(%s)" % sg(r ** 3), sg(r), [sg(-r), sg(r ** 3 // 3) if r ** 3 % 3 == 0 else sg(r * 3), "no existe"], "%s³ = %s: <b>%s</b>." % ("(%s)" % sg(r) if r < 0 else sg(r), sg(r ** 3), sg(r)))
    if t == "frac":
        a, b = R.randint(1, 12), R.randint(2, 12)
        if a == b:
            return None
        f = F(a * a, b * b)
        return M("Calcula: √(%s)" % fq(f), fq(F(a, b)), [fq(f / 2), fq(F(b, a)), fq(F(a * a, b))], "√%d / √%d = <b>%s</b>." % (f.numerator, f.denominator, fq(F(a, b))))
    if t == "neg":
        r = R.randint(2, 9)
        return M("¿Cuánto vale √(−%d)?" % (r * r), "no es un número real", [sg(-r), str(r), sg(-r * r)], "Ningún número real al cuadrado da negativo: <b>no es un número real</b>.")
    n = R.randint(20, 400)
    r = int(math.isqrt(n))
    if r * r == n:
        return None
    return M("¿Entre qué dos enteros consecutivos está √%d?" % n, "entre %d y %d" % (r, r + 1), ["entre %d y %d" % (r - 1, r), "entre %d y %d" % (r + 1, r + 2), "entre %d y %d" % (n // 2, n // 2 + 1)], "%d² = %d &lt; %d &lt; %d = %d²: <b>entre %d y %d</b>." % (r, r * r, n, (r + 1) ** 2, r + 1, r, r + 1))


def s_radicales():
    t = R.choice(["simp", "simp", "suma", "prod", "intro"] if LV == 3 else ["simp", "suma", "prod", "racion", "racion", "fracc"])
    if t == "simp":
        k = R.randint(2, 7)
        m = R.choice([2, 3, 5, 6, 7, 10])
        n = k * k * m
        return M("Simplifica: √%d" % n, raiz(n), ["%d√%d" % (m, k * k) if m * m != k * k else "√%d" % (k * m), "%d√%d" % (k * k, m), "%d√%d" % (k, m + 1)], "%d = %d² · %d, así que √%d = <b>%s</b>." % (n, k, m, n, raiz(n)))
    if t == "suma":
        m = R.choice([2, 3, 5, 7])
        a, b = R.randint(1, 5), R.randint(1, 5)
        n1, n2 = a * a * m, b * b * m
        if n1 == n2:
            return None
        c = nz(R, -3, 4)
        r = a + c * b
        ok = raiz(m, r) if r > 0 else ("−" + raiz(m, -r) if r < 0 else "0")
        q = "√%d %s %s√%d" % (n1, "+" if c > 0 else "−", "" if abs(c) == 1 else str(abs(c)), n2)
        return M("Calcula: %s" % q, ok, ["√%d" % (n1 + c * n2) if n1 + c * n2 > 0 else "0", raiz(m, a + abs(c) * b + 1), raiz(m, abs(r) + 2)], "√%d = %s y √%d = %s; sumamos los semejantes: <b>%s</b>." % (n1, raiz(n1), n2, raiz(n2), ok))
    if t == "prod":
        a, b = R.choice([(2, 8), (3, 12), (2, 18), (5, 20), (3, 27), (6, 24), (2, 32), (7, 28), (3, 6), (2, 10), (5, 10), (6, 15)])
        p = a * b
        return M("Calcula y simplifica: √%d · √%d" % (a, b), raiz(p), ["√%d" % (a + b), raiz(p, 2), "%d" % (a * b)], "√%d · √%d = √%d = <b>%s</b>." % (a, b, p, raiz(p)))
    if t == "intro":
        k, m = R.randint(2, 6), R.choice([2, 3, 5, 6, 7])
        return M("Introduce el factor dentro de la raíz: %d√%d" % (k, m), "√%d" % (k * k * m), ["√%d" % (k * m), "√%d" % (k + m), "√%d" % (k * k + m)], "%d√%d = √(%d² · %d) = <b>√%d</b>." % (k, m, k, m, k * k * m))
    if t == "racion":
        a, m = R.randint(1, 12), R.choice([2, 3, 5, 6, 7])
        f = F(a, m)
        ok = ("%s√%d" % ("" if f.numerator == 1 else str(f.numerator), m)) + ("/%d" % f.denominator if f.denominator != 1 else "")
        return M("Racionaliza: %d/√%d" % (a, m), ok, ["%d√%d" % (a, m), "%d/%d" % (a, m), "√%d/%d" % (a, m) if a != 1 else "%d√%d/%d" % (m, m, m)], "Multiplicamos arriba y abajo por √%d: %d√%d/%d = <b>%s</b>." % (m, a, m, m, ok))
    b = R.choice([4, 8, 9, 16, 25, 27, 32, 64, 81, 125])
    n, k = R.choice([(2, 1), (3, 1), (2, 3), (3, 2), (4, 1), (5, 1), (2, -1), (3, -1)])
    v = b ** (F(k, n))
    if v.denominator > 1000 if isinstance(v, F) else False:
        return None
    root = round(b ** (1.0 / n))
    if root ** n != b:
        return None
    val = F(root) ** k
    return M("Calcula: %d<sup>%s</sup>" % (b, ("%d/%d" % (k, n)) if k > 0 else "−1/%d" % n), fq(val), [fq(F(b * k, n)) if F(b * k, n) != val else fq(val + 1), fq(-val), fq(1 / val) if 1 / val != val else fq(val * 2)],
             "a<sup>m/n</sup> = (ⁿ√a)<sup>m</sup>: ⁿ√%d = %d, y %d%s = <b>%s</b>." % (b, root, root, sup(k), fq(val)))


def s_log():
    t = R.choice(["val", "val", "prop", "eq", "dec"])
    if t == "val":
        b = R.choice([2, 3, 5, 10])
        e = R.randint(-3, 6)
        x = F(b) ** e
        if x > 10 ** 6:
            return None
        return M("Calcula: log<sub>%d</sub> %s" % (b, fq(x)), sg(e), [sg(-e) if e else "1", fq(x / b) if x / b != e else sg(e + 1), sg(e + 1)], "%d%s = %s, así que el logaritmo vale <b>%s</b>." % (b, sup(e) if e != 1 else "¹", fq(x), sg(e)))
    if t == "prop":
        k = R.choice(["prod", "coc", "pot"])
        a, b = R.randint(2, 9), R.randint(2, 9)
        if k == "prod":
            return M("Si log 2 ≈ 0,301 y log 3 ≈ 0,477, ¿cuánto vale log 6?", "0,778", ["0,143", "0,602", "1,431"], "log 6 = log 2 + log 3 ≈ <b>0,778</b>.") if R.random() < 0.3 else \
                M("¿A qué es igual log(%d · x)?" % a, "log %d + log x" % a, ["log %d · log x" % a, "%d · log x" % a, "log(%d + x)" % a], "El logaritmo de un producto es la suma: <b>log %d + log x</b>." % a)
        if k == "coc":
            return M("¿A qué es igual log(x / %d)?" % a, "log x − log %d" % a, ["log x / log %d" % a, "log(x − %d)" % a, "log x + log %d" % a], "El logaritmo de un cociente es la resta: <b>log x − log %d</b>." % a)
        return M("¿A qué es igual log(x%s)?" % sup(a), "%d · log x" % a, ["(log x)%s" % sup(a), "log x + %d" % a, "log(%dx)" % a], "El exponente sale multiplicando: <b>%d · log x</b>." % a)
    if t == "eq":
        b = R.choice([2, 3, 5, 10])
        e = R.randint(1, 5)
        if b ** e > 100000:
            return None
        if R.random() < 0.5:
            return M("Resuelve: log<sub>%d</sub> x = %d" % (b, e), "x = %s" % num(b ** e), ["x = %d" % (b * e), "x = %d" % (e ** b) if e ** b != b ** e else "x = %d" % (b + e), "x = %s" % num(b ** (e + 1))], "x = %d%s = <b>%s</b>." % (b, sup(e) if e != 1 else "¹", num(b ** e)))
        return M("Resuelve: %d<sup>x</sup> = %s" % (b, num(b ** e)), "x = %d" % e, ["x = %d" % (e + 1), "x = %s" % num(b ** e // b), "x = %d" % (b ** e // e) if b ** e % e == 0 and b ** e // e != e else "x = %d" % (e + 2)], "%s = %d%s: <b>x = %d</b>." % (num(b ** e), b, sup(e) if e != 1 else "¹", e))
    k = R.randint(-3, 6)
    x = F(10) ** k
    return M("Calcula: log %s" % (num(int(x)) if x.denominator == 1 else d(x)), sg(k), [sg(-k) if k else "1", sg(k + 1), str(len(str(abs(k))) + 9)], "log es en base 10 y 10%s = %s: <b>%s</b>." % (sup(k) if k != 1 else "¹", num(int(x)) if x.denominator == 1 else d(x), sg(k)))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(48002 + (lv - 2) * 1000)
    seen = set()
    if lv == 2:
        sets = [("Propiedades de las potencias", mix(R, seen, [(s_prop, 20)])), ("Potencias de exponente negativo", mix(R, seen, [(s_prop, 20)])), ("Notación científica", mix(R, seen, [(s_cient, 20)])),
                ("Raíces cuadradas y cúbicas", mix(R, seen, [(s_raices, 20)])), ("Repaso", mix(R, seen, [(s_cient, 10), (s_raices, 10)]))]
        think = ["Misma base: al multiplicar se suman los exponentes; al dividir se restan; potencia de potencia: se multiplican.",
                 "Exponente negativo: a⁻ⁿ = 1/aⁿ. Por ejemplo, 2⁻³ = 1/8.",
                 "<b>Notación científica</b>: un número entre 1 y 10 por una potencia de 10, como 3,2 · 10⁵ = 320 000 o 4,5 · 10⁻³ = 0,0045."]
        ex = [("0,00072 en notación científica", ["La coma se mueve 4 lugares a la derecha"], "7,2 · 10⁻⁴"), ("2⁵ · 2⁻⁸", ["5 + (−8) = −3"], "2⁻³ = 1/8")]
        mist = [["Pensar que 2⁻³ = −8", "2⁻³ = 1/8, es positivo."], ["Mover la coma hacia el lado equivocado", "Números pequeños: exponente negativo."], ["Escribir 32 · 10⁴", "El primer factor debe estar entre 1 y 10: 3,2 · 10⁵."]]
        slug, title, short, kb, ks, sort = "potencias-y-notacion-cientifica", "Potencias y notación científica", "Potencias", "a⁻ⁿ = 1/aⁿ", "Notación científica: 3,2 · 10⁵.", 2
        meta = "Fichas de matemáticas de 2.º de ESO: propiedades de las potencias, exponente negativo, notación científica y raíces cuadradas y cúbicas. 100 ejercicios con soluciones."
        std = "Potencias de exponente entero y sus propiedades; notación científica; raíces cuadradas y cúbicas"
    elif lv == 3:
        sets = [("Propiedades de las potencias", mix(R, seen, [(s_prop, 20)])), ("Notación científica", mix(R, seen, [(s_cient, 20)])), ("Operar en notación científica", mix(R, seen, [(s_cient, 20)])),
                ("Simplificar radicales", mix(R, seen, [(s_radicales, 20)])), ("Operar con radicales", mix(R, seen, [(s_radicales, 20)]))]
        think = ["Las propiedades de las potencias valen también con exponentes negativos: a⁻ⁿ = 1/aⁿ.",
                 "En notación científica, para multiplicar se multiplican los números y se suman los exponentes; al final se ajusta para que el primer factor esté entre 1 y 10.",
                 "Para simplificar un radical se sacan los factores cuadrados: √50 = √(25 · 2) = 5√2. Solo se suman los radicales <b>semejantes</b>."]
        ex = [("√12 + √27", ["2√3 + 3√3"], "5√3"), ("(3 · 10⁵) · (4 · 10⁻²)", ["12 · 10³"], "1,2 · 10⁴")]
        mist = [["Sumar radicales distintos", "√2 + √3 no es √5."], ["Dejar el resultado como 12 · 10³", "Ajusta: 1,2 · 10⁴."], ["Sacar mal un factor", "√18 = √(9 · 2) = 3√2."]]
        slug, title, short, kb, ks, sort = "potencias-y-radicales", "Potencias, notación científica y radicales", "Potencias y radicales", "√(a² · b) = a√b", "Solo se suman radicales semejantes.", 2
        meta = "Fichas de matemáticas de 3.º de ESO: propiedades de las potencias, notación científica, simplificar, sumar y multiplicar radicales. 100 ejercicios con soluciones."
        std = "Potencias de exponente entero; notación científica y operaciones; radicales: simplificación y operaciones"
    else:
        sets = [("Potencias de exponente fraccionario", mix(R, seen, [(s_radicales, 20)])), ("Operar y racionalizar", mix(R, seen, [(s_radicales, 20)])), ("Logaritmos", mix(R, seen, [(s_log, 20)])),
                ("Propiedades de los logaritmos", mix(R, seen, [(s_log, 20)])), ("Notación científica", mix(R, seen, [(s_cient, 20)]))]
        think = ["a<sup>m/n</sup> = ⁿ√(a<sup>m</sup>): 8<sup>2/3</sup> = (∛8)² = 4.",
                 "<b>Racionalizar</b> es quitar la raíz del denominador: 6/√3 = 6√3/3 = 2√3.",
                 "log<sub>b</sub> x = y significa b<sup>y</sup> = x. Propiedades: log(a · b) = log a + log b; log(a/b) = log a − log b; log(aⁿ) = n · log a."]
        ex = [("log<sub>2</sub> 32", ["2⁵ = 32"], "5"), ("10/√5", ["10√5/5"], "2√5")]
        mist = [["Pensar que log(a + b) = log a + log b", "La suma no se separa; el producto sí."], ["Racionalizar solo el denominador", "Multiplica arriba y abajo."], ["Confundir a<sup>1/2</sup> con a/2", "a<sup>1/2</sup> = √a."]]
        slug, title, short, kb, ks, sort = "radicales-y-logaritmos", "Radicales y logaritmos", "Radicales y logaritmos", "logᵦ x = y ⇔ bʸ = x", "log(a · b) = log a + log b.", 2
        meta = "Fichas de matemáticas de 4.º de ESO: potencias de exponente fraccionario, racionalizar, logaritmos y sus propiedades y notación científica. 100 ejercicios con soluciones."
        std = "Potencias de exponente fraccionario y radicales; racionalización; logaritmos y sus propiedades"
    body = L(think, ex, mist)
    faq = [("¿Para qué sirve la notación científica?", "Para escribir números muy grandes o muy pequeños de forma corta, como la masa de un átomo o la distancia a una estrella."),
           ("¿Qué son radicales semejantes?", "Radicales con el mismo índice y el mismo radicando, como 3√2 y 5√2. Solo esos se pueden sumar.")]
    unit(lv, R, slug, "N", std, title, short, meta, kb, ks, body, faq, sets, sort)


if __name__ == "__main__":
    build(2)
