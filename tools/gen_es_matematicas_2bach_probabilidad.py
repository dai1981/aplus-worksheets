# -*- coding: utf-8 -*-
"""
España Matemáticas II (2.º de Bachillerato): Probabilidad (Sentido estocástico)
Sucesos y álgebra de sucesos, regla de Laplace con combinatoria, probabilidad de la unión, sucesos independientes, probabilidad condicionada y tablas de contingencia,
probabilidad total y teorema de Bayes (diagramas de árbol).
Errores: P(A ∪ B) = P(A) + P(B) sin restar la intersección, confundir P(A|B) con P(B|A), confundir independientes con incompatibles.
"""
import math
import random
from fractions import Fraction as F
from es_bach import M, mix, sg, num, unit, L, nf, fq, d, r2, tabla, W

R = random.Random(52012)


def p(x):
    x = F(x)
    try:
        return d(x)
    except ValueError:
        return fq(x)


def pr():
    return F(R.randint(1, 9), 10)


def s_sucesos():
    t = R.choice(["union", "union", "contrario", "inter", "morgan", "ninguno"])
    a, b = pr(), pr()
    i = F(R.randint(0, int(min(a, b) * 10)), 10)
    if a + b - i > 1:
        return None
    if t == "union":
        return M("Si P(A) = %s, P(B) = %s y P(A ∩ B) = %s, ¿cuánto vale P(A ∪ B)?" % (p(a), p(b), p(i)), p(a + b - i), W([p(a + b) if a + b <= 1 else p(a * b), p(a * b), p(a + b - 2 * i) if a + b - 2 * i >= 0 else p(i), p(1 - i), p(a + b - i - F(1, 10)), p(max(a, b))]), "P(A ∪ B) = P(A) + P(B) − P(A ∩ B) = <b>%s</b>." % p(a + b - i))
    if t == "inter":
        u = a + b - i
        return M("Si P(A) = %s, P(B) = %s y P(A ∪ B) = %s, ¿cuánto vale P(A ∩ B)?" % (p(a), p(b), p(u)), p(i), W([p(a * b) if a * b != i else p(i + F(1, 10)), p(a + b - u + F(1, 10)), p(u - a), p(1 - u)]), "P(A ∩ B) = P(A) + P(B) − P(A ∪ B) = <b>%s</b>." % p(i))
    if t == "contrario":
        return M("Si P(A) = %s, ¿cuánto vale P(Ā) (suceso contrario)?" % p(a), p(1 - a), W([p(a), p(1 + a) if 1 + a <= 1 else "1", "0", p(1 - a / 2)]), "P(Ā) = 1 − P(A) = <b>%s</b>." % p(1 - a))
    if t == "morgan":
        u = a + b - i
        return M("Si P(A ∪ B) = %s, ¿cuánto vale P(Ā ∩ B̄)?" % p(u), p(1 - u), W([p(u), p(1 - i) if 1 - i != 1 - u else p(1 - u + F(1, 10)), "0", p((1 - a) * (1 - b)) if (1 - a) * (1 - b) != 1 - u else p(1 - u - F(1, 10)) if u < 1 else "1"]), "Leyes de De Morgan: Ā ∩ B̄ es el contrario de A ∪ B → <b>%s</b>." % p(1 - u))
    u = a + b - i
    return M("Si P(A) = %s, P(B) = %s y P(A ∩ B) = %s, ¿cuál es la probabilidad de que ocurra A pero no B?" % (p(a), p(b), p(i)), p(a - i), W([p(a), p(a - b) if a > b else p(b - i), p(u - i) if u - i != a - i else p(a)]), "P(A ∩ B̄) = P(A) − P(A ∩ B) = <b>%s</b>." % p(a - i))


