# -*- coding: utf-8 -*-
"""
España Matemáticas ESO: Sistemas de ecuaciones lineales (Sentido algebraico)
build(lv): lv = 2 → «sistemas-de-ecuaciones»: comprobar soluciones, sustitución, igualación, reducción, interpretación gráfica, problemas;
lv = 3 → «sistemas-de-ecuaciones-y-problemas»: sistemas con paréntesis y fracciones, número de soluciones (compatible, incompatible), problemas.
Errores: sustituir en la misma ecuación de la que se ha despejado, no multiplicar todos los términos al reducir, dar solo el valor de x.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, E, sg, fq, num, unit, L, Kids, nz, kosy

R = None
LV = 2
K = None


def eq(a, b, c):
    return "%s = %s" % (E((a, "x"), (b, "y")), sg(c))


def sist(e1, e2):
    return "<span class='sys'>%s<br>%s</span>" % (e1, e2)


def par_(x, y):
    return "x = %s, y = %s" % (fq(x), fq(y))


def gen():
    x, y = nz(R, -6, 7), nz(R, -6, 7)
    while True:
        a, b, c, e = nz(R, -5, 5), nz(R, -5, 5), nz(R, -5, 5), nz(R, -5, 5)
        if a * e - b * c != 0:
            break
    return x, y, (a, b, a * x + b * y), (c, e, c * x + e * y)


def wrongs(x, y):
    return [par_(y, x) if x != y else par_(x, y + 1), par_(-x, y), par_(x, -y) if y else par_(x + 1, y), par_(x + 1, y - 1), par_(-y, -x)]


def s_comprobar():
    x, y, p, q = gen()
    cand = [(x, y), (y, x), (x, -y), (-x, y), (x + 1, y)]
    cand = [c for i, c in enumerate(cand) if c not in cand[:i]][:4]
    R.shuffle(cand)
    return M("¿Cuál de estos pares es solución del sistema %s?" % sist(eq(*p), eq(*q)) + " Opciones: " + "; ".join("(%s, %s)" % (sg(a), sg(b)) for a, b in cand),
             "(%s, %s)" % (sg(x), sg(y)), ["(%s, %s)" % (sg(a), sg(b)) for a, b in cand if (a, b) != (x, y)], "Sustituimos en las dos ecuaciones y se cumplen ambas: <b>(%s, %s)</b>." % (sg(x), sg(y)))


def s_resolver():
    x, y = nz(R, -6, 7), nz(R, -6, 7)
    t = R.choice(["sust", "igual", "red", "red"])
    if t == "sust":
        a, c = nz(R, -4, 4), nz(R, -4, 4)
        k = nz(R, -5, 5)
        p = (k, -1, k * x - y)
        q = (a, c, a * x + c * y)
        if a + c * k == 0:
            return None
        e1 = "y = %s" % E((k, "x"), (y - k * x, ""))
        how = "Sustitución: llevamos y = %s a la segunda ecuación" % E((k, "x"), (y - k * x, ""))
        return M("Resuelve: %s" % sist(e1, eq(*q)), par_(x, y), wrongs(x, y), "%s: <b>%s</b>." % (how, par_(x, y)))
    if t == "igual":
        k1, k2 = nz(R, -4, 4), nz(R, -4, 4)
        if k1 == k2:
            return None
        e1 = "y = %s" % E((k1, "x"), (y - k1 * x, ""))
        e2 = "y = %s" % E((k2, "x"), (y - k2 * x, ""))
        return M("Resuelve: %s" % sist(e1, e2), par_(x, y), wrongs(x, y), "Igualación: %s = %s → x = %s; y = %s: <b>%s</b>." % (E((k1, "x"), (y - k1 * x, "")), E((k2, "x"), (y - k2 * x, "")), sg(x), sg(y), par_(x, y)))
    x, y, p, q = gen()
    return M("Resuelve: %s" % sist(eq(*p), eq(*q)), par_(x, y), wrongs(x, y), "Reducción: multiplicamos para igualar coeficientes, sumamos o restamos y despejamos: <b>%s</b>." % par_(x, y))


def s_complejo():
    x, y = nz(R, -5, 6), nz(R, -5, 6)
    t = R.choice(["par", "frac"])
    if t == "par":
        k, a, b = nz(R, -3, 3), nz(R, -3, 3), nz(R, -3, 3)
        c = nz(R, -4, 4)
        e1 = "%s(%s) %s %s = %s" % (sg(k) if k != -1 else "−", E((1, "x"), (a, "")), "+" if c > 0 else "−", E((abs(c), "y")), sg(k * (x + a) + c * y))
        e2 = eq(1, b if b else 1, x + (b if b else 1) * y)
        return M("Resuelve: %s" % sist(e1, e2), par_(x, y), wrongs(x, y), "Quitamos paréntesis y resolvemos: <b>%s</b>." % par_(x, y))
    m, n = R.choice([2, 3, 4]), R.choice([2, 3, 5])
    x = m * nz(R, -3, 3)
    y = n * nz(R, -3, 3)
    c1 = F(x, m) + F(y, n)
    e1 = "x/%d + y/%d = %s" % (m, n, fq(c1))
    a = nz(R, -3, 3)
    e2 = eq(1, a, x + a * y)
    return M("Resuelve: %s" % sist(e1, e2), par_(x, y), wrongs(x, y), "Multiplicamos la primera por %d para quitar denominadores: <b>%s</b>." % (m * n // __import__('math').gcd(m, n), par_(x, y)))


def s_tipo():
    a, b = nz(R, -4, 4), nz(R, -4, 4)
    c = R.randint(-9, 9)
    k = R.choice([2, 3, -2])
    t = R.choice(["comp", "inc", "indet"])
    if t == "comp":
        x, y, p, q = gen()
        e1, e2 = eq(*p), eq(*q)
        ok = "compatible determinado (una solución)"
    elif t == "inc":
        e1, e2 = eq(a, b, c), eq(k * a, k * b, k * c + R.choice([1, 2, 3, -1]))
        ok = "incompatible (ninguna solución)"
    else:
        e1, e2 = eq(a, b, c), eq(k * a, k * b, k * c)
        ok = "compatible indeterminado (infinitas soluciones)"
    opts = ["compatible determinado (una solución)", "incompatible (ninguna solución)", "compatible indeterminado (infinitas soluciones)", "no se puede saber"]
    return M("¿Cómo es el sistema %s?" % sist(e1, e2), ok, [o for o in opts if o != ok], "%s: <b>%s</b>." % ({"comp": "Las rectas se cortan en un punto", "inc": "Las rectas son paralelas", "indet": "Las dos ecuaciones son la misma recta"}[t], ok))


def s_grafica():
    x, y = R.randint(-3, 3), R.randint(-3, 3)
    m1, m2 = R.sample([-2, -1, 1, 2, F(1, 2), F(-1, 2)], 2)
    b1, b2 = y - m1 * x, y - m2 * x
    if abs(b1) > 4 or abs(b2) > 4 or F(b1).denominator != 1 or F(b2).denominator != 1:
        return None
    pic = kosy(lines=[(m1, b1, "#1565c0", ""), (m2, b2, "#c62828", "")], lo=-5, hi=5)
    ok = "x = %s, y = %s" % (sg(x), sg(y))
    return M(pic + "Las rectas representan las dos ecuaciones de un sistema. ¿Cuál es su solución?", ok, ["x = %s, y = %s" % (sg(y), sg(x)) if x != y else "x = %s, y = %s" % (sg(x + 1), sg(y)), "x = 0, y = %s" % sg(int(b1)) if (x, y) != (0, int(b1)) else "x = 1, y = 1", "no tiene solución"],
             "La solución es el punto donde se cortan: <b>(%s, %s)</b>." % (sg(x), sg(y)))


def s_problema():
    p, q = K.two()
    t = R.choice(["edades", "precio", "granja", "monedas", "numeros", "examen"])
    if t == "edades":
        a, b = R.randint(8, 20), R.randint(30, 50)
        return M("La suma de las edades de %s y su madre es %d años, y la madre tiene %d años más. ¿Qué edad tiene %s?" % (p[0], a + b, b - a, p[0]), "%d años" % a, ["%d años" % b, "%d años" % ((a + b) // 2), "%d años" % (b - a)],
                 "x + y = %d, y − x = %d → <b>x = %d</b>." % (a + b, b - a, a))
    if t == "precio":
        x, y = R.randint(2, 9), R.randint(1, 5)
        m1, n1, m2, n2 = R.randint(1, 4), R.randint(1, 4), R.randint(1, 4), R.randint(1, 4)
        if m1 * n2 == m2 * n1:
            return None
        return M("%d bocadillos y %d refrescos cuestan %d €; %d bocadillos y %d refrescos cuestan %d €. ¿Cuánto cuesta un bocadillo?" % (m1, n1, m1 * x + n1 * y, m2, n2, m2 * x + n2 * y), "%d €" % x, ["%d €" % y, "%d €" % (x + y), "%d €" % (x + 1)] if x != y else ["%d €" % (x + 2), "%d €" % (x + y), "%d €" % (x + 1)],
                 "Planteamos y resolvemos el sistema: bocadillo <b>%d €</b>, refresco %d €." % (x, y))
    if t == "granja":
        g, c = R.randint(5, 30), R.randint(5, 30)
        return M("En una granja hay gallinas y conejos: %d cabezas y %d patas. ¿Cuántos conejos hay?" % (g + c, 2 * g + 4 * c), str(c), [str(g), str((g + c) // 2), str(2 * g + 4 * c - (g + c))] if g != c else [str(c + 1), str(c - 1), str(2 * c)],
                 "x + y = %d, 2x + 4y = %d → <b>%d conejos</b>." % (g + c, 2 * g + 4 * c, c))
    if t == "monedas":
        a, b = R.randint(3, 15), R.randint(3, 15)
        return M("En una hucha hay %d monedas de 1 € y de 2 €, con un total de %d €. ¿Cuántas monedas de 2 € hay?" % (a + b, a + 2 * b), str(b), [str(a), str((a + b) // 2), str(a + 2 * b - (a + b) - 1)] if a != b else [str(b + 1), str(b - 1), str(2 * b)],
                 "x + y = %d, x + 2y = %d → <b>y = %d</b>." % (a + b, a + 2 * b, b))
    if t == "numeros":
        a, b = R.randint(10, 60), R.randint(2, 40)
        return M("Dos números suman %d y su diferencia es %d. ¿Cuál es el mayor?" % (2 * a + b, b), str(a + b), [str(a), str(2 * a + b), str((2 * a + b) // 2)] if (2 * a + b) // 2 != a + b else [str(a), str(2 * a + b), str(a + b + 1)],
                 "x + y = %d, x − y = %d → 2x = %d, <b>x = %d</b>." % (2 * a + b, b, 2 * a + 2 * b, a + b))
    n, ok_ = R.randint(10, 20), R.randint(5, 15)
    if ok_ >= n:
        return None
    pts = 3 * ok_ - (n - ok_)
    return M("En un examen de %d preguntas, cada acierto suma 3 puntos y cada fallo resta 1. %s contestó todas y obtuvo %d puntos. ¿Cuántas acertó?" % (n, p[0], pts), str(ok_), [str(n - ok_), str(pts // 3), str(ok_ + 1)],
             "x + y = %d, 3x − y = %d → 4x = %d, <b>x = %d</b>." % (n, pts, n + pts, ok_))


def build(lv):
    global R, LV, K
    LV = lv
    R = random.Random(48007 + (lv - 2) * 1000)
    K = Kids(R)
    seen = set()
    if lv == 2:
        sets = [("Soluciones de un sistema", mix(R, seen, [(s_comprobar, 20)])), ("Sustitución e igualación", mix(R, seen, [(s_resolver, 20)])), ("Reducción", mix(R, seen, [(s_resolver, 20)])),
                ("Interpretación gráfica", mix(R, seen, [(s_grafica, 14), (s_tipo, 6)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        slug, title, short, sort = "sistemas-de-ecuaciones", "Sistemas de ecuaciones lineales", "Sistemas", 7
        meta = "Fichas de matemáticas de 2.º de ESO: soluciones de un sistema, sustitución, igualación, reducción, interpretación gráfica y problemas. 100 ejercicios con soluciones."
        std = "Sistemas de dos ecuaciones lineales con dos incógnitas: métodos de resolución e interpretación gráfica; resolución de problemas"
    else:
        sets = [("Resolver sistemas", mix(R, seen, [(s_resolver, 20)])), ("Sistemas con paréntesis y fracciones", mix(R, seen, [(s_complejo, 20)])), ("Número de soluciones", mix(R, seen, [(s_tipo, 14), (s_grafica, 6)])),
                ("Interpretación gráfica", mix(R, seen, [(s_grafica, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
        slug, title, short, sort = "sistemas-de-ecuaciones", "Sistemas de ecuaciones y problemas", "Sistemas", 6
        meta = "Fichas de matemáticas de 3.º de ESO: métodos de resolución, sistemas con paréntesis y fracciones, número de soluciones, gráficas y problemas. 100 ejercicios con soluciones."
        std = "Sistemas de ecuaciones lineales: métodos algebraicos y gráfico; clasificación según el número de soluciones; resolución de problemas"
    think = ["Un <b>sistema</b> de dos ecuaciones con dos incógnitas busca el par (x, y) que cumple las dos a la vez.",
             "<b>Sustitución</b>: despeja una incógnita y llévala a la otra ecuación. <b>Igualación</b>: despeja la misma en las dos e iguala. <b>Reducción</b>: multiplica para que una incógnita se anule al sumar.",
             "Gráficamente, cada ecuación es una recta: si se cortan, una solución; si son paralelas, ninguna; si coinciden, infinitas."]
    ex = [("x + y = 7 y x − y = 1", ["Sumamos: 2x = 8", "x = 4, y = 3"], "x = 4, y = 3")]
    mist = [["Sustituir en la misma ecuación", "Lleva el valor despejado a la otra ecuación."], ["No multiplicar todos los términos", "Al multiplicar una ecuación, multiplica los dos miembros enteros."], ["Dar solo una incógnita", "La solución es el par (x, y)."]]
    body = L(think, ex, mist)
    faq = [("¿Qué método es mejor?", "Depende: si una incógnita ya está despejada, sustitución; si los coeficientes son opuestos o fáciles de igualar, reducción."),
           ("¿Qué significa que un sistema sea incompatible?", "Que no tiene solución: sus rectas son paralelas.")]
    unit(lv, R, slug, "A", std, title, short, meta, "Solución: el par (x, y) de las dos", "Gráficamente, el punto de corte.", body, faq, sets, sort)


if __name__ == "__main__":
    build(2)
