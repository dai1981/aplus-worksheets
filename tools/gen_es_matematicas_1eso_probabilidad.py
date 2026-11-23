# -*- coding: utf-8 -*-
"""
España Matemáticas ESO: Probabilidad (Sentido estocástico)
build(lv): lv = 1 → experimentos aleatorios, espacio muestral, sucesos, regla de Laplace, frecuencia relativa;
lv = 2 → Laplace con dados, urnas y baraja española, suceso contrario, unión de sucesos, frecuencia y ley de los grandes números;
lv = 3 → experimentos compuestos, diagramas de árbol, con y sin reemplazamiento, tablas de contingencia;
lv = 4 → probabilidad condicionada, sucesos independientes, probabilidad total en tablas y árboles.
Errores: contar mal los casos posibles, sumar probabilidades de sucesos compatibles sin restar la intersección, olvidar que sin reemplazamiento cambia el total.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, fq, d, num, unit, L, Kids, tabla

R = None
LV = 1
K = None
PALOS = ["oros", "copas", "espadas", "bastos"]


def P(x):
    return fq(F(x))


def W3(ok, *xs):
    out = []
    for x in xs:
        x = F(x)
        if x != ok and 0 <= x <= 1 and x not in out:
            out.append(x)
    return [P(x) for x in out]


def s_conceptos():
    q, a, w = R.choice([("Lanzar un dado y anotar el número es un experimento…", "aleatorio", ["determinista", "imposible", "seguro"]),
                        ("Calentar agua a 100 °C a nivel del mar y ver si hierve es un experimento…", "determinista", ["aleatorio", "imposible", "compuesto"]),
                        ("¿Cuál es el espacio muestral al lanzar una moneda?", "E = {cara, cruz}", ["E = {cara}", "E = {1, 2}", "E = {cara, cruz, canto}"]),
                        ("¿Cuántos elementos tiene el espacio muestral al lanzar un dado?", "6", ["1", "12", "36"]),
                        ("¿Cuántos resultados posibles hay al lanzar dos monedas?", "4", ["2", "3", "8"]),
                        ("¿Cuántos resultados posibles hay al lanzar dos dados?", "36", ["12", "6", "11"]),
                        ("¿Cuál es el suceso contrario de «sacar par» al lanzar un dado?", "sacar impar", ["sacar un 6", "sacar par", "no lanzar"]),
                        ("Un suceso que ocurre siempre se llama…", "suceso seguro", ["suceso imposible", "suceso elemental", "suceso contrario"]),
                        ("¿Cuánto vale la probabilidad de un suceso imposible?", "0", ["1", "1/2", "−1"]),
                        ("¿Cuánto vale la probabilidad de un suceso seguro?", "1", ["0", "100", "1/2"]),
                        ("¿Cuántas cartas tiene la baraja española?", "40", ["48", "52", "36"]),
                        ("En la baraja española, ¿cuántas cartas hay de cada palo?", "10", ["12", "13", "4"]),
                        ("Si P(A) = 0,3, ¿cuánto vale P(no A)?", "0,7", ["0,3", "1,3", "0,03"]),
                        ("Sacar un 7 al lanzar un dado normal es un suceso…", "imposible", ["seguro", "probable", "elemental"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_laplace():
    t = R.choice(["dado", "urna", "urna", "ruleta", "baraja", "baraja"])
    if t == "dado":
        ev, n = R.choice([("un número par", 3), ("un múltiplo de 3", 2), ("un número mayor que 4", 2), ("un número menor que 5", 4), ("un número primo", 3), ("un divisor de 6", 4), ("un 6", 1), ("un número mayor que 1", 5)])
        p = F(n, 6)
        return M("Lanzamos un dado. ¿Cuál es la probabilidad de sacar %s?" % ev, P(p), W3(p, F(n, 12), 1 - p, F(1, 6) if p != F(1, 6) else F(1, 3), F(n + 1, 6)), "Casos favorables %d de 6: <b>%s</b>." % (n, P(p)))
    if t == "urna":
        cols = R.sample(["rojas", "azules", "verdes", "blancas", "negras"], 3)
        ns = [R.randint(1, 9) for _ in cols]
        i = R.randrange(3)
        tot = sum(ns)
        p = F(ns[i], tot)
        return M("Una urna tiene %d bolas %s, %d %s y %d %s. Sacamos una al azar. ¿Cuál es la probabilidad de que sea %s?" % (ns[0], cols[0], ns[1], cols[1], ns[2], cols[2], cols[i][:-1] if cols[i] != "azules" else "azul"),
                 P(p), W3(p, F(ns[i], tot - ns[i]) if tot != 2 * ns[i] else F(1, 3), 1 - p, F(1, 3), F(ns[i], 10)), "%d favorables de %d posibles: <b>%s</b>." % (ns[i], tot, P(p)))
    if t == "ruleta":
        n = R.choice([4, 5, 6, 8, 10])
        k = R.randint(1, n - 1)
        p = F(k, n)
        return M("Una ruleta tiene %d sectores iguales y %d son rojos. ¿Cuál es la probabilidad de que salga rojo?" % (n, k), P(p), W3(p, F(k, n - k) if n != 2 * k else F(1, 3), 1 - p, F(1, n), F(k + 1, n)), "<b>%s</b>." % P(p))
    ev, n = R.choice([("un as", 4), ("una carta de oros", 10), ("una figura (sota, caballo o rey)", 12), ("el rey de copas", 1), ("una carta que no sea de espadas", 30), ("un 7", 4), ("una figura de bastos", 3), ("un número menor que 4", 12)])
    p = F(n, 40)
    return M("Sacamos una carta de una baraja española de 40 cartas. ¿Cuál es la probabilidad de que sea %s?" % ev, P(p), W3(p, F(n, 48), F(n, 52), 1 - p, F(1, 40) if n != 1 else F(1, 10)), "%d casos favorables de 40: <b>%s</b>." % (n, P(p)))


def s_frecuencia():
    n = R.choice([50, 100, 200, 400, 500])
    k = R.randint(n // 10, n // 2)
    t = R.choice(["fr", "estima", "gn"])
    if t == "fr":
        p = F(k, n)
        return M("Lanzamos una chincheta %d veces y cae con la punta hacia arriba %d veces. ¿Cuál es la frecuencia relativa de «punta arriba»?" % (n, k), d(p) if p.denominator in (1, 2, 4, 5, 10, 20, 25, 50, 100, 125, 250, 500) else P(p),
                 [str(k), d(F(n - k, n)) if F(n - k, n).denominator in (2, 4, 5, 10, 20, 25, 50, 100, 125, 250, 500) else P(1 - p), d(F(k, 1000))], "f = %d / %d = <b>%s</b>." % (k, n, d(p) if p.denominator in (1, 2, 4, 5, 10, 20, 25, 50, 100, 125, 250, 500) else P(p)))
    if t == "estima":
        p = F(R.choice([1, 2, 3]), R.choice([4, 5, 10]))
        m = R.choice([200, 300, 500, 1000])
        if (p * m).denominator != 1:
            return None
        return M("La probabilidad de que un tornillo salga defectuoso es %s. ¿Cuántos defectuosos esperamos en %d tornillos?" % (P(p), m), str(int(p * m)), [str(int(p * m) * 2), str(m - int(p * m)), str(p.numerator)], "%s · %d = <b>%d</b>." % (P(p), m, int(p * m)))
    q, a, w = R.choice([("Al repetir un experimento muchas veces, la frecuencia relativa de un suceso…", "se acerca a su probabilidad", ["se aleja de su probabilidad", "vale siempre 1", "es siempre 0,5"]),
                        ("Lanzamos una moneda 10 veces y sale cara 7 veces. ¿Está trucada seguro?", "no: con pocas tiradas pueden salir resultados así", ["sí, seguro", "sí, porque 7 &gt; 5", "no, porque las monedas no se trucan"]),
                        ("Si ha salido cruz 5 veces seguidas, la probabilidad de cara en la siguiente tirada es…", "1/2", ["mayor que 1/2", "menor que 1/2", "1"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_contrario():
    t = R.choice(["contra", "union", "union", "dos_dados", "monedas"])
    if t == "contra":
        p = F(R.randint(1, 19), 20)
        return M("La probabilidad de que llueva mañana es %s. ¿Cuál es la probabilidad de que no llueva?" % d(p), d(1 - p), [d(p), d(1 - p + F(1, 10)) if 1 - p + F(1, 10) <= 1 else d(F(1, 2)), d(p / 2)], "P(no A) = 1 − P(A) = <b>%s</b>." % d(1 - p))
    if t == "union":
        A, B = R.choice([(("par", {2, 4, 6}), ("mayor que 3", {4, 5, 6})), (("múltiplo de 3", {3, 6}), ("impar", {1, 3, 5})), (("primo", {2, 3, 5}), ("par", {2, 4, 6})), (("menor que 3", {1, 2}), ("mayor que 4", {5, 6})), (("par", {2, 4, 6}), ("1", {1}))])
        p = F(len(A[1] | B[1]), 6)
        return M("Lanzamos un dado. ¿Cuál es la probabilidad de sacar un número %s o %s?" % (A[0], B[0]), P(p), W3(p, F(len(A[1]) + len(B[1]), 6), F(len(A[1] & B[1]), 6), F(len(A[1]), 6) * F(len(B[1]), 6), 1 - p),
                 "P(A ∪ B) = P(A) + P(B) − P(A ∩ B) = %s: <b>%s</b>." % (", ".join(map(str, sorted(A[1] | B[1]))), P(p)))
    if t == "dos_dados":
        s = R.randint(2, 12)
        n = 6 - abs(7 - s)
        p = F(n, 36)
        return M("Lanzamos dos dados y sumamos los puntos. ¿Cuál es la probabilidad de que la suma sea %d?" % s, P(p), W3(p, F(1, 11), F(n, 12), F(1, 36) if n != 1 else F(1, 6), F(n, 6)), "Hay %d parejas que suman %d de 36: <b>%s</b>." % (n, s, P(p)))
    k = R.randint(0, 3)
    from math import comb
    p = F(comb(3, k), 8)
    return M("Lanzamos tres monedas. ¿Cuál es la probabilidad de obtener exactamente %d cara%s?" % (k, "" if k == 1 else "s"), P(p), W3(p, F(1, 4), F(1, 8) if p != F(1, 8) else F(3, 8), F(k, 3), F(1, 2)), "Hay %d casos de 8: <b>%s</b>." % (comb(3, k), P(p)))


def s_arbol():
    a, b = R.randint(2, 7), R.randint(2, 7)
    n = a + b
    t = R.choice(["con", "sin", "sin", "distinto", "moneda_dado"])
    if t == "con":
        p = F(a, n) ** 2
        return M("Una urna tiene %d bolas rojas y %d azules. Sacamos una, la devolvemos y sacamos otra. ¿Probabilidad de que las dos sean rojas?" % (a, b), P(p), W3(p, F(a, n) * F(a - 1, n - 1), F(2 * a, n), F(a, n), F(a * a, n)),
                 "Con reemplazamiento: %s · %s = <b>%s</b>." % (P(F(a, n)), P(F(a, n)), P(p)))
    if t == "sin":
        p = F(a, n) * F(a - 1, n - 1)
        return M("Una urna tiene %d bolas rojas y %d azules. Sacamos dos bolas sin devolver la primera. ¿Probabilidad de que las dos sean rojas?" % (a, b), P(p), W3(p, F(a, n) ** 2, F(a - 1, n), F(a, n), F(a * (a - 1), n * n)),
                 "Sin reemplazamiento: %s · %s = <b>%s</b>." % (P(F(a, n)), P(F(a - 1, n - 1)), P(p)))
    if t == "distinto":
        p = 2 * F(a, n) * F(b, n - 1)
        return M("Una urna tiene %d bolas rojas y %d azules. Sacamos dos sin reemplazamiento. ¿Probabilidad de que sean de distinto color?" % (a, b), P(p), W3(p, F(a, n) * F(b, n - 1), 2 * F(a, n) * F(b, n), F(1, 2), 1 - p),
                 "Dos ramas: RA y AR. %s + %s = <b>%s</b>." % (P(F(a, n) * F(b, n - 1)), P(F(b, n) * F(a, n - 1)), P(p)))
    ev, k = R.choice([("cara y un 6", 1), ("cruz y un número par", 3), ("cara y un número mayor que 2", 4), ("cruz y un múltiplo de 3", 2)])
    p = F(1, 2) * F(k, 6)
    return M("Lanzamos una moneda y un dado. ¿Probabilidad de obtener %s?" % ev, P(p), W3(p, F(1, 2) + F(k, 6), F(k, 6), F(1, 8), F(k, 8)), "Son independientes: 1/2 · %s = <b>%s</b>." % (P(F(k, 6)), P(p)))


def s_tabla():
    a, b, c, e = [R.randint(4, 25) for _ in range(4)]
    tot = a + b + c + e
    pic = tabla(["", "Usa gafas", "No usa gafas", "Total"], [["Chicas", str(a), str(b), str(a + b)], ["Chicos", str(c), str(e), str(c + e)], ["Total", str(a + c), str(b + e), str(tot)]])
    t = R.choice(["simple", "inter", "cond", "cond2"] if LV >= 4 else ["simple", "inter", "simple", "inter"])
    if t == "simple":
        p = F(a + c, tot)
        return M(pic + "Elegimos una persona al azar. ¿Probabilidad de que use gafas?", P(p), W3(p, F(a, tot), F(a + c, a + b), F(b + e, tot), F(a, a + c)), "%d de %d: <b>%s</b>." % (a + c, tot, P(p)))
    if t == "inter":
        p = F(a, tot)
        return M(pic + "Elegimos una persona al azar. ¿Probabilidad de que sea chica y use gafas?", P(p), W3(p, F(a, a + b), F(a, a + c), F(a + b, tot) * F(a + c, tot) if F(a + b, tot) * F(a + c, tot) != p else F(1, 2), F(a + b, tot)),
                 "Casilla chica–gafas: %d de %d: <b>%s</b>." % (a, tot, P(p)))
    if t == "cond":
        p = F(a, a + b)
        return M(pic + "Elegimos una chica al azar. ¿Probabilidad de que use gafas? Es P(gafas | chica).", P(p), W3(p, F(a, tot), F(a, a + c), F(a + c, tot), F(b, a + b)), "Solo miramos la fila de chicas: %d de %d = <b>%s</b>." % (a, a + b, P(p)))
    p = F(c, a + c)
    return M(pic + "Elegimos al azar a una persona que usa gafas. ¿Probabilidad de que sea chico? Es P(chico | gafas).", P(p), W3(p, F(c, tot), F(c, c + e), F(c + e, tot), F(a, a + c)), "Solo la columna de gafas: %d de %d = <b>%s</b>." % (c, a + c, P(p)))


def s_condicionada():
    t = R.choice(["formula", "indep", "total", "dados"])
    if t == "formula":
        pb = F(R.randint(2, 8), 10)
        pab = pb * F(R.randint(1, 4), 5)
        p = pab / pb
        return M("Si P(A ∩ B) = %s y P(B) = %s, ¿cuánto vale P(A | B)?" % (d(pab), d(pb)), d(p) if p.denominator in (1, 2, 4, 5, 10, 20, 25, 50) else P(p),
                 [d(pab * pb), d(pb / pab) if pb / pab <= 1 and (pb / pab).denominator in (1, 2, 4, 5, 10) else P(1 - p), d(pab)], "P(A | B) = P(A ∩ B) / P(B) = <b>%s</b>." % (d(p) if p.denominator in (1, 2, 4, 5, 10, 20, 25, 50) else P(p)))
    if t == "indep":
        pa, pb = F(R.randint(1, 9), 10), F(R.randint(1, 9), 10)
        ok = R.random() < 0.5
        pab = pa * pb if ok else pa * pb + F(R.choice([1, 2, 3]), 100)
        if pab > min(pa, pb):
            return None
        return M("P(A) = %s, P(B) = %s y P(A ∩ B) = %s. ¿Son A y B independientes?" % (d(pa), d(pb), d(pab)), "sí" if ok else "no", ["no" if ok else "sí", "solo si P(A) = P(B)", "no se puede saber"],
                 "P(A) · P(B) = %s %s P(A ∩ B): <b>%s</b>." % (d(pa * pb), "=" if ok else "≠", "son independientes" if ok else "no son independientes"))
    if t == "total":
        p1 = F(R.randint(3, 7), 10)
        a1, a2 = F(R.randint(1, 9), 10), F(R.randint(1, 9), 10)
        p = p1 * a1 + (1 - p1) * a2
        return M("El %s %% de los alumnos va en autobús. De ellos, llega tarde el %s %%; de los demás, el %s %%. ¿Qué probabilidad hay de que un alumno al azar llegue tarde?" % (d(p1 * 100), d(a1 * 100), d(a2 * 100)),
                 d(p), [d(a1 + a2), d((a1 + a2) / 2), d(p1 * a1)], "Probabilidad total: %s · %s + %s · %s = <b>%s</b>." % (d(p1), d(a1), d(1 - p1), d(a2), d(p)))
    s = R.randint(4, 10)
    fav = [(i, j) for i in range(1, 7) for j in range(1, 7) if i + j == s]
    k = R.choice([1, 2, 3, 4, 5, 6])
    cond = [x for x in fav if x[0] == k]
    p = F(len(cond), 6)
    q = F(len(fav), 36)
    if not cond:
        return None
    return M("Lanzamos dos dados. Sabiendo que el primero ha salido %d, ¿qué probabilidad hay de que la suma sea %d?" % (k, s), P(p), W3(p, q, F(1, 36), F(1, 2), F(len(cond), 36)), "Si el primero es %d, el segundo debe ser %d: 1 caso de 6, <b>%s</b>." % (k, s - k, P(p)))


def build(lv):
    global R, LV, K
    LV = lv
    R = random.Random(47014 + (lv - 1) * 1000)
    K = Kids(R)
    seen = set()
    if lv == 1:
        sets = [("Experimentos y sucesos", mix(R, seen, [(s_conceptos, 12), (s_contrario, 8)])), ("Regla de Laplace", mix(R, seen, [(s_laplace, 20)])), ("Dados, urnas y barajas", mix(R, seen, [(s_laplace, 20)])),
                ("Frecuencia relativa", mix(R, seen, [(s_frecuencia, 20)])), ("Suceso contrario y repaso", mix(R, seen, [(s_contrario, 10), (s_laplace, 10)]))]
        think = ["Un experimento es <b>aleatorio</b> si no se puede saber el resultado antes de hacerlo. El <b>espacio muestral</b> es el conjunto de todos los resultados.",
                 "<b>Regla de Laplace</b>: si todos los resultados son igual de probables, P(A) = casos favorables / casos posibles.",
                 "La probabilidad está entre 0 (imposible) y 1 (seguro). P(no A) = 1 − P(A)."]
        slug, title, kb, ks, sort = "probabilidad", "Probabilidad y regla de Laplace", "P(A) = favorables / posibles", "Siempre entre 0 y 1.", 14
        meta = "Fichas de matemáticas de 1.º de ESO: experimentos aleatorios, espacio muestral, regla de Laplace con dados, urnas y baraja española. 100 ejercicios con soluciones."
        std = "Fenómenos aleatorios; espacio muestral y sucesos; asignación de probabilidades mediante la regla de Laplace y mediante frecuencias relativas"
    elif lv == 2:
        sets = [("Regla de Laplace", mix(R, seen, [(s_laplace, 20)])), ("Suceso contrario y unión", mix(R, seen, [(s_contrario, 20)])), ("Dos dados y monedas", mix(R, seen, [(s_contrario, 10), (s_laplace, 10)])),
                ("Frecuencia y probabilidad", mix(R, seen, [(s_frecuencia, 20)])), ("Repaso", mix(R, seen, [(s_conceptos, 12), (s_laplace, 8)]))]
        think = ["P(A) = casos favorables / casos posibles, si todos los casos son igual de probables.", "P(no A) = 1 − P(A).",
                 "Unión: P(A ∪ B) = P(A) + P(B) − P(A ∩ B). Si A y B no tienen casos comunes, basta con sumar.",
                 "Al repetir un experimento muchas veces, la frecuencia relativa se acerca a la probabilidad."]
        slug, title, kb, ks, sort = "probabilidad", "Probabilidad: sucesos y Laplace", "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)", "P(no A) = 1 − P(A).", 13
        meta = "Fichas de matemáticas de 2.º de ESO: regla de Laplace, suceso contrario, unión de sucesos, dos dados y frecuencia relativa. 100 ejercicios con soluciones."
        std = "Experimentos aleatorios; regla de Laplace; suceso contrario, unión e intersección; frecuencia relativa y ley de los grandes números"
    elif lv == 3:
        sets = [("Regla de Laplace", mix(R, seen, [(s_laplace, 20)])), ("Unión y suceso contrario", mix(R, seen, [(s_contrario, 20)])), ("Diagramas de árbol", mix(R, seen, [(s_arbol, 20)])),
                ("Con y sin reemplazamiento", mix(R, seen, [(s_arbol, 20)])), ("Tablas de contingencia", mix(R, seen, [(s_tabla, 20)]))]
        think = ["En un <b>experimento compuesto</b> se multiplican las probabilidades a lo largo de cada rama del árbol y se suman las ramas que interesan.",
                 "<b>Con reemplazamiento</b>, la urna vuelve a estar igual. <b>Sin reemplazamiento</b>, cambian el número de bolas y el total.",
                 "En una <b>tabla de contingencia</b>, P(A ∩ B) es la casilla dividida entre el total."]
        slug, title, kb, ks, sort = "probabilidad", "Probabilidad: experimentos compuestos", "Árbol: multiplica por cada rama", "Y suma las ramas que buscas.", 12
        meta = "Fichas de matemáticas de 3.º de ESO: Laplace, unión de sucesos, diagramas de árbol, extracciones con y sin reemplazamiento y tablas de contingencia. 100 ejercicios con soluciones."
        std = "Experimentos simples y compuestos; diagramas de árbol y tablas de contingencia; cálculo de probabilidades"
    else:
        sets = [("Tablas de contingencia", mix(R, seen, [(s_tabla, 20)])), ("Probabilidad condicionada", mix(R, seen, [(s_condicionada, 20)])), ("Diagramas de árbol", mix(R, seen, [(s_arbol, 20)])),
                ("Independencia y probabilidad total", mix(R, seen, [(s_condicionada, 20)])), ("Repaso", mix(R, seen, [(s_contrario, 10), (s_tabla, 10)]))]
        think = ["P(A | B) es la probabilidad de A sabiendo que ha ocurrido B: P(A | B) = P(A ∩ B) / P(B).",
                 "A y B son <b>independientes</b> si P(A ∩ B) = P(A) · P(B).",
                 "<b>Probabilidad total</b>: se suman las probabilidades de todas las ramas que llevan al suceso."]
        slug, title, kb, ks, sort = "probabilidad", "Probabilidad condicionada", "P(A | B) = P(A ∩ B) / P(B)", "Independientes: P(A ∩ B) = P(A) · P(B).", 13
        meta = "Fichas de matemáticas de 4.º de ESO: tablas de contingencia, probabilidad condicionada, independencia, árboles y probabilidad total. 100 ejercicios con soluciones."
        std = "Probabilidad condicionada; sucesos dependientes e independientes; diagramas de árbol y tablas de contingencia; probabilidad total"
    ex = [("Urna con 3 rojas y 2 azules: dos rojas sin reemplazamiento", ["3/5 · 2/4"], "6/20 = 3/10"), ("Dado: sacar par o mayor que 4", ["{2, 4, 5, 6}"], "4/6 = 2/3")]
    mist = [["Contar mal los casos posibles", "Con dos dados hay 36 casos, no 12."], ["Sumar sin restar la intersección", "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)."], ["Olvidar que sin reemplazamiento cambia el total", "Tras sacar una bola, quedan una menos."]]
    body = L(think, ex, mist)
    faq = [("¿Qué dice la regla de Laplace?", "Que, si todos los resultados son igual de probables, la probabilidad es el número de casos favorables dividido entre el de casos posibles."),
           ("¿Cómo es la baraja española?", "Tiene 40 cartas de cuatro palos (oros, copas, espadas y bastos): del 1 al 7, sota, caballo y rey.")]
    unit(lv, R, slug, "S", std, title, "Probabilidad", meta, kb, ks, body, faq, sets, sort)


if __name__ == "__main__":
    build(1)