def s_laplace():
    t = R.choice(["urna2", "urna2", "comite", "dados", "cartas"])
    if t == "urna2":
        r, b = R.randint(2, 8), R.randint(2, 8)
        n = r + b
        k = R.choice(["dos_r", "una_cada"])
        if k == "dos_r":
            v = F(math.comb(r, 2), math.comb(n, 2))
            return M("Una urna tiene %d bolas rojas y %d blancas. Se sacan 2 a la vez. ¿Cuál es la probabilidad de que las dos sean rojas?" % (r, b), fq(v), W([fq(F(r * r, n * n)), fq(F(r, n)), fq(F(math.comb(r, 2), n * n)), fq(F(r - 1, n - 1))]), "C<sub>%d,2</sub>/C<sub>%d,2</sub> = %d/%d = <b>%s</b>." % (r, n, math.comb(r, 2), math.comb(n, 2), fq(v)))
        v = F(r * b, math.comb(n, 2))
        return M("Una urna tiene %d bolas rojas y %d blancas. Se sacan 2 a la vez. ¿Cuál es la probabilidad de sacar una de cada color?" % (r, b), fq(v), W([fq(F(r * b, n * n)), fq(F(1, 2)), fq(F(2 * r * b, n * n)), fq(F(r * b, n * (n - 1)))]), "(%d · %d)/C<sub>%d,2</sub> = %d/%d = <b>%s</b>." % (r, b, n, r * b, math.comb(n, 2), fq(v)))
    if t == "comite":
        h, m_ = R.randint(3, 7), R.randint(3, 7)
        k = R.choice([2, 3])
        v = F(math.comb(m_, k), math.comb(h + m_, k))
        return M("En un grupo hay %d chicos y %d chicas. Se eligen %d personas al azar. ¿Probabilidad de que todas sean chicas?" % (h, m_, k), fq(v), W([fq(F(m_, h + m_) ** k), fq(F(m_, h + m_)), fq(F(k, h + m_)), fq(F(math.comb(m_, k), math.comb(h + m_, k - 1))) if math.comb(h + m_, k - 1) else "0"]), "C<sub>%d,%d</sub>/C<sub>%d,%d</sub> = <b>%s</b>." % (m_, k, h + m_, k, fq(v)))
    if t == "dados":
        s = R.randint(3, 11)
        fav = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s)
        return M("Se lanzan dos dados. ¿Cuál es la probabilidad de que la suma sea %d?" % s, fq(F(fav, 36)), W([fq(F(1, 11)), fq(F(fav, 21)), fq(F(s, 36)), fq(F(fav + 1, 36))]), "Hay %d casos favorables de 36: <b>%s</b>." % (fav, fq(F(fav, 36))))
    k = R.choice(["oros", "figura", "as"])
    fav = {"oros": 10, "figura": 12, "as": 4}[k]
    txt = {"oros": "sea de oros", "figura": "sea una figura (sota, caballo o rey)", "as": "sea un as"}[k]
    return M("Se saca una carta de una baraja española de 40 cartas. ¿Cuál es la probabilidad de que %s?" % txt, fq(F(fav, 40)), W([fq(F(1, 40)), fq(F(fav, 48)), fq(F(1, 4)) if fav != 10 else fq(F(1, 10)), fq(F(fav + 2, 40))]), "Laplace: %d/40 = <b>%s</b>." % (fav, fq(F(fav, 40))))


def s_independencia():
    t = R.choice(["prod", "prod", "comprobar", "teo", "almenos"])
    a, b = pr(), pr()
    if t == "prod":
        return M("A y B son independientes con P(A) = %s y P(B) = %s. ¿Cuánto vale P(A ∩ B)?" % (p(a), p(b)), p(a * b), W([p(a + b) if a + b <= 1 else "0", p(min(a, b)), "0", p(a * b + F(1, 10))]), "Independientes: P(A ∩ B) = P(A) · P(B) = <b>%s</b>." % p(a * b))
    if t == "comprobar":
        ind = R.random() < 0.5
        i = a * b if ind else a * b + F(R.choice([1, 2]), 100)
        if i > min(a, b):
            return None
        ok = "sí, porque P(A ∩ B) = P(A) · P(B)" if ind else "no, porque P(A ∩ B) ≠ P(A) · P(B)"
        return M("Si P(A) = %s, P(B) = %s y P(A ∩ B) = %s, ¿son A y B independientes?" % (p(a), p(b), p(i)), ok, [x for x in ["sí, porque P(A ∩ B) = P(A) · P(B)", "no, porque P(A ∩ B) ≠ P(A) · P(B)", "no, porque son incompatibles", "sí, porque P(A ∩ B) ≠ 0"] if x != ok], "P(A) · P(B) = %s: <b>%s</b>." % (p(a * b), ok))
    if t == "almenos":
        q = R.choice([F(1, 2), F(1, 6), F(1, 3), F(1, 10), F(1, 4)])
        n = R.randint(2, 5)
        v = 1 - (1 - q) ** n
        return M("La probabilidad de acertar un tiro es %s. Si se tira %d veces (de forma independiente), ¿cuál es la probabilidad de acertar al menos una vez?" % (fq(q), n), fq(v), W([fq(q * n) if q * n <= 1 else fq(q), fq(q ** n), fq((1 - q) ** n), fq(1 - q)]), "1 − P(fallar todas) = 1 − (%s)<sup>%d</sup> = <b>%s</b>." % (fq(1 - q), n, fq(v)))
    q_, a_, w = R.choice([("Dos sucesos incompatibles con probabilidad positiva…", "no pueden ser independientes", ["siempre son independientes", "tienen P(A ∪ B) = 0", "tienen P(A ∩ B) = P(A) · P(B)"]),
                          ("Si A y B son independientes, P(A|B) es…", "P(A)", ["P(B)", "P(A) · P(B)", "0"]), ("Sacar dos cartas sin devolver la primera son sucesos…", "dependientes", ["independientes", "incompatibles", "seguros"])])
    return M(q_, a_, w, "Respuesta: <b>%s</b>." % a_)


