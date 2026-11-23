# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Operaciones con decimales (Sentido numérico)
Sumar y restar decimales, multiplicar un decimal por un natural y por un decimal, multiplicar y dividir por 10, 100 y 1000,
dividir un decimal entre un natural; 6.º: dividir entre un decimal y cociente decimal. Problemas de dinero y medidas.
Errores: colocar mal la coma del producto, mover la coma hacia el lado equivocado al multiplicar por 10, alinear por la derecha al sumar.
"""
import random
from fractions import Fraction as F
from es_c3 import M, mix, lesson, make_unit, num, d, POR, DIV

R = None
LV = 6


def dx(k=None):
    k = k or R.choice([1, 2])
    return F(R.randint(11, 999 if k == 2 else 99) if k == 1 else R.randint(101, 9999), 10 ** k)


def S(x):
    return d(x)


def s1_sumar():
    a, b = dx(), dx()
    k = R.choice(["+", "-"])
    if k == "-" and a < b:
        a, b = b, a
    if a == b:
        return None
    r = a + b if k == "+" else a - b
    ka, kb = len(S(a).split(",")[1]) if "," in S(a) else 0, len(S(b).split(",")[1]) if "," in S(b) else 0
    bad = None
    if ka != kb:
        na, nb = int(a * 10 ** ka), int(b * 10 ** kb)
        kk = max(ka, kb)
        bad = d(F(na + nb if k == "+" else abs(na - nb), 10 ** kk))
    op = "+" if k == "+" else "−"
    return M("Calcula: %s %s %s" % (S(a), op, S(b)), S(r), [bad, S(r + F(1, 10)), S(r + 1), S(r - F(1, 100)) if r > F(1, 100) else S(r + F(1, 100))],
             "Coma debajo de coma: <b>%s</b>." % S(r))


def s2_por10():
    a = dx(R.choice([1, 2, 3]))
    m = R.choice([10, 100, 1000])
    k = R.choice(["×", ":"])
    r = a * m if k == "×" else a / m
    try:
        return M("Calcula: %s %s %s" % (S(a), POR if k == "×" else DIV, num(m)), S(r), [S(a / m if k == "×" else a * m), S(r * 10), S(r / 10)],
                 "%s la coma %d %s a la %s: <b>%s</b>." % ("Movemos", len(str(m)) - 1, "lugar" if m == 10 else "lugares", "derecha" if k == "×" else "izquierda", S(r)))
    except ValueError:
        return None


def s3_mult():
    k = R.choice(["nat", "dec"] if LV == 6 else ["nat", "nat", "dec"])
    if k == "nat":
        a = dx()
        n = R.randint(2, 25)
        r = a * n
        ka = len(S(a).split(",")[1])
        return M("Calcula: %s %s %d" % (S(a), POR, n), S(r), [S(r * 10), S(r / 10), S(r + a), S(r + 1)],
                 "Multiplicamos como si no hubiera coma y separamos %d %s decimales: <b>%s</b>." % (ka, "cifra" if ka == 1 else "cifras", S(r)))
    a, b = dx(1), dx(1)
    r = a * b
    return M("Calcula: %s %s %s" % (S(a), POR, S(b)), S(r), [S(r * 10), S(r / 10), S(a + b), S(r + F(1, 10))],
             "Multiplicamos sin comas y separamos tantas cifras decimales como tienen los dos factores juntos (2): <b>%s</b>." % S(r))


def s4_div():
    k = R.choice(["dec_nat", "dec_nat", "nat_nat", "dec_dec"] if LV == 6 else ["dec_nat", "dec_nat", "nat_nat"])
    if k == "dec_nat":
        n = R.randint(2, 9)
        q = F(R.randint(11, 999), 100)
        a = q * n
        return M("Calcula: %s %s %d" % (S(a), DIV, n), S(q), [S(q * 10), S(q / 10), S(q + F(1, 10)), S(q + 1)], "Dividimos y, al bajar la primera cifra decimal, ponemos la coma en el cociente: <b>%s</b>." % S(q))
    if k == "nat_nat":
        n = R.choice([2, 4, 5, 8, 10, 20, 25])
        a = R.randint(3, 99)
        if a % n == 0:
            return None
        q = F(a, n)
        try:
            S(q)
        except ValueError:
            return None
        return M("Calcula con decimales: %d %s %d" % (a, DIV, n), S(q), ["%d y resto %d" % (a // n, a % n), S(q * 10), S(q + F(1, 10)), S(q / 10)],
                 "Añadimos ceros como decimales y seguimos dividiendo: <b>%s</b>." % S(q))
    b = F(R.randint(2, 9), 10) if R.random() < 0.6 else F(R.randint(11, 49), 10)
    q = R.randint(2, 40)
    a = b * q
    return M("Calcula: %s %s %s" % (S(a), DIV, S(b)), num(q), [num(q * 10), S(F(q, 10)), num(q + 1)],
             "Multiplicamos los dos por 10 para quitar la coma del divisor: %s %s %s = <b>%d</b>." % (S(a * 10), DIV, S(b * 10), q))


def s5_problema():
    k = R.choice(["compra", "cambio", "reparte", "metros", "litros", "kilos"])
    if k == "compra":
        p = F(R.randint(105, 899), 100)
        n = R.randint(2, 9)
        return M("Un cuaderno cuesta %s €. ¿Cuánto cuestan %d cuadernos?" % (d(p, 2), n), "%s €" % S(p * n), ["%s €" % S(p + n), "%s €" % S(p * n * 10), "%s €" % S(p * (n - 1)), "%s €" % S(p * n + 1)],
                 "%s × %d = <b>%s €</b>." % (S(p), n, S(p * n)))
    if k == "cambio":
        a, b = F(R.randint(105, 999), 100), F(R.randint(105, 999), 100)
        m = 20 if a + b < 20 else 50
        return M("Compras un libro de %s € y un cómic de %s €. Pagas con %d €. ¿Cuánto te devuelven?" % (S(a), S(b), m), "%s €" % S(m - a - b), ["%s €" % S(a + b), "%s €" % S(m - a), "%s €" % S(m - a - b + 1), "%s €" % S(m - a - b + F(1, 10))],
                 "%s + %s = %s €; %d − %s = <b>%s €</b>." % (S(a), S(b), S(a + b), m, S(a + b), S(m - a - b)))
    if k == "reparte":
        n = R.choice([2, 3, 4, 5, 6])
        q = F(R.randint(150, 2500), 100)
        t = q * n
        return M("%d amigos pagan a partes iguales una cena de %s €. ¿Cuánto paga cada uno?" % (n, S(t)), "%s €" % S(q), ["%s €" % S(t - n), "%s €" % S(q * 10), "%s €" % S(q + 1), "%s €" % S(q / 10)],
                 "%s : %d = <b>%s €</b>." % (S(t), n, S(q)))
    if k == "metros":
        L = F(R.randint(30, 99), 10)
        c = F(R.randint(5, 25), 10)
        if L <= c:
            return None
        return M("Tenemos una cuerda de %s m y cortamos un trozo de %s m. ¿Cuánto queda?" % (S(L), S(c)), "%s m" % S(L - c), ["%s m" % S(L + c), "%s m" % S(L - c + 1), "%s m" % S(L - c - F(1, 10)) if L - c > F(1, 10) else None],
                 "%s − %s = <b>%s m</b>." % (S(L), S(c), S(L - c)))
    if k == "litros":
        v = F(R.choice([25, 33, 50, 75, 125, 150]), 100)
        n = R.choice([4, 6, 8, 12, 24])
        return M("Una caja tiene %d botellas de %s L. ¿Cuántos litros hay en la caja?" % (n, S(v)), "%s L" % S(v * n), ["%s L" % S(v + n), "%s L" % S(v * n * 10), "%s L" % S(v * n / 10), "%s L" % S(v * (n - 1))],
                 "%s × %d = <b>%s L</b>." % (S(v), n, S(v * n)))
    p = F(R.randint(120, 495), 100)
    kg = F(R.choice([5, 15, 25, 2, 3]), 10) if LV == 6 else R.choice([2, 3, 4, 5])
    r = p * kg
    try:
        return M("Las manzanas cuestan %s € el kilo. ¿Cuánto cuestan %s kg?" % (S(p), S(kg)), "%s €" % S(r), ["%s €" % S(p + kg), "%s €" % S(r * 10), "%s €" % S(r / 10), "%s €" % S(r + F(1, 10))],
                 "%s × %s = <b>%s €</b>." % (S(p), S(kg), S(r)))
    except ValueError:
        return None


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40009 + lv * 1000)
    seen = set()
    sets = [
        ("Sumar y restar decimales", mix(R, seen, [(s1_sumar, 20)])),
        ("Multiplicar y dividir por 10, 100 y 1000", mix(R, seen, [(s2_por10, 20)])),
        ("Multiplicar decimales", mix(R, seen, [(s3_mult, 20)])),
        ("Dividir con decimales", mix(R, seen, [(s4_div, 20)])),
        ("Problemas", mix(R, seen, [(s5_problema, 20)])),
    ]
    think = ["Para <b>sumar y restar</b>, coloca coma debajo de coma y completa con ceros.",
             "Para <b>multiplicar</b>, multiplica sin comas y separa en el resultado tantas cifras decimales como tengan los factores entre los dos.",
             "× 10, 100, 1000: la coma se mueve 1, 2 o 3 lugares a la <b>derecha</b>. : 10, 100, 1000: a la <b>izquierda</b>.",
             "Para dividir un decimal entre un natural, pon la coma en el cociente al bajar la primera cifra decimal."]
    if lv == 6:
        think.append("Para dividir entre un decimal, multiplica dividendo y divisor por 10 o 100 hasta que el divisor no tenga coma.")
    body = lesson(think,
                  [("2,35 × 4", ["235 × 4 = 940", "2 cifras decimales"], "9,40 = 9,4"),
                   ("6,3 : 0,7" if lv == 6 else "8,4 : 4", ["× 10: 63 : 7"] if lv == 6 else ["8 : 4 = 2, ponemos la coma, 4 : 4 = 1"], "9" if lv == 6 else "2,1")],
                  [["Colocar mal la coma del producto", "Cuenta las cifras decimales de los dos factores."],
                   ["Mover la coma al lado equivocado", "Al multiplicar por 10 el número se hace mayor: 3,5 × 10 = 35."],
                   ["Alinear por la derecha al sumar", "4,5 + 2,38: el 5 son décimas, va debajo del 3."]])
    faq = [("¿Cómo se multiplica un número decimal?", "Se multiplica como si no tuviera coma y en el resultado se separan, desde la derecha, tantas cifras decimales como tengan los dos factores juntos."),
           ("¿Cómo se divide entre 10, 100 o 1000?", "Se mueve la coma 1, 2 o 3 lugares a la izquierda: 45,6 : 100 = 0,456.")]
    make_unit(R, "operaciones-con-decimales", "N",
              "Suma, resta, multiplicación y división con números decimales; multiplicación y división por la unidad seguida de ceros; resolución de problemas de dinero y medida",
              "Operaciones con números decimales", "Operaciones con decimales",
              "Fichas de matemáticas de %d.º de Primaria: sumar, restar, multiplicar y dividir decimales, multiplicar y dividir por 10, 100 y 1000 y problemas con dinero y medidas. 100 ejercicios con soluciones." % lv,
              "× 10: la coma a la derecha", ": 10: la coma a la izquierda.",
              body, faq, sets, 9, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
