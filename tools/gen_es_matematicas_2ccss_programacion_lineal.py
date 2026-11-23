# -*- coding: utf-8 -*-
"""
España Matemáticas Aplicadas a las Ciencias Sociales II (2.º de Bachillerato): Programación lineal (Sentido algebraico)
Traducir restricciones a inecuaciones, región factible, vértices, función objetivo (máximo y mínimo), problemas de producción y de mezclas.
Errores: tomar el vértice equivocado, olvidar x ≥ 0 e y ≥ 0, evaluar la función objetivo en un punto que no es vértice, cambiar «al menos» por «como mucho».
"""
import math
import random
from fractions import Fraction as F
from es_ccss import M, mix, num, unit, L, W, eu, E, sg
from ws_common import text, line
from de_common import wrap

R = random.Random(54003)
SYM = {"<=": "≤", ">=": "≥"}


def ineq(a, b, c, s):
    return "%s %s %s" % (E((a, "x"), (b, "y")), SYM[s], sg(c))


def sysc(cons):
    return "<span class='sys'>%s</span>" % "<br>".join([ineq(*c) for c in cons] + ["x ≥ 0, y ≥ 0"])


def ok_pt(cons, x, y):
    if x < 0 or y < 0:
        return False
    for a, b, c, s in cons:
        v = a * x + b * y
        if (s == "<=" and v > c) or (s == ">=" and v < c):
            return False
    return True


def vertices(cons):
    L_ = [(a, b, c) for a, b, c, s in cons] + [(1, 0, 0), (0, 1, 0)]
    out = set()
    for i in range(len(L_)):
        for j in range(i + 1, len(L_)):
            a1, b1, c1 = L_[i]
            a2, b2, c2 = L_[j]
            dt = a1 * b2 - a2 * b1
            if dt == 0:
                continue
            x, y = F(c1 * b2 - c2 * b1, dt), F(a1 * c2 - a2 * c1, dt)
            if ok_pt(cons, x, y):
                out.add((x, y))
    return sorted(out)


def pt(v):
    return "(%s, %s)" % tuple(str(c) if c.denominator == 1 else "%d/%d" % (c.numerator, c.denominator) for c in v)


def region(kind):
    """dos restricciones que se cortan en un vértice entero (x0, y0); kind '<=' (máximo) o '>=' (mínimo)"""
    for _ in range(400):
        x0, y0 = R.randint(1, 8), R.randint(1, 8)
        a1, b1 = R.randint(1, 5), R.randint(1, 5)
        a2, b2 = R.randint(1, 5), R.randint(1, 5)
        if a1 * b2 <= a2 * b1 or math.gcd(a1, b1) > 1 or math.gcd(a2, b2) > 1:          # la 1.ª más inclinada; coeficientes simplificados
            continue
        c1, c2 = a1 * x0 + b1 * y0, a2 * x0 + b2 * y0
        cons = [(a1, b1, c1, kind), (a2, b2, c2, kind)]
        vs = vertices(cons)
        if any(v[0].denominator > 1 or v[1].denominator > 1 for v in vs):
            continue
        if kind == "<=" and len(vs) == 4 and max(max(v) for v in vs) <= 20:
            return cons, vs, (x0, y0)
        if kind == ">=" and len(vs) == 3 and max(max(v) for v in vs) <= 20:
            return cons, vs, (x0, y0)
    return None


