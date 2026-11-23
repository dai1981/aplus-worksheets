# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de Primaria: Fracciones equivalentes (Sentido numérico)
Reconocer fracciones equivalentes con dibujos, obtenerlas multiplicando o dividiendo numerador y denominador por el mismo número
(amplificar y simplificar), comprobar la equivalencia con productos cruzados, comparar fracciones con distinto denominador sencillo.
Errores: multiplicar solo el numerador, sumar el mismo número arriba y abajo.
"""
import random
from fractions import Fraction as Fr
from es_common import mcq, mix, lesson, make_unit, POR, DIV, fr, tira, circulo, Kids

R = random.Random(44011)
K = Kids(R)


def base():
    d = R.choice([2, 3, 4, 5, 6])
    n = R.randint(1, d - 1)
    if Fr(n, d).denominator != d:
        return None
    return n, d


def s1_dibujo():
    b = base()
    if not b:
        return None
    n, d = b
    m = R.choice([2, 3, 4])
    if d * m > 12:
        m = 2
    if d * m > 12:
        return None
    pic = "<div>%s%s</div>" % (tira(d, n, 260), tira(d * m, n * m, 260))
    return mcq(pic + "Las dos tiras tienen la misma parte coloreada. ¿Qué fracción es igual a %s?" % fr(n, d), fr(n * m, d * m),
               [fr(n + m, d + m), fr(n * m, d), fr(n, d * m), fr(n * m + 1, d * m)], "Se colorea lo mismo: %s = <b>%s</b>." % (fr(n, d), fr(n * m, d * m)))


def s2_amplificar():
    b = base()
    if not b:
        return None
    n, d = b
    m = R.randint(2, 6)
    k = R.choice(["fr", "num", "den"])
    if k == "fr":
        return mcq("¿Qué fracción es equivalente a %s?" % fr(n, d), fr(n * m, d * m), [fr(n + m, d + m), fr(n * m, d), fr(n, d * m), fr(d * m, n * m)],
                   "Multiplicamos numerador y denominador por %d: <b>%s</b>." % (m, fr(n * m, d * m)))
    if k == "num":
        return mcq("Completa para que sean equivalentes: %s = %s" % (fr(n, d), fr("?", d * m)), str(n * m), [str(n + d * m - d), str(n * m + 1), str(d * m - n), str(n)],
                   "%d %s %d = %d, así que %d %s %d = <b>%d</b>." % (d, POR, m, d * m, n, POR, m, n * m))
    return mcq("Completa para que sean equivalentes: %s = %s" % (fr(n, d), fr(n * m, "?")), str(d * m), [str(d + n * m - n), str(d * m + 1), str(n * m + d), str(d)],
               "%d %s %d = %d, así que %d %s %d = <b>%d</b>." % (n, POR, m, n * m, d, POR, m, d * m))


def s3_simplificar():
    b = base()
    if not b:
        return None
    n, d = b
    m = R.randint(2, 6)
    N, D = n * m, d * m
    if D > 40:
        return None
    k = R.choice(["irred", "irred", "div"])
    if k == "irred":
        half = Fr(N, D)
        ws = [fr(N - 1, D - 1), fr(N // m * 2, D // m * 2) if m > 2 else fr(n + 1, d + 1), fr(N, D // m), fr(n, d + 1)]
        return mcq("Simplifica %s hasta la fracción más sencilla (irreducible)." % fr(N, D), fr(n, d), ws,
                   "Dividimos numerador y denominador entre %d: %d %s %d = %d y %d %s %d = %d → <b>%s</b>." % (m, N, DIV, m, n, D, DIV, m, d, fr(n, d)))
    return mcq("Divide el numerador y el denominador de %s entre %d. ¿Qué fracción obtienes?" % (fr(N, D), m), fr(n, d), [fr(N - m, D - m), fr(n, D), fr(N, d), fr(n + 1, d)],
               "%d %s %d = %d; %d %s %d = %d → <b>%s</b>." % (N, DIV, m, n, D, DIV, m, d, fr(n, d)))


def s4_comprobar():
    k = R.choice(["si_no", "cual", "comparar"])
    if k == "si_no":
        b = base()
        if not b:
            return None
        n, d = b
        m = R.randint(2, 5)
        ok = R.random() < 0.5
        N, D = (n * m, d * m) if ok else (n + m, d + m)
        return mcq("¿Son equivalentes %s y %s?" % (fr(n, d), fr(N, D)), "sí" if ok else "no", ["no" if ok else "sí", "solo si se simplifican", "no se puede saber"],
                   "Productos cruzados: %d %s %d = %d y %d %s %d = %d. %s" % (n, POR, D, n * D, d, POR, N, d * N, "Son iguales: <b>sí</b>." if ok else "Son distintos: <b>no</b>."))
    if k == "cual":
        b = base()
        if not b:
            return None
        n, d = b
        eq = [(n * m, d * m) for m in (2, 3, 4)]
        noeq = [(n + 1, d + 1), (n * 2, d + 2), (n + 2, d * 2), (n * 3, d * 2)]
        noeq = [x for x in noeq if Fr(*x) != Fr(n, d)]
        bad = R.choice(noeq)
        return mcq("¿Qué fracción <b>no</b> es equivalente a %s?" % fr(n, d), fr(*bad), [fr(*x) for x in eq], "%s no es igual a %s: <b>%s</b>." % (fr(*bad), fr(n, d), fr(*bad)))
    d1 = R.choice([2, 3, 4, 5])
    m = R.choice([2, 3]) if d1 < 5 else 2
    d2 = d1 * m
    a = R.randint(1, d1 - 1)
    b2 = R.randint(1, d2 - 1)
    if a * m == b2:
        return None
    ok = "%s %s %s" % (fr(a, d1), "&lt;" if a * m < b2 else "&gt;", fr(b2, d2))
    return mcq("Compara %s y %s. ¿Qué es correcto?" % (fr(a, d1), fr(b2, d2)), ok, ["%s %s %s" % (fr(a, d1), "&gt;" if a * m < b2 else "&lt;", fr(b2, d2)), "%s = %s" % (fr(a, d1), fr(b2, d2)), "no se pueden comparar"],
               "%s = %s, y %s %s %s: <b>%s</b>." % (fr(a, d1), fr(a * m, d2), fr(a * m, d2), "&lt;" if a * m < b2 else "&gt;", fr(b2, d2), ok))


def s5_problema():
    (p, g), (q, h) = K.two()
    k = R.choice(["pizza", "camino", "tarta", "chocolate", "botella"])
    a = R.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5)])
    m = R.choice([2, 3])
    b = (a[0] * m, a[1] * m)
    same = R.random() < 0.6
    if not same:
        b = (b[0] + R.choice([1, -1]), b[1])
        if b[0] <= 0 or b[0] >= b[1]:
            return None
    obj = {"pizza": "pizza", "camino": "camino", "tarta": "tarta", "chocolate": "tableta de chocolate", "botella": "botella de agua"}[k]
    verb = {"pizza": "se come", "camino": "recorre", "tarta": "se come", "chocolate": "se come", "botella": "se bebe"}[k]
    big = (b[0] * a[1] > a[0] * b[1])
    ok = "los dos lo mismo" if same else (q if big else p)
    return mcq("%s %s %s de una %s y %s %s %s de otra %s igual. ¿Quién %s más?" % (p, verb, fr(*a), obj, q, verb, fr(*b), obj, verb) if k != "camino" else
               "%s recorre %s de un camino y %s recorre %s del mismo camino. ¿Quién recorre más?" % (p, fr(*a), q, fr(*b)),
               ok, [x for x in [p, q, "los dos lo mismo", "no se puede saber"] if x != ok],
               "%s = %s%s: <b>%s</b>." % (fr(*a), fr(a[0] * m, a[1] * m), "" if same else ", y %s %s %s" % (fr(a[0] * m, a[1] * m), "&lt;" if big else "&gt;", fr(*b)), ok))


def main():
    seen = set()
    sets = [
        ("Fracciones equivalentes con dibujos", mix(R, seen, [(s1_dibujo, 16), (s2_amplificar, 4)])),
        ("Amplificar fracciones", mix(R, seen, [(s2_amplificar, 20)])),
        ("Simplificar fracciones", mix(R, seen, [(s3_simplificar, 20)])),
        ("Comprobar y comparar", mix(R, seen, [(s4_comprobar, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    body = lesson(
        ["Dos fracciones son <b>equivalentes</b> si representan la misma parte de la unidad: %s = %s." % (fr(1, 2), fr(2, 4)),
         "Para obtener una fracción equivalente, <b>multiplica</b> (amplificar) o <b>divide</b> (simplificar) el numerador y el denominador por el <b>mismo número</b>.",
         "Para comprobar si dos fracciones son equivalentes, multiplica en cruz: si los productos son iguales, son equivalentes."],
        [("Amplifica %s por 3" % fr(2, 5), ["2 × 3 = 6", "5 × 3 = 15"], fr(6, 15)),
         ("Simplifica %s" % fr(12, 18), ["Dividimos entre 6", "12 : 6 = 2; 18 : 6 = 3"], fr(2, 3))],
        [["Multiplicar solo el numerador", "Haz lo mismo arriba y abajo."],
         ["Sumar el mismo número", "%s no es igual a %s: hay que multiplicar, no sumar." % (fr(1, 2), fr(2, 3))],
         ["Dejar la fracción sin simplificar del todo", "Sigue dividiendo hasta que no haya un divisor común."]],
        "<div>%s%s</div>" % (tira(2, 1, 260), tira(4, 2, 260)))
    faq = [("¿Cómo se sabe si dos fracciones son equivalentes?", "Multiplicando en cruz: 2/3 y 8/12 son equivalentes porque 2 × 12 = 24 y 3 × 8 = 24."),
           ("¿Qué es simplificar una fracción?", "Es dividir el numerador y el denominador entre el mismo número para obtener una fracción equivalente con números más pequeños.")]
    make_unit(R, "fracciones-equivalentes", "N",
              "Fracciones equivalentes: reconocimiento y obtención por amplificación y simplificación; comparación de fracciones",
              "Fracciones equivalentes", "Fracciones equivalentes",
              "Fichas de matemáticas de 4.º de Primaria: fracciones equivalentes con dibujos, amplificar y simplificar fracciones, productos cruzados y comparar fracciones. 100 ejercicios con soluciones.",
              "Multiplica o divide arriba y abajo por el mismo número", "Equivalentes: los productos cruzados son iguales.",
              body, faq, sets, 11)


if __name__ == "__main__":
    main()
