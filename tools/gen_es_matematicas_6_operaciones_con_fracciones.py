# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Operaciones con fracciones (Sentido numérico)
Sumar y restar fracciones con el mismo denominador y con distinto denominador (reducir a común denominador),
multiplicar una fracción por un número natural; 6.º también multiplicar y dividir fracciones.
Errores: sumar numeradores y denominadores, olvidar simplificar, dividir sin invertir la segunda fracción.
"""
import random
from math import gcd
from fractions import Fraction as F
from es_c3 import M, mix, lesson, make_unit, num, fq, fr, NB, POR, DIV

R = None
LV = 6


def fx():
    d = R.randint(2, 12 if LV == 6 else 10)
    n = R.randint(1, d - 1)
    return F(n, d)


def raw(n, d):
    return fr(n, d)


def s1_mismo():
    d = R.randint(3, 15)
    a, b = R.randint(1, d), R.randint(1, d)
    k = R.choice(["+", "-"])
    if k == "-":
        a, b = max(a, b) + 1, min(a, b)
    r = F(a + b if k == "+" else a - b, d)
    if r == 0:
        return None
    op = "+" if k == "+" else "−"
    return M("Calcula y simplifica: %s %s %s" % (fr(a, d), op, fr(b, d)), fq(r, mixto=False), [raw(a + b if k == "+" else a - b, 2 * d) if (a + b if k == "+" else a - b) else None, raw(a + b if k == "-" else a - b, d) if (a - b if k == "+" else a + b) > 0 else None, fq(r + F(1, d)), fq(r * 2)],
             "Mismo denominador: operamos los numeradores. <b>%s</b>%s." % (raw(a + b if k == "+" else a - b, d), (" = <b>%s</b>" % fq(r)) if r.denominator != d else ""))


def s2_distinto():
    a, b = fx(), fx()
    if a.denominator == b.denominator:
        return None
    k = R.choice(["+", "-"])
    if k == "-" and a <= b:
        a, b = b, a
    if a == b:
        return None
    r = a + b if k == "+" else a - b
    op = "+" if k == "+" else "−"
    l = a.denominator * b.denominator // gcd(a.denominator, b.denominator)
    if l > (36 if LV == 6 else 24):
        return None
    na, nb = a.numerator * l // a.denominator, b.numerator * l // b.denominator
    bad = raw(a.numerator + b.numerator if k == "+" else abs(a.numerator - b.numerator), a.denominator + b.denominator) if (a.numerator - b.numerator or k == "+") else None
    return M("Calcula y simplifica: %s %s %s" % (fq(a), op, fq(b)), fq(r), [bad, fq(r + F(1, l)), fq(F(na + nb if k == "+" else na - nb, l * 2)) if (na - nb or k == "+") else None, fq(a * b) if a * b != r else None, fq(r * 2)],
             "Común denominador %d: %s %s %s = %s%s." % (l, raw(na, l), op, raw(nb, l), raw(na + nb if k == "+" else na - nb, l), " = <b>%s</b>" % fq(r) if r.denominator != l else ""))


def s3_por_natural():
    a = fx()
    n = R.randint(2, 12)
    r = a * n
    return M("Calcula y simplifica: %s %s %d" % (fq(a), POR, n), fq(r, mixto=False), [raw(a.numerator * n, a.denominator * n), raw(a.numerator, a.denominator * n), fq(a + n), fq(r + 1)],
             "Multiplicamos el numerador por %d: %s%s." % (n, raw(a.numerator * n, a.denominator), " = <b>%s</b>" % fq(r) if r.denominator != a.denominator or r.numerator != a.numerator * n else ""))


def s4_mult_div():
    a, b = fx(), fx()
    k = R.choice(["×", ":"])
    if k == "×":
        r = a * b
        return M("Calcula y simplifica: %s %s %s" % (fq(a), POR, fq(b)), fq(r), [raw(a.numerator * b.denominator, a.denominator * b.numerator) if a / b != r else None, fq(a + b), raw(a.numerator + b.numerator, a.denominator * b.denominator) if (a.numerator + b.numerator) else None, fq(r * 2)],
                 "Numerador por numerador y denominador por denominador: %s%s." % (raw(a.numerator * b.numerator, a.denominator * b.denominator), " = <b>%s</b>" % fq(r) if r.denominator != a.denominator * b.denominator else ""))
    r = a / b
    return M("Calcula y simplifica: %s %s %s" % (fq(a), DIV, fq(b)), fq(r), [fq(a * b), fq(b / a), fq(r + 1), fq(r * 2)],
             "Multiplicamos en cruz (o por la inversa de %s): %s%s." % (fq(b), raw(a.numerator * b.denominator, a.denominator * b.numerator), " = <b>%s</b>" % fq(r) if r.denominator != a.denominator * b.numerator or r.numerator != a.numerator * b.denominator else ""))


def s5_problema():
    k = R.choice(["leer", "pintar", "botella", "receta", "reparto"] if LV == 6 else ["leer", "pintar", "botella", "receta"])
    a, b = fx(), fx()
    if k == "leer":
        if a + b >= 1 or a.denominator == b.denominator:
            return None
        r = 1 - a - b
        return M("Hugo lee %s de un libro el lunes y %s el martes. ¿Qué fracción del libro le falta por leer?" % (fq(a), fq(b)), fq(r), [fq(a + b), fq(1 - a), fq(r + F(1, 12)) if r + F(1, 12) < 1 else None, raw(a.numerator + b.numerator, a.denominator + b.denominator)],
                 "Lee %s + %s = %s; le falta 1 − %s = <b>%s</b>." % (fq(a), fq(b), fq(a + b), fq(a + b), fq(r)))
    if k == "pintar":
        if a + b >= 1 or a.denominator == b.denominator:
            return None
        return M("Sofía pinta %s de una pared y Mateo %s. ¿Qué fracción de la pared han pintado entre los dos?" % (fq(a), fq(b)), fq(a + b), [raw(a.numerator + b.numerator, a.denominator + b.denominator), fq(1 - a - b), fq(a * b)],
                 "%s + %s = <b>%s</b>." % (fq(a), fq(b), fq(a + b)))
    if k == "botella":
        n = R.randint(3, 12)
        v = R.choice([F(1, 4), F(1, 2), F(3, 4), F(1, 3), F(2, 5)])
        return M("Cada vaso tiene %s de litro. ¿Cuántos litros hay en %d vasos?" % (fq(v), n), fq(v * n, mixto=True) + " L", [fq(v + n) + " L", raw(v.numerator, v.denominator * n) + " L", fq(v * (n - 1), mixto=True) + " L"],
                 "%s × %d = <b>%s L</b>." % (fq(v), n, fq(v * n, mixto=True)))
    if k == "receta":
        h = R.choice([F(1, 2), F(3, 4), F(2, 3), F(1, 4)])
        n = R.choice([2, 3, 4])
        return M("Una receta lleva %s de kilo de harina. ¿Cuánta harina hace falta para %d recetas?" % (fq(h), n), fq(h * n, mixto=True) + " kg", [fq(h + n, mixto=True) + " kg", raw(h.numerator * n, h.denominator * n) + " kg", fq(h * (n + 1), mixto=True) + " kg"],
                 "%s × %d = <b>%s kg</b>." % (fq(h), n, fq(h * n, mixto=True)))
    t = R.choice([F(3, 4), F(1, 2), F(2, 3), F(5, 6), F(3, 2), F(2, 1)])
    p = R.choice([F(1, 4), F(1, 6), F(1, 8), F(1, 3)])
    if (t / p).denominator != 1:
        return None
    return M("¿Cuántas botellas de %s de litro se llenan con %s litros de zumo?" % (fq(p), fq(t, mixto=True)), num(int(t / p)), [fq(t * p), num(int(t / p) + 1), num(int(t / p) * 2)], "%s : %s = <b>%d</b>." % (fq(t), fq(p), int(t / p)))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40007 + lv * 1000)
    seen = set()
    if lv == 6:
        sets = [
            ("Sumar y restar con el mismo denominador", mix(R, seen, [(s1_mismo, 20)])),
            ("Sumar y restar con distinto denominador", mix(R, seen, [(s2_distinto, 20)])),
            ("Multiplicar fracciones", mix(R, seen, [(s3_por_natural, 8), (s4_mult_div, 12)])),
            ("Dividir fracciones y repaso", mix(R, seen, [(s4_mult_div, 14), (s2_distinto, 6)])),
            ("Problemas", mix(R, seen, [(s5_problema, 20)])),
        ]
    else:
        sets = [
            ("Sumar y restar con el mismo denominador", mix(R, seen, [(s1_mismo, 20)])),
            ("Sumar y restar con distinto denominador", mix(R, seen, [(s2_distinto, 20)])),
            ("Fracción por un número natural", mix(R, seen, [(s3_por_natural, 20)])),
            ("Repaso", mix(R, seen, [(s1_mismo, 7), (s2_distinto, 7), (s3_por_natural, 6)])),
            ("Problemas", mix(R, seen, [(s5_problema, 20)])),
        ]
    think = ["Con el <b>mismo denominador</b>, se suman o restan los numeradores y se deja el denominador.",
             "Con <b>distinto denominador</b>, primero se reducen a común denominador (por ejemplo, con el m.c.m.).",
             "Para multiplicar una fracción por un número, se multiplica el numerador por ese número. Al final, <b>simplifica</b>."]
    if lv == 6:
        think.append("Multiplicar fracciones: numerador × numerador y denominador × denominador. Dividir: se multiplica en cruz (por la fracción inversa).")
    body = lesson(think,
                  [("%s + %s" % (fr(1, 4), fr(2, 3)), ["Común denominador 12", "%s + %s" % (fr(3, 12), fr(8, 12))], fr(11, 12)),
                   ("%s %s %s" % (fr(3, 4), DIV, fr(1, 2)) if lv == 6 else "%s × 4" % fr(3, 8), ["3 × 2 = 6; 4 × 1 = 4", "%s" % fr(6, 4)] if lv == 6 else ["3 × 4 = 12", fr(12, 8)], fq(F(3, 2), True) if lv == 6 else fq(F(3, 2), True))],
                  [["Sumar los denominadores", "%s + %s = %s, no %s." % (fr(1, 4), fr(1, 4), fr(2, 4), fr(2, 8))],
                   ["No reducir a común denominador", "Antes de sumar %s y %s, pásalas a sextos." % (fr(1, 2), fr(1, 3))],
                   ["Dividir sin multiplicar en cruz" if lv == 6 else "Olvidar simplificar", "%s : %s = %s." % (fr(1, 2), fr(1, 4), "2") if lv == 6 else "%s = %s." % (fr(6, 8), fr(3, 4))]])
    faq = [("¿Cómo se suman fracciones con distinto denominador?", "Se buscan fracciones equivalentes con el mismo denominador (el m.c.m. de los denominadores), se suman los numeradores y se simplifica el resultado."),
           ("¿Cómo se divide una fracción entre otra?", "Se multiplica la primera por la inversa de la segunda (o en cruz): 3/4 : 1/2 = 3/4 × 2/1 = 6/4 = 3/2.")]
    make_unit(R, "operaciones-con-fracciones", "N",
              "Suma y resta de fracciones con igual y distinto denominador; producto de una fracción por un número natural" + ("; multiplicación y división de fracciones" if lv == 6 else "") + "; resolución de problemas",
              "Operaciones con fracciones", "Operaciones con fracciones",
              "Fichas de matemáticas de %d.º de Primaria: sumar y restar fracciones con igual y distinto denominador, multiplicar%s fracciones y problemas. 100 ejercicios con soluciones." % (lv, " y dividir" if lv == 6 else ""),
              "Distinto denominador: común primero", "Al terminar, simplifica.",
              body, faq, sets, 7, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