def pic(cons, vs, kind, mark=None):
    top = max(max(max(v) for v in vs) + 2, 6)
    top = int(top)
    S = 220.0 / top
    X = lambda x: 40 + float(x) * S
    Y = lambda y: 250 - float(y) * S
    s = []
    if kind == "<=":
        poly = vs[:]
        cx, cy = sum(v[0] for v in poly) / len(poly), sum(v[1] for v in poly) / len(poly)
        import math
        poly.sort(key=lambda v: math.atan2(float(v[1] - cy), float(v[0] - cx)))
    else:
        ys = sorted(vs, key=lambda v: (v[0], -v[1]))
        poly = [(0, top)] + ys + [(top, 0), (top, top)]
    s.append("<polygon points='%s' fill='#bbdefb' fill-opacity='0.7' stroke='none'/>" % " ".join("%.1f,%.1f" % (X(x), Y(y)) for x, y in poly))
    step = 2 if top > 10 else 1
    for k in range(0, top + 1, step):
        s.append(line(X(k), Y(0), X(k), Y(top), "#e0e0e0", 1))
        s.append(line(X(0), Y(k), X(top), Y(k), "#e0e0e0", 1))
        if k:
            s.append(text(X(k), Y(0) + 16, str(k), 11))
            s.append(text(X(0) - 8, Y(k) + 4, str(k), 11, anchor="end"))
    for a, b, c, _ in cons:
        P = []
        for x in (0, top):
            if b:
                y = F(c - a * x, b)
                P.append((x, y))
        if a:
            for y in (0, top):
                P.append((F(c - b * y, a), y))
        P = [(x, y) for x, y in P if -0.01 <= x <= top + 0.01 and -0.01 <= y <= top + 0.01]
        if len(P) >= 2:
            P.sort()
            s.append(line(X(P[0][0]), Y(P[0][1]), X(P[-1][0]), Y(P[-1][1]), "#1565c0", 2))
    s.append(line(X(0), Y(0), X(top) + 8, Y(0), "#263238", 2))
    s.append(line(X(0), Y(0), X(0), Y(top) - 8, "#263238", 2))
    s.append(text(X(top) + 12, Y(0) + 4, "x", 14, italic=True))
    s.append(text(X(0), Y(top) - 12, "y", 14, italic=True))
    for v in vs:
        s.append("<circle cx='%.1f' cy='%.1f' r='4' fill='#c62828'/>" % (X(v[0]), Y(v[1])))
    return wrap(300, 280, "".join(s), "región factible", lg=True)


def s_traducir():
    a, b = R.randint(2, 6), R.randint(10, 60)
    q, ok, w = R.choice([
        ("Se fabrican x mesas e y sillas. Debe haber, al menos, el %s de sillas que de mesas." % ("doble" if a == 2 else "triple" if a == 3 else "cuádruple" if a == 4 else "quíntuple" if a == 5 else "séxtuple"), "y ≥ %dx" % a, ["y ≤ %dx" % a, "x ≥ %dy" % a, "%dy ≥ x" % a]),
        ("Se compran x kg de manzanas e y kg de peras. En total, como mucho %d kg." % b, "x + y ≤ %d" % b, ["x + y ≥ %d" % b, "x · y ≤ %d" % b, "x ≤ %d, y ≤ %d" % (b, b)]),
        ("Hay x alumnos de Ciencias e y de Ciencias Sociales en una excursión. Tienen que ir, como mínimo, %d alumnos." % b, "x + y ≥ %d" % b, ["x + y ≤ %d" % b, "x ≥ %d" % b, "x + y = %d" % b]),
        ("Se invierten x miles de euros en bolsa e y en renta fija. Lo invertido en bolsa no puede superar a lo de renta fija." , "x ≤ y", ["x ≥ y", "x + y ≤ 1", "y ≤ x"]),
        ("Un autobús lleva x adultos e y niños. Debe haber al menos un adulto por cada %d niños." % a, "%dx ≥ y" % a, ["x ≥ %dy" % a, "%dx ≤ y" % a, "x + y ≥ %d" % a]),
        ("Se producen x camisetas e y sudaderas. Cada camiseta usa %d m de tela y cada sudadera %d m; hay %d m." % (a, a + 1, b), "%s ≤ %d" % (E((a, "x"), (a + 1, "y")), b), ["%s ≥ %d" % (E((a, "x"), (a + 1, "y")), b), "%s ≤ %d" % (E((a + 1, "x"), (a, "y")), b), "x + y ≤ %d" % b]),
        ("Se fabrican x unidades de A e y de B. De A hay que hacer, como mínimo, %d unidades más que de B." % a, "x ≥ y + %d" % a, ["y ≥ x + %d" % a, "x ≤ y + %d" % a, "x ≥ %dy" % a])])
    return M(q + " ¿Qué inecuación lo expresa?", ok, w, "«Al menos» o «como mínimo» → ≥; «como mucho» o «no superar» → ≤: <b>%s</b>." % ok)


def s_punto():
    kind = R.choice(["<=", ">="])
    r = region(kind)
    if not r:
        return None
    cons, vs, P = r
    good = [(x, y) for x in range(0, 21) for y in range(0, 21) if ok_pt(cons, x, y) and (x, y) not in vs]
    bad = [(x, y) for x in range(0, 21) for y in range(0, 21) if not ok_pt(cons, x, y)]
    if not good or len(bad) < 3:
        return None
    g = R.choice(good)
    bs = R.sample(bad, 3)
    return M("¿Qué punto pertenece a la región factible? %s" % sysc(cons), pt(g), [pt(b) for b in bs],
             "Se sustituye en cada inecuación: %s las cumple todas; los demás fallan en alguna. <b>%s</b>." % (pt(g), pt(g)))


