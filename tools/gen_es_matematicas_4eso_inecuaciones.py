# -*- coding: utf-8 -*-
"""
España Matemáticas 4.º de ESO: Inecuaciones (Sentido algebraico)
Inecuaciones de primer grado (con paréntesis y denominadores), solución en intervalos, de segundo grado (raíces y signo), sistemas de inecuaciones con una incógnita,
inecuaciones con dos incógnitas (semiplanos) y problemas.
Errores: no cambiar el sentido de la desigualdad al multiplicar o dividir por un negativo, tomar el intervalo de fuera en las de segundo grado, cerrar el intervalo con &lt; o &gt;.
"""
import random
from fractions import Fraction as F
from es_eso import M, mix, sg, fq, num, unit, L, E, P2, MINUS, eur, Kids

R = random.Random(50005)
K = Kids(R)
INF, MINF = "+∞", MINUS + "∞"
SIG = {"<": "&lt;", ">": "&gt;", "<=": "≤", ">=": "≥"}
FLIP = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}


def ivl(a, b, ca=False, cb=False):
    return "%s%s, %s%s" % ("[" if ca else "(", MINF if a is None else fq(a), INF if b is None else fq(b), "]" if cb else ")")


def sol_lin(op, v):
    """x op v → intervalo"""
    if op in ("<", "<="):
        return ivl(None, v, False, op == "<=")
    return ivl(v, None, op == ">=", False)


def wrong_lin(op, v):
    return [sol_lin(FLIP[op], v), sol_lin(op.replace("=", "") if "=" in op else op + "=", v), sol_lin(op, -v) if v else sol_lin(op, 1)]


def s_lineal():
    t = R.choice(["simple", "neg", "neg", "par"])
    op = R.choice(list(SIG))
    x = R.randint(-8, 8)
    if t == "simple":
        a, b = R.randint(2, 7), R.randint(-12, 12)
        c = a * x + b
        lhs = E((a, "x"), (b, ""))
        return M("Resuelve %s %s %s." % (lhs, SIG[op], sg(c)), sol_lin(op, x), wrong_lin(op, x), "%dx %s %s → x %s %s. <b>%s</b>." % (a, SIG[op], sg(c - b), SIG[op], sg(x), sol_lin(op, x)))
    if t == "neg":
        a, b = R.randint(2, 7), R.randint(-12, 12)
        c = -a * x + b
        lhs = E((b, ""), (-a, "x"))
        return M("Resuelve %s %s %s." % (lhs, SIG[op], sg(c)), sol_lin(FLIP[op], x), [sol_lin(op, x), sol_lin(FLIP[op], -x) if x else sol_lin(FLIP[op], 1), sol_lin(op, -x) if x else sol_lin(op, 2)],
                 "−%dx %s %s → al dividir entre −%d cambia el sentido: x %s %s. <b>%s</b>." % (a, SIG[op], sg(c - b), a, SIG[FLIP[op]], sg(x), sol_lin(FLIP[op], x)))
    a, b, c = R.randint(2, 5), R.randint(-6, 6), R.randint(1, 4)
    # a(x + b) − c x op k  → (a − c) x + ab
    if a == c:
        return None
    k = (a - c) * x + a * b
    lhs = "%d(%s) − %dx" % (a, E((1, "x"), (b, "")), c) if c > 1 else "%d(%s) − x" % (a, E((1, "x"), (b, "")))
    final = op if a > c else FLIP[op]
    return M("Resuelve %s %s %s." % (lhs, SIG[op], sg(k)), sol_lin(final, x), [sol_lin(FLIP[final], x), sol_lin(final, -x) if x else sol_lin(final, 3), sol_lin(final, F(k, a - c) if a != c else 0) if F(k, a - c) != x else sol_lin(final, x + 1)],
             "%s %s %s → x %s %s. <b>%s</b>." % (E((a - c, "x"), (a * b, "")), SIG[op], sg(k), SIG[final], sg(x), sol_lin(final, x)))


def s_fracciones():
    op = R.choice(list(SIG))
    t = R.choice(["uno", "dos"])
    if t == "uno":
        d, a = R.choice([2, 3, 4, 5]), R.randint(-6, 6)
        k = R.randint(-5, 5)
        v = d * k - a
        lhs = "(%s)/%d" % (E((1, "x"), (a, "")), d)
        return M("Resuelve %s %s %s." % (lhs, SIG[op], sg(k)), sol_lin(op, v), wrong_lin(op, v) + [sol_lin(op, k - a)], "Multiplicamos por %d: %s %s %s → x %s %s. <b>%s</b>." % (d, E((1, "x"), (a, "")), SIG[op], sg(d * k), SIG[op], sg(v), sol_lin(op, v)))
    p, q = R.sample([2, 3, 4, 5, 6], 2)
    # x/p − x/q op k → x (q − p)/(pq) op k
    k = R.randint(-4, 4)
    if k == 0:
        return None
    co = F(q - p, p * q)
    v = F(k) / co
    final = op if co > 0 else FLIP[op]
    return M("Resuelve x/%d − x/%d %s %s." % (p, q, SIG[op], sg(k)), sol_lin(final, v), [sol_lin(FLIP[final], v), sol_lin(final, -v), sol_lin(final, F(k * p * q))],
             "Denominador común %d: %sx %s %s → x %s %s. <b>%s</b>." % (p * q, sg(q - p), SIG[op], sg(k * p * q), SIG[final], fq(v), sol_lin(final, v)))


