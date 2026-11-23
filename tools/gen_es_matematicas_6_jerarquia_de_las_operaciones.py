# -*- coding: utf-8 -*-
"""
España Matemáticas 6.º (y 5.º) de Primaria: Jerarquía de las operaciones (Sentido numérico)
Orden de las operaciones: paréntesis, multiplicaciones y divisiones, sumas y restas; propiedad distributiva;
expresiones para problemas; 6.º también con potencias.
Errores: operar de izquierda a derecha sin mirar la jerarquía, olvidar el paréntesis, restar antes que dividir.
"""
import random
from es_c3 import M, mix, lesson, make_unit, num, POR, DIV

R = None
LV = 6


def ev(t):
    return eval(t.replace("×", "*").replace(":", "//").replace("−", "-").replace("²", "**2"))


def ltr(t):
    """error: de izquierda a derecha sin jerarquía"""
    toks = t.replace("(", "").replace(")", "").split()
    v = int(toks[0])
    for i in range(1, len(toks), 2):
        o, b = toks[i], int(toks[i + 1].replace("²", ""))
        if "²" in toks[i + 1]:
            b = b * b
        v = {"+": v + b, "−": v - b, "×": v * b, ":": v // b if b and v % b == 0 else v * 1000}[o]
    return v


def gen():
    k = R.choice(["a+bxc", "a-bxc", "axb+cxd", "a+b:c", "(a+b)xc", "ax(b-c)", "a-(b+c)", "(a-b):c", "axb-c:d"] + (["a+b2", "(a+b)2"] if LV == 6 else []))
    a, b, c, d = R.randint(2, 30), R.randint(2, 12), R.randint(2, 9), R.randint(2, 9)
    t = {"a+bxc": "%d + %d × %d" % (a, b, c), "a-bxc": "%d − %d × %d" % (a + b * c, b, c), "axb+cxd": "%d × %d + %d × %d" % (b, c, d, a % 10 + 2),
         "a+b:c": "%d + %d : %d" % (a, b * c, c), "(a+b)xc": "(%d + %d) × %d" % (a, b, c), "ax(b-c)": "%d × (%d − %d)" % (c, a + b, b),
         "a-(b+c)": "%d − (%d + %d)" % (a + b + c + 5, b, c), "(a-b):c": "(%d − %d) : %d" % (a + b * c, a, c), "axb-c:d": "%d × %d − %d : %d" % (b, c, d * a % 40 + d, d),
         "a+b2": "%d + %d²" % (a, c), "(a+b)2": "(%d + %d)²" % (b % 6 + 1, c)}[k]
    if k == "axb-c:d" and (d * a % 40 + d) % d:
        return None
    return t


def s1_sin():
    t = gen()
    if not t or "(" in t:
        return None
    v = ev(t)
    w = ltr(t)
    if v < 0 or w == v or w > 10 ** 5:
        w = v + 10
    return M("Calcula: %s" % t, num(v), [num(w), num(v + 1), num(v - 2) if v > 2 else num(v + 3), num(v * 2)], "Primero %s; después sumas y restas: <b>%s</b>." % ("la potencia y " if "²" in t else "", num(v)) if "²" in t else "Primero multiplicaciones y divisiones; después sumas y restas: <b>%s</b>." % num(v))


def s2_con():
    t = gen()
    if not t or "(" not in t:
        return None
    v = ev(t)
    w = ev(t.replace("(", "").replace(")", "")) if "²" not in t else ev(t.replace("(", "").replace(")", ""))
    if v < 0:
        return None
    return M("Calcula: %s" % t, num(v), [num(w) if w >= 0 and w != v else num(v + 5), num(v + 1), num(v + 10), num(v - 1)], "Primero el paréntesis: <b>%s</b>." % num(v))


def s3_distrib():
    a, b, c = R.randint(2, 9), R.randint(10, 60), R.randint(2, 9)
    k = R.choice(["igual", "calc", "sacar"])
    if k == "igual":
        ok = "%d × %d + %d × %d" % (a, b, a, c)
        return M("¿Qué expresión es igual a %d × (%d + %d)?" % (a, b, c), ok, ["%d × %d + %d" % (a, b, c), "%d + %d × %d" % (a, b, c), "%d × %d × %d" % (a, b, c)], "Propiedad distributiva: <b>%s</b> = %d." % (ok, a * (b + c)))
    if k == "calc":
        n = R.randint(11, 99)
        if n % 10 == 0:
            return None
        return M("Calcula usando la propiedad distributiva: %d × %d" % (a, n), num(a * n), [num(a * (n // 10 * 10) + n % 10), num(a * n + a), num(a * (n // 10 * 10)), num(a * n - 10)],
                 "%d × %d + %d × %d = %d + %d = <b>%s</b>." % (a, n // 10 * 10, a, n % 10, a * (n // 10 * 10), a * (n % 10), num(a * n)))
    return M("Completa: %d × %d + %d × %d = %d × (___ + %d)" % (a, b, a, c, a, c), str(b), [str(a), str(a * b), str(b + c)], "Sacamos factor común %d: %d × (%d + %d)." % (a, a, b, c))


def s4_expresion():
    p = R.choice(["Lucía", "Hugo", "Martina", "Pablo", "Sofía", "Mateo"])
    k = R.choice(["compra", "reparto", "sobra", "dos"])
    a, b, c = R.randint(3, 9), R.randint(2, 15), R.randint(20, 50)
    if k == "compra":
        t = "%d − %d × %d" % (c * 2, a, b)
        if ev(t) < 0:
            return None
        return M("%s tiene %d € y compra %d cuadernos de %d €. ¿Qué expresión calcula el dinero que le queda?" % (p, c * 2, a, b), t, ["(%d − %d) × %d" % (c * 2, a, b), "%d − %d + %d" % (c * 2, a, b), "%d × %d − %d" % (c * 2, a, b)],
                 "<b>%s</b> = %d €." % (t, ev(t)))
    if k == "reparto":
        t = "(%d + %d) : %d" % (a * 10, b * 10 if (a * 10 + b * 10) % 5 == 0 else b * 10, 5)
        return M("%s tiene %d cromos y le regalan %d. Los reparte entre 5 amigos. ¿Qué expresión da los cromos de cada amigo?" % (p, a * 10, b * 10), t, ["%d + %d : 5" % (a * 10, b * 10), "%d × %d : 5" % (a * 10, b * 10), "(%d − %d) : 5" % (max(a, b) * 10, min(a, b) * 10)],
                 "Primero juntamos y después repartimos: <b>%s</b> = %d." % (t, ev(t)))
    if k == "sobra":
        t = "%d − %d × %d" % (c * 3, a, b)
        if ev(t) < 0:
            return None
        return M("En un teatro hay %d butacas. Se ocupan %d filas de %d butacas. ¿Qué expresión da las butacas libres?" % (c * 3, a, b), t, ["(%d − %d) × %d" % (c * 3, a, b), "%d − %d − %d" % (c * 3, a, b), "%d × %d − %d" % (a, b, c * 3)],
                 "<b>%s</b> = %d." % (t, ev(t)))
    t = "%d × %d + %d × %d" % (a, b, a + 1, b + 2)
    return M("Una entrada de adulto cuesta %d € y una de niño, %d €. ¿Qué expresión da lo que pagan %d adultos y %d niños?" % (b, b + 2, a, a + 1), t, ["(%d + %d) × (%d + %d)" % (a, a + 1, b, b + 2), "%d × %d + %d + %d" % (a, b, a + 1, b + 2), "%d + %d × %d + %d" % (a, b, a + 1, b + 2)],
             "<b>%s</b> = %d €." % (t, ev(t)))


def s5_parentesis():
    a, b, c = R.randint(2, 20), R.randint(2, 9), R.randint(2, 9)
    target = (a + b) * c
    plain = a + b * c
    if target == plain:
        return None
    ok = "(%d + %d) × %d" % (a, b, c)
    return M("¿Dónde hay que poner el paréntesis para que %d + %d × %d dé %d?" % (a, b, c, target), ok, ["%d + (%d × %d)" % (a, b, c), "no hace falta paréntesis", "%d + %d × (%d)" % (a, b, c)],
             "Sin paréntesis da %d. Con <b>%s</b> da %d." % (plain, ok, target))


def build(lv):
    global R, LV
    LV = lv
    R = random.Random(40005 + lv * 1000)
    seen = set()
    sets = [
        ("Sin paréntesis", mix(R, seen, [(s1_sin, 20)])),
        ("Con paréntesis", mix(R, seen, [(s2_con, 20)])),
        ("Propiedad distributiva", mix(R, seen, [(s3_distrib, 14), (s5_parentesis, 6)])),
        ("Repaso", mix(R, seen, [(s1_sin, 7), (s2_con, 7), (s5_parentesis, 6)])),
        ("Expresiones para problemas", mix(R, seen, [(s4_expresion, 20)])),
    ]
    body = lesson(
        ["Cuando hay varias operaciones, se hacen en este orden: 1.º lo que está entre <b>paréntesis</b>; 2.º " + ("las <b>potencias</b>; 3.º " if lv == 6 else "") + "las <b>multiplicaciones y divisiones</b>; después, las <b>sumas y restas</b>.",
         "Si hay varias del mismo nivel, de izquierda a derecha.",
         "Propiedad distributiva: 4 × (10 + 3) = 4 × 10 + 4 × 3."],
        [("8 + 4 × 5", ["Primero 4 × 5 = 20", "8 + 20"], "28"),
         ("(8 + 4) × 5", ["Primero 8 + 4 = 12", "12 × 5"], "60")],
        [["Operar de izquierda a derecha", "8 + 4 × 5 no es 60: es 28."],
         ["Olvidar el paréntesis", "El paréntesis va siempre primero."],
         ["Restar antes de dividir", "20 − 12 : 4 = 20 − 3 = 17."]])
    faq = [("¿En qué orden se hacen las operaciones combinadas?", "Primero los paréntesis, " + ("después las potencias, " if lv == 6 else "") + "después las multiplicaciones y divisiones y, por último, las sumas y restas. Las del mismo tipo, de izquierda a derecha."),
           ("¿Qué es la propiedad distributiva?", "Multiplicar un número por una suma es igual que multiplicarlo por cada sumando y sumar los resultados: 6 × (20 + 3) = 6 × 20 + 6 × 3.")]
    make_unit(R, "jerarquia-de-las-operaciones", "N",
              "Operaciones combinadas con números naturales: jerarquía de las operaciones y uso del paréntesis; propiedad distributiva; expresiones numéricas para resolver problemas",
              "Jerarquía de las operaciones", "Jerarquía de las operaciones",
              "Fichas de matemáticas de %d.º de Primaria: operaciones combinadas con y sin paréntesis, jerarquía de las operaciones, propiedad distributiva y expresiones para problemas. 100 ejercicios con soluciones." % lv,
              "Paréntesis → × y : → + y −", "8 + 4 × 5 = 28, no 60.",
              body, faq, sets, 5, grade="%d-primaria" % lv)


if __name__ == "__main__":
    build(6)