def s_vertices():
    kind = R.choice(["<=", "<=", ">="])
    r = region(kind)
    if not r:
        return None
    cons, vs, P = r
    ok = ", ".join(pt(v) for v in vs)
    (a1, b1, c1, _), (a2, b2, c2, _) = cons
    alt = [(F(c1, a1), F(0)), (F(0), F(c1, b1)), (F(c2, a2), F(0)), (F(0), F(c2, b2))]
    wrongs = []
    for k in range(4):
        w_ = [v for v in vs if v != tuple(P)] + [alt[k]]
        w_ = sorted(set(w_))
        s_ = ", ".join(pt(v) for v in w_)
        if s_ != ok:
            wrongs.append(s_)
    wrongs.append(", ".join(pt(v) for v in vs if v != (0, 0)) + ", (%d, %d)" % (P[1], P[0]) if P[0] != P[1] else None)
    return M(pic(cons, vs, kind) + "¿Cuáles son los vértices de la región factible? %s" % sysc(cons), ok, W(wrongs),
             "Se cortan las rectas dos a dos y se quedan los puntos que cumplen todas las restricciones: <b>%s</b>." % ok)


def best(vs, p, q, kind):
    vals = [(p * v[0] + q * v[1], v) for v in vs]
    vals.sort()
    if kind == "<=":
        if vals[-1][0] == vals[-2][0]:
            return None
        return vals[-1], vals
    if vals[0][0] == vals[1][0]:
        return None
    return vals[0], vals


def s_optimo():
    kind = R.choice(["<=", "<=", ">="])
    r = region(kind)
    if not r:
        return None
    cons, vs, P = r
    p, q = R.randint(1, 9), R.randint(1, 9)
    b = best(vs, p, q, kind)
    if not b:
        return None
    (val, v), vals = b
    word = "máximo" if kind == "<=" else "mínimo"
    ok = "%s en %s" % (val, pt(v))
    others = ["%s en %s" % (x, pt(w)) for x, w in vals if w != v]
    others.append("%s en %s" % (p * P[1] + q * P[0], pt((P[1], P[0]))) if P[0] != P[1] else None)
    others.append("no tiene %s (la región no está acotada)" % word if kind == ">=" else "no tiene máximo")
    return M(pic(cons, vs, kind) + "En la región %s, ¿cuál es el %s de F(x, y) = %s?" % (sysc(cons), word, E((p, "x"), (q, "y"))), ok, W(others),
             "Se evalúa F en los vértices: %s. El %s es <b>%s</b>." % ("; ".join("F%s = %s" % (pt(w), x) for x, w in vals), word, ok))


CTX_MAX = [("Un taller fabrica x mesas e y sillas. Cada mesa necesita %d h de carpintería y %d h de barnizado; cada silla, %d h y %d h. Cada semana hay %d h de carpintería y %d h de barnizado. "
            "Cada mesa deja %d € de beneficio y cada silla %d €.", "mesas", "sillas", "beneficio"),
           ("Una pastelería hace x tartas e y bizcochos. Una tarta lleva %d kg de harina y %d kg de azúcar; un bizcocho, %d kg y %d kg. Tiene %d kg de harina y %d kg de azúcar. "
            "Gana %d € por tarta y %d € por bizcocho.", "tartas", "bizcochos", "beneficio"),
           ("Un agricultor siembra x hectáreas de trigo e y de maíz. Cada hectárea de trigo necesita %d jornadas de trabajo y %d unidades de agua; la de maíz, %d jornadas y %d unidades. "
            "Dispone de %d jornadas y %d unidades de agua. Cada hectárea de trigo da %d cientos de euros y la de maíz %d cientos.", "ha de trigo", "ha de maíz", "beneficio")]
CTX_MIN = [("Una granja mezcla x kg del pienso A e y kg del pienso B. Cada kg de A aporta %d unidades de proteína y %d de fibra; cada kg de B, %d y %d. Se necesitan al menos %d unidades de proteína y %d de fibra. "
            "El kg de A cuesta %d € y el de B %d €.", "kg de A", "kg de B", "coste"),
           ("Una empresa contrata x autobuses pequeños e y grandes para una excursión. Un pequeño lleva %d grupos de alumnos y %d profesores; uno grande, %d grupos y %d profesores. Hay que llevar al menos %d grupos y %d profesores. "
            "Un pequeño cuesta %d cientos de euros y uno grande %d cientos.", "pequeños", "grandes", "coste")]