def s_cuadratica():
    t = R.choice(["dos", "dos", "dos", "sin", "cuad"])
    if t == "cuad":
        r = R.randint(1, 9)
        op = R.choice(["<", "<=", ">", ">="])
        inside = op in ("<", "<=")
        ok = ivl(-r, r, op == "<=", op == "<=") if inside else "(%s, %s%s ∪ %s%s, %s)" % (MINF, sg(-r), "]" if op == ">=" else ")", "[" if op == ">=" else "(", sg(r), INF)
        out = "(%s, %s%s ∪ %s%s, %s)" % (MINF, sg(-r), "]" if op == "<=" else ")", "[" if op == "<=" else "(", sg(r), INF) if inside else ivl(-r, r, op == "<", op == "<")
        return M("Resuelve x² − %d %s 0." % (r * r, SIG[op]), ok, [out, sol_lin(op, r), ivl(-r * r, r * r, True, True), ivl(-r, r, op != "<=", op != "<=") if inside else ivl(-r, r, True, True)], "x² − %d = 0 → x = ±%d. Entre las raíces la parábola es negativa; fuera, positiva. <b>%s</b>." % (r * r, r, ok))
    if t == "sin":
        a, b = R.randint(-5, 5), R.randint(1, 6)
        f = P2(1, -2 * a, a * a + b)
        op = R.choice(["<", ">"])
        ok = "ℝ (todos los números)" if op == ">" else "no tiene solución"
        return M("Resuelve %s %s 0." % (f, SIG[op]), ok, ["no tiene solución" if op == ">" else "ℝ (todos los números)", ivl(a - b, a + b), "x = %s" % sg(a)], "No tiene raíces reales y abre hacia arriba: siempre es positiva. <b>%s</b>." % ok)
    r1, r2 = sorted(R.sample(range(-7, 8), 2))
    f = P2(1, -(r1 + r2), r1 * r2)
    op = R.choice(list(SIG))
    inside = op in ("<", "<=")
    cl = "=" in op
    ok = ivl(r1, r2, cl, cl) if inside else "(%s, %s%s ∪ %s%s, %s)" % (MINF, sg(r1), "]" if cl else ")", "[" if cl else "(", sg(r2), INF)
    out = "(%s, %s%s ∪ %s%s, %s)" % (MINF, sg(r1), "]" if cl else ")", "[" if cl else "(", sg(r2), INF) if inside else ivl(r1, r2, cl, cl)
    return M("Resuelve %s %s 0." % (f, SIG[op]), ok, [out, ivl(r1, r2, not cl, not cl) if inside else ivl(-r2, -r1, cl, cl), ivl(-r2, -r1, cl, cl) if inside else "(%s, %s%s ∪ %s%s, %s)" % (MINF, sg(r1), ")" if cl else "]", "(" if cl else "[", sg(r2), INF)],
             "Raíces: x = %s y x = %s. Entre las raíces es negativa y fuera, positiva. Buscamos donde es %s: <b>%s</b>." % (sg(r1), sg(r2), "negativa" if inside else "positiva", ok))