def s_condicionada():
    t = R.choice(["formula", "formula", "tabla", "tabla", "tabla"])
    if t == "formula":
        b = pr()
        i = F(R.randint(1, int(b * 10)), 10)
        if i == b:
            return None
        return M("Si P(B) = %s y P(A ∩ B) = %s, ¿cuánto vale P(A|B)?" % (p(b), p(i)), fq(i / b) if (i / b).denominator not in (1, 2, 4, 5, 10) else p(i / b), W([p(i * b), fq(b / i) if b / i <= 1 else p(i), p(b - i), p(i)]), "P(A|B) = P(A ∩ B)/P(B) = %s/%s = <b>%s</b>." % (p(i), p(b), fq(i / b) if (i / b).denominator not in (1, 2, 4, 5, 10) else p(i / b)))
    a, b_, c, d_ = R.randint(5, 40), R.randint(5, 40), R.randint(5, 40), R.randint(5, 40)
    n = a + b_ + c + d_
    tab = tabla(["", "Deporte", "No deporte", "Total"], [["Chicos", a, b_, a + b_], ["Chicas", c, d_, c + d_], ["Total", a + c, b_ + d_, n]])
    k = R.choice(["cond", "cond2", "inter", "marg"])
    if k == "cond":
        return M(tab + "Se elige un alumno al azar. Si es chica, ¿qué probabilidad hay de que haga deporte? (%d alumnos)" % n, fq(F(c, c + d_)), W([fq(F(c, n)), fq(F(c, a + c)), fq(F(c + d_, n)), fq(F(d_, c + d_))]), "P(D | chica) = %d/%d = <b>%s</b>." % (c, c + d_, fq(F(c, c + d_))))
    if k == "cond2":
        return M(tab + "Si un alumno hace deporte, ¿qué probabilidad hay de que sea chico? (%d alumnos)" % n, fq(F(a, a + c)), W([fq(F(a, a + b_)), fq(F(a, n)), fq(F(a + c, n)), fq(F(c, a + c))]), "P(chico | D) = %d/%d = <b>%s</b>." % (a, a + c, fq(F(a, a + c))))
    if k == "inter":
        return M(tab + "¿Qué probabilidad hay de que un alumno elegido al azar sea chico y no haga deporte? (%d alumnos)" % n, fq(F(b_, n)), W([fq(F(b_, a + b_)), fq(F(b_, b_ + d_)), fq(F(a + b_, n) * F(b_ + d_, n)), fq(F(a, n))]), "P = %d/%d = <b>%s</b>." % (b_, n, fq(F(b_, n))))
    return M(tab + "¿Qué probabilidad hay de que un alumno al azar haga deporte? (%d alumnos)" % n, fq(F(a + c, n)), W([fq(F(a, n)), fq(F(a + c, a + b_)), fq(F(b_ + d_, n)), fq(F(c, n))]), "P(D) = %d/%d = <b>%s</b>." % (a + c, n, fq(F(a + c, n))))