def s_problema():
    kind = R.choice(["<=", "<=", ">="])
    r = region(kind)
    if not r:
        return None
    cons, vs, P = r
    (a1, b1, c1, _), (a2, b2, c2, _) = cons
    p, q = R.randint(2, 9), R.randint(2, 9)
    b = best(vs, p, q, kind)
    if not b:
        return None
    (val, v), vals = b
    tpl, nx, ny, obj = R.choice(CTX_MAX if kind == "<=" else CTX_MIN)
    txt = tpl % (a1, a2, b1, b2, c1, c2, p, q)
    ok = "%d %s y %d %s" % (v[0], nx, v[1], ny)
    return M(txt + " ¿Qué %s hace que el %s sea %s?" % ("producción" if kind == "<=" else "elección", obj, "máximo" if kind == "<=" else "mínimo"), ok,
             W(["%d %s y %d %s" % (w[0], nx, w[1], ny) for x, w in vals if w != v] + ["%d %s y %d %s" % (v[1], nx, v[0], ny) if v[0] != v[1] else None, "%d %s y %d %s" % (v[0] + 1, nx, v[1], ny), "%d %s y %d %s" % (v[0], nx, v[1] + 1, ny)]),
             "Restricciones: %s; %s; x, y ≥ 0. Vértices: %s. F = %s vale %s en %s: <b>%s</b>." % (ineq(a1, b1, c1, kind), ineq(a2, b2, c2, kind), ", ".join(pt(w) for w in vs), E((p, "x"), (q, "y")),
                                                                                              "lo máximo" if kind == "<=" else "lo mínimo", pt(v), ok))


seen = set()
sets = [("Traducir restricciones", mix(R, seen, [(s_traducir, 20)])), ("Región factible", mix(R, seen, [(s_punto, 20)])), ("Vértices", mix(R, seen, [(s_vertices, 20)])),
        ("Función objetivo", mix(R, seen, [(s_optimo, 20)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
think = ["En un problema de <b>programación lineal</b> se busca el máximo o el mínimo de una <b>función objetivo</b> F(x, y) = ax + by con unas <b>restricciones</b> (inecuaciones lineales).",
         "Las soluciones de todas las restricciones forman la <b>región factible</b>. Recuerda x ≥ 0 e y ≥ 0 si son cantidades.",
         "Los <b>vértices</b> se obtienen cortando las rectas dos a dos (sistemas de dos ecuaciones) y quedándose con los que cumplen todo.",
         "<b>Teorema</b>: si hay óptimo, está en un vértice (o en un lado entero). Basta evaluar F en los vértices."]
ex = [("Máx F = 3x + 2y con x + y ≤ 6, 2x + y ≤ 8, x, y ≥ 0", ["vértices (0, 0), (4, 0), (2, 4), (0, 6)", "F = 0, 12, 14, 12"], "máximo 14 en (2, 4)")]
mist = [["Olvidar x ≥ 0 e y ≥ 0", "Una producción no puede ser negativa."], ["Cambiar «al menos» por «como mucho»", "Al menos → ≥; como mucho → ≤."], ["Quedarse con un punto que no es vértice", "Compara solo los valores en los vértices."]]
body = L(think, ex, mist, pic([(1, 1, 6, "<="), (2, 1, 8, "<=")], [(F(0), F(0)), (F(4), F(0)), (F(2), F(4)), (F(0), F(6))], "<="))
faq = [("¿Por qué el óptimo está en un vértice?", "Porque F = ax + by tiene rectas de nivel paralelas; al desplazarlas, el último punto que tocan de la región es un vértice (o un lado)."),
       ("¿Qué pasa si la región no está acotada?", "Puede no haber máximo; en los problemas de coste mínimo con restricciones ≥ suele haber mínimo en un vértice.")]
unit(2, R, "programacion-lineal", "A", "Programación lineal bidimensional: inecuaciones lineales, región factible, vértices, función objetivo y resolución de problemas de producción y de mezclas",
     "Programación lineal", "Programación lineal", "Fichas de Matemáticas Aplicadas a las Ciencias Sociales II: restricciones, región factible, vértices, función objetivo y problemas de máximos y mínimos. 100 ejercicios.",
     "El óptimo está en un vértice", "Evalúa F en todos los vértices.", body, faq, sets, 3)