def s_sistema():
    a, b = sorted(R.sample(range(-8, 9), 2))
    ca, cb = R.random() < 0.5, R.random() < 0.5
    k1, k2 = R.randint(2, 5), R.randint(2, 5)
    m1, m2 = R.randint(-6, 6), R.randint(-6, 6)
    e1 = "%s %s %s" % (E((k1, "x"), (m1, "")), "≥" if ca else "&gt;", sg(k1 * a + m1))
    e2 = "%s %s %s" % (E((k2, "x"), (m2, "")), "≤" if cb else "&lt;", sg(k2 * b + m2))
    t = R.choice(["ok", "ok", "ok", "vacio"])
    if t == "vacio":
        e1 = "%s %s %s" % (E((k1, "x"), (m1, "")), "≥" if ca else "&gt;", sg(k1 * b + m1))
        e2 = "%s %s %s" % (E((k2, "x"), (m2, "")), "≤" if cb else "&lt;", sg(k2 * a + m2))
        return M("Resuelve el sistema: <span class='sys'>%s<br>%s</span>" % (e1, e2), "no tiene solución", [ivl(a, b, cb, ca), ivl(b, None, ca), ivl(None, a, False, cb)], "x %s %s y x %s %s: no hay números que cumplan las dos. <b>No tiene solución</b>." % ("≥" if ca else "&gt;", sg(b), "≤" if cb else "&lt;", sg(a)))
    ok = ivl(a, b, ca, cb)
    return M("Resuelve el sistema: <span class='sys'>%s<br>%s</span>" % (e1, e2), ok, [ivl(a, b, not ca, not cb), "(%s, %s%s ∪ %s%s, %s)" % (MINF, sg(a), ")" if ca else "]", "(" if cb else "[", sg(b), INF), ivl(a, None, ca), ivl(None, b, False, cb)],
             "Primera: x %s %s. Segunda: x %s %s. La solución es lo común: <b>%s</b>." % ("≥" if ca else "&gt;", sg(a), "≤" if cb else "&lt;", sg(b), ok))


def s_dos_incognitas():
    a, b, c = R.randint(-4, 4), R.randint(1, 4), R.randint(-8, 8)
    op = R.choice(list(SIG))
    lhs = E((a, "x"), (b, "y")) if a else E((b, "y"))
    pts = [(R.randint(-5, 5), R.randint(-5, 5)) for _ in range(12)]

    def ok_(p):
        v = a * p[0] + b * p[1]
        return {"<": v < c, ">": v > c, "<=": v <= c, ">=": v >= c}[op]
    yes = [p for p in pts if ok_(p)]
    no = [p for p in pts if not ok_(p)]
    if not yes or len(set(no)) < 3:
        return None
    t = R.choice(["si", "si", "no"])
    P = lambda p: "(%s, %s)" % (sg(p[0]), sg(p[1]))
    no = sorted(set(no))
    R.shuffle(no)
    if t == "si":
        p = R.choice(yes)
        return M("¿Qué punto es solución de %s %s %s?" % (lhs, SIG[op], sg(c)), P(p), [P(q) for q in no], "Sustituimos: %s → %s %s %s, se cumple. <b>%s</b>." % (P(p), sg(a * p[0] + b * p[1]), SIG[op], sg(c), P(p)))
    q, a_, w = R.choice([("¿Qué representa la solución de una inecuación lineal con dos incógnitas?", "un semiplano", ["una recta", "un punto", "un intervalo"]),
                         ("En la solución de 2x + y ≤ 4, ¿la recta 2x + y = 4 forma parte de ella?", "sí, porque es ≤", ["no, nunca", "solo el punto (0, 4)", "solo si x &gt; 0"]),
                         ("Para saber qué semiplano es la solución de x + y &gt; 3, ¿qué se suele hacer?", "probar con un punto, por ejemplo (0, 0)", ["despejar x", "elevar al cuadrado", "dibujar una parábola"]),
                         ("¿Es (0, 0) solución de x − 2y &gt; 5?", "no, porque 0 &gt; 5 es falso", ["sí, siempre", "sí, porque 0 = 0", "depende de y"])])
    return M(q, a_, w, "Respuesta: <b>%s</b>." % a_)


