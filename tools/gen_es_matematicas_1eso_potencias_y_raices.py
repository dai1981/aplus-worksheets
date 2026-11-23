# -*- coding: utf-8 -*-
"""
España Matemáticas 1.º de ESO: Potencias y raíces cuadradas (Sentido numérico)
Potencias de base natural y entera, propiedades (producto, cociente, potencia de potencia), potencias de 10, raíz cuadrada exacta y entera.
Errores: multiplicar base por exponente (2⁵ = 10), sumar exponentes al sumar potencias, confundir raíz cuadrada y mitad.
"""
import random
from es_eso import M, mix, sg, num, sup, unit, L, Kids, nz, table

R = random.Random(47003)
K = Kids(R)


def pw(b, e):
    return ("(%s)" % sg(b) if b < 0 else str(b)) + sup(e) if e != 1 else ("(%s)" % sg(b) if b < 0 else str(b)) + "¹"


def s_valor():
    t = R.choice(["calc", "calc", "neg", "escribe", "10"])
    if t == "calc":
        b, e = R.randint(2, 9), R.randint(2, 4)
        if b ** e > 10000:
            return None
        return M("Calcula: %s" % pw(b, e), num(b ** e), [num(b * e), num(b ** (e - 1)), num(e ** b) if e ** b != b ** e else num(b ** e + b)], "%s = %s = <b>%s</b>." % (pw(b, e), " · ".join([str(b)] * e), num(b ** e)))
    if t == "neg":
        b, e = R.randint(-6, -2), R.randint(2, 5)
        return M("Calcula: %s" % pw(b, e), sg(b ** e), [sg(-(b ** e)), sg(b * e), sg(abs(b) ** e + 1)], "Base negativa: exponente %s, resultado %s: <b>%s</b>." % ("par" if e % 2 == 0 else "impar", "positivo" if e % 2 == 0 else "negativo", sg(b ** e)))
    if t == "escribe":
        b, e = R.randint(2, 12), R.randint(3, 7)
        prod = " · ".join([str(b)] * e)
        return M("¿Cómo se escribe %s como potencia?" % prod, pw(b, e), [pw(e, b), "%d · %d" % (b, e), pw(b, e - 1), pw(b, e + 1)], "El %d se repite %d veces: <b>%s</b>." % (b, e, pw(b, e)))
    e = R.randint(2, 7)
    n = 10 ** e
    return M("¿Cuánto vale 10%s?" % sup(e), num(n), [num(10 * e), num(n // 10), num(n * 10)], "Un 1 seguido de %d ceros: <b>%s</b>." % (e, num(n)))


def s_prop():
    b = R.randint(2, 9)
    m, n = R.randint(2, 9), R.randint(2, 9)
    t = R.choice(["prod", "coc", "pot", "mismo_exp", "cero"])
    if t == "prod":
        return M("Escribe como una sola potencia: %s · %s" % (pw(b, m), pw(b, n)), pw(b, m + n), [pw(b, m * n), pw(b * b, m + n), pw(b, abs(m - n)) if m != n else pw(b, m + n + 1)],
                 "Misma base: se suman los exponentes, %d + %d = %d: <b>%s</b>." % (m, n, m + n, pw(b, m + n)))
    if t == "coc":
        if m <= n:
            m, n = n + m, n
        return M("Escribe como una sola potencia: %s : %s" % (pw(b, m), pw(b, n)), pw(b, m - n), [pw(b, m + n), pw(1, m - n), pw(b, m // n) if m % n == 0 and m // n != m - n else pw(b, m - n + 1)],
                 "Misma base: se restan los exponentes, %d − %d = %d: <b>%s</b>." % (m, n, m - n, pw(b, m - n)))
    if t == "pot":
        m, n = R.randint(2, 5), R.randint(2, 5)
        return M("Escribe como una sola potencia: (%s)%s" % (pw(b, m), sup(n)), pw(b, m * n), [pw(b, m + n) if m + n != m * n else pw(b, m * n + 1), pw(b * n, m), pw(b, m ** n) if m ** n != m * n else pw(b, m * n + 2)],
                 "Potencia de una potencia: se multiplican los exponentes, %d · %d = %d: <b>%s</b>." % (m, n, m * n, pw(b, m * n)))
    if t == "mismo_exp":
        a, c, e = R.randint(2, 6), R.randint(2, 6), R.randint(2, 5)
        if a == c:
            return None
        return M("Escribe como una sola potencia: %s · %s" % (pw(a, e), pw(c, e)), pw(a * c, e), [pw(a * c, 2 * e), pw(a + c, e), pw(a, c * e)], "Mismo exponente: se multiplican las bases: <b>%s</b>." % pw(a * c, e))
    q, a, w = R.choice([("¿Cuánto vale %s⁰?" % b, "1", ["0", str(b), "no existe"]), ("¿Cuánto vale %s¹?" % b, str(b), ["1", "0", str(b * b)]),
                        ("¿Cuánto vale 1%s?" % sup(m), "1", [str(m), "0", str(m + 1)]), ("¿Cuánto vale 0%s?" % sup(m), "0", ["1", str(m), "no existe"])])
    return M(q, a, w, "Respuesta: <b>%s</b>." % a)


def s_raiz():
    t = R.choice(["exacta", "exacta", "entera", "entre", "cuad"])
    if t == "exacta":
        r = R.randint(4, 30)
        return M("Calcula: √%s" % num(r * r), num(r), [num(r * r // 2), num(r + 1), num(r * 2)], "%d · %d = %s: <b>%d</b>." % (r, r, num(r * r), r))
    if t == "entera":
        r = R.randint(4, 20)
        n = r * r + R.randint(1, 2 * r)
        return M("Calcula la raíz cuadrada entera de %d y su resto." % n, "raíz %d, resto %d" % (r, n - r * r), ["raíz %d, resto %d" % (r + 1, n - (r + 1) ** 2 if n > (r + 1) ** 2 else (r + 1) ** 2 - n), "raíz %d, resto %d" % (r, n - r * r + 1), "raíz %d, resto 0" % r],
                 "%d² = %d ≤ %d &lt; %d = %d². Resto: %d − %d = %d. Raíz <b>%d</b>, resto <b>%d</b>." % (r, r * r, n, (r + 1) ** 2, r + 1, n, r * r, n - r * r, r, n - r * r))
    if t == "entre":
        r = R.randint(3, 15)
        n = r * r + R.randint(1, 2 * r)
        return M("¿Entre qué dos números enteros está √%d?" % n, "entre %d y %d" % (r, r + 1), ["entre %d y %d" % (r - 1, r), "entre %d y %d" % (r + 1, r + 2), "entre %d y %d" % (n // 2 - 1, n // 2)],
                 "%d² = %d y %d² = %d: <b>entre %d y %d</b>." % (r, r * r, r + 1, (r + 1) ** 2, r, r + 1))
    n = R.randint(5, 25)
    return M("¿Cuál de estos números es un cuadrado perfecto: %s, %s, %s o %s?" % tuple(num(x) for x in sorted([n * n, n * n + 1, n * n - 2, (n + 1) * (n + 1) - 3])), num(n * n),
             [num(n * n + 1), num(n * n - 2), num((n + 1) * (n + 1) - 3)], "%d · %d = <b>%s</b>." % (n, n, num(n * n)))


def s_problema():
    p = K.next()[0]
    t = R.choice(["cajas", "cuadrado", "virus", "tablero", "cubo"])
    if t == "cajas":
        n = R.randint(4, 8)
        return M("En un almacén hay %d cajas. Cada caja tiene %d paquetes y cada paquete %d botes. ¿Cuántos botes hay? Escríbelo como potencia." % (n, n, n), "%s = %s" % (pw(n, 3), num(n ** 3)),
                 ["%s = %s" % (pw(n, 2), num(n ** 2)), "%d · 3 = %d" % (n, 3 * n), "%s = %s" % (pw(3, n), num(3 ** n))], "%d · %d · %d = <b>%s = %s</b>." % (n, n, n, pw(n, 3), num(n ** 3)))
    if t == "cuadrado":
        r = R.randint(5, 30)
        return M("Un jardín cuadrado tiene una superficie de %s m². ¿Cuánto mide su lado?" % num(r * r), "%d m" % r, ["%s m" % num(r * r // 4), "%d m" % (r * 2), "%d m" % (r + 2)], "√%s = <b>%d m</b>." % (num(r * r), r))
    if t == "virus":
        h = R.randint(3, 8)
        b = R.choice([2, 3])
        return M("Una bacteria se divide en %d cada hora. Si empezamos con 1, ¿cuántas habrá después de %d horas?" % (b, h), num(b ** h), [num(b * h), num(b ** (h - 1)), num(b ** h + 1)], "%s = <b>%s</b>." % (pw(b, h), num(b ** h)))
    if t == "tablero":
        n = R.randint(5, 15)
        return M("Un tablero cuadrado tiene %d casillas en cada lado. ¿Cuántas casillas tiene en total?" % n, num(n * n), [num(4 * n), num(2 * n), num(n * n + n)], "%d² = <b>%s</b>." % (n, num(n * n)))
    n = R.randint(2, 9)
    return M("%s forma un cubo grande con cubitos: %d de largo, %d de ancho y %d de alto. ¿Cuántos cubitos usa?" % (p, n, n, n), num(n ** 3), [num(3 * n), num(n * n), num(6 * n * n)], "%d³ = <b>%s</b>." % (n, num(n ** 3)))


seen = set()
sets = [("Calcular potencias", mix(R, seen, [(s_valor, 20)])), ("Propiedades de las potencias", mix(R, seen, [(s_prop, 20)])), ("Raíces cuadradas", mix(R, seen, [(s_raiz, 20)])),
        ("Repaso de potencias y raíces", mix(R, seen, [(s_valor, 7), (s_prop, 7), (s_raiz, 6)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
body = L(["Una <b>potencia</b> es una multiplicación de factores iguales: 2⁵ = 2 · 2 · 2 · 2 · 2 = 32. La base es 2 y el exponente, 5.",
          "Con la misma base: al multiplicar se suman los exponentes; al dividir, se restan. Potencia de potencia: se multiplican.",
          "La <b>raíz cuadrada</b> de 49 es 7 porque 7² = 49. Si no es exacta, buscamos el cuadrado más cercano por debajo."],
         [("3⁴ · 3² : 3³", ["3⁴⁺² = 3⁶", "3⁶⁻³ = 3³"], "3³ = 27"), ("√90", ["9² = 81 ≤ 90 &lt; 100 = 10²", "90 − 81 = 9"], "raíz entera 9, resto 9")],
         [["Multiplicar base por exponente", "2⁵ = 32, no 10."], ["Sumar exponentes al sumar potencias", "2³ + 2² = 8 + 4 = 12, no 2⁵."], ["Confundir la raíz con la mitad", "√16 = 4, no 8."]],
         table(["n", "1", "2", "3", "4", "5", "6"], [["n²", "1", "4", "9", "16", "25", "36"], ["n³", "1", "8", "27", "64", "125", "216"]]))
faq = [("¿Cuánto vale cualquier número elevado a 0?", "1, siempre que la base no sea 0. Por ejemplo, 7⁰ = 1."), ("¿Qué es un cuadrado perfecto?", "Un número que es el cuadrado de un entero, como 49 = 7².")]
unit(1, R, "potencias-y-raices", "N", "Potencias de exponente natural: significado y propiedades; potencias de base 10; raíz cuadrada exacta y entera",
     "Potencias y raíces cuadradas", "Potencias y raíces",
     "Fichas de matemáticas de 1.º de ESO: calcular potencias, propiedades de las potencias, potencias de 10, raíces cuadradas y problemas. 100 ejercicios con soluciones.",
     "Misma base: se suman los exponentes", "Al dividir, se restan.", body, faq, sets, 3)
