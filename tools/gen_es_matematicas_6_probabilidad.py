# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Probabilidad (Sentido estocástico)
Sucesos seguros, posibles e imposibles; regla de Laplace (casos favorables / casos posibles) con dados, monedas, bolsas, ruletas y cartas;
probabilidad como fracción, decimal y porcentaje; contar casos con diagramas de árbol; frecuencia relativa en experimentos.
Errores: contar mal los casos posibles, pensar que un resultado es más probable porque ha salido menos, olvidar casos en el árbol.
"""
import random
from fractions import Fraction as F
from es_c3 import M, mix, lesson, make_unit, num, d, fr, fq
from es_common import use

R = None
LV = 6


def s1_laplace():
    k = R.choice(["dado", "dado", "baraja", "letras", "numeros"])
    if k == "dado":
        q, f = R.choice([("un número par", 3), ("un número mayor que 4", 2), ("un múltiplo de 3", 2), ("un número primo", 3), ("un 6", 1), ("un número menor que 5", 4), ("un divisor de 6", 4), ("un número impar mayor que 1", 2)])
        return M("Lanzas un dado de seis caras. ¿Qué probabilidad hay de sacar %s?" % q, fq(F(f, 6)), [fr(f + 1, 6), fq(F(6 - f, 6)), fr(1, f) if f > 1 else fr(1, 2), fr(f, 12)],
                 "Casos favorables: %d; posibles: 6. P = %s%s." % (f, fr(f, 6), " = <b>%s</b>" % fq(F(f, 6)) if F(f, 6).denominator != 6 else ""))
    if k == "baraja":
        q, f = R.choice([("una carta de oros", 10), ("un as", 4), ("una figura (sota, caballo o rey)", 12), ("el rey de copas", 1), ("una carta que no sea de espadas", 30), ("un 7", 4)])
        return M("En una baraja española de 40 cartas, sacas una al azar. ¿Qué probabilidad hay de sacar %s?" % q, fq(F(f, 40)), [fq(F(40 - f, 40)), fr(f, 48) if f != 1 else fr(1, 4), fr(1, f) if f > 1 else fr(1, 10), fq(F(f, 10)) if f < 10 else fr(f, 52)],
                 "Favorables: %d; posibles: 40. P = %s = <b>%s</b>." % (f, fr(f, 40), fq(F(f, 40))))
    if k == "letras":
        w = R.choice(["MATEMÁTICAS", "ESPAÑA", "PROBABILIDAD", "CALCULADORA", "ESTADÍSTICA"])
        L = R.choice(sorted(set(w)))
        f = w.count(L)
        return M("Escribimos cada letra de la palabra %s en una tarjeta y sacamos una al azar. ¿Qué probabilidad hay de sacar una %s?" % (w, L), fq(F(f, len(w))), [fr(1, len(set(w))), fq(F(len(w) - f, len(w))), fr(f, len(w) + 1)],
                 "Hay %d %s entre %d letras: <b>%s</b>." % (f, L, len(w), fq(F(f, len(w)))))
    n = R.choice([10, 20, 30, 50])
    q, cond = R.choice([("un número par", lambda x: x % 2 == 0), ("un múltiplo de 5", lambda x: x % 5 == 0), ("un número de dos cifras", lambda x: x >= 10), ("un múltiplo de 3", lambda x: x % 3 == 0)])
    f = sum(1 for x in range(1, n + 1) if cond(x))
    return M("En una urna hay %d bolas numeradas del 1 al %d. ¿Qué probabilidad hay de sacar %s?" % (n, n, q), fq(F(f, n)), [fq(F(n - f, n)), fr(f, 100) if n != 100 else fr(f, 10), fr(1, f) if f > 1 else fr(1, 2)],
             "Favorables: %d; posibles: %d. P = <b>%s</b>." % (f, n, fq(F(f, n))))


def s2_formas():
    p = R.choice([F(1, 2), F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(1, 10), F(3, 10), F(7, 10), F(1, 20), F(3, 20), F(1, 25)])
    k = R.choice(["dec", "pc", "dec"])
    if k == "dec":
        return M("Escribe la probabilidad %s como número decimal." % fq(p), d(p), [d(p * 10) if p * 10 < 1 else d(p / 10), "%d,%d" % (p.numerator, p.denominator), d(1 - p)], "%d : %d = <b>%s</b>." % (p.numerator, p.denominator, d(p)))
    return M("Escribe la probabilidad %s como porcentaje." % fq(p), "%s %%" % d(p * 100), ["%s %%" % d(p * 10), "%d %%" % p.denominator, "%s %%" % d(100 - p * 100)], "%s = %s = <b>%s %%</b>." % (fq(p), fr(int(p * 100), 100) if (p * 100).denominator == 1 else d(p), d(p * 100)))


def s3_arbol():
    k = R.choice(["monedas", "dado_moneda", "menu", "ropa", "dos_monedas_p"])
    if k == "monedas":
        n = R.choice([2, 3])
        return M("Lanzamos %d monedas. ¿Cuántos resultados posibles hay?" % n, str(2 ** n), [str(2 * n), str(n), str(2 ** n + 1)], "Cada moneda tiene 2 resultados: %s = <b>%d</b>." % (" × ".join(["2"] * n), 2 ** n))
    if k == "dado_moneda":
        return M("Lanzamos un dado y una moneda. ¿Cuántos resultados posibles hay?", "12", ["8", "6", "2"], "6 × 2 = <b>12</b>.")
    if k == "menu":
        a, b, c = R.randint(2, 4), R.randint(2, 4), R.randint(1, 3)
        return M("Un menú tiene %d primeros, %d segundos y %d postres. ¿Cuántos menús distintos se pueden elegir?" % (a, b, c), str(a * b * c), [str(a + b + c), str(a * b), str(a * b * c + 1)], "Diagrama de árbol: %d × %d × %d = <b>%d</b>." % (a, b, c, a * b * c))
    if k == "ropa":
        a, b = R.randint(2, 5), R.randint(2, 4)
        return M("Vega tiene %d camisetas y %d pantalones. ¿Cuántos conjuntos distintos puede formar?" % (a, b), str(a * b), [str(a + b), str(a * b - 1), str(2 * a * b)], "%d × %d = <b>%d</b>." % (a, b, a * b))
    q, f = R.choice([("dos caras", 1), ("una cara y una cruz (en cualquier orden)", 2), ("al menos una cruz", 3)])
    return M("Lanzamos dos monedas. ¿Qué probabilidad hay de obtener %s?" % q, fq(F(f, 4)), [fr(1, 3), fq(F(4 - f, 4)) if f != 2 else fr(1, 3) + "", fr(f, 2) if f < 2 else fr(1, 4)],
             "Resultados: CC, CX, XC, XX (4). Favorables: %d → <b>%s</b>." % (f, fq(F(f, 4))))


def s4_frecuencia():
    n = R.choice([20, 40, 50, 100, 200])
    k = R.choice(["rel", "prev", "compara"])
    if k == "rel":
        c = R.randint(1, n - 1)
        return M("Lanzamos una chincheta %d veces y cae con la punta hacia arriba %d veces. ¿Cuál es la frecuencia relativa de «punta arriba»?" % (n, c), fq(F(c, n)), [fr(c, 100) if n != 100 else fr(c, 10), fq(F(n - c, n)), fr(n, c) if c else None],
                 "%d de %d: <b>%s</b>." % (c, n, fq(F(c, n))))
    if k == "prev":
        p = R.choice([F(1, 2), F(1, 4), F(1, 5), F(1, 10), F(1, 6)])
        m = R.choice([60, 120, 300, 600]) if p.denominator == 6 else R.choice([40, 100, 200, 400])
        return M("La probabilidad de que una ruleta pare en rojo es %s. Si la giramos %d veces, ¿cuántas veces esperamos que salga rojo, aproximadamente?" % (fq(p), m), num(int(p * m)), [num(int(p * m) * 2), num(m), num(p.denominator)],
                 "%s de %d = <b>%s</b> (aproximadamente)." % (fq(p), m, num(int(p * m))))
    return M("Una moneda ha salido cara 5 veces seguidas. En el siguiente lanzamiento, ¿qué es más probable?", "las dos cosas son igual de probables", ["cruz, porque toca", "cara, porque está saliendo", "no se puede lanzar"],
             "La moneda no recuerda los lanzamientos anteriores: cara y cruz tienen probabilidad %s." % fr(1, 2))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40022 + lv * 1000)
    suc, comp, frac = use("gen_es_matematicas_4_probabilidad", 40122 + lv * 1000, "s1_sucesos", "s2_comparar", "s3_fraccion")
    seen = set()
    sets = [
        ("Seguro, posible, imposible y más probable", mix(R, seen, [(suc, 10), (comp, 10)])),
        ("Regla de Laplace", mix(R, seen, [(s1_laplace, 14), (frac, 6)])),
        ("Probabilidad como decimal y porcentaje", mix(R, seen, [(s2_formas, 12), (s1_laplace, 8)])),
        ("Contar casos con diagramas de árbol", mix(R, seen, [(s3_arbol, 20)])),
        ("Experimentos y frecuencias", mix(R, seen, [(s4_frecuencia, 20)])),
    ]
    body = lesson(
        ["Un suceso es <b>seguro</b> si ocurre siempre, <b>imposible</b> si no ocurre nunca y <b>posible</b> si puede ocurrir o no.",
         "<b>Regla de Laplace</b>: si todos los resultados son igual de probables, P = casos favorables / casos posibles. La probabilidad está entre 0 (imposible) y 1 (seguro).",
         "Para contar los casos posibles puedes hacer un <b>diagrama de árbol</b> o multiplicar las opciones de cada paso."],
        [("Sacar un número primo con un dado", ["Primos: 2, 3, 5 → 3 casos", "Posibles: 6"], "%s = %s = 0,5" % (fr(3, 6), fr(1, 2))),
         ("Lanzar dos monedas", ["2 × 2 = 4 resultados: CC, CX, XC, XX"], "4")],
        [["Contar mal los casos posibles", "Con dos monedas hay 4 resultados, no 3: CX y XC son distintos."],
         ["Creer que «ya toca»", "Los lanzamientos anteriores no cambian la probabilidad."],
         ["Probabilidad mayor que 1", "Si te sale más de 1, revisa: favorables nunca supera a posibles."]])
    faq = [("¿Qué es la regla de Laplace?", "Una forma de calcular probabilidades cuando todos los resultados son igual de probables: se divide el número de casos favorables entre el número de casos posibles."),
           ("¿Qué valores puede tomar una probabilidad?", "Entre 0 y 1. Un suceso imposible tiene probabilidad 0 y uno seguro, 1. También se puede expresar en porcentaje, de 0 % a 100 %.")]
    make_unit(R, "probabilidad", "S",
              "Incertidumbre y probabilidad: sucesos seguros, posibles e imposibles; regla de Laplace; probabilidad expresada como fracción, decimal y porcentaje; recuento de casos con diagramas de árbol; frecuencia relativa en experimentos aleatorios",
              "Probabilidad: la regla de Laplace", "Probabilidad",
              "Fichas de matemáticas de %d.º de Primaria: sucesos seguros, posibles e imposibles, regla de Laplace, probabilidad como fracción, decimal y porcentaje, diagramas de árbol y experimentos. 100 ejercicios con soluciones." % lv,
              "Favorables / posibles", "Entre 0 (imposible) y 1 (seguro).",
              body, faq, sets, 22, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