def s_problema():
    t = R.choice(["movil", "nota", "taxi", "rect", "entradas"])
    p, _ = K.next()
    if t == "movil":
        f1, c1 = R.choice([(10, 5), (15, 3), (8, 6), (20, 2)])
        f2, c2 = R.choice([(0, 10), (2, 9), (5, 8)])
        if c2 <= c1 or f1 <= f2:
            return None
        n = F(f1 - f2, c2 - c1)
        if n.denominator > 1:
            return None
        return M("La tarifa A cuesta %d € fijos más %d céntimos por minuto; la B, %d € fijos más %d céntimos por minuto. ¿A partir de cuántos minutos es más barata la A?" % (f1, c1, f2, c2), "más de %d minutos" % (n * 100), ["menos de %d minutos" % (n * 100), "más de %d minutos" % (n * 10), "más de %d minutos" % (f1 + f2)],
                 "%d + 0,%02dx &lt; %d + 0,%02dx → 0,%02dx &gt; %d → x &gt; %d. <b>Más de %d minutos</b>." % (f1, c1, f2, c2, c2 - c1, f1 - f2, n * 100, n * 100))
    if t == "nota":
        a, b = R.randint(3, 7), R.randint(4, 8)
        need = 5 * 3 - a - b
        if not 0 < need <= 10:
            return None
        return M("%s ha sacado un %d y un %d en dos exámenes. ¿Qué nota necesita en el tercero para que la media sea al menos 5?" % (p, a, b), "%d o más" % need, ["%d o menos" % need, "%d o más" % (need + 1), "5 o más", "%d o más" % (need - 1)], "(%d + %d + x)/3 ≥ 5 → x ≥ <b>%d</b>." % (a, b, need))
    if t == "taxi":
        b, k, mx = R.randint(2, 5), R.choice([2, 3]), R.randint(20, 45)
        if (mx - b) % k == 0:
            return None
        v = (mx - b) // k
        return M("Un taxi cobra %d € al subir y %d € por kilómetro. Si solo llevamos %d €, ¿cuántos km como máximo podemos recorrer?" % (b, k, mx), "%d km" % v, ["%d km" % (v + 1), "%d km" % (mx // k), "%d km" % (mx - b), "%d km" % (v - 1)], "%d + %dx ≤ %d → x ≤ %s. <b>%d km</b>." % (b, k, mx, fq(F(mx - b, k)), v))
    if t == "rect":
        a, P = R.randint(3, 12), R.choice([40, 50, 60, 80])
        mx = P // 2 - a
        return M("Un rectángulo tiene un lado de %d cm. ¿Cuánto puede medir el otro lado si el perímetro no debe superar %d cm?" % (a, P), "como mucho %d cm" % mx, ["como mucho %d cm" % (P - 2 * a), "al menos %d cm" % mx, "como mucho %d cm" % (P // 2)], "2 · %d + 2x ≤ %d → x ≤ <b>%d cm</b>." % (a, P, mx))
    pr, tot = R.choice([(6, 50), (8, 70), (12, 100), (7, 60), (9, 80)])
    v = tot // pr
    return M("Las entradas de cine cuestan %d €. Con %d €, ¿cuántas se pueden comprar como máximo?" % (pr, tot), "%d" % v, ["%d" % (v + 1), "%d" % (tot - pr), "%s" % fq(F(tot, pr))], "%dx ≤ %d → x ≤ %s → <b>%d</b> entradas." % (pr, tot, fq(F(tot, pr)), v))


seen = set()
sets = [("Inecuaciones de primer grado", mix(R, seen, [(s_lineal, 20)])), ("Con paréntesis y denominadores", mix(R, seen, [(s_lineal, 6), (s_fracciones, 14)])), ("Inecuaciones de segundo grado", mix(R, seen, [(s_cuadratica, 20)])),
        ("Sistemas y semiplanos", mix(R, seen, [(s_sistema, 12), (s_dos_incognitas, 8)])), ("Problemas", mix(R, seen, [(s_problema, 20)]))]
think = ["Se resuelven como las ecuaciones, con una regla más: si se <b>multiplica o divide por un número negativo</b>, cambia el sentido de la desigualdad.",
         "La solución suele ser un <b>intervalo</b>: con ≤ o ≥ el extremo se incluye (corchete); con &lt; o &gt;, no (paréntesis).",
         "Segundo grado: hallamos las raíces y miramos el signo. Si x² − … &lt; 0, la solución está <b>entre las raíces</b>; si &gt; 0, <b>fuera</b>.",
         "Sistema de inecuaciones: resolvemos cada una y tomamos lo que tienen en común."]
ex = [("5 − 2x &gt; 11", ["−2x &gt; 6", "x &lt; −3 (cambia el sentido)"], "(−∞, −3)"), ("x² − x − 6 ≤ 0", ["raíces −2 y 3", "entre las raíces"], "[−2, 3]")]
mist = [["No cambiar el sentido con un negativo", "−2x &gt; 6 → x &lt; −3."], ["Tomar el intervalo de fuera", "Para &lt; 0 la parábola (a &gt; 0) está entre las raíces."], ["Cerrar el intervalo con &lt;", "Con &lt; o &gt; el extremo no se incluye."]]
body = L(think, ex, mist)
faq = [("¿Por qué cambia el sentido al multiplicar por un negativo?", "Porque 2 &lt; 5 pero −2 &gt; −5: al cambiar de signo, el orden se invierte."),
       ("¿Qué pasa si una inecuación de segundo grado no tiene raíces?", "La parábola no corta el eje: o se cumple siempre (ℝ) o no se cumple nunca.")]
unit(4, R, "inecuaciones", "A", "Inecuaciones de primer y segundo grado con una incógnita; sistemas de inecuaciones; inecuaciones lineales con dos incógnitas; interpretación y resolución de problemas",
     "Inecuaciones", "Inecuaciones", "Fichas de matemáticas de 4.º de ESO: inecuaciones de primer y segundo grado, intervalos, sistemas de inecuaciones, semiplanos y problemas. 100 ejercicios con soluciones.",
     "Por un negativo, cambia el sentido", "−2x &gt; 6 → x &lt; −3", body, faq, sets, 5)