def s_bayes():
    p1 = F(R.choice([2, 3, 4, 5, 6]), 10)
    p2 = 1 - p1
    d1, d2 = F(R.randint(1, 9), 100), F(R.randint(1, 9), 100)
    if d1 == d2:
        return None
    t = R.choice(["total", "total", "bayes", "bayes", "bayes"])
    ctx = R.choice([("Dos máquinas A y B fabrican el %s y el %s de las piezas; son defectuosas el %s y el %s respectivamente.", "una pieza sea defectuosa", "si una pieza es defectuosa, ¿qué probabilidad hay de que venga de A"),
                    ("En una ciudad el %s de los coches son de gasolina y el %s diésel; tienen una avería el %s y el %s respectivamente.", "un coche tenga una avería", "si un coche tiene una avería, ¿qué probabilidad hay de que sea de gasolina")])
    pc = lambda x: "%s %%" % d(x * 100)
    txt = ctx[0] % (pc(p1), pc(p2), pc(d1), pc(d2))
    tot = p1 * d1 + p2 * d2
    if t == "total":
        return M("%s ¿Cuál es la probabilidad de que %s?" % (txt, ctx[1]), p(tot), W([p(d1 + d2), p((d1 + d2) / 2), p(p1 * d1), p(tot + F(1, 100))]), "Probabilidad total: %s · %s + %s · %s = <b>%s</b>." % (p(p1), p(d1), p(p2), p(d2), p(tot)))
    v = p1 * d1 / tot
    return M("%s Calcula: %s? (a las milésimas)" % (txt, ctx[2]), r2(float(v), 3), W([r2(float(p1), 3), r2(float(p1 * d1), 3), r2(float(d1 / (d1 + d2)), 3), r2(float(1 - v), 3)]), "Bayes: P(A|D) = P(A)P(D|A)/P(D) = %s/%s ≈ <b>%s</b>." % (p(p1 * d1), p(tot), r2(float(v), 3)))


seen = set()
sets = [("Sucesos y operaciones", mix(R, seen, [(s_sucesos, 20)])), ("Regla de Laplace y combinatoria", mix(R, seen, [(s_laplace, 20)])), ("Sucesos independientes", mix(R, seen, [(s_independencia, 20)])),
        ("Probabilidad condicionada", mix(R, seen, [(s_condicionada, 20)])), ("Probabilidad total y Bayes", mix(R, seen, [(s_bayes, 20)]))]
think = ["<b>Unión</b>: P(A ∪ B) = P(A) + P(B) − P(A ∩ B). <b>Contrario</b>: P(Ā) = 1 − P(A).",
         "<b>Condicionada</b>: P(A|B) = P(A ∩ B)/P(B). A y B son <b>independientes</b> si P(A ∩ B) = P(A) · P(B).",
         "<b>Probabilidad total</b>: si A₁, A₂, … reparten todos los casos, P(B) = Σ P(Aᵢ) · P(B|Aᵢ).",
         "<b>Teorema de Bayes</b>: P(Aᵢ|B) = P(Aᵢ) · P(B|Aᵢ) / P(B). Sirve para «volver hacia atrás» en un árbol."]
ex = [("Máquina A: 60 %, 3 % defectuosas; B: 40 %, 5 %", ["P(D) = 0,6 · 0,03 + 0,4 · 0,05 = 0,038"], "P(A|D) = 0,018/0,038 ≈ 0,474")]
mist = [["Olvidar restar P(A ∩ B)", "Si no, se cuenta dos veces."], ["Confundir P(A|B) y P(B|A)", "La condición (lo que ya sabemos) va detrás de la barra."], ["Independientes = incompatibles", "Incompatibles no pueden ocurrir a la vez; independientes no se influyen."]]
body = L(think, ex, mist)
faq = [("¿Para qué sirve el teorema de Bayes?", "Para actualizar una probabilidad con nueva información: por ejemplo, la probabilidad de tener una enfermedad si un test da positivo."),
       ("¿Cómo se organiza un problema de probabilidad total?", "Con un diagrama de árbol: primero las causas (A₁, A₂…) y después el resultado B en cada rama.")]
unit(2, R, "probabilidad", "S", "Probabilidad: álgebra de sucesos, regla de Laplace, probabilidad condicionada, independencia, probabilidad total y teorema de Bayes",
     "Probabilidad", "Probabilidad", "Fichas de Matemáticas II (2.º de Bachillerato): sucesos, Laplace, independencia, probabilidad condicionada, tablas de contingencia, probabilidad total y Bayes. 100 ejercicios.",
     "P(A|B) = P(A ∩ B) / P(B)", "Bayes: vuelve hacia atrás en el árbol.", body, faq, sets, 12)
